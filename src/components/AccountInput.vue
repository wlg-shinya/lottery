<script setup lang="ts">
import { ref, watchEffect } from "vue";
import { VarcharMax } from "../openapi";
import { PASSWORD_MAX_LENGTH } from "../constant";

const props = defineProps<{
  buttonClass: string;
  buttonText: string;
  hideUserName: boolean;
}>();

const emit = defineEmits<{
  click: [email: string, userName: string, password: string];
}>();

const email = ref("");
const userName = ref("");
const password = ref("");
const showPassword = ref(false);

watchEffect(() => {
  // テキスト入力の上限切りつめ
  if (email.value.length > VarcharMax.users_email) {
    email.value = email.value.slice(0, VarcharMax.users_email);
  }
  if (userName.value.length > VarcharMax.users_account_name) {
    userName.value = userName.value.slice(0, VarcharMax.users_account_name);
  }
  if (password.value.length > PASSWORD_MAX_LENGTH) {
    password.value = password.value.slice(0, PASSWORD_MAX_LENGTH);
  }
});

function onClickSubmitButton() {
  emit("click", email.value, userName.value, password.value);
}

function onClickShowPasswordButton() {
  showPassword.value = !showPassword.value;
}

function canClick(): boolean {
  const baseFlag = email.value !== "" && password.value !== "";
  return props.hideUserName ? baseFlag : baseFlag && userName.value !== "";
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">Eメール</span>
        <input v-model="email" type="text" class="form-control" />
      </div>
      <div v-if="!hideUserName" class="input-group">
        <span class="input-group-text" style="width: 100px">ユーザー名</span>
        <input v-model="userName" type="text" class="form-control" />
      </div>
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">パスワード</span>
        <input v-model="password" :type="showPassword ? 'text' : 'password'" class="form-control" />
        <button @click="onClickShowPasswordButton" :class="`btn ${showPassword ? 'btn-secondary' : 'btn-outline-secondary'}`">
          <span class="mdi mdi-eye" />
        </button>
      </div>
      <button @click="onClickSubmitButton" :class="`btn ${buttonClass}`" :disabled="!canClick()">{{ buttonText }}</button>
    </div>
  </div>
</template>
