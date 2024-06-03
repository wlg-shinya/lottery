<script setup lang="ts">
import router from "../router";

function onClickSignupButton() {
  router.push("/signup");
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">アカウント</span>
        <input type="text" class="form-control" />
      </div>
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">パスワード</span>
        <input type="password" class="form-control" />
      </div>
      <button class="btn btn-outline-primary">サインイン</button>
      <button @click="onClickSignupButton" class="btn btn-link">作ったくじ引きを保存したい？ならばアカウント登録です</button>
    </div>
  </div>
</template>
