<script setup lang="ts">
import router from "../router";

function onClickButton() {
  router.go(-1);
}
</script>

<template>
  <button @click="onClickButton" class="btn">
    <span class="mdi mdi-arrow-left text-primary mdi-24px" />
  </button>
</template>
