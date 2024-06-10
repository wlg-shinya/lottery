<script setup lang="ts">
import { ref } from "vue";
import { DefaultApiClient } from "../openapi";
import { LotteryPublicData } from "../lottery-data";
import { getErrorMessage } from "../error";
import LocalStorageLottery from "../local-storage-lottery";
import { type LotteryUserInputData, defaultLotteryResultData } from "../lottery-data";
import router from "../router";
import Message from "../components/Message.vue";
import BackButton from "../components/BackButton.vue";
import SimpleShowText from "../components/OmitText.vue";

const _message = ref();
const allData = ref<LotteryPublicData[]>([]);

async function onStart() {
  await updateAllData();
}

async function onClickData(data: LotteryPublicData) {
  try {
    // ローカルストレージからデータを得る
    const lotteryTopData = await LocalStorageLottery.load()
      .then(async (result) => result)
      .catch((error) => {
        throw error;
      });

    // 自分自身のデータなら特に何もしない
    const mine = await DefaultApiClient.isLotteryIdMineApiIsLotteryIdMineGet(data.id, lotteryTopData.accessToken)
      .then((response) => response.data)
      .catch((error) => {
        throw error;
      });
    if (mine) return;

    // 選択したデータを更新 or 新規追加する
    let favoriteFirst = false;
    const favoritedData = lotteryTopData.listData.list.find((x) => x.inputData.id === data.id);
    if (favoritedData) {
      favoritedData.inputData = data as LotteryUserInputData;
    } else {
      lotteryTopData.listData.list.push({
        inputData: data as LotteryUserInputData,
        resultData: structuredClone(defaultLotteryResultData),
      });
      favoriteFirst = true;
    }

    // 選択したデータをローカルストレージに保存してHomeに戻る
    await LocalStorageLottery.save(lotteryTopData)
      .then(() => {
        // TODO:サインインしていたら今回選択したデータをお気に入りにしたと宣言する
        if (favoriteFirst) {
        }

        // Homeに戻る
        router.push("/");
      })
      .catch((error) => {
        throw error;
      });
  } catch (error) {
    _message.value.set(getErrorMessage(error), "text-danger");
  }
}

async function updateAllData() {
  // TODO:読込済みデータをキャッシュとして扱い更新処理負荷軽減を検討する

  // 更新前に古いデータをクリア
  allData.value = [];
  // 最新くじ引きデータをサーバーから全取得
  await DefaultApiClient.readLotteriesApiReadLotteriesGet()
    .then(async (response) => {
      for (const lottery of response.data) {
        // ユーザーIDからくじ引きを作成したユーザ名を得る
        const user_name = await DefaultApiClient.readUserApiReadUserGet(lottery.user_id)
          .then((response2) => response2.data.account_name)
          .catch((error) => {
            throw error;
          });

        // これまでの情報で公開用データを構築
        allData.value.push({
          id: lottery.id,
          text: lottery.text ?? "",
          title: lottery.title ?? "",
          description: lottery.description ?? "",
          user_name: user_name,
        });
      }
    })
    .catch((error) => {
      _message.value.set(getErrorMessage(error), "text-danger");
    });
}

onStart();
</script>

<template>
  <div>
    <BackButton />
    <div class="d-flex flex-column justify-content-center">
      <Message ref="_message" />
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th class="col-5">くじ引き名</th>
            <th class="col-2">作成者</th>
            <th class="col-5">説明</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in allData" @click="onClickData(data)" :key="JSON.stringify(data)">
            <td>{{ data.title }}</td>
            <td>{{ data.user_name }}</td>
            <td style="white-space: pre-wrap">
              <SimpleShowText :text="data.description" :length="32" :allowLineFeed="false" :initOmit="true" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
