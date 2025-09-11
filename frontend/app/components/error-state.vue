<script setup lang="ts">
/**
 * Reusable error state component with retry functionality
 */

type Props = {
  title?: string;
  message?: string;
  showRetry?: boolean;
  retryText?: string;
  icon?: string;
};

type Emits = {
  retry: [];
};

withDefaults(defineProps<Props>(), {
  title: 'Something went wrong',
  message: 'An unexpected error occurred. Please try again.',
  showRetry: true,
  retryText: 'Try Again',
  icon: 'i-heroicons-exclamation-triangle',
});

defineEmits<Emits>();
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <UIcon
      :name="icon"
      class="w-12 h-12 text-red-500 mb-4"
    />

    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
      {{ title }}
    </h3>

    <p class="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
      {{ message }}
    </p>

    <div v-if="showRetry || $slots.actions" class="flex gap-3">
      <slot name="actions">
        <UButton
          v-if="showRetry"
          color="primary"
          @click="$emit('retry')"
        >
          {{ retryText }}
        </UButton>
      </slot>
    </div>
  </div>
</template>
