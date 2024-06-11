<script setup lang="ts">
import { ref } from "vue";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import AccountPasswordInput from "./AccountPasswordInput.vue";
import Message from "./Message.vue";

const message = ref();

async function onClickSignupButton(account: string, password: string) {
  await DefaultApiClient.signupApiSignupPost({
    account_name: account,
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
    <AccountPasswordInput @click="onClickSignupButton" buttonClass="btn-primary" buttonText="新規登録" />
    <Message ref="message" />
  </div>
</template>
