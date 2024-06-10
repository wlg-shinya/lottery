<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryData } from "../lottery-data";
import { DefaultApiClient } from "../openapi";
import FlexTextarea from "./FlexTextarea.vue";
import RotateSlot from "./RotateSlot.vue";

// TODO:ほかのユーザが作成したくじ引きを利用可能（＝お気に入り）にする
// TODO:ほかのユーザが作成したくじ引きを抽選した回数をDB保存＆集計表示する

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
// 入力されたデータに変化あったらイベント発火
watch(data, () => emit("change", data.value), { deep: true });

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initData,
  () => onUpdateInitData()
);

// 抽選対象群
// INPUT_TEXT_PLACEHOLDER_TEXT の条件をここで表現
const lotteryTargets = computed(() => data.value.inputData.text.split("\n").filter((x) => x));

async function onUpdateInitData() {
  // まず編集不可にしておく
  editable.value = false;

  // 編集データに初期データを反映させる
  if (props.initData) {
    data.value = props.initData;

    // 編集可能かどうか判断する
    if (props.initData.inputData.id !== -1) {
      if (props.accessToken) {
        await DefaultApiClient.isLotteryIdMineApiIsLotteryIdMineGet(props.initData.inputData.id, props.accessToken)
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
}

function onClickResultClearButton() {
  data.value.resultData.result = "";
}

function onInputText(inputText: string) {
  data.value.inputData.text = inputText;
}

function onInputDescription(inputText: string) {
  data.value.inputData.description = inputText;
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
  return data.value.inputData.text !== "";
}

function showInputDescription(): boolean {
  // タイトルが入力されていれば表示ON
  return data.value.inputData.title !== "";
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div class="d-flex flex-column align-items-center w-100">
      <FlexTextarea
        class="w-100"
        @input="onInputText"
        :initText="data.inputData.text"
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
            v-model="data.inputData.title"
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
          :initText="data.inputData.description"
          :placeholder="editable ? `説明をつけるとこのくじ引きをよりわかりやすくできます\n未入力でも問題ありません` : ''"
          :disabled="!editable"
          :minHeightPx="90"
        />
      </div>
    </div>
  </div>
</template>
