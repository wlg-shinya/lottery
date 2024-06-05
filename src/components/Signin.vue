<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
import { NoSignupError, InvalidPasswordError } from "../error";
import { DefaultApiClient } from "../openapi";
import AccountPasswordInput from "./AccountPasswordInput.vue";

const accountPasswordInput = ref();

async function onClickSigninButton(account: string, password: string) {
  await DefaultApiClient.readUsersApiReadUsersGet()
    .then(async (response) => {
      const users = response.data;
      const user = users.find((x) => x.account_name === account);
      if (!user) {
        throw new NoSignupError(account);
      } else if (user.identification !== password) {
        throw new InvalidPasswordError();
      } else {
        // TODO:サインイン成功処理の実装
      }
    })
    .catch((error: Error) => {
      accountPasswordInput.value.setMessage(error.message, "text-danger");
    });
}

function onClickSignupButton() {
  router.push("/signup");
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <AccountPasswordInput
        ref="accountPasswordInput"
        @click="onClickSigninButton"
        :showPassword="false"
        buttonClass="btn-outline-primary"
        buttonText="サインイン"
      />
      <button @click="onClickSignupButton" class="btn btn-link">作ったくじ引きを保存したい？ならばアカウント登録です</button>
    </div>
  </div>
</template>
