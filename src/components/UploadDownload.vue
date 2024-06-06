<script setup lang="ts">
import { ref } from "vue";
import Message from "./Message.vue";

const props = defineProps<{
  accessToken: string;
}>();

const emit = defineEmits<{
  upload: [accessToken: string];
  download: [accessToken: string];
}>();

defineExpose({ setMessage });

function onClickUploadButton() {
  emit("upload", props.accessToken);
}

function onClickDownloadButton() {
  emit("download", props.accessToken);
}

const message = ref();

function show(): boolean {
  // アクセストークンが取得できていれば表示ON
  return props.accessToken !== "";
}

function setMessage(body: string, color: string) {
  message.value.set(body, color);
}
</script>

<template>
  <div v-show="show()" class="d-flex flex-column align-items-center">
    <div>
      <button @click="onClickUploadButton()" class="btn btn-success"><span class="mdi mdi-upload" />サーバーに保存</button>
      <button @click="onClickDownloadButton()" class="btn btn-outline-success"><span class="mdi mdi-download" />サーバーから読込</button>
    </div>
    <Message ref="message" />
  </div>
</template>
