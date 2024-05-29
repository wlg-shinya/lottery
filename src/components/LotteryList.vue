<script setup lang="ts">
import { ref, watch } from "vue";
import { type LotteryListData, defaultLotteryListData } from "../lottery-data";

const props = defineProps<{
  initData: LotteryListData;
}>();
// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initData,
  () => (data.value = props.initData)
);

const emit = defineEmits<{
  selected: [index: number];
}>();

const data = ref(defaultLotteryListData);

function onClickData(index: number) {
  emit("selected", index);
}
</script>

<template>
  <div>
    <table class="table table-hover border text-center">
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
        <tr v-for="(d, index) in data.list" :key="index" @click="onClickData(index)" :class="data.selectedIndex === index ? 'table-active' : ''">
          <td>{{ index }}</td>
          <td>{{ d.title }}</td>
          <td>
            <button @click.stop="" class="btn btn-danger"><span class="mdi mdi-trash-can" /></button>
          </td>
        </tr>
        <tr>
          <td colspan="3">
            <button class="btn btn-primary w-100"><span class="mdi mdi-plus" /></button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
