<script setup lang="ts">
import ContactUs from "./components/ContactUs.vue";
const TITLE = import.meta.env.VITE_APP_TITLE;
</script>

<template>
  <div class="card">
    <div class="card-header text-center">
      <h1>{{ TITLE }}</h1>
    </div>
    <div class="card-body">
      <router-view />
    </div>
    <div class="card-footer">
      <ContactUs />
    </div>
  </div>
</template>
