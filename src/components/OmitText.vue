<script setup lang="ts">
import { ref, computed } from "vue";

const props = defineProps<{
  text: string;
  length: number;
  allowLineFeed: boolean;
  initOmit: boolean;
}>();

const needOmit = computed(() => props.text.length > props.length);

const omit = ref(needOmit.value ? props.initOmit : false);

function onClickSwitchButton() {
  omit.value = !omit.value;
}

function omitText() {
  // 処理対象文字列を得る
  // 改行を許可する場合は渡された文字列全部が、許可しない場合は1行目が処理対象になる
  let text = props.allowLineFeed ? props.text : props.text.split("\n")[0];

  // 指定文字数で切る
  return text.slice(0, props.length);
}

function fullText() {
  return props.text;
}

function showText(): string {
  return omit.value ? omitText() : fullText();
}
</script>

<template>
  <div>
    <span>{{ showText() }}</span>
    <span v-if="needOmit">
      <button @click="onClickSwitchButton" class="btn btn-link p-0">{{ omit ? "...もっと見る" : "一部を表示" }}</button>
    </span>
  </div>
</template>
