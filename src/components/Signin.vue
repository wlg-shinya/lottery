<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
import { InvalidAccountOrPasswordError } from "../error";
import { DefaultApiClient } from "../openapi";
import AccountPasswordInput from "./AccountPasswordInput.vue";

const emit = defineEmits<{
  signin: [accessToken: string];
}>();

const accountPasswordInput = ref();

async function onClickSigninButton(account: string, password: string) {
  // TODO:サインインをサーバサイドで行うようにする
  // MEMO:
  // アカウントとパスワードを送信してアクセストークンを返すようなAPI
  // - アクセストークンは期限付きでサーバサイドに保存
  // - POST/PUT/DELETE についてはアクセストークンを合わせて送信。サーバサイドでアクセストークンを処理して適切にリソース変更
  // - フロント側ではアクセストークンをlocalStorageに保存してもOK
  await DefaultApiClient.readUsersApiReadUsersGet()
    .then(async (response) => {
      const users = response.data;
      const user = users.find((x) => x.account_name === account);
      if (!user || user.identification !== password) {
        throw new InvalidAccountOrPasswordError();
      } else {
        emit("signin", user.id.toString());
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
      <button @click="onClickSignupButton" class="btn btn-link">作ったくじ引きをサーバーに保存したい？ならばアカウント登録です</button>
    </div>
  </div>
</template>
