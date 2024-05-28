<script setup lang="ts">
// ref. https://qiita.com/tsmd/items/fce7bf1f65f03239eef0

import { ref } from "vue";

const flexTextareaDummy = ref();
const inputText = ref("");

const emit = defineEmits<{
  input: [text: string];
}>();

function onInputFlexTextarea() {
  flexTextareaDummy.value.textContent = inputText.value + "\u200b";
  emit("input", inputText.value);
}
</script>

<template>
  <div class="FlexTextarea">
    <div ref="flexTextareaDummy" class="FlexTextarea__dummy" aria-hidden="true" />
    <textarea id="FlexTextarea" class="FlexTextarea__textarea input-body form-control" @input="onInputFlexTextarea" v-model="inputText" />
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
