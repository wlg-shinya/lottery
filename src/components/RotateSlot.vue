<script setup lang="ts">
const props = defineProps<{
  slots: string[];
  slotClass: string;
}>();
</script>

<template>
  <div>
    <span :class="slotClass">{{ slots[0] }}</span>
  </div>
</template>
