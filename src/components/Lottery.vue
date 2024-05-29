<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryData } from "../lottery-data";
import FlexTextarea from "./FlexTextarea.vue";

const PLACEHOLDER_TEXT = "一行がひとつのくじとなります\n空白行は無視されます";

const props = defineProps<{
  initData: LotteryData;
}>();

const emit = defineEmits<{
  changed: [data: LotteryData];
}>();

// TODO:認証情報をもとに編集可能かどうかを判断するように。DB書き込みも同様にする必要がある
const editable = ref(true);

const inputData = ref<LotteryData>(structuredClone(defaultLotteryData));
// 入力されたデータに変化あったらイベント発火
watch(inputData, () => emit("changed", inputData.value), { deep: true });

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initData,
  () => (inputData.value = props.initData)
);

// 抽選対象群
// PLACEHOLDER_TEXT の条件をここで表現
const lotteryTargets = computed(() => inputData.value.text.split("\n").filter((x) => x));

function onClickLotteryButton() {
  // 抽選
  const result = lotteryTargets.value[random(lotteryTargets.value.length)];
  // 結果の記録と履歴保存
  inputData.value.result = result;
  inputData.value.history.push(result);
}

function onInputFlexTextarea(inputText: string) {
  inputData.value.text = inputText;
}

function random(max: number) {
  // TODO:サーバサイドから得るべきか検討する
  return Math.floor(Math.random() * max);
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div v-if="inputData.title">
      <h2>{{ inputData.title }}</h2>
    </div>
    <FlexTextarea
      @input="onInputFlexTextarea"
      :initText="inputData.text"
      :placeholder="PLACEHOLDER_TEXT"
      :disabled="!editable"
      style="min-width: 250px"
    />
    <div>
      <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg">抽選</button>
    </div>
    <div v-if="inputData.result">
      <span>結果</span>
      <h1>{{ inputData.result }}</h1>
    </div>
    <div v-if="editable">
      <div class="input-group">
        <span class="input-group-text"><span class="mdi mdi-pencil" /></span>
        <input v-model="inputData.title" class="form-control" placeholder="このくじ引きに名前をつける" />
      </div>
    </div>
  </div>
</template>
