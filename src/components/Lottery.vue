<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { LotteryData, defaultLotteryData } from "../lottery-data";
import { DefaultApiClient, VarcharMax } from "../openapi";
import FlexTextarea from "./FlexTextarea.vue";
import RotateSlot from "./RotateSlot.vue";

const INPUT_TEXT_PLACEHOLDER_TEXT = "一行がひとつのくじとなります\n空白行は無視されます";
const LOTTERY_TARGETS_SHOW_CLASS = "fs-1 fw-bold";

const props = defineProps<{
  initData: LotteryData | null;
  accessToken: string;
}>();

const emit = defineEmits<{
  change: [data: LotteryData];
}>();

const editable = ref(false);

const data = ref<LotteryData>(structuredClone(defaultLotteryData));
watch(
  data,
  () => {
    // テキスト入力の上限切りつめ
    if (data.value.contentsData.text.length > VarcharMax.lotteries_text) {
      data.value.contentsData.text = data.value.contentsData.text.slice(0, VarcharMax.lotteries_text);
    }
    if (data.value.contentsData.title.length > VarcharMax.lotteries_title) {
      data.value.contentsData.title = data.value.contentsData.title.slice(0, VarcharMax.lotteries_title);
    }
    if (data.value.contentsData.description.length > VarcharMax.lotteries_description) {
      data.value.contentsData.description = data.value.contentsData.description.slice(0, VarcharMax.lotteries_description);
    }

    // 入力されたデータに変化あったらイベント発火
    emit("change", data.value);
  },
  { deep: true }
);

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initData,
  () => onUpdateInitData()
);

// 抽選対象群
// INPUT_TEXT_PLACEHOLDER_TEXT の条件をここで表現
const lotteryTargets = computed(() => data.value.contentsData.text.split("\n").filter((x) => x));

async function onUpdateInitData() {
  // まず編集不可にしておく
  editable.value = false;

  // 編集データに初期データを反映させる
  if (props.initData) {
    data.value = props.initData;

    // 編集可能かどうか判断する
    if (data.value.contentsData.id !== -1) {
      if (props.accessToken) {
        await DefaultApiClient.isLotteryIdMineApiIsLotteryIdMineGet(data.value.contentsData.id, props.accessToken)
          .then((response) => {
            if (response.data) {
              // サーバーに問い合わせたうえで自分の作成したデータだと判明したら編集可能
              editable.value = true;
            }
          })
          .catch((_error) => {
            // エラーが発生したら編集不可。エラー自体は特にハンドリング不要
          });
      } else {
        // 他の人が作ったデータは編集不可
      }
    } else {
      // ローカルで作成したデータは編集可能
      editable.value = true;
    }
  }
}

function onClickLotteryButton() {
  // 抽選対象がなければ何もしない
  if (lotteryTargets.value.length === 0) return;
  // 抽選
  const result = lotteryTargets.value[random(lotteryTargets.value.length)];
  // 結果の記録と履歴保存
  data.value.resultData.result = result;
  data.value.resultData.histories.push(result);
  // 抽選した回数を増やすようサーバーに通達
  if (props.accessToken && data.value.contentsData.id !== -1) {
    // 特に待つ必要なし。エラーが発生しても抽選回数が増えないだけなのでスルー
    DefaultApiClient.incrementLotteryUsedCountApiIncrementLotteryUsedCountPost(data.value.contentsData.id, props.accessToken).catch(() => {});
  }
}

function onClickResultClearButton() {
  data.value.resultData.result = "";
}

function onInputText(inputText: string) {
  data.value.contentsData.text = inputText;
}

function onInputDescription(inputText: string) {
  data.value.contentsData.description = inputText;
}

function random(max: number) {
  return Math.floor(Math.random() * max);
}

function showRotateSlot(): boolean {
  // 結果が表示される状況じゃなく、抽選対象が2個以上ある場合に表示
  return !showResult() && lotteryTargets.value.length > 1;
}

function showResult(): boolean {
  // 抽選結果があれば表示ON
  return data.value.resultData.result !== "";
}

function showInputTitle(): boolean {
  // 抽選対象が入力されていれば表示ON
  return data.value.contentsData.text !== "";
}

function showInputDescription(): boolean {
  // タイトルが入力されていれば表示ON
  return data.value.contentsData.title !== "";
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div class="d-flex flex-column align-items-center w-100">
      <FlexTextarea
        class="w-100"
        @input="onInputText"
        :initText="data.contentsData.text"
        :placeholder="INPUT_TEXT_PLACEHOLDER_TEXT"
        :disabled="!editable"
        :minHeightPx="120"
      />
      <div class="w-100">
        <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg w-100">抽選</button>
      </div>
      <div v-show="showRotateSlot()">
        <div class="d-flex flex-column align-items-center">
          <span>...</span>
          <RotateSlot :slots="lotteryTargets" :slotClass="LOTTERY_TARGETS_SHOW_CLASS" />
        </div>
      </div>
      <div v-show="showResult()">
        <div class="d-flex flex-column align-items-center">
          <span>結果</span>
          <div :class="LOTTERY_TARGETS_SHOW_CLASS">{{ data.resultData.result }}</div>
          <button @click="onClickResultClearButton()" class="btn btn-outline-danger"><span class="mdi mdi-eraser" />結果を消す</button>
        </div>
      </div>
      <div v-show="showInputTitle()" class="w-100">
        <div class="input-group">
          <span class="input-group-text">くじ引き名</span>
          <input
            v-model="data.contentsData.title"
            class="form-control"
            :placeholder="editable ? '名前をつけると別のくじ引きも作成できます' : ''"
            :disabled="!editable"
          />
        </div>
      </div>
      <div v-show="showInputDescription()" class="w-100">
        <FlexTextarea
          class="w-100"
          @input="onInputDescription"
          :initText="data.contentsData.description"
          :placeholder="editable ? `説明をつけるとこのくじ引きをよりわかりやすくできます\n未入力でも問題ありません` : ''"
          :disabled="!editable"
          :minHeightPx="90"
        />
      </div>
    </div>
  </div>
</template>
