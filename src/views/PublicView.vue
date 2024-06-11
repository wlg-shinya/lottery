<script setup lang="ts">
import { ref, computed } from "vue";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import LocalStorageLottery from "../local-storage-lottery";
import { LotteryUserInputData, LotteryPublicData, defaultLotteryResultData } from "../lottery-data";
import router from "../router";
import Message from "../components/Message.vue";
import BackButton from "../components/BackButton.vue";
import SimpleShowText from "../components/OmitText.vue";

const message = ref();
const allData = ref<LotteryPublicData[]>([]);

const showData = computed(() => allData.value.filter((x) => x.title));

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

    // 自分自身のデータならここで処理中断
    const mine = await DefaultApiClient.isLotteryIdMineApiIsLotteryIdMineGet(data.id, lotteryTopData.accessToken)
      .then((response) => response.data)
      .catch((error) => {
        throw error;
      });
    if (mine) return;

    // 選択したデータを更新 or 新規追加する
    const pullData = lotteryTopData.listData.list.find((x) => x.inputData.id === data.id);
    if (pullData) {
      pullData.inputData = data as LotteryUserInputData;
    } else {
      lotteryTopData.listData.list.push({
        inputData: data as LotteryUserInputData,
        resultData: structuredClone(defaultLotteryResultData),
      });
    }

    // 選択したデータをローカルストレージに保存してHomeに戻る
    await LocalStorageLottery.save(lotteryTopData)
      .then(() => {
        router.push("/");
      })
      .catch((error) => {
        throw error;
      });
  } catch (error) {
    message.value.set(getErrorMessage(error), "text-danger");
  }
}

async function updateAllData() {
  // 更新前に古いデータをクリア
  allData.value = [];

  try {
    // 最新の各種データをサーバーから取得
    const response = await Promise.all([DefaultApiClient.readLotteriesApiReadLotteriesGet(), DefaultApiClient.readUsersApiReadUsersGet()])
      .then((response) => response)
      .catch((error) => {
        throw error;
      });
    const allLotteries = response[0].data;
    const allUsers = response[1].data;

    // 取得できた各種データから公開するべきデータを構築する
    for (const lottery of allLotteries) {
      // ユーザーIDからくじ引きを作成したユーザ名を得る
      const user_name = allUsers.find((x) => x.id === lottery.user_id)?.account_name;
      if (!user_name) {
        throw new Error(`Not found user_id(${lottery.id})`);
      }

      // このくじ引きがほかの人にどれだけ取得されているか集計する
      const pulledCount = allUsers.reduce((acc, current) => {
        // あるユーザがこのくじ引きIDを取得していたら1、そうでなければ0としてその累計を算出
        const count = current.pull_lottery_ids?.some((id) => id === lottery.id) ? 1 : 0;
        return acc + count;
      }, 0);

      // これまでの情報で公開用データを構築
      allData.value.push({
        id: lottery.id,
        text: lottery.text ?? "",
        title: lottery.title ?? "",
        description: lottery.description ?? "",
        mine: false, // 公開情報を見ている時点ではサインインしていないユーザーとして考える
        user_name: user_name,
        pulled_count: pulledCount,
      });
    }
  } catch (error) {
    message.value.set(getErrorMessage(error), "text-danger");
  }
}

onStart();
</script>

<template>
  <div>
    <BackButton />
    <div class="d-flex flex-column justify-content-center">
      <Message ref="message" />
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th class="col-5">くじ引き名</th>
            <th class="col-2">作成者</th>
            <th class="col-5">説明</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in showData" @click="onClickData(data)" :key="JSON.stringify(data)">
            <td>
              {{ data.title }}<br />
              <span class="mdi mdi-content-copy"></span><span class="fw-light">{{ data.pulled_count.toLocaleString() }}</span>
            </td>
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
