<script setup lang="ts">
import { ref, watch } from "vue";
import router from "../router";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import AccountPasswordInput from "./AccountPasswordInput.vue";
import Message from "./Message.vue";
import Signout from "../components/Signout.vue";

const props = defineProps<{
  accessToken: string;
}>();

const emit = defineEmits<{
  signin: [accessToken: string];
  signout: [];
}>();

watch(
  () => props.accessToken,
  async (newValue: string) => {
    // サインインが確定したらユーザ名を得る
    if (newValue) {
      const users = await DefaultApiClient.readUserByAccessTokenApiReadUserByAccessTokenGet(newValue)
        .then((response) => response.data)
        .catch((error) => {
          message.value.set(getErrorMessage(error), "text-danger");
        });
      username.value = users?.account_name ?? "";
    }
  }
);

const message = ref();
const username = ref("");

async function onClickSigninButton(account: string, password: string) {
  await DefaultApiClient.signinApiSigninPost({
    account_name: account,
    identification: password,
  })
    .then(async (response) => {
      emit("signin", response.data.access_token);
      // これまでのメッセージをクリアしておく
      message.value.set("", "");
    })
    .catch((error: Error) => {
      message.value.set(getErrorMessage(error), "text-danger");
    });
}

function onClickSignupButton() {
  router.push("/signup");
}

async function onSignout() {
  emit("signout");
}
</script>

<template>
  <div class="d-flex flex-column justify-content-center">
    <div v-if="!props.accessToken">
      <AccountPasswordInput @click="onClickSigninButton" buttonClass="btn-outline-primary" buttonText="サインイン" />
      <button @click="onClickSignupButton" class="btn btn-link">作ったくじ引きをサーバーに保存したい？ではアカウントを作りましょう</button>
    </div>
    <div v-else>
      <div v-show="username">
        <span>ようこそ</span>
        <span class="fs-2 p-2">{{ username }}</span>
        <span>さん</span>
      </div>
      <Signout @signout="onSignout" />
    </div>
    <Message ref="message" />
  </div>
</template>
