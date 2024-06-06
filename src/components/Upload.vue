<script setup lang="ts">
import { ref } from "vue";
import Message from "./Message.vue";

const props = defineProps<{
  accessToken: string;
}>();

const emit = defineEmits<{
  click: [accessToken: string];
}>();

defineExpose({ setMessage });

function onClickButton() {
  emit("click", props.accessToken);
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
    <button @click="onClickButton()" class="btn btn-success"><span class="mdi mdi-upload" />サーバーに保存</button>
    <Message ref="message" />
  </div>
</template>
