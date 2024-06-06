<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryTopData } from "../lottery-data";
import LocalStorageLottery from "../local-storage-lottery";
import { DefaultApiClient, LotteryCreate } from "../openapi";
import { CanNotCreateLotteryError, CanNotUpdateLotteryError } from "../error";
import Modal from "../components/Modal.vue";
import Signin from "../components/Signin.vue";
import Lottery from "../components/Lottery.vue";
import LotteryList from "../components/LotteryList.vue";
import LotteryHistoryList from "../components/LotteryHistoryList.vue";
import Upload from "../components/Upload.vue";

const modal = ref();
const upload = ref();

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
  // 自分が作成したおみくじデータのダウンロード
  // DefaultApiClient.readLotteriesApiReadLotteriesGet().then((response) => {
  //   response.filter()
  // });
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

function onClickUpload(accessToken: string) {
  // 作成したくじ引きデータをDBに書き込む
  try {
    for (const list of lotteryListData.value.list) {
      const data: LotteryCreate = {
        user_id: Number(accessToken), // TODO:OpenAPI側もアクセストークンで処理するように変更
        text: list.inputData.text,
        title: list.inputData.title,
      };
      if (list.inputData.id < 0) {
        // IDが未定なら新規追加
        DefaultApiClient.createLotteryApiCreateLotteryPost(data).catch(() => {
          throw new CanNotCreateLotteryError(data);
        });
      } else {
        // IDが設定済みなら更新
        DefaultApiClient.updateLotteryApiUpdateLotteryPut(list.inputData.id, data).catch(() => {
          throw new CanNotUpdateLotteryError({ 999: list.inputData.id, data });
        });
      }
    }

    // 正常終了
    upload.value.setMessage("保存しました", "text-success");
  } catch (e: any) {
    const error = e as Error;
    upload.value.setMessage(error.message, "text-danger");
  }
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
            <Lottery @change="onChangeLottery" :initData="selectedLotteryData" />
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
    <hr />
    <Upload ref="upload" @click="onClickUpload" :accessToken="lotteryTopData.accessToken" />
  </div>
</template>
