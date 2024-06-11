<script setup lang="ts">
import { ref, watchEffect } from "vue";
import { DefaultApiClient } from "../openapi";
import LocalStorageLottery from "../local-storage-lottery";
import { getErrorMessage } from "../error";
import BackButton from "../components/BackButton.vue";
import Message from "../components/Message.vue";

const message = ref();
const oldPassword = ref("");
const newPassword = ref("");
const showOldPassword = ref(false);
const showNewPassword = ref(false);

watchEffect(async () => {
  if (oldPassword.value && !newPassword.value) {
    message.value.set("新しいパスワードも入力する必要があります", "text-danger");
  } else if (!oldPassword.value && newPassword.value) {
    message.value.set("現在のパスワードも入力する必要があります", "text-danger");
  } else if (oldPassword.value && newPassword.value) {
    if (oldPassword.value === newPassword.value) {
      message.value.set("新しいパスワードは現在のパスワードと異なる必要があります", "text-danger");
    } else {
      message.value.set("", "");
    }
  }
});

async function onClickSubmitButton() {
  try {
    // ローカルストレージからデータを得る
    const lotteryTopData = await LocalStorageLottery.load()
      .then(async (result) => result)
      .catch((error) => {
        throw error;
      });
    if (!lotteryTopData.accessToken) return;

    // パスワード変更をして成功したら新しいアクセストークンをローカル保存する
    await DefaultApiClient.changePasswordApiChangePasswordPut({
      access_token: lotteryTopData.accessToken,
      old_password: oldPassword.value,
      new_password: newPassword.value,
    })
      .then(async (response) => {
        lotteryTopData.accessToken = response.data.access_token;
        await LocalStorageLottery.save(lotteryTopData)
          .then(() => {
            message.value.set("パスワードを更新しました", "text-success");
          })
          .catch((error) => {
            throw error;
          });
      })
      .catch((error) => {
        throw error;
      });
  } catch (error) {
    message.value.set(getErrorMessage(error), "text-danger");
  }
}

function disabledSubmitButton(): boolean {
  return !oldPassword.value || !newPassword.value || oldPassword.value === newPassword.value;
}
</script>

<template>
  <div>
    <BackButton />
    <div class="d-flex justify-content-center">
      <div class="d-flex flex-column">
        <div class="input-group">
          <span class="input-group-text" style="width: 150px">現在のパスワード</span>
          <input v-model="oldPassword" :type="showOldPassword ? 'text' : 'password'" class="form-control" />
          <button @click="showOldPassword = !showOldPassword" :class="`btn ${showOldPassword ? 'btn-secondary' : 'btn-outline-secondary'}`">
            <span class="mdi mdi-eye" />
          </button>
        </div>
        <div class="input-group">
          <span class="input-group-text" style="width: 150px">新しいパスワード</span>
          <input v-model="newPassword" :type="showNewPassword ? 'text' : 'password'" class="form-control" />
          <button @click="showNewPassword = !showNewPassword" :class="`btn ${showNewPassword ? 'btn-secondary' : 'btn-outline-secondary'}`">
            <span class="mdi mdi-eye" />
          </button>
        </div>
        <button @click="onClickSubmitButton" class="btn btn-primary" :disabled="disabledSubmitButton()">変更</button>
        <Message ref="message" />
      </div>
    </div>
  </div>
</template>
