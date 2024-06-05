<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  showPassword: boolean;
  buttonClass: string;
  buttonText: string;
}>();

const emit = defineEmits<{
  click: [account: string, password: string];
}>();

class Message {
  body: string = "";
  color: string = ""; // ex. 'text-primary' ref. https://getbootstrap.jp/docs/5.3/utilities/colors/

  valid(): boolean {
    return this.body !== "" && this.color !== "";
  }

  set(body: string, color: string) {
    this.body = body;
    this.color = color;
  }
}

const account = ref("");
const password = ref("");
const message = ref<Message>(new Message());

async function onClickButton() {
  emit("click", account.value, password.value);
}

function canClick(): boolean {
  return account.value !== "" && password.value !== "";
}

function showMessage(): boolean {
  return message.value.valid();
}

function setMessage(body: string, color: string) {
  message.value.set(body, color);
}

defineExpose({ setMessage });
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
      <div v-show="showMessage()" class="text-center">
        <span :class="`${message.color} fw-bold`">{{ message.body }}</span>
      </div>
    </div>
  </div>
</template>
