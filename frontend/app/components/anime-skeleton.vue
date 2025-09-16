<script setup lang="ts">
type Props = {
  count?: number;
};

const _props = withDefaults(defineProps<Props>(), {
  count: 4,
});
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    <UCard
      v-for="n in count"
      :key="n"
      class="animate-pulse"
    >
      <div class="h-64 bg-gray-200 dark:bg-gray-700 rounded-t-lg" />
      <div class="p-4 space-y-3">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4" />
      </div>
    </UCard>
  </div>
</template>
