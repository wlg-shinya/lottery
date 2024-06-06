<script setup lang="ts">
// スロット回転表現
// あくまでも表現でありこのコンポネントから回転中の値を取得することは想定していない（≒目押し禁止）
import { ref } from "vue";

const props = defineProps<{
  slots: string[];
  slotClass: string;
}>();

const slotIndex = ref(0);

function incrementSlotIndex() {
  if (slotIndex.value < props.slots.length - 1) slotIndex.value++;
  else slotIndex.value = 0;
}

function update() {
  incrementSlotIndex();
  setTimeout(() => update(), 64);
}

update();
</script>

<template>
  <div>
    <div :class="slotClass">{{ slots[slotIndex] }}</div>
  </div>
</template>
