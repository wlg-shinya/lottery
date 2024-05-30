<script setup lang="ts">
import { ref, watch } from "vue";
import { type LotteryData, defaultLotteryListData } from "../lottery-data";
import LocalStorageLottery from "../local-storage-lottery";
import Modal from "../components/Modal.vue";
import Lottery from "../components/Lottery.vue";
import LotteryList from "../components/LotteryList.vue";
import LotteryHistoryList from "../components/LotteryHistoryList.vue";
import ContactUs from "../components/ContactUs.vue";

const TITLE = import.meta.env.VITE_APP_TITLE;

const modal = ref();

const lotteryListData = ref(structuredClone(defaultLotteryListData));
// データに変化あり次第ローカルストレージに保存
watch(
  () => lotteryListData,
  () => LocalStorageLottery.save(lotteryListData.value),
  { deep: true }
);

const selectedLotteryData = () => lotteryListData.value.list[lotteryListData.value.selectedIndex];

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

function onClearHistoryLotteryHistoryList() {
  modal.value.show("注意", "履歴を本当にクリアしますか？この操作は取り消せません", "クリア", () => doClearHistory());
}

function onChangeShowCountLotteryHistoryList(value: number) {
  selectedLotteryData().result.historyShowCount = value;
}

function showLotteryList(): boolean {
  // 最初のデータでタイトルを入力したか、データが一つよりも多くある場合は表示ON
  return lotteryListData.value.list[0].input.title !== "" || lotteryListData.value.list.length > 1;
}

function showLotteryHistoryList(): boolean {
  // 履歴がひとつでもあれば表示ON
  return selectedLotteryData().result.histories.length > 0;
}

function doClearHistory() {
  selectedLotteryData().result.histories = [];
}

onStart();
</script>

<template>
  <div>
    <Modal ref="modal" />
    <div class="card">
      <div class="card-header text-center">
        <h1>{{ TITLE }}</h1>
      </div>
      <div class="card-body">
        <table class="table table-borderless">
          <tbody>
            <tr>
              <td class="col-4">
                <LotteryList v-show="showLotteryList()" @select="onSelectLotteryList" :initData="lotteryListData" />
              </td>
              <td class="col-4">
                <Lottery @change="onChangeLottery" :initData="selectedLotteryData()" />
              </td>
              <td class="col-4">
                <LotteryHistoryList
                  v-show="showLotteryHistoryList()"
                  @clearHistory="onClearHistoryLotteryHistoryList"
                  @changeShowCount="onChangeShowCountLotteryHistoryList"
                  :histories="selectedLotteryData().result.histories"
                  :initShowCount="selectedLotteryData().result.historyShowCount"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer">
        <ContactUs />
      </div>
    </div>
  </div>
</template>
