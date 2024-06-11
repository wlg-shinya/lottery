<script setup lang="ts">
import { ref } from "vue";
import { DefaultApiClient } from "../openapi";
import BackButton from "../components/BackButton.vue";

const oldPassword = ref("");
const newPassword = ref("");
const showOldPassword = ref(false);
const showNewPassword = ref(false);

function disabledSubmitButton(): boolean {
  return !oldPassword.value || !newPassword.value || oldPassword.value !== newPassword.value;
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
        <button class="btn btn-primary" :disabled="disabledSubmitButton()">変更</button>
      </div>
    </div>
  </div>
</template>
