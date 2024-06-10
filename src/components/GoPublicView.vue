<script setup lang="ts">
import router from "../router";

function onClickGoPublicViewButton() {
  router.push("/public");
}
</script>

<template>
  <div>
    <button @click="onClickGoPublicViewButton" class="btn btn-lg btn-link">みんなの作ったくじ引きを見る</button>
  </div>
</template>
