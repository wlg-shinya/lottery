<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
import AccountPasswordInput from "./AccountPasswordInput.vue";

const accountPasswordInput = ref();

function onClickSigninButton(account: string, password: string) {
  console.log({ account, password });
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
