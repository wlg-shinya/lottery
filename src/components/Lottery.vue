<script setup lang="ts">
import { ref, watch, computed } from "vue";
import LocalStorageLottery from "../local-storage-lottery";
import FlexTextarea from "./FlexTextarea.vue";

const PLACEHOLDER_TEXT = "一行がひとつのくじとなります\n空白行は無視されます";

const text = ref("");
const result = ref("");
const title = ref("");

// TODO:認証情報をもとに編集可能かどうかを判断するように。DB書き込みも同様にする必要がある
const editable = ref(true);

// 入力された文字に変化あり次第ローカルストレージに保存
watch([text, result, title], () =>
  LocalStorageLottery.save({
    text: text.value,
    result: result.value,
    title: title.value,
  })
);

// 抽選対象群
// PLACEHOLDER_TEXT の条件をここで表現
const lotteryTargets = computed(() => text.value.split("\n").filter((x) => x));

async function onStart() {
  await LocalStorageLottery.setup();
  // ローカルストレージのデータから初期文字列を復元
  await LocalStorageLottery.load().then((data) => {
    text.value = data.text;
    result.value = data.result;
  });
}

function onClickLotteryButton() {
  result.value = lotteryTargets.value[random(lotteryTargets.value.length)];
}

function onInputFlexTextarea(inputText: string) {
  text.value = inputText;
}

function random(max: number) {
  // TODO:サーバサイドから得るべきか検討する
  return Math.floor(Math.random() * max);
}

onStart();
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div v-if="title">
      <h2>{{ title }}</h2>
    </div>
    <FlexTextarea @input="onInputFlexTextarea" :initText="text" :placeholder="PLACEHOLDER_TEXT" :disabled="!editable" style="min-width: 250px" />
    <div>
      <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg">抽選</button>
    </div>
    <div v-if="result">
      <span>結果</span>
      <h1>{{ result }}</h1>
    </div>
    <div v-if="editable">
      <div class="input-group">
        <span class="input-group-text"><span class="mdi mdi-pencil" /></span>
        <input v-model="title" class="form-control" placeholder="このくじ引きに名前をつける" />
      </div>
    </div>
  </div>
</template>
