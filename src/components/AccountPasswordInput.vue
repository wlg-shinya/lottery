<script setup lang="ts">
import { ref } from "vue";
import Message from "./Message.vue";

defineProps<{
  showPassword: boolean; // TODO:このフラグの廃止をしてパスワード表示切り替え機能に対応する
  buttonClass: string;
  buttonText: string;
}>();

const emit = defineEmits<{
  click: [account: string, password: string];
}>();

defineExpose({ setMessage });

const message = ref();
const account = ref("");
const password = ref("");

async function onClickButton() {
  emit("click", account.value, password.value);
}

function canClick(): boolean {
  return account.value !== "" && password.value !== "";
}

function setMessage(body: string, color: string) {
  message.value.set(body, color);
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">アカウント</span>
        <input v-model="account" type="text" class="form-control" />
      </div>
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">パスワード</span>
        <input v-model="password" :type="showPassword ? 'text' : 'password'" class="form-control" />
      </div>
      <button @click="onClickButton" :class="`btn ${buttonClass}`" :disabled="!canClick()">{{ buttonText }}</button>
      <Message ref="message" />
    </div>
  </div>
</template>
