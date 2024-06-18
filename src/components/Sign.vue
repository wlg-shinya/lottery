<script setup lang="ts">
import { ref, watch } from "vue";
import router from "../router";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import AccountInput from "./AccountInput.vue";
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
    // サインインが確定したらユーザ名とEメールを得る
    if (newValue) {
      const users = await DefaultApiClient.readUserByAccessTokenApiReadUserByAccessTokenGet(newValue)
        .then((response) => response.data)
        .catch((error) => {
          message.value.set(getErrorMessage(error), "text-danger");
        });
      username.value = users?.account_name ?? "";
      email.value = users?.email ?? "";
      message.value.set("", "");
    }
  }
);

const message = ref();
const username = ref("");
const email = ref("");

async function onClickSigninButton(email: string, _userName: string, password: string) {
  await DefaultApiClient.signinApiSigninPost({
    email: email,
    identification: password,
  })
    .then(async (response) => {
      emit("signin", response.data.access_token);
      message.value.set("サインインしました", "text-success");
    })
    .catch((error: Error) => {
      message.value.set(getErrorMessage(error), "text-danger");
    });
}

function onClickSignupButton() {
  router.push("/signup");
}

function onClickGoProfileButton() {
  router.push("/profile");
}

async function onSignout() {
  emit("signout");
  message.value.set("", "");
}
</script>

<template>
  <div class="d-flex flex-column justify-content-center">
    <div v-if="!props.accessToken">
      <AccountInput
        @click="onClickSigninButton"
        :submitLabel="'サインイン'"
        :emailLabel="'登録したEメールアドレス'"
        :passwordLabel="'パスワード'"
        userNameLabel=""
        initEmail=""
      />
      <button @click="onClickSignupButton" class="btn btn-link p-0">作ったくじ引きをサーバーに保存したい？ではアカウントを作りましょう</button>
    </div>
    <div v-else>
      <div v-if="username" class="d-flex flex-column justify-content-center">
        <div class="text-center">
          <span>ようこそ</span>
          <span class="fs-2 p-2">{{ username }}</span>
          <span>さん</span>
        </div>
        <button @click="onClickGoProfileButton" class="btn btn-link p-0">個人設定の編集</button>
      </div>
      <Signout @signout="onSignout" />
      <AccountInput
        @click="onClickSigninButton"
        :submitLabel="'サインインの更新'"
        :passwordLabel="'アクセスの有効期限が切れたらパスワードを入力してください'"
        :initEmail="email"
        emailLabel=""
        userNameLabel=""
      />
    </div>
    <Message ref="message" />
  </div>
</template>
