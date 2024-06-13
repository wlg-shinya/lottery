<script setup lang="ts">
import { ref } from "vue";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import AccountInput from "./AccountInput.vue";
import Message from "./Message.vue";

const message = ref();

async function onClickSignupButton(email: string, userName: string, password: string) {
  await DefaultApiClient.signupStep1ApiSignupStep1Post({
    email: email,
    account_name: userName,
    identification: password,
  })
    .then((response) => {
      message.value.set(response.data, "text-success");
    })
    .catch((error) => {
      message.value.set(getErrorMessage(error), "text-danger");
    });
}
</script>

<template>
  <div class="d-flex flex-column justify-content-center">
    <AccountInput
      @click="onClickSignupButton"
      :hideUserName="false"
      :submitLabel="'新規登録'"
      :emailLabel="'受信を確認できるEメールアドレス'"
      :userNameLabel="'登録したいユーザー名'"
      :passwordLabel="'サインイン時に入力するパスワード'"
    />
    <Message ref="message" />
  </div>
</template>
