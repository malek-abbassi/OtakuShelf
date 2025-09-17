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
    >
      <USkeleton class="h-64 rounded-t-lg rounded-b-none" />
      <div class="p-4 space-y-3">
        <USkeleton class="h-4 w-3/4" />
        <USkeleton class="h-4 w-1/2" />
        <USkeleton class="h-4 w-1/4" />
      </div>
    </UCard>
  </div>
</template>
