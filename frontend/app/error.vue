<script setup lang="ts">
// https://nuxt.com/docs/getting-started/error-handling
import type { NuxtError } from '#app';

import { useErrorHandler } from '~/composables/use-error-handler';

const props = defineProps<{
  error: NuxtError;
}>();

const { showSuccessToast } = useErrorHandler();

function handleError() {
  showSuccessToast('Redirecting to home page...', 'Navigation');
  clearError({ redirect: '/' });
}

function handleRetry() {
  showSuccessToast('Retrying...', 'Action');
  refreshNuxtData();
}

// Check if we're in development mode
const isDev = computed(() => import.meta.dev);

// Log error for debugging in production
if (import.meta.server) {
  console.error('Server Error:', props.error);
}

// Computed property for template usage
const showErrorDetails = computed(() => isDev.value && props.error.message);

// Error recovery suggestions based on error type
const errorSuggestions = computed(() => {
  const suggestions = [];

  if (props.error.statusCode === 404) {
    suggestions.push({
      text: 'Check the URL for typos',
      action: null,
    });
    suggestions.push({
      text: 'Go back to the previous page',
      action: () => window.history.back(),
    });
  }
  else if (props.error.statusCode === 500) {
    suggestions.push({
      text: 'Try refreshing the page',
      action: () => window.location.reload(),
    });
    suggestions.push({
      text: 'Clear your browser cache',
      action: null,
    });
  }
  else if (props.error.statusCode >= 400 && props.error.statusCode < 500) {
    suggestions.push({
      text: 'Check your internet connection',
      action: null,
    });
    suggestions.push({
      text: 'Try again in a few moments',
      action: handleRetry,
    });
  }

  return suggestions;
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="max-w-md w-full">
      <UCard class="text-center">
        <template #header>
          <div class="flex justify-center mb-4">
            <div class="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center">
              <UIcon name="i-heroicons-exclamation-triangle" class="text-red-600 dark:text-red-400 text-2xl" />
            </div>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ error.statusCode === 404 ? 'Page Not Found' : 'Something went wrong' }}
          </h1>
        </template>

        <div class="space-y-4">
          <p class="text-gray-600 dark:text-gray-400">
            {{ error.statusCode === 404
              ? 'The page you are looking for does not exist.'
              : 'We encountered an unexpected error. Please try again.'
            }}
          </p>

          <!-- Error Recovery Suggestions -->
          <div v-if="errorSuggestions.length > 0" class="text-left">
            <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              What you can try:
            </h3>
            <ul class="space-y-2">
              <li v-for="suggestion in errorSuggestions" :key="suggestion.text" class="flex items-start gap-2">
                <UIcon name="i-heroicons-light-bulb" class="text-yellow-500 mt-0.5 flex-shrink-0 w-4 h-4" />
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  {{ suggestion.text }}
                  <UButton
                    v-if="suggestion.action"
                    variant="link"
                    size="xs"
                    class="p-0 h-auto text-primary-600 hover:text-primary-700"
                    @click="suggestion.action"
                  >
                    Do this
                  </UButton>
                </span>
              </li>
            </ul>
          </div>

          <div v-if="showErrorDetails" class="text-left">
            <details class="mt-4">
              <summary class="cursor-pointer text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
                Error Details (Development Only)
              </summary>
              <pre class="mt-2 text-xs bg-gray-100 dark:bg-gray-800 p-2 rounded overflow-auto">{{ error.message }}</pre>
            </details>
          </div>
        </div>

        <template #footer>
          <div class="flex gap-2 justify-center flex-wrap">
            <UButton color="secondary" variant="outline" @click="handleRetry">
              <UIcon name="i-heroicons-arrow-path" class="mr-2" />
              Retry
            </UButton>
            <UButton color="primary" @click="handleError">
              <UIcon name="i-heroicons-home" class="mr-2" />
              Go Home
            </UButton>
          </div>
        </template>
      </UCard>
    </div>
  </div>
</template>
