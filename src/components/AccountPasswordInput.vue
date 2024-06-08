<script setup lang="ts">
import { ref } from "vue";
import Message from "./Message.vue";

defineProps<{
  buttonClass: string;
  buttonText: string;
}>();

const emit = defineEmits<{
  click: [account: string, password: string];
}>();

defineExpose({ setMessage, clear });

const message = ref();
const account = ref("");
const password = ref("");
const showPassword = ref(false);

function onClickSubmitButton() {
  emit("click", account.value, password.value);
}

function onClickShowPasswordButton() {
  showPassword.value = !showPassword.value;
}

function canClick(): boolean {
  return account.value !== "" && password.value !== "";
}

function setMessage(body: string, color: string) {
  message.value.set(body, color);
}

function clear() {
  account.value = "";
  password.value = "";
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
        <button @click="onClickShowPasswordButton" :class="`btn ${showPassword ? 'btn-secondary' : 'btn-outline-secondary'}`">
          <span class="mdi mdi-eye" />
        </button>
      </div>
      <button @click="onClickSubmitButton" :class="`btn ${buttonClass}`" :disabled="!canClick()">{{ buttonText }}</button>
      <Message ref="message" />
    </div>
  </div>
</template>
