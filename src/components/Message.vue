<script setup lang="ts">
import { ref } from "vue";

defineExpose({ set });

class Message {
  body: string = "";
  color: string = ""; // ex. 'text-primary' ref. https://getbootstrap.jp/docs/5.3/utilities/colors/

  valid(): boolean {
    return this.body !== "" && this.color !== "";
  }

  set(body: string, color: string) {
    this.body = body;
    this.color = color;
  }
}

const message = ref<Message>(new Message());

function showMessage(): boolean {
  return message.value.valid();
}

function set(body: string, color: string) {
  message.value.set(body, color);
}
</script>

<template>
  <div>
    <div v-show="showMessage()">
      <pre :class="`${message.color} fw-bold fs-6`">{{ message.body }}</pre>
    </div>
  </div>
</template>
