<script setup lang="ts">
import { ref } from "vue";
import { DefaultApiClient } from "../openapi";
import { LotteryPublicData } from "../lottery-data";
import { getErrorMessage } from "../error";
import Message from "../components/Message.vue";

const _message = ref();
const allData = ref<LotteryPublicData[]>([]);

async function onStart() {
  await updateAllData();
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
  <div class="d-flex flex-column justify-content-center">
    <Message ref="_message" />
    <table class="table table-striped text-center">
      <thead>
        <tr>
          <th class="col-4">くじ引き名</th>
          <th class="col-2">作成者</th>
          <th class="col-4">説明</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="data in allData" :key="JSON.stringify(data)">
          <td>{{ data.title }}</td>
          <td>{{ data.user_name }}</td>
          <td>{{ data.description }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
