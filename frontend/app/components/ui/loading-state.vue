<script setup lang="ts">
type Props = {
  variant?: 'spinner' | 'skeleton' | 'pulse';
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  fullScreen?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  variant: 'spinner',
  size: 'md',
  text: 'Loading...',
  fullScreen: false,
});

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };
  return sizes[props.size];
});

const textSizeClasses = computed(() => {
  const sizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  };
  return sizes[props.size];
});
</script>

<template>
  <div
    class="flex items-center justify-center"
    :class="fullScreen ? 'fixed inset-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm' : ''"
  >
    <div class="flex flex-col items-center space-y-3">
      <!-- Spinner variant -->
      <div
        v-if="variant === 'spinner'"
        class="animate-spin rounded-full border-2 border-primary-200 border-t-primary-600 dark:border-primary-800 dark:border-t-primary-400"
        :class="sizeClasses"
      />

      <!-- Pulse variant -->
      <div
        v-else-if="variant === 'pulse'"
        class="animate-pulse bg-primary-200 dark:bg-primary-800 rounded-full"
        :class="sizeClasses"
      />

      <!-- Skeleton variant -->
      <div
        v-else-if="variant === 'skeleton'"
        class="space-y-3"
      >
        <div class="animate-pulse flex space-x-4">
          <div class="rounded-full bg-gray-200 dark:bg-gray-700 h-10 w-10" />
          <div class="flex-1 space-y-2 py-1">
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
            <div class="space-y-2">
              <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded" />
              <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6" />
            </div>
          </div>
        </div>
      </div>

      <!-- Loading text -->
      <p
        v-if="text && variant !== 'skeleton'"
        class="text-gray-600 dark:text-gray-400 font-medium"
        :class="textSizeClasses"
      >
        {{ text }}
      </p>
    </div>
  </div>
</template>
