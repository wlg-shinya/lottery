<script setup lang="ts">
import { ref, watchEffect } from "vue";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import { PASSWORD_MAX_LENGTH } from "../constant";
import LocalStorageLottery from "../local-storage-lottery";
import HomeButton from "../components/HomeButton.vue";
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

  // テキスト入力の上限切りつめ
  if (oldPassword.value.length > PASSWORD_MAX_LENGTH) {
    oldPassword.value = oldPassword.value.slice(0, PASSWORD_MAX_LENGTH);
  }
  if (newPassword.value.length > PASSWORD_MAX_LENGTH) {
    newPassword.value = newPassword.value.slice(0, PASSWORD_MAX_LENGTH);
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
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <HomeButton />
      <div>
        <label for="oldPassword" class="form-label">現在のパスワード</label>
        <div class="input-group">
          <input v-model="oldPassword" id="oldPassword" :type="showOldPassword ? 'text' : 'password'" class="form-control" />
          <button @click="showOldPassword = !showOldPassword" :class="`btn ${showOldPassword ? 'btn-secondary' : 'btn-outline-secondary'}`">
            <span class="mdi mdi-eye" />
          </button>
        </div>
      </div>
      <div>
        <label for="newPassword" class="form-label">新しいパスワード</label>
        <div class="input-group">
          <input v-model="newPassword" id="newPassword" :type="showNewPassword ? 'text' : 'password'" class="form-control" />
          <button @click="showNewPassword = !showNewPassword" :class="`btn ${showNewPassword ? 'btn-secondary' : 'btn-outline-secondary'}`">
            <span class="mdi mdi-eye" />
          </button>
        </div>
      </div>
      <button @click="onClickSubmitButton" class="btn btn-primary mt-3" :disabled="disabledSubmitButton()">変更</button>
      <Message ref="message" />
    </div>
  </div>
</template>
