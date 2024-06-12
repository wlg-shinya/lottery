<script setup lang="ts">
const props = defineProps<{
  text: string;
  highlight: string;
}>();

// ref. https://qiita.com/mas0061/items/c2e9cd0d27e09448d28e
const sanitaize = {
  encode: function (str: string) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  },

  decode: function (str: string) {
    return str
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&amp;/g, "&");
  },
};

function showText(): string {
  if (props.highlight) {
    const safeText = sanitaize.encode(props.text);
    const safeHighlight = sanitaize.encode(props.highlight);
    const regexp = new RegExp(safeHighlight, "gi");
    return safeText.replace(regexp, (x) => {
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
