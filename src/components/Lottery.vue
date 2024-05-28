<script setup lang="ts">
import { ref, computed } from "vue";

const inputLotteryList = ref("");
const resultLottery = ref("");

const lotteryList = computed(() => inputLotteryList.value.split("\n"));

function onClickLotteryButton() {
  resultLottery.value = lotteryList.value[random(lotteryList.value.length)];
}

function random(max: number) {
  // TODO:サーバサイドから得るべきか検討する
  return Math.floor(Math.random() * max);
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div>
      <textarea v-model="inputLotteryList" class="input-body form-control" id="lotteryList"></textarea>
    </div>
    <div>
      <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg">抽選</button>
    </div>
    <div v-id="resultLottery">
      <span>結果</span>
      <h1>{{ resultLottery }}</h1>
    </div>
  </div>
</template>
