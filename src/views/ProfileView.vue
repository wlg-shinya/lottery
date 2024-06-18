<script setup lang="ts">
import { ref, watchEffect } from "vue";
import { LotteryTopData } from "../lottery-data";
import { DefaultApiClient, VarcharMax } from "../openapi";
import { getErrorMessage } from "../error";
import { PASSWORD_MAX_LENGTH } from "../constant";
import LocalStorageLottery from "../local-storage-lottery";
import HomeButton from "../components/HomeButton.vue";
import Message from "../components/Message.vue";

const messageTop = ref();
const messageChangeUserName = ref();
const messageChangePassword = ref();
const lotteryTopData = ref<LotteryTopData | null>(null);
const userName = ref("");
const oldPassword = ref("");
const newPassword = ref("");
const showOldPassword = ref(false);
const showNewPassword = ref(false);

watchEffect(async () => {
  // サインインチェック
  if (lotteryTopData.value) {
    if (lotteryTopData.value.accessToken === "") {
      messageTop.value.set("サインインしてください", "text-danger");
      return;
    }
  } else {
    return;
  }

  // メッセージ更新
  if (oldPassword.value && !newPassword.value) {
    messageChangePassword.value.set("新しいパスワードも入力する必要があります", "text-danger");
  } else if (!oldPassword.value && newPassword.value) {
    messageChangePassword.value.set("現在のパスワードも入力する必要があります", "text-danger");
  } else if (oldPassword.value && newPassword.value) {
    if (oldPassword.value === newPassword.value) {
      messageChangePassword.value.set("新しいパスワードは現在のパスワードと異なる必要があります", "text-danger");
    } else {
      messageChangePassword.value.set("", "");
    }
  }

  // テキスト入力の上限切りつめ
  if (userName.value.length > VarcharMax.users_account_name) {
    userName.value = userName.value.slice(0, VarcharMax.users_account_name);
  }
  if (oldPassword.value.length > PASSWORD_MAX_LENGTH) {
    oldPassword.value = oldPassword.value.slice(0, PASSWORD_MAX_LENGTH);
  }
  if (newPassword.value.length > PASSWORD_MAX_LENGTH) {
    newPassword.value = newPassword.value.slice(0, PASSWORD_MAX_LENGTH);
  }
});

async function onClickChangeUserNameButton() {
  // サインインしていなかったら何もしない
  const topData = lotteryTopData.value;
  if (!topData || !topData.accessToken) return;

  // 新しいユーザー名をサーバーに反映する
  await DefaultApiClient.updateUserAccountNameApiUpdateUserAccountNamePut(topData.accessToken, userName.value)
    .then(() => {
      messageChangeUserName.value.set("ユーザー名を更新しました", "text-success");
    })
    .catch((error) => {
      messageChangeUserName.value.set(getErrorMessage(error), "text-danger");
    });
}

async function onClickChangePasswordButton() {
  // サインインしていなかったら何もしない
  const topData = lotteryTopData.value;
  if (!topData || !topData.accessToken) return;

  // パスワード変更をして成功したら新しいアクセストークンをローカル保存する
  await DefaultApiClient.changePasswordApiChangePasswordPost({
    access_token: topData.accessToken,
    old_password: oldPassword.value,
    new_password: newPassword.value,
  })
    .then(async (response) => {
      topData.accessToken = response.data.access_token;
      await LocalStorageLottery.save(topData)
        .then(() => {
          messageChangePassword.value.set("パスワードを更新しました", "text-success");
        })
        .catch((error) => {
          throw error;
        });
    })
    .catch((error) => {
      messageChangePassword.value.set(getErrorMessage(error), "text-danger");
    });
}

function disabledChangeUserNameButton(): boolean {
  return !userName.value;
}

function disabledChangePasswordButton(): boolean {
  return !oldPassword.value || !newPassword.value || oldPassword.value === newPassword.value;
}

async function created() {
  // ローカスストレージのデータを得る
  await LocalStorageLottery.load()
    .then(async (result) => {
      lotteryTopData.value = result;

      // アクセストークンが得られていればユーザーデータも得る
      if (lotteryTopData.value.accessToken) {
        await DefaultApiClient.readUserByAccessTokenApiReadUserByAccessTokenGet(lotteryTopData.value.accessToken)
          .then((response) => {
            // ユーザー名
            userName.value = response.data.account_name;
          })
          .catch((error) => {
            throw error;
          });
      }
    })
    .catch((error) => {
      messageTop.value.set(getErrorMessage(error), "text-danger");
    });
}
created();
</script>

<template>
  <div class="d-flex flex-column justify-content-center">
    <HomeButton />
    <Message ref="messageTop" />
    <div v-if="lotteryTopData?.accessToken !== ''">
      <div class="d-flex justify-content-center">
        <div>
          <label for="userName" class="form-label">ユーザー名</label>
          <input v-model="userName" id="userName" class="form-control" />
          <button @click="onClickChangeUserNameButton" class="btn btn-primary mt-2 w-100" :disabled="disabledChangeUserNameButton()">
            ユーザー名変更
          </button>
          <Message ref="messageChangeUserName" />
        </div>
      </div>
      <div class="d-flex flex-column mt-4">
        <div class="d-flex justify-content-center">
          <div>
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
            <button @click="onClickChangePasswordButton" class="btn btn-primary mt-2 w-100" :disabled="disabledChangePasswordButton()">
              パスワード変更
            </button>
          </div>
        </div>
        <Message ref="messageChangePassword" />
      </div>
    </div>
  </div>
</template>
