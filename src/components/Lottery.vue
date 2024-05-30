<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { type LotteryData, defaultLotteryData } from "../lottery-data";
import FlexTextarea from "./FlexTextarea.vue";

const PLACEHOLDER_TEXT = "一行がひとつのくじとなります\n空白行は無視されます";

const props = defineProps<{
  initData: LotteryData;
}>();

const emit = defineEmits<{
  change: [data: LotteryData];
}>();

// TODO:認証情報をもとに編集可能かどうかを判断するように。DB書き込みも同様にする必要がある
const editable = ref(true);

const data = ref<LotteryData>(structuredClone(defaultLotteryData));
// 入力されたデータに変化あったらイベント発火
watch(data, () => emit("change", data.value), { deep: true });

// 初期データはローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initData,
  () => (data.value = props.initData)
);

// 抽選対象群
// PLACEHOLDER_TEXT の条件をここで表現
const lotteryTargets = computed(() => data.value.input.text.split("\n").filter((x) => x));

function onClickLotteryButton() {
  // 抽選
  const result = lotteryTargets.value[random(lotteryTargets.value.length)];
  // 結果の記録と履歴保存
  data.value.result.result = result;
  data.value.result.histories.push(result);
}

function onInputFlexTextarea(inputText: string) {
  data.value.input.text = inputText;
}

function random(max: number) {
  return Math.floor(Math.random() * max);
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div v-if="data.input.title">
      <h2>{{ data.input.title }}</h2>
    </div>
    <div class="d-flex flex-row">
      <div class="d-flex flex-column align-items-center">
        <FlexTextarea
          @input="onInputFlexTextarea"
          :initText="data.input.text"
          :placeholder="PLACEHOLDER_TEXT"
          :disabled="!editable"
          style="min-width: 250px"
        />
        <div>
          <button @click="onClickLotteryButton()" class="btn btn-primary btn-lg">抽選</button>
        </div>
        <div v-if="data.result.result">
          <span>結果</span>
          <h1>{{ data.result.result }}</h1>
        </div>
        <div v-if="editable">
          <div class="input-group">
            <span class="input-group-text"><span class="mdi mdi-pencil" /></span>
            <input v-model="data.input.title" class="form-control" placeholder="このくじ引きに名前をつける" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
