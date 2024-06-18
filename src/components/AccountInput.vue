<script setup lang="ts">
import { ref, watch, watchEffect } from "vue";
import { VarcharMax } from "../openapi";
import { PASSWORD_MAX_LENGTH } from "../constant";

const props = defineProps<{
  submitLabel: string;
  emailLabel: string;
  userNameLabel: string;
  passwordLabel: string;
  initEmail: string;
}>();

const emit = defineEmits<{
  click: [email: string, userName: string, password: string];
}>();

const email = ref("");
const userName = ref("");
const password = ref("");
const showPassword = ref(false);
const invalidEmail = ref<boolean>(!props.emailLabel);
const invalidUserName = ref<boolean>(!props.userNameLabel);
const buttonMargin = ref(invalidEmail.value && invalidUserName.value ? "" : "mt-3");

watch(
  () => props.initEmail,
  async (newValue: string) => {
    email.value = newValue;
  }
);

watchEffect(() => {
  // テキスト入力の上限切りつめ
  if (email.value.length > VarcharMax.users_email) {
    email.value = email.value.slice(0, VarcharMax.users_email);
  }
  if (userName.value.length > VarcharMax.users_account_name) {
    userName.value = userName.value.slice(0, VarcharMax.users_account_name);
  }
  if (password.value.length > PASSWORD_MAX_LENGTH) {
    password.value = password.value.slice(0, PASSWORD_MAX_LENGTH);
  }
});

function onClickSubmitButton() {
  emit("click", email.value, userName.value, password.value);
}

function onClickShowPasswordButton() {
  showPassword.value = !showPassword.value;
}

function canClick(): boolean {
  const emailFlag = invalidEmail.value || email.value !== "";
  const userNameFlag = invalidUserName.value || userName.value !== "";
  const passwordFlag = password.value !== "";
  return emailFlag && userNameFlag && passwordFlag;
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div>
      <div v-if="!invalidEmail">
        <label for="email" class="form-label">{{ emailLabel }}</label>
        <input v-model="email" id="email" type="text" class="form-control" />
      </div>
      <div v-if="!invalidUserName">
        <label for="userName" class="form-label">{{ userNameLabel }}</label>
        <input v-model="userName" id="userName" type="text" class="form-control" />
      </div>
      <div>
        <label for="password" class="form-label">{{ passwordLabel }}</label>
        <div class="input-group">
          <input v-model="password" :type="showPassword ? 'text' : 'password'" class="form-control" />
          <button @click="onClickShowPasswordButton" :class="`btn ${showPassword ? 'btn-secondary' : 'btn-outline-secondary'}`">
            <span class="mdi mdi-eye" />
          </button>
        </div>
      </div>
      <button @click="onClickSubmitButton" :class="`btn btn-primary w-100 ${buttonMargin}`" :disabled="!canClick()">{{ submitLabel }}</button>
    </div>
  </div>
</template>
