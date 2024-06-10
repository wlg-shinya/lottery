<script setup lang="ts">
import { ref } from "vue";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import AccountPasswordInput from "./AccountPasswordInput.vue";

const accountPasswordInput = ref();

async function onClickSignupButton(account: string, password: string) {
  await DefaultApiClient.signupApiSignupPost({
    account_name: account,
    identification: password,
  })
    .then(() => {
      accountPasswordInput.value.setMessage("ユーザー登録しました。戻ってサインインしてください", "text-success");
    })
    .catch((error) => {
      accountPasswordInput.value.setMessage(getErrorMessage(error), "text-danger");
    });
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <AccountPasswordInput ref="accountPasswordInput" @click="onClickSignupButton" buttonClass="btn-primary" buttonText="新規登録" />
    </div>
  </div>
</template>
