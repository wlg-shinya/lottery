<script setup lang="ts">
import { ref } from "vue";
import Message from "./Message.vue";

const emit = defineEmits<{
  upload: [];
  download: [];
}>();

defineExpose({ setMessage });

function onClickUploadButton() {
  emit("upload");
}

function onClickDownloadButton() {
  emit("download");
}

const _message = ref();

function setMessage(body: string, color: string) {
  _message.value.set(body, color);
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <div>
      <button @click="onClickUploadButton()" class="btn btn-success"><span class="mdi mdi-upload" />サーバーに保存</button>
      <button @click="onClickDownloadButton()" class="btn btn-outline-success"><span class="mdi mdi-download" />サーバーから読込</button>
    </div>
    <Message ref="_message" />
  </div>
</template>
