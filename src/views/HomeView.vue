<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryTopData } from "../lottery-data";
import LocalStorageLottery from "../local-storage-lottery";
import Modal from "../components/Modal.vue";
import Signin from "../components/Signin.vue";
import Lottery from "../components/Lottery.vue";
import LotteryList from "../components/LotteryList.vue";
import LotteryHistoryList from "../components/LotteryHistoryList.vue";

const modal = ref();

const lotteryTopData = ref(structuredClone(defaultLotteryTopData));
// データに変化あり次第ローカルストレージに保存
watch(
  () => lotteryTopData,
  () => LocalStorageLottery.save(lotteryTopData.value),
  { deep: true }
);

const lotteryListData = computed(() => lotteryTopData.value.listData);
const selectedLotteryData = computed(() => lotteryListData.value.list[lotteryListData.value.selectedIndex]);

async function onStart() {
  await LocalStorageLottery.setup();
  await LocalStorageLottery.load().then((result) => {
    lotteryTopData.value = result;
  });
}

function onSignin(accessToken: string) {
  lotteryTopData.value.accessToken = accessToken;
}

function onSelectLotteryList(index: number) {
  lotteryListData.value.selectedIndex = index;
}

function onChangeLottery(data: LotteryData) {
  lotteryListData.value.list[lotteryListData.value.selectedIndex] = data;
}

function onClearHistoryLotteryHistoryList() {
  modal.value.show("注意", "履歴を本当にクリアしますか？この操作は取り消せません", "クリア", () => doClearHistory());
}

function onChangeShowCountLotteryHistoryList(value: number) {
  selectedLotteryData.value.resultData.historyShowCount = value;
}

function showLotteryList(): boolean {
  // 最初のデータでタイトルを入力したか、データが一つよりも多くある場合は表示ON
  return lotteryListData.value.list[0].inputData.title !== "" || lotteryListData.value.list.length > 1;
}

function showLotteryHistoryList(): boolean {
  // 履歴がひとつでもあれば表示ON
  return selectedLotteryData.value.resultData.histories.length > 0;
}

function doClearHistory() {
  selectedLotteryData.value.resultData.histories = [];
}

onStart();
</script>

<template>
  <div>
    <Modal ref="modal" />
    <Signin @signin="onSignin" />
    <hr />
    <table class="table table-borderless">
      <tbody>
        <tr>
          <td class="col-4">
            <LotteryList v-show="showLotteryList()" @select="onSelectLotteryList" :initData="lotteryListData" />
          </td>
          <td class="col-4">
            <Lottery @change="onChangeLottery" :initData="selectedLotteryData" :accessToken="lotteryTopData.accessToken" />
          </td>
          <td class="col-4">
            <LotteryHistoryList
              v-show="showLotteryHistoryList()"
              @clearHistory="onClearHistoryLotteryHistoryList"
              @changeShowCount="onChangeShowCountLotteryHistoryList"
              :histories="selectedLotteryData.resultData.histories"
              :initShowCount="selectedLotteryData.resultData.historyShowCount"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
