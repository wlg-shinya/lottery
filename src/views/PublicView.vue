<script setup lang="ts">
import { ref, watchEffect, computed } from "vue";
import { DefaultApiClient, VarcharMax } from "../openapi";
import { getErrorMessage } from "../error";
import { LotteryContentsData, LotteryPublicData, defaultLotteryResultData } from "../lottery-data";
import LocalStorageLottery from "../local-storage-lottery";
import router from "../router";
import Message from "../components/Message.vue";
import HomeButton from "../components/HomeButton.vue";
import OmitText from "../components/OmitText.vue";
import HighlightText from "../components/HighlightText.vue";

const USED_MDI_CLASS = "mdi mdi-counter";
const PULL_MDI_CLASS = "mdi mdi-download";
const FILTER_MAX_LENGTH = Math.max(VarcharMax.lotteries_text, VarcharMax.lotteries_description);

const message = ref();
const allData = ref<LotteryPublicData[]>([]);
const filter = ref("");

// ソートタイプ
type SortType = "used" | "pull";
const sortType = ref<SortType>("used");

watchEffect(() => {
  // テキスト入力の上限切りつめ
  if (filter.value.length > FILTER_MAX_LENGTH) {
    filter.value = filter.value.slice(0, FILTER_MAX_LENGTH);
  }
});

const showData = computed((): LotteryPublicData[] => allData.value.filter((x) => x.title));
const sortedShowDataByUsedCountDesc = computed((): LotteryPublicData[] =>
  showData.value.slice().sort((a, b) => (a.usedCount < b.usedCount ? 1 : -1))
);
const sortedShowDataByPulledCountDesc = computed((): LotteryPublicData[] =>
  showData.value.slice().sort((a, b) => (a.pulledCount < b.pulledCount ? 1 : -1))
);
const sortedShowData = computed((): LotteryPublicData[] => {
  switch (sortType.value) {
    case "used":
      return sortedShowDataByUsedCountDesc.value;
    case "pull":
      return sortedShowDataByPulledCountDesc.value;
  }
});
const filteredSortedShowData = computed((): LotteryPublicData[] => {
  if (filter.value) {
    return sortedShowData.value.filter((x) => x.filteredString.search(filter.value.toLocaleLowerCase()) !== -1);
  } else {
    return sortedShowData.value;
  }
});

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
    const pullData = lotteryTopData.listData.list.find((x) => x.contentsData.id === data.id);
    if (pullData) {
      pullData.contentsData = data as LotteryContentsData;
    } else {
      lotteryTopData.listData.list.push({
        contentsData: data as LotteryContentsData,
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
      const data: LotteryPublicData = {
        id: lottery.id,
        text: lottery.text ?? "",
        title: lottery.title ?? "",
        description: lottery.description ?? "",
        mine: false, // 公開情報を見ている時点ではサインインしていないユーザーとして考える
        usedCount: lottery.used_count ?? 0,
        username: user_name,
        pulledCount: pulledCount,
        filteredString: "",
      };
      // タイトルと説明文の大文字小文字区別なしを検索フィルター対象文字列とする
      data.filteredString = `${data.title.toLocaleLowerCase()}\n${data.description?.toLocaleLowerCase()}`;
      allData.value.push(data);
    }
  } catch (error) {
    message.value.set(getErrorMessage(error), "text-danger");
  }
}

function numberToShowString(value: number) {
  return value.toLocaleString();
}

onStart();
</script>

<template>
  <div>
    <div class="d-flex flex-column justify-content-center">
      <HomeButton />
      <Message ref="message" />
      <div class="d-flex">
        <button @click="sortType = 'used'" :class="`btn ${sortType === 'used' ? 'btn' : 'text'}-primary`">
          <span :class="`${USED_MDI_CLASS} mdi-36px`" />
        </button>
        <button @click="sortType = 'pull'" :class="`btn ${sortType === 'pull' ? 'btn' : 'text'}-primary`">
          <span :class="`${PULL_MDI_CLASS} mdi-36px`" />
        </button>
        <div class="input-group">
          <span class="input-group-text"><span class="mdi mdi-magnify mdi-36px" /></span>
          <input v-model="filter" class="form-control fs-3" />
        </div>
      </div>
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th class="col-5">くじ引き名</th>
            <th class="col-2">作成者</th>
            <th class="col-5">説明</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in filteredSortedShowData" @click="onClickData(data)" :key="JSON.stringify(data)">
            <td>
              <HighlightText :text="data.title" :highlight="filter" /><br />
              <span :class="`${USED_MDI_CLASS} mdi-24px pe-2`" style="vertical-align: middle" />
              <span class="fw-light pe-4">{{ numberToShowString(data.usedCount) }}</span>
              <span :class="`${PULL_MDI_CLASS} mdi-24px pe-2`" style="vertical-align: middle" />
              <span class="fw-light pe-4">{{ numberToShowString(data.pulledCount) }}</span>
            </td>
            <td>{{ data.username }}</td>
            <td style="white-space: pre-wrap">
              <OmitText :text="data.description" :length="32" :allowLineFeed="false" :initOmit="true" :highlight="filter" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
