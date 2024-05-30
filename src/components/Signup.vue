<script setup lang="ts">
import router from "../router";

function onClickBackButton() {
  router.push("/");
}
</script>

<template>
  <div class="d-flex justify-content-center">
    <div class="d-flex flex-column">
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">ユーザ名</span>
        <input type="text" class="form-control" />
      </div>
      <div class="input-group">
        <span class="input-group-text" style="width: 100px">パスワード</span>
        <input type="password" class="form-control" />
      </div>
      <button class="btn btn-primary">登録</button>
      <button @click="onClickBackButton" class="btn btn-link"><span class="mdi mdi-arrow-left" />戻る</button>
    </div>
  </div>
</template>
