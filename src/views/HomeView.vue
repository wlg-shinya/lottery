<script setup lang="ts">
import Lottery from "../components/Lottery.vue";

const title = `${import.meta.env.VITE_APP_TITLE}`;
// const ADMIN_EMAIL = import.meta.env.VITE_ADMIN_EMAIL;
</script>

<template>
  <div class="card">
    <div class="card-header text-center">
      <h1>{{ title }}</h1>
    </div>
    <div class="card-body">
      <Suspense>
        <Lottery />
      </Suspense>
    </div>
    <div class="card-footer">
      <!-- <ul>
        <li>〇〇な機能に対応してほしい！</li>
      </ul>
      <span>ご要望は Chatwork 上で {{ ADMIN_EMAIL }} にコンタクトください</span> -->
    </div>
  </div>
</template>
