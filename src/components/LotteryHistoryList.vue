<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  histories: string[];
}>();

const historiesReversed = computed(() => props.histories.slice().reverse());
</script>

<template>
  <div>
    <table class="table table-sm table-striped table-borderless text-center">
      <tbody>
        <tr v-for="(history, index) in historiesReversed" :key="index">
          <td>{{ props.histories.length - index }}回目</td>
          <td style="min-width: 100px">{{ history }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
