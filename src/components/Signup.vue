<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
import { AlreadyExistsError } from "../error";
import { DefaultApiClient } from "../openapi";
import AccountPasswordInput from "./AccountPasswordInput.vue";

const accountPasswordInput = ref();

async function onClickSignupButton(account: string, password: string) {
  await DefaultApiClient.readUsersApiReadUsersGet()
    .then(async (response) => {
      const users = response.data;
      if (users.some((x) => x.account_name === account)) {
        throw new AlreadyExistsError(account);
      }
      await DefaultApiClient.createUserApiCreateUserPost({
        account_name: account,
        identification: password,
      })
        .then(() => {
          accountPasswordInput.value.setMessage("ユーザー登録しました。戻ってサインインしてください", "text-success");
        })
        .catch((error) => {
          throw error;
        });
    })
    .catch((error: Error) => {
      accountPasswordInput.value.setMessage(error.message, "text-danger");
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
