<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import AccountPasswordInput from "./AccountPasswordInput.vue";

const emit = defineEmits<{
  signin: [accessToken: string];
}>();

defineExpose({ clear });

const accountPasswordInput = ref();

async function onClickSigninButton(account: string, password: string) {
  await DefaultApiClient.signinApiSigninPost({
    account_name: account,
    identification: password,
  })
    .then(async (response) => {
      emit("signin", response.data.access_token);
    })
    .catch((error: Error) => {
      accountPasswordInput.value.setMessage(getErrorMessage(error), "text-danger");
    });
}

function onClickSignupButton() {
  router.push("/signup");
}

function clear() {
  accountPasswordInput.value.clear();
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <AccountPasswordInput ref="accountPasswordInput" @click="onClickSigninButton" buttonClass="btn-outline-primary" buttonText="サインイン" />
      <button @click="onClickSignupButton" class="btn btn-link">作ったくじ引きをサーバーに保存したい？ではアカウントを作りましょう</button>
    </div>
  </div>
</template>
