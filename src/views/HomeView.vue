<script setup lang="ts">
import { ref, watch, computed } from "vue";
import {
  type LotteryTopData,
  type LotteryData,
  type LotteryContentsData,
  defaultLotteryTopData,
  defaultLotteryListData,
  defaultLotteryData,
  defaultLotteryResultData,
} from "../lottery-data";
import LocalStorageLottery from "../local-storage-lottery";
import { DefaultApiClient, LotteryCreate } from "../openapi";
import { getErrorMessage } from "../error";
import Modal from "../components/Modal.vue";
import Signin from "../components/Signin.vue";
import Signout from "../components/Signout.vue";
import Lottery from "../components/Lottery.vue";
import LotteryList from "../components/LotteryList.vue";
import LotteryHistoryList from "../components/LotteryHistoryList.vue";
import UploadDownload from "../components/UploadDownload.vue";
import GoPublicView from "../components/GoPublicView.vue";

const modal = ref();
const uploadDownload = ref();
const signin = ref();

const lotteryTopData = ref(structuredClone(defaultLotteryTopData));
watch(
  lotteryTopData,
  (newValue: LotteryTopData) => {
    // データに変化あり次第ローカルストレージに保存
    LocalStorageLottery.save(newValue);

    // 以前選択していたデータがなくなっていたら末尾を選択する
    if (!newValue.listData.list.some((x) => x === selectedLotteryData.value)) {
      const lastIndex = Math.max(newValue.listData.list.length - 1, 0);
      selectedLotteryData.value = newValue.listData.list[lastIndex];
    }
  },
  { deep: true }
);

// 現在選択中のデータ
// selectedLotteryData.value への直代入は参照先の変更（＝選択変更）中身の変更はプロパティ経由にする必要がある
const selectedLotteryData = ref<LotteryData | null>(null);

const reverseLotteryData = computed((): LotteryData[] => lotteryTopData.value.listData.list.slice().reverse());
const localLotteryData = computed((): LotteryData[] => reverseLotteryData.value.filter((x) => x.contentsData.id === -1));
const serverSavedLotteryData = computed((): LotteryData[] => reverseLotteryData.value.filter((x) => x.contentsData.id !== -1));
const serverSavedMyLotteryData = computed((): LotteryData[] => serverSavedLotteryData.value.filter((x) => x.contentsData.mine));
const pullLotteryData = computed((): LotteryData[] => serverSavedLotteryData.value.filter((x) => !x.contentsData.mine));

async function onStart() {
  await LocalStorageLottery.setup();
  await LocalStorageLottery.load().then((result) => {
    lotteryTopData.value = result;
  });
}

async function onSignin(accessToken: string) {
  // サインイン済みの場合はユーザー確認の上でサインアウトしてからサインインする
  // 新規サインインの時は普通にサインイン
  if (lotteryTopData.value.accessToken) {
    modal.value.show("注意", "サーバーに保存していないデータはすべて消えます。よろしいですか？", "OK", async () => {
      doSignout();
      await doSignin(accessToken);
    });
  } else {
    await doSignin(accessToken);
  }
}

function onSignout() {
  // ローカルデータが消えるのでユーザー確認してからサインアウト
  if (lotteryTopData.value.accessToken) {
    modal.value.show("注意", "サーバーに保存していないデータはすべて消えます。よろしいですか？", "OK", async () => {
      signin.value.clear();
      doSignout();
    });
  }
}

function onSelectLotteryList(data: LotteryData) {
  selectedLotteryData.value = data;
}

function onAddNewLotteryList() {
  lotteryTopData.value.listData.list.push(structuredClone(defaultLotteryData));
  // 今回追加したデータを選択する
  selectedLotteryData.value = lotteryTopData.value.listData.list[lotteryTopData.value.listData.list.length - 1];
}

function onDeleteLotteryList(data: LotteryData) {
  // 指定されたデータを厳密な参照値比較によって特定して削除後の一覧を作成する
  const deletedList = lotteryTopData.value.listData.list.filter((x) => x !== data);
  // 削除の結果、データが空になるならデフォルトデータを入れておく
  if (deletedList.length === 0) {
    deletedList.push(structuredClone(defaultLotteryData));
  }
  // 削除結果を反映
  lotteryTopData.value.listData.list = deletedList;
}

function onChangeLottery(data: LotteryData) {
  if (selectedLotteryData.value) {
    selectedLotteryData.value.contentsData = data.contentsData;
    selectedLotteryData.value.resultData = data.resultData;
  }
}

function onClearHistoryLotteryHistoryList() {
  modal.value.show("注意", "履歴を本当にクリアしますか？この操作は取り消せません", "クリア", () => doClearHistory());
}

function onChangeShowCountLotteryHistoryList(value: number) {
  if (selectedLotteryData.value) {
    selectedLotteryData.value.resultData.historyShowCount = value;
  }
}

async function onUpload() {
  uploadData(lotteryTopData.value.accessToken);
}

async function onDownload() {
  modal.value.show("注意", "サーバーに保存していないデータはすべて消えます。よろしいですか？", "OK", () =>
    downloadData(lotteryTopData.value.accessToken, true)
  );
}

function showLocalLotteryList(): boolean {
  // ローカルデータにタイトルを入力したか、ローカルデータが一つよりも多くある場合は表示ON
  return (
    (localLotteryData.value.length > 0 && localLotteryData.value[0].contentsData.title !== "") ||
    localLotteryData.value.length > 1 ||
    showServerSavedMyLotteryList()
  );
}

function showServerSavedMyLotteryList(): boolean {
  // サーバー保存済みの自分のデータが一つでもあれば表示ON
  return serverSavedMyLotteryData.value.length > 0;
}

function showPullLotteryList(): boolean {
  // 他人が作成したデータが一つでもあれば表示ON
  return pullLotteryData.value.length > 0;
}

function showLotteryHistoryList(): boolean {
  if (selectedLotteryData.value) {
    // 履歴がひとつでもあれば表示ON
    return selectedLotteryData.value.resultData.histories.length > 0;
  } else {
    // データ未選択なら表示できるものはない
    return false;
  }
}

function showUploadDownload(): boolean {
  // アクセストークンが取得できていれば表示ON
  return lotteryTopData.value.accessToken !== "";
}

function doClearHistory() {
  if (selectedLotteryData.value) {
    selectedLotteryData.value.resultData.histories = [];
  }
}

async function uploadData(accessToken: string) {
  let uploaded = false;

  try {
    // ローカル側で削除されたデータがあればサーバー側も削除する
    await DefaultApiClient.readMyLotteriesApiReadMyLotteriesGet(accessToken)
      .then(async (response) => {
        const serverIds = response.data.map((x) => x.id);
        const localIds = lotteryTopData.value.listData.list.map((x) => x.contentsData.id);
        const deletedIds = serverIds.filter((id) => !localIds.some((x) => x === id));
        for (const id of deletedIds) {
          await DefaultApiClient.deleteLotteryApiDeleteLotteryDelete(id, { access_token: accessToken })
            .then(() => (uploaded = true))
            .catch((error) => {
              throw error;
            });
        }
      })
      .catch((error) => {
        throw error;
      });

    // ローカル側にあるほかの人が作成したデータのIDリストをアップロード
    const pullIds = pullLotteryData.value.map((x) => x.contentsData.id);
    if (pullIds.length > 0) {
      await DefaultApiClient.updateUserPullLotteryIdsApiUpdateUserPullLotteryIdsPut(accessToken, pullIds)
        .then(() => (uploaded = true))
        .catch((error) => {
          throw error;
        });
    }

    // ローカル側をサーバー側にすべてアップロード
    for (const list of lotteryTopData.value.listData.list) {
      if (list.contentsData.text) {
        // 抽選対象が入力されていたら保存する
        const data: LotteryCreate = {
          access_token: accessToken,
          text: list.contentsData.text,
          title: list.contentsData.title,
          description: list.contentsData.description,
        };
        if (list.contentsData.id < 0) {
          // IDが未定なら新規追加
          await DefaultApiClient.createLotteryApiCreateLotteryPost(data)
            .then((response2) => {
              // サーバー保存の結果得られたIDで更新することで、ローカル作成状態でないことにする
              list.contentsData.id = response2.data.id;
              uploaded = true;
            })
            .catch((error) => {
              throw error;
            });
        } else {
          if (list.contentsData.mine) {
            // 自分が作成したデータなので更新
            await DefaultApiClient.updateLotteryApiUpdateLotteryPut(list.contentsData.id, data)
              .then(() => (uploaded = true))
              .catch((error) => {
                throw error;
              });
          } else {
            // 自分が作成したデータではないので何もしない
          }
        }
      }
    }

    if (uploaded) {
      uploadDownload.value.setMessage("サーバーに保存しました", "text-success");
    } else {
      uploadDownload.value.setMessage("保存するデータがありません", "text-warning");
    }
  } catch (error) {
    uploadDownload.value.setMessage(getErrorMessage(error), "text-danger");
  }
}

async function downloadData(accessToken: string, showWarning: boolean) {
  let downloaded = false;
  const createOrUpdateLotteryContentsData = (contents: LotteryContentsData) => {
    const oldData = lotteryTopData.value.listData.list.find((x) => x.contentsData.id === contents.id);
    if (oldData) {
      // ローカルにデータがすでにある場合は内容を置き換え
      oldData.contentsData = contents;
    } else {
      // ローカルにデータがない場合は新規追加
      lotteryTopData.value.listData.list.push({
        contentsData: contents,
        resultData: structuredClone(defaultLotteryResultData),
      });
    }
    downloaded = true;
  };

  try {
    // 自分が作成してサーバーに保存したデータをダウンロードしてローカルに反映させる
    await DefaultApiClient.readMyLotteriesApiReadMyLotteriesGet(accessToken)
      .then((response) => {
        if (response.data.length > 0) {
          // ローカルにデフォルトデータしかない場合はそれを捨てる
          if (JSON.stringify(lotteryTopData.value.listData) === JSON.stringify(defaultLotteryListData)) {
            lotteryTopData.value.listData.list = [];
          }

          // データ作成 or 更新
          for (const lottery of response.data) {
            const newData: LotteryContentsData = {
              id: lottery.id,
              text: lottery.text ?? "",
              title: lottery.title ?? "",
              description: lottery.description ?? "",
              mine: true, // 自分のデータだけ取得してきているので true 固定
            };
            createOrUpdateLotteryContentsData(newData);
          }
        }
      })
      .catch((error) => {
        throw error;
      });

    // ほかの人が作成したデータをダウンロードしてローカルに反映させる
    await DefaultApiClient.readUserByAccessTokenApiReadUserByAccessTokenGet(accessToken)
      .then(async (response) => {
        const pullLotteryIds = response.data.pull_lottery_ids;
        if (pullLotteryIds) {
          for (const id of pullLotteryIds) {
            // 最新データをダウンロードしてくる
            const pullLottery = await DefaultApiClient.readLotteryApiReadLotteryGet(id)
              .then((response2) => response2.data)
              .catch((error) => {
                throw error;
              });
            const newData: LotteryContentsData = {
              id: pullLottery.id,
              text: pullLottery.text ?? "",
              title: pullLottery.title ?? "",
              description: pullLottery.description ?? "",
              mine: false, // 自分のものではないので false 固定
            };
            createOrUpdateLotteryContentsData(newData);
          }
        }
      })
      .catch((error) => {
        throw error;
      });

    if (downloaded) {
      uploadDownload.value.setMessage("サーバーから読み込みました", "text-success");
    } else if (showWarning) {
      uploadDownload.value.setMessage("サーバーにデータがありませんでした", "text-warning");
    }
  } catch (error) {
    uploadDownload.value.setMessage(getErrorMessage(error), "text-danger");
  }
}

async function doSignin(accessToken: string) {
  // サインインで取得したアクセストークンをローカルに保存
  lotteryTopData.value.accessToken = accessToken;
  // データをダウンロードしてくる
  await downloadData(accessToken, false);
}

function doSignout() {
  // サインインで取得したアクセストークンを削除
  lotteryTopData.value.accessToken = "";
  // ローカルデータを初期化
  lotteryTopData.value.listData = structuredClone(defaultLotteryListData);
}

onStart();
</script>

<template>
  <div>
    <Modal ref="modal" />
    <div class="d-flex flex-column align-items-center">
      <Signin ref="signin" @signin="onSignin" />
      <Signout @signout="onSignout" />
    </div>
    <hr />
    <table class="table table-borderless">
      <tbody>
        <tr>
          <td class="col-4">
            <LotteryList
              v-show="showLocalLotteryList()"
              @select="onSelectLotteryList"
              @delete="onDeleteLotteryList"
              :list="localLotteryData"
              header="ローカルで作成中"
              :addable="true"
              @add_new="onAddNewLotteryList"
            />
            <LotteryList
              v-show="showServerSavedMyLotteryList()"
              @select="onSelectLotteryList"
              @delete="onDeleteLotteryList"
              :list="serverSavedMyLotteryData"
              header="サーバーに保存済み"
              :addable="false"
            />
            <LotteryList
              v-show="showPullLotteryList()"
              @select="onSelectLotteryList"
              @delete="onDeleteLotteryList"
              :list="pullLotteryData"
              header="ほかの人が作成"
              :addable="false"
            />
          </td>
          <td class="col-4">
            <Lottery @change="onChangeLottery" :initData="selectedLotteryData" :accessToken="lotteryTopData.accessToken" />
          </td>
          <td class="col-4">
            <LotteryHistoryList
              v-if="selectedLotteryData"
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
    <hr />
    <div class="d-flex justify-content-center">
      <GoPublicView />
    </div>
  </div>
</template>
