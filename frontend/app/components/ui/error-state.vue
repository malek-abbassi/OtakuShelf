<script setup lang="ts">
type Props = {
  title?: string;
  message?: string;
  icon?: string;
  actionText?: string;
  showRetry?: boolean;
  variant?: 'error' | 'warning' | 'info';
};

const props = withDefaults(defineProps<Props>(), {
  title: 'Something went wrong',
  message: 'An unexpected error occurred. Please try again.',
  icon: 'i-heroicons-exclamation-triangle',
  actionText: 'Try Again',
  showRetry: true,
  variant: 'error',
});

const emit = defineEmits<{
  retry: [];
  action: [];
}>();

const variantClasses = computed(() => {
  const variants = {
    error: {
      icon: 'text-error-500 dark:text-error-400',
      title: 'text-error-900 dark:text-error-100',
      message: 'text-error-700 dark:text-error-300',
      background: 'bg-error-50 dark:bg-error-950/50 border-error-200 dark:border-error-800',
    },
    warning: {
      icon: 'text-warning-500 dark:text-warning-400',
      title: 'text-warning-900 dark:text-warning-100',
      message: 'text-warning-700 dark:text-warning-300',
      background: 'bg-warning-50 dark:bg-warning-950/50 border-warning-200 dark:border-warning-800',
    },
    info: {
      icon: 'text-info-500 dark:text-info-400',
      title: 'text-info-900 dark:text-info-100',
      message: 'text-info-700 dark:text-info-300',
      background: 'bg-info-50 dark:bg-info-950/50 border-info-200 dark:border-info-800',
    },
  };
  return variants[props.variant];
});

function handleRetry() {
  emit('retry');
}
</script>

<template>
  <div
    class="rounded-lg border p-6 text-center"
    :class="variantClasses.background"
  >
    <!-- Error Icon -->
    <div class="mx-auto mb-4">
      <UIcon
        :name="icon"
        class="text-4xl"
        :class="variantClasses.icon"
      />
    </div>

    <!-- Title -->
    <h3
      class="text-lg font-semibold mb-2"
      :class="variantClasses.title"
    >
      {{ title }}
    </h3>

    <!-- Message -->
    <p
      class="text-sm mb-6 max-w-md mx-auto"
      :class="variantClasses.message"
    >
      {{ message }}
    </p>

    <!-- Actions -->
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <UButton
        v-if="showRetry"
        :color="variant"
        variant="solid"
        @click="handleRetry"
      >
        <UIcon name="i-heroicons-arrow-path" class="mr-2" />
        {{ actionText }}
      </UButton>

      <!-- Additional action slot -->
      <slot name="actions" />
    </div>

    <!-- Additional content slot -->
    <slot />
  </div>
</template>
