<script setup lang="ts"></script>

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
      <button class="btn btn-outline-primary">サインイン</button>
      <button class="btn btn-link">作ったくじ引きを保存したいのでユーザ登録する</button>
    </div>
  </div>
</template>
