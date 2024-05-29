<script setup lang="ts">
import { ref, watch } from "vue";
import { type LotteryData, defaultLotteryListData } from "../lottery-data";
import LocalStorageLottery from "../local-storage-lottery";
import Lottery from "../components/Lottery.vue";
import LotteryList from "../components/LotteryList.vue";
import ContactUs from "../components/ContactUs.vue";

const TITLE = import.meta.env.VITE_APP_TITLE;

const lotteryListData = ref(structuredClone(defaultLotteryListData));
// データに変化あり次第ローカルストレージに保存
watch(
  () => lotteryListData,
  () => LocalStorageLottery.save(lotteryListData.value),
  { deep: true }
);

async function onStart() {
  await LocalStorageLottery.setup();
  await LocalStorageLottery.load().then((result) => {
    lotteryListData.value = result;
  });
}

function onSelectLotteryList(index: number) {
  lotteryListData.value.selectedIndex = index;
}

function onChangeLottery(data: LotteryData) {
  lotteryListData.value.list[lotteryListData.value.selectedIndex] = data;
}

function showLotteryList(): boolean {
  // 最初のデータでタイトルを入力したか、データが一つよりも多くある場合はリスト表示ON
  return lotteryListData.value.list[0].input.title !== "" || lotteryListData.value.list.length > 1;
}

onStart();
</script>

<template>
  <div class="card">
    <div class="card-header text-center">
      <h1>{{ TITLE }}</h1>
    </div>
    <div class="card-body">
      <div class="d-flex">
        <div v-show="showLotteryList()" class="col-3">
          <LotteryList @select="onSelectLotteryList" :initData="lotteryListData" />
        </div>
        <div class="col-auto flex-fill">
          <Lottery @change="onChangeLottery" :initData="lotteryListData.list[lotteryListData.selectedIndex]" />
        </div>
      </div>
    </div>
    <div class="card-footer">
      <ContactUs />
    </div>
  </div>
</template>
