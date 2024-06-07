<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryTopData, defaultLotteryListData, defaultLotteryResultData } from "../lottery-data";
import LocalStorageLottery from "../local-storage-lottery";
import { DefaultApiClient, LotteryCreate } from "../openapi";
import { getErrorMessage } from "../error";
import Modal from "../components/Modal.vue";
import Signin from "../components/Signin.vue";
import Lottery from "../components/Lottery.vue";
import LotteryList from "../components/LotteryList.vue";
import LotteryHistoryList from "../components/LotteryHistoryList.vue";
import UploadDownload from "../components/UploadDownload.vue";

const modal = ref();
const uploadDownload = ref();

const lotteryTopData = ref(structuredClone(defaultLotteryTopData));
// データに変化あり次第ローカルストレージに保存
watch(
  () => lotteryTopData,
  () => LocalStorageLottery.save(lotteryTopData.value),
  { deep: true }
);

const selectedLotteryData = computed(() => lotteryTopData.value.listData.list[lotteryTopData.value.listData.selectedIndex]);
const isDefaultLotteryListData = computed(() => JSON.stringify(lotteryTopData.value.listData) === JSON.stringify(defaultLotteryListData));

async function onStart() {
  await LocalStorageLottery.setup();
  await LocalStorageLottery.load().then((result) => {
    lotteryTopData.value = result;
  });
}

async function onSignin(accessToken: string) {
  // サインインで取得したアクセストークンをローカルに保存
  lotteryTopData.value.accessToken = accessToken;
  // ローカルに作成したデータがない場合はダウンロードしてくる
  if (isDefaultLotteryListData.value) {
    await downloadData(accessToken);
  }
}

function onSelectLotteryList(index: number) {
  lotteryTopData.value.listData.selectedIndex = index;
}

function onChangeLottery(data: LotteryData) {
  lotteryTopData.value.listData.list[lotteryTopData.value.listData.selectedIndex] = data;
}

function onClearHistoryLotteryHistoryList() {
  modal.value.show("注意", "履歴を本当にクリアしますか？この操作は取り消せません", "クリア", () => doClearHistory());
}

function onChangeShowCountLotteryHistoryList(value: number) {
  selectedLotteryData.value.resultData.historyShowCount = value;
}

async function onUpload() {
  uploadData(lotteryTopData.value.accessToken);
}

async function onDownload() {
  downloadData(lotteryTopData.value.accessToken);
}

function showLotteryList(): boolean {
  // 最初のデータでタイトルを入力したか、データが一つよりも多くある場合は表示ON
  return (
    (lotteryTopData.value.listData.list.length > 0 && lotteryTopData.value.listData.list[0].inputData.title !== "") ||
    lotteryTopData.value.listData.list.length > 1
  );
}

function showLotteryHistoryList(): boolean {
  // 履歴がひとつでもあれば表示ON
  return selectedLotteryData.value.resultData.histories.length > 0;
}

function showUploadDownload(): boolean {
  // アクセストークンが取得できていれば表示ON
  return lotteryTopData.value.accessToken !== "";
}

function doClearHistory() {
  selectedLotteryData.value.resultData.histories = [];
}

async function uploadData(accessToken: string) {
  await DefaultApiClient.readMyLotteriesApiReadMyLotteriesGet(accessToken)
    .then(async (response) => {
      // ローカル側で削除されたデータがあればサーバー側も削除する
      const serverIds = response.data.map((x) => x.id);
      const localIds = lotteryTopData.value.listData.list.map((x) => x.inputData.id);
      const deletedIds = serverIds.filter((id) => !localIds.some((x) => x === id));
      for (const id of deletedIds) {
        // 削除命令は一気に発行して問題ないので await しない
        DefaultApiClient.deleteLotteryApiDeleteLotteryDelete(id, { access_token: accessToken }).catch((error) => {
          throw error;
        });
      }

      // ローカル側をサーバー側にすべてアップロード
      let uploaded = false;
      for (const list of lotteryTopData.value.listData.list) {
        if (list.inputData.text) {
          // 抽選対象が入力されていたら保存する
          const data: LotteryCreate = {
            access_token: accessToken,
            text: list.inputData.text,
            title: list.inputData.title,
          };
          if (list.inputData.id < 0) {
            // IDが未定なら新規追加
            await DefaultApiClient.createLotteryApiCreateLotteryPost(data)
              .then(() => (uploaded = true))
              .catch((error) => {
                throw error;
              });
          } else {
            // IDが設定済みなら更新
            await DefaultApiClient.updateLotteryApiUpdateLotteryPut(list.inputData.id, data)
              .then(() => (uploaded = true))
              .catch((error) => {
                throw error;
              });
          }
        }
      }

      // 正常終了
      if (uploaded) {
        uploadDownload.value.setMessage("サーバーに保存しました", "text-success");
      } else {
        uploadDownload.value.setMessage("保存するデータがありません", "text-warning");
      }
    })
    .catch((error) => {
      uploadDownload.value.setMessage(getErrorMessage(error), "text-danger");
    });
}

async function downloadData(accessToken: string) {
  await DefaultApiClient.readMyLotteriesApiReadMyLotteriesGet(accessToken)
    .then((response) => {
      // サーバー上にデータがあるときのみローカルと差し替える
      if (response.data.length > 0) {
        lotteryTopData.value.listData.list = [];
        for (const lottery of response.data) {
          lotteryTopData.value.listData.list.push({
            inputData: {
              id: lottery.id,
              text: lottery.text ?? "",
              title: lottery.title ?? "",
            },
            resultData: defaultLotteryResultData,
          });
        }
        lotteryTopData.value.listData.selectedIndex = 0;

        // 正常終了
        uploadDownload.value.setMessage("サーバーから読み込みました", "text-success");
      } else {
        uploadDownload.value.setMessage("サーバーにデータがありませんでした", "text-warning");
      }
    })
    .catch((error) => {
      uploadDownload.value.setMessage(getErrorMessage(error), "text-danger");
    });
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
            <LotteryList v-show="showLotteryList()" @select="onSelectLotteryList" :initData="lotteryTopData.listData" />
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
    <div v-show="showUploadDownload()">
      <hr />
      <UploadDownload ref="uploadDownload" @upload="onUpload" @download="onDownload" />
    </div>
  </div>
</template>
