<script setup lang="ts">
const props = defineProps<{
  text: string;
  highlight: string;
}>();

function sanitaize(s: string) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function showText(): string {
  if (props.highlight) {
    const textSan = sanitaize(props.text);
    const highlightSan = sanitaize(props.highlight);
    const regexp = new RegExp(highlightSan, "gi");
    return textSan.replace(regexp, (x) => {
      return `<span class="highlight">${x}</span>`;
    });
  } else {
    return props.text;
  }
}
</script>

<template>
  <span v-html="showText()" />
</template>

<style>
.highlight {
  background-color: yellow;
}
</style>
