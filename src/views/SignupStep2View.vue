<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { DefaultApiClient } from "../openapi";
import { getErrorMessage } from "../error";
import BackButton from "../components/BackButton.vue";
import Message from "../components/Message.vue";

const message = ref();

async function onStart() {
  try {
    const signupToken = useRoute().query["signup_token"]?.toString();
    if (!signupToken) {
      throw new Error("サインアップに失敗しました。再度サインアップを試してください");
    }
    await DefaultApiClient.signupStep2ApiSignupStep2Post({
      signup_token: signupToken,
    })
      .then(() => {})
      .catch((error) => {
        throw error;
      });
    message.value.set("サインアップしました。ホームに戻ってサインインしてください", "text-success");
  } catch (error) {
    message.value.set(getErrorMessage(error), "text-danger");
  }
}

onStart();
</script>

<template>
  <div>
    <BackButton />
    <div class="d-flex flex-column justify-content-center">
      <Message ref="message" />
    </div>
  </div>
</template>
