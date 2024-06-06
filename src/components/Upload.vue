<script setup lang="ts">
const props = defineProps<{
  accessToken: string;
}>();

const emit = defineEmits<{
  click: [accessToken: string];
}>();

function onClickButton() {
  emit("click", props.accessToken);
}

function show(): boolean {
  // アクセストークンが取得できていれば表示ON
  return props.accessToken !== "";
}
</script>

<template>
  <div v-show="show()" class="d-flex flex-column align-items-center">
    <button @click="onClickButton()" class="btn btn-success"><span class="mdi mdi-upload" />サーバーに保存</button>
  </div>
</template>
