<script setup lang="ts">
import { ref, watch, computed } from "vue";
import LocalStorageLottery from "../local-storage-lottery";
import FlexTextarea from "./FlexTextarea.vue";

const inputLotteryList = ref("");
const resultLottery = ref("");

// 入力された文字に変化あり次第ローカルストレージに保存
watch(inputLotteryList, () =>
  LocalStorageLottery.save({
    input: inputLotteryList.value,
  })
);

// 抽選文字列一覧
// - 改行単位
// - 空行は抽選対象外
const lotteryList = computed(() => inputLotteryList.value.split("\n").filter((x) => x));

async function onStart() {
  await LocalStorageLottery.setup();
  // ローカルストレージのデータから初期文字列を復元
  await LocalStorageLottery.load().then((data) => {
    inputLotteryList.value = data.input;
  });
}

function onClickLotteryButton() {
  resultLottery.value = lotteryList.value[random(lotteryList.value.length)];
}

function onInputFlexTextarea(text: string) {
  inputLotteryList.value = text;
}

function random(max: number) {
  // TODO:サーバサイドから得るべきか検討する
  return Math.floor(Math.random() * max);
}

onStart();
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div>
      <FlexTextarea @input="onInputFlexTextarea" :initText="inputLotteryList" style="min-width: 200px" />
    </div>
    <div>
      <ul>
        <li>一行がひとつのくじとなります</li>
        <li>空白行は無視されます</li>
      </ul>
    </div>
    <div>
      <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg">抽選</button>
    </div>
    <div v-if="resultLottery">
      <span>結果</span>
      <h1>{{ resultLottery }}</h1>
    </div>
  </div>
</template>
