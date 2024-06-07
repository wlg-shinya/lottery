<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
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

function onClickBackButton() {
  router.push("/");
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <AccountPasswordInput
        ref="accountPasswordInput"
        @click="onClickSignupButton"
        :showPassword="true"
        buttonClass="btn-primary"
        buttonText="新規登録"
      />
      <button @click="onClickBackButton" class="btn btn-link"><span class="mdi mdi-arrow-left" />戻る</button>
    </div>
  </div>
</template>
