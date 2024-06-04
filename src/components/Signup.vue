<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
import { dbUserCreate } from "../db";

const username = ref("");
const password = ref("");

function onClickSignupButton() {
  dbUserCreate(username.value, password.value);
}

function onClickBackButton() {
  router.push("/");
}

function canSignup(): boolean {
  return username.value !== "" && password.value !== "";
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">アカウント</span>
        <input v-model="username" type="text" class="form-control" />
      </div>
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">パスワード</span>
        <input v-model="password" type="text" class="form-control" />
      </div>
      <button @click="onClickSignupButton" class="btn btn-primary" :disabled="!canSignup()">新規登録</button>
      <button @click="onClickBackButton" class="btn btn-link"><span class="mdi mdi-arrow-left" />戻る</button>
    </div>
  </div>
</template>
