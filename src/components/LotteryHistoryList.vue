<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { defaultLotteryResultData } from "../lottery-data";

const props = defineProps<{
  histories: string[];
  initShowCount: number;
}>();

const emit = defineEmits<{
  clearHistory: [];
  changeShowCount: [value: number];
}>();

const showCount = ref(defaultLotteryResultData.historyShowCount);
watch(showCount, () => emit("changeShowCount", showCount.value));

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initShowCount,
  () => (showCount.value = props.initShowCount)
);

const historiesReversed = computed(() => props.histories.slice().reverse().slice(0, showCount.value));

function onClickClearHistoryButton() {
  emit("clearHistory");
}
</script>

<template>
  <div v-if="props.histories.length > 0">
    <div class="input-group">
      <span class="input-group-text">上限</span>
      <input v-model="showCount" type="number" class="form-control form-control-sm" />
    </div>
    <table class="table table-sm table-striped table-borderless text-center">
      <tbody>
        <tr v-for="(history, index) in historiesReversed" :key="index">
          <td>{{ props.histories.length - index }}回目</td>
          <td style="min-width: 100px">{{ history }}</td>
        </tr>
      </tbody>
    </table>
    <button @click="onClickClearHistoryButton" class="btn btn-danger w-100"><span class="mdi mdi-trash-can" /></button>
  </div>
</template>
