<script setup lang="ts">
import { useErrorHandler } from '~/composables/use-error-handler';

const { toasts, removeToast } = useErrorHandler();

function getToastIcon(type: string) {
  switch (type) {
    case 'success':
      return 'i-heroicons-check-circle';
    case 'error':
      return 'i-heroicons-exclamation-circle';
    case 'warning':
      return 'i-heroicons-exclamation-triangle';
    case 'info':
      return 'i-heroicons-information-circle';
    default:
      return 'i-heroicons-information-circle';
  }
}

function getToastColor(type: string) {
  switch (type) {
    case 'success':
      return 'success';
    case 'error':
      return 'error';
    case 'warning':
      return 'warning';
    case 'info':
      return 'info';
    default:
      return 'info';
  }
}
</script>

<template>
  <div class="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
    <TransitionGroup
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 transform translate-x-full"
      enter-to-class="opacity-100 transform translate-x-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 transform translate-x-0"
      leave-to-class="opacity-0 transform translate-x-full"
    >
      <UAlert
        v-for="toast in toasts"
        :key="toast.id"
        :color="getToastColor(toast.type)"
        variant="soft"
        class="shadow-lg border"
        :data-testid="`toast-${toast.type}`"
      >
        <template #icon>
          <UIcon :name="getToastIcon(toast.type)" class="w-5 h-5" />
        </template>

        <div class="flex-1">
          <h4 class="font-semibold text-sm">
            {{ toast.title }}
          </h4>
          <p v-if="toast.message" class="text-sm mt-1">
            {{ toast.message }}
          </p>
        </div>

        <template #actions>
          <div class="flex items-center gap-2">
            <UButton
              v-if="toast.action"
              :color="getToastColor(toast.type)"
              variant="ghost"
              size="xs"
              @click="toast.action.handler"
            >
              {{ toast.action.label }}
            </UButton>
            <UButton
              color="neutral"
              variant="ghost"
              size="xs"
              @click="removeToast(toast.id)"
            >
              <UIcon name="i-heroicons-x-mark" class="w-4 h-4" />
            </UButton>
          </div>
        </template>
      </UAlert>
    </TransitionGroup>
  </div>
</template>
