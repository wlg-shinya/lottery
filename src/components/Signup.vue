<script setup lang="ts">
import { ref } from "vue";
import router from "../router";
import { AlreadyExistsError } from "../error";
import { DefaultApiClient, Users } from "../openapi";

class Message {
  body: string = "";
  color: string = ""; // ex. 'text-primary' ref. https://getbootstrap.jp/docs/5.3/utilities/colors/

  valid(): boolean {
    return this.body !== "" && this.color !== "";
  }

  set(body: string, color: string) {
    this.body = body;
    this.color = color;
  }
}

const username = ref("");
const password = ref("");
const message = ref<Message>(new Message());

async function onClickSignupButton() {
  await DefaultApiClient.readUsersApiReadUsersGet()
    .then(async (response) => {
      const users: Users[] = response.data;
      if (users.some((x) => x.account_name === username.value)) {
        throw new AlreadyExistsError(username.value);
      }
      await DefaultApiClient.createUserApiCreateUserPost({
        account_name: username.value,
        identification: password.value,
      })
        .then(() => {
          message.value.set("ユーザー登録しました。戻ってサインインしてください", "text-success");
        })
        .catch((error) => {
          throw error;
        });
    })
    .catch((error: Error) => {
      message.value.set(error.message, "text-danger");
    });
}

function onClickBackButton() {
  router.push("/");
}

function canSignup(): boolean {
  return username.value !== "" && password.value !== "";
}

function showMessage(): boolean {
  // メッセージデータが有効なら表示
  return message.value.valid();
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">アカウント</span>
        <input v-model="username" type="text" class="form-control" />
      </div>
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">パスワード</span>
        <input v-model="password" type="text" class="form-control" />
      </div>
      <button @click="onClickSignupButton" class="btn btn-primary" :disabled="!canSignup()">新規登録</button>
      <div v-show="showMessage()" class="text-center">
        <span :class="`${message.color} fw-bold`">{{ message.body }}</span>
      </div>
      <button @click="onClickBackButton" class="btn btn-link"><span class="mdi mdi-arrow-left" />戻る</button>
    </div>
  </div>
</template>
