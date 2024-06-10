<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryTopData, defaultLotteryListData, defaultLotteryData, defaultLotteryResultData } from "../lottery-data";
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

const _modal = ref();
const _uploadDownload = ref();
const _signin = ref();

const lotteryTopData = ref(structuredClone(defaultLotteryTopData));
// データに変化あり次第ローカルストレージに保存
watch(
  () => lotteryTopData,
  () => LocalStorageLottery.save(lotteryTopData.value),
  { deep: true }
);

// 現在選択中のデータ
// selectedLotteryData.value への直代入は参照先の変更（＝選択変更）であり値は変更されない点に注意
const selectedLotteryData = ref<LotteryData | null>(null);

const localLotteryData = computed((): LotteryData[] => lotteryTopData.value.listData.list.filter((x) => x.inputData.id === -1));
const serverSavedLotteryData = computed((): LotteryData[] => lotteryTopData.value.listData.list.filter((x) => x.inputData.id !== -1));

async function onStart() {
  await LocalStorageLottery.setup();
  await LocalStorageLottery.load().then((result) => {
    lotteryTopData.value = result;
    // ローカルストレージからデータを得られたら先頭要素を選択するようにする
    resetSelectedLotteryData();
  });
}

async function onSignin(accessToken: string) {
  // サインイン済みの場合はユーザー確認の上でサインアウトしてからサインインする
  // 新規サインインの時は普通にサインイン
  if (lotteryTopData.value.accessToken) {
    _modal.value.show("注意", "サーバーに保存していないデータはすべて消えます。よろしいですか？", "OK", async () => {
      signout();
      await signin(accessToken);
    });
  } else {
    await signin(accessToken);
  }
}

function onSignout() {
  // ローカルデータが消えるのでユーザー確認してからサインアウト
  if (lotteryTopData.value.accessToken) {
    _modal.value.show("注意", "サーバーに保存していないデータはすべて消えます。よろしいですか？", "OK", async () => {
      _signin.value.clear();
      signout();
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
  // MEMO:選択状態リセットを2段階にする理由
  // 削除結果を反映すると選択している参照オブジェクトがいつ参照できなくなるかは不定なので削除前に比較する必要がある
  // しかし選択状態のリセットは削除結果を反映した後のデータで行いたい。このジレンマの解消のため
  const requierdResetSelectedLotteryData = selectedLotteryData.value === data;
  // 指定されたデータを厳密な参照値比較によって特定して削除後の一覧を作成する
  const deletedList = lotteryTopData.value.listData.list.filter((x) => x !== data);
  // 削除の結果、データが空になるならデフォルトデータを入れておく
  if (deletedList.length === 0) {
    deletedList.push(structuredClone(defaultLotteryData));
  }
  // 削除結果を反映
  lotteryTopData.value.listData.list = deletedList;
  // 削除結果反映後のデータで選択状態をリセット
  if (requierdResetSelectedLotteryData) {
    resetSelectedLotteryData();
  }
}

function onChangeLottery(data: LotteryData) {
  if (selectedLotteryData.value) {
    selectedLotteryData.value.inputData = data.inputData;
    selectedLotteryData.value.resultData = data.resultData;
  }
}

function onClearHistoryLotteryHistoryList() {
  _modal.value.show("注意", "履歴を本当にクリアしますか？この操作は取り消せません", "クリア", () => doClearHistory());
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
  _modal.value.show("注意", "サーバーに保存していないデータはすべて消えます。よろしいですか？", "OK", () =>
    downloadData(lotteryTopData.value.accessToken, true)
  );
}

function showLocalLotteryList(): boolean {
  // ローカルデータにタイトルを入力したか、ローカルデータが一つよりも多くある場合は表示ON
  return (
    (localLotteryData.value.length > 0 && localLotteryData.value[0].inputData.title !== "") ||
    localLotteryData.value.length > 1 ||
    showServerSavedLotteryList()
  );
}

function showServerSavedLotteryList(): boolean {
  // サーバー保存済みデータが一つでもあれば表示ON
  return serverSavedLotteryData.value.length > 0;
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
  await DefaultApiClient.readMyLotteriesApiReadMyLotteriesGet(accessToken)
    .then(async (response) => {
      let uploaded = false;

      // ローカル側で削除されたデータがあればサーバー側も削除する
      const serverIds = response.data.map((x) => x.id);
      const localIds = lotteryTopData.value.listData.list.map((x) => x.inputData.id);
      const deletedIds = serverIds.filter((id) => !localIds.some((x) => x === id));
      for (const id of deletedIds) {
        await DefaultApiClient.deleteLotteryApiDeleteLotteryDelete(id, { access_token: accessToken })
          .then(() => (uploaded = true))
          .catch((error) => {
            throw error;
          });
      }

      // ローカル側をサーバー側にすべてアップロード
      for (const list of lotteryTopData.value.listData.list) {
        if (list.inputData.text) {
          // 抽選対象が入力されていたら保存する
          const data: LotteryCreate = {
            access_token: accessToken,
            text: list.inputData.text,
            title: list.inputData.title,
            description: list.inputData.description,
          };
          if (list.inputData.id < 0) {
            // IDが未定なら新規追加
            await DefaultApiClient.createLotteryApiCreateLotteryPost(data)
              .then((response) => {
                // サーバー保存の結果得られたIDで更新することで、ローカル作成状態でないことにする
                list.inputData.id = response.data.id;
                uploaded = true;
              })
              .catch((error) => {
                throw error;
              });
          } else {
            const mine = await DefaultApiClient.isLotteryIdMineApiIsLotteryIdMineGet(list.inputData.id, accessToken)
              .then((response) => response.data)
              .catch((error) => {
                throw error;
              });
            if (mine) {
              // IDが設定済みなら更新
              await DefaultApiClient.updateLotteryApiUpdateLotteryPut(list.inputData.id, data)
                .then(() => (uploaded = true))
                .catch((error) => {
                  throw error;
                });
            } else {
              // 自分の作成したデータではないので何もしない
            }
          }
        }
      }

      // 正常終了
      if (uploaded) {
        _uploadDownload.value.setMessage("サーバーに保存しました", "text-success");
      } else {
        _uploadDownload.value.setMessage("保存するデータがありません", "text-warning");
      }
    })
    .catch((error) => {
      _uploadDownload.value.setMessage(getErrorMessage(error), "text-danger");
    });
}

async function downloadData(accessToken: string, showWarning: boolean) {
  await DefaultApiClient.readMyLotteriesApiReadMyLotteriesGet(accessToken)
    .then((response) => {
      if (response.data.length > 0) {
        for (const lottery of response.data) {
          // ローカルにデフォルトデータしかない場合はそれを捨てる
          if (JSON.stringify(lotteryTopData.value.listData) === JSON.stringify(defaultLotteryListData)) {
            lotteryTopData.value.listData.list = [];
          }

          const oneListData = lotteryTopData.value.listData.list.find((x) => x.inputData.id === lottery.id);
          if (oneListData) {
            // ローカルにデータがすでにある場合は内容を最新に置き換え
            oneListData.inputData = {
              id: lottery.id,
              text: lottery.text ?? "",
              title: lottery.title ?? "",
              description: lottery.description ?? "",
            };
          } else {
            // ローカルにデータがない場合は新規追加
            lotteryTopData.value.listData.list.push({
              inputData: {
                id: lottery.id,
                text: lottery.text ?? "",
                title: lottery.title ?? "",
                description: lottery.description ?? "",
              },
              resultData: structuredClone(defaultLotteryResultData),
            });
          }
        }

        // 選択状態をリセット
        resetSelectedLotteryData();

        // 正常終了
        _uploadDownload.value.setMessage("サーバーから読み込みました", "text-success");
      } else if (showWarning) {
        _uploadDownload.value.setMessage("サーバーにデータがありませんでした", "text-warning");
      }
    })
    .catch((error) => {
      _uploadDownload.value.setMessage(getErrorMessage(error), "text-danger");
    });
}

async function signin(accessToken: string) {
  // サインインで取得したアクセストークンをローカルに保存
  lotteryTopData.value.accessToken = accessToken;
  // データをダウンロードしてくる
  await downloadData(accessToken, false);
}

function signout() {
  // サインインで取得したアクセストークンを削除
  lotteryTopData.value.accessToken = "";
  // ローカルデータを初期化
  lotteryTopData.value.listData = structuredClone(defaultLotteryListData);
  // 選択状態をリセット
  resetSelectedLotteryData();
}

function resetSelectedLotteryData() {
  selectedLotteryData.value = lotteryTopData.value.listData.list[0];
}

onStart();
</script>

<template>
  <div>
    <Modal ref="_modal" />
    <div class="d-flex flex-column align-items-center">
      <Signin ref="_signin" @signin="onSignin" />
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
              v-show="showServerSavedLotteryList()"
              @select="onSelectLotteryList"
              @delete="onDeleteLotteryList"
              :list="serverSavedLotteryData"
              header="サーバーに保存済み"
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
      <UploadDownload ref="_uploadDownload" @upload="onUpload" @download="onDownload" />
    </div>
    <hr />
    <div class="d-flex justify-content-center">
      <GoPublicView />
    </div>
  </div>
</template>
