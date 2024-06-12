<script setup lang="ts">
import { ref, watchEffect } from "vue";
import { VarcharMax } from "../openapi";
import { PASSWORD_MAX_LENGTH } from "../constant";

defineProps<{
  buttonClass: string;
  buttonText: string;
}>();

const emit = defineEmits<{
  click: [account: string, password: string];
}>();

const account = ref("");
const password = ref("");
const showPassword = ref(false);

watchEffect(() => {
  // テキスト入力の上限切りつめ
  if (account.value.length > VarcharMax.users_account_name) {
    account.value = account.value.slice(0, VarcharMax.users_account_name);
  }
  if (password.value.length > PASSWORD_MAX_LENGTH) {
    password.value = password.value.slice(0, PASSWORD_MAX_LENGTH);
  }
});

function onClickSubmitButton() {
  emit("click", account.value, password.value);
}

function onClickShowPasswordButton() {
  showPassword.value = !showPassword.value;
}

function canClick(): boolean {
  return account.value !== "" && password.value !== "";
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
    </div>
  </div>
</template>
