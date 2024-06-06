<script setup lang="ts">
const props = defineProps<{
  slots: string[];
  slotClass: string;
}>();
</script>

<template>
  <div>
    <div :class="slotClass">{{ slots[0] }}</div>
  </div>
</template>
