<script setup lang="ts">
import router from "../router";

function onClickButton() {
  router.push("/");
}
</script>

<template>
  <button @click="onClickButton" class="btn">
    <span class="mdi mdi-home text-primary mdi-36px" />
  </button>
</template>
