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

function onSelectedLotteryList(index: number) {
  lotteryListData.value.selectedIndex = index;
}

function onChangedLottery(data: LotteryData) {
  lotteryListData.value.list[lotteryListData.value.selectedIndex] = data;
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
        <div class="col-3">
          <LotteryList @selected="onSelectedLotteryList" :initData="lotteryListData" />
        </div>
        <div class="col-auto flex-fill">
          <Lottery @changed="onChangedLottery" :initData="lotteryListData.list[lotteryListData.selectedIndex]" />
        </div>
      </div>
    </div>
    <div class="card-footer">
      <ContactUs />
    </div>
  </div>
</template>
