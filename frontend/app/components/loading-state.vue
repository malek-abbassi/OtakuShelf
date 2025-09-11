<script setup lang="ts">
/**
 * Reusable loading state component with customizable messaging
 */

type Props = {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
  centered?: boolean;
};

withDefaults(defineProps<Props>(), {
  message: 'Loading...',
  size: 'md',
  centered: true,
});

const sizeClasses = {
  sm: 'w-6 h-6',
  md: 'w-8 h-8',
  lg: 'w-12 h-12',
};
</script>

<template>
  <div
    class="flex items-center gap-3"
    :class="centered ? 'justify-center py-8' : ''"
  >
    <UIcon
      name="i-heroicons-arrow-path"
      class="animate-spin text-blue-600"
      :class="sizeClasses[size]"
    />
    <p class="text-gray-600 dark:text-gray-400">
      {{ message }}
    </p>
  </div>
</template>
