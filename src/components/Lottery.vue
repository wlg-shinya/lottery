<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryData } from "../lottery-data";
import FlexTextarea from "./FlexTextarea.vue";

const INPUT_TEXT_PLACEHOLDER_TEXT = "一行がひとつのくじとなります\n空白行は無視されます";

const props = defineProps<{
  initData: LotteryData;
}>();

const emit = defineEmits<{
  change: [data: LotteryData];
}>();

// TODO:認証情報をもとに編集可能かどうかを判断するように。DB書き込みも同様にする必要がある
const editable = ref(true);

const data = ref<LotteryData>(structuredClone(defaultLotteryData));
// 入力されたデータに変化あったらイベント発火
watch(data, () => emit("change", data.value), { deep: true });

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initData,
  () => (data.value = props.initData)
);

// 抽選対象群
// INPUT_TEXT_PLACEHOLDER_TEXT の条件をここで表現
const lotteryTargets = computed(() => data.value.input.text.split("\n").filter((x) => x));

function onClickLotteryButton() {
  // 抽選対象がなければ何もしない
  if (lotteryTargets.value.length === 0) return;
  // 抽選
  const result = lotteryTargets.value[random(lotteryTargets.value.length)];
  // 結果の記録と履歴保存
  data.value.result.result = result;
  data.value.result.histories.push(result);
}

function onInputFlexTextarea(inputText: string) {
  data.value.input.text = inputText;
}

function random(max: number) {
  return Math.floor(Math.random() * max);
}

function showResult(): boolean {
  // 抽選結果があれば表示ON
  return data.value.result.result !== "";
}

function showInputTitle(): boolean {
  // 抽選対象が入力されていれば表示ON
  return data.value.input.text !== "";
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div class="d-flex flex-column align-items-center w-100">
      <FlexTextarea
        class="w-100"
        @input="onInputFlexTextarea"
        :initText="data.input.text"
        :placeholder="INPUT_TEXT_PLACEHOLDER_TEXT"
        :disabled="!editable"
      />
      <div class="w-100">
        <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg w-100">抽選</button>
      </div>
      <div v-show="showResult()">
        <span>結果</span>
        <h1>{{ data.result.result }}</h1>
      </div>
      <div v-show="showInputTitle()" class="w-100">
        <div class="input-group">
          <span class="input-group-text">くじ引き名</span>
          <input
            v-model="data.input.title"
            class="form-control"
            placeholder="名前をつけると別のくじ引きも作成できるようになります"
            :disabled="!editable"
          />
        </div>
      </div>
    </div>
  </div>
</template>
