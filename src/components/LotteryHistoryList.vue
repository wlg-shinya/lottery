<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  histories: string[];
}>();

const emit = defineEmits<{
  cleared: [];
}>();

const historiesReversed = computed(() => props.histories.slice().reverse());

function onClickClearButton() {
  emit("cleared");
}
</script>

<template>
  <div v-if="props.histories.length > 0">
    <table class="table table-sm table-striped table-borderless text-center">
      <tbody>
        <tr v-for="(history, index) in historiesReversed" :key="index">
          <td>{{ props.histories.length - index }}回目</td>
          <td style="min-width: 100px">{{ history }}</td>
        </tr>
        <tr>
          <td colspan="2">
            <button @click="onClickClearButton" class="btn btn-danger w-100"><span class="mdi mdi-trash-can" /></button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
