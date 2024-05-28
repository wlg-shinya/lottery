<script setup lang="ts">
import { ref, computed } from "vue";
import FlexTextarea from "./FlexTextarea.vue";

const inputLotteryList = ref("");
const resultLottery = ref("");

// 抽選文字列一覧
// - 改行単位
// - 空行は抽選対象外
const lotteryList = computed(() => inputLotteryList.value.split("\n").filter((x) => x));

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
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div>
      <FlexTextarea @input="onInputFlexTextarea" style="min-width: 200px" />
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
