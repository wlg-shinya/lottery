<script setup lang="ts">
import { ref, watch } from "vue";
import { type LotteryListData, defaultLotteryData, defaultLotteryListData } from "../lottery-data";

const props = defineProps<{
  initData: LotteryListData;
}>();

const emit = defineEmits<{
  selected: [index: number];
}>();

const listData = ref(structuredClone(defaultLotteryListData));

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initData,
  () => (listData.value = props.initData)
);

function onClickData(index: number) {
  emit("selected", index);
}

function onClickAddButton() {
  addNewData();
}

function onClickDeleteButton(index: number) {
  listData.value.list = listData.value.list.filter((_x, i) => index !== i);
  // 最後の一つを削除した場合は初期状態を復元する
  if (listData.value.list.length === 0) {
    addNewData();
  }
  // 選択インデックスの更新
  if (listData.value.selectedIndex >= index && listData.value.selectedIndex > 0) {
    listData.value.selectedIndex--;
  }
}

function addNewData() {
  listData.value.list.push(structuredClone(defaultLotteryData));
}
</script>

<template>
  <div>
    <table class="table table-hover border text-center align-middle">
      <thead>
        <tr>
          <th class="col-1">#</th>
          <th class="col-auto">
            <span>くじ引き名</span>
          </th>
          <th class="col-1"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(d, index) in listData.list"
          :key="index"
          @click="onClickData(index)"
          :class="listData.selectedIndex === index ? 'table-active' : ''"
        >
          <td>{{ index }}</td>
          <td>{{ d.input.title }}</td>
          <td>
            <button @click.stop="onClickDeleteButton(index)" class="btn btn-danger"><span class="mdi mdi-trash-can" /></button>
          </td>
        </tr>
        <tr>
          <td colspan="3">
            <button @click="onClickAddButton" class="btn btn-primary w-100"><span class="mdi mdi-plus" /></button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
