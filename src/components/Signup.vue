<script setup lang="ts">
import { ref } from "vue";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import AccountInput from "./AccountInput.vue";
import Message from "./Message.vue";

const message = ref();

async function onClickSignupButton(email: string, accountName: string, password: string) {
  await DefaultApiClient.signupStep1ApiSignupStep1Post({
    email: email,
    account_name: accountName,
    identification: password,
  })
    .then(() => {
      message.value.set("ユーザー登録しました。戻ってサインインしてください", "text-success");
    })
    .catch((error) => {
      message.value.set(getErrorMessage(error), "text-danger");
    });
}
</script>

<template>
  <div class="d-flex flex-column justify-content-center">
    <AccountInput @click="onClickSignupButton" buttonClass="btn-primary" buttonText="新規登録" />
    <Message ref="message" />
  </div>
</template>
