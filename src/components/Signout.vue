<script setup lang="ts">
const emit = defineEmits<{
  signout: [];
}>();

function onSignout() {
  emit("signout");
}
</script>

<template>
  <div class="d-flex flex-column align-items-center">
    <button @click="onSignout" class="btn btn-link p-0">サインアウト</button>
  </div>
</template>
