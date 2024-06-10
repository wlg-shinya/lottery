<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryData, defaultLotteryListData } from "../lottery-data";
import Modal from "./Modal.vue";

const props = defineProps<{
  list: LotteryData[];
  header: string;
  addable: boolean;
}>();

const emit = defineEmits<{
  select: [data: LotteryData];
  add_new: [];
  delete: [data: LotteryData];
}>();

const modal = ref();
const listData = ref(structuredClone(defaultLotteryListData));

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.list,
  () => (listData.value.list = props.list)
);

const existsDefaultLotteryData = computed(() => listData.value.list.some((x) => JSON.stringify(x) === JSON.stringify(defaultLotteryData)));

function onClickData(data: LotteryData) {
  emit("select", data);
}

function onClickAddButton() {
  // デフォルトデータが存在する場合は新規追加しない
  if (existsDefaultLotteryData.value) return;
  // チェックに通過したので新規追加
  emit("add_new");
}

function onClickDeleteButton(data: LotteryData) {
  modal.value.show("注意", "本当に削除しますか？この操作は取り消せません", "削除", () => emit("delete", data));
}

// function addNewData() {
//   listData.value.list.push(structuredClone(defaultLotteryData));
// }

// function doDelete(index: number) {
//   listData.value.list = listData.value.list.filter((_x, i) => index !== i);
//   // 最後の一つを削除した場合は初期状態を復元する
//   if (listData.value.list.length === 0) {
//     addNewData();
//   }
// }
</script>

<template>
  <div>
    <Modal ref="modal" />
    <table class="table table-hover border text-center align-middle">
      <thead>
        <tr>
          <th class="col-auto">
            <span>{{ header }}</span>
          </th>
          <th class="col-1"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(d, index) in listData.list" :key="index" @click="onClickData(d)">
          <td>{{ d.inputData.title }}</td>
          <td>
            <button @click.stop="onClickDeleteButton(d)" class="btn btn-danger"><span class="mdi mdi-trash-can" /></button>
          </td>
        </tr>
        <tr v-if="addable">
          <td colspan="2">
            <button @click="onClickAddButton" class="btn btn-primary w-100" :disabled="existsDefaultLotteryData">
              <span class="mdi mdi-plus" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
