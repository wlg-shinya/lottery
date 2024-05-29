<script setup lang="ts">
import { ref, watch, computed } from "vue";
import LocalStorageLottery from "../local-storage-lottery";
import FlexTextarea from "./FlexTextarea.vue";

const PLACEHOLDER_TEXT = "一行がひとつのくじとなります\n空白行は無視されます";

const input = ref("");
const result = ref("");

// TODO:認証情報をもとに編集可能かどうかを判断するように。DB書き込みも同様にする必要がある
const editable = ref(true);

// 入力された文字に変化あり次第ローカルストレージに保存
watch([input, result], () =>
  LocalStorageLottery.save({
    input: input.value,
    result: result.value,
  })
);

// 抽選対象群
// PLACEHOLDER_TEXT の条件をここで表現
const lotteryTargets = computed(() => input.value.split("\n").filter((x) => x));

async function onStart() {
  await LocalStorageLottery.setup();
  // ローカルストレージのデータから初期文字列を復元
  await LocalStorageLottery.load().then((data) => {
    input.value = data.input;
    result.value = data.result;
  });
}

function onClickLotteryButton() {
  result.value = lotteryTargets.value[random(lotteryTargets.value.length)];
}

function onInputFlexTextarea(text: string) {
  input.value = text;
}

function random(max: number) {
  // TODO:サーバサイドから得るべきか検討する
  return Math.floor(Math.random() * max);
}

onStart();
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <FlexTextarea @input="onInputFlexTextarea" :initText="input" :placeholder="PLACEHOLDER_TEXT" :disabled="!editable" style="min-width: 250px" />
    <div>
      <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg">抽選</button>
    </div>
    <div v-if="result">
      <span>結果</span>
      <h1>{{ result }}</h1>
    </div>
  </div>
</template>
