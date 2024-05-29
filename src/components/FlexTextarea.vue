<script setup lang="ts">
// 入力された文字列に合わせて可変する textarea
// ref. https://qiita.com/tsmd/items/fce7bf1f65f03239eef0

import { ref, watch } from "vue";

const props = defineProps<{
  initText: string;
  placeholder: string;
}>();

const emit = defineEmits<{
  input: [text: string];
}>();

const flexTextareaDummy = ref();
const inputText = ref("");

// 入力文字列に初期文字列を設定
// 初期文字列はローカルストレージ読込による遅延が起きるので watch で検出する
watch(
  () => props.initText,
  () => (inputText.value = props.initText)
);

function onInputFlexTextarea() {
  flexTextareaDummy.value.textContent = inputText.value + "\u200b";
  emit("input", inputText.value);
}
</script>

<template>
  <div class="FlexTextarea">
    <div ref="flexTextareaDummy" class="FlexTextarea__dummy" aria-hidden="true" />
    <textarea
      id="FlexTextarea"
      class="FlexTextarea__textarea input-body form-control"
      @input="onInputFlexTextarea"
      v-model="inputText"
      :placeholder="placeholder"
    />
  </div>
</template>

<style>
.FlexTextarea {
  position: relative;
}

.FlexTextarea__dummy {
  overflow: hidden;
  visibility: hidden;
  box-sizing: border-box;
  padding: 5px 15px;
  min-height: 120px;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
  border: 1px solid;
}

.FlexTextarea__textarea {
  position: absolute;
  top: 0;
  left: 0;
  display: block;
  overflow: hidden;
  box-sizing: border-box;
  padding: 5px 15px;
  width: 100%;
  height: 100%;
  background-color: transparent;
  border: 1px solid #b6c3c6;
  border-radius: 4px;
  color: inherit;
  font: inherit;
  letter-spacing: inherit;
  resize: none;
}
</style>
