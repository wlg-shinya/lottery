<script setup lang="ts">
import { ref } from "vue";
import XLogoSvg from "./XLogoSvg.vue";

const iconSize = ref(24);
const xUrl = ref(import.meta.env.VITE_X_URL);

function onClickLogoButton(url: string) {
  window.open(url, "_blank");
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <span>お問い合わせはこちら</span>
    <button @click="onClickLogoButton(xUrl)" class="btn btn-dark"><XLogoSvg :style="`width: ${iconSize}px; height: ${iconSize}px`" /></button>
  </div>
</template>
