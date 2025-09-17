<script setup lang="ts">
import { useErrorHandler } from '~/composables/use-error-handler';

const { isOnline, hasNetworkErrors, clearNetworkErrors } = useErrorHandler();
</script>

<template>
  <div v-if="!isOnline || hasNetworkErrors" class="fixed bottom-4 left-4 z-50">
    <UAlert
      color="warning"
      variant="soft"
      class="shadow-lg border max-w-sm"
      data-testid="network-status-alert"
    >
      <template #icon>
        <UIcon
          :name="isOnline ? 'i-heroicons-exclamation-triangle' : 'i-heroicons-wifi-slash'"
          class="w-5 h-5"
        />
      </template>

      <div class="flex-1">
        <h4 class="font-semibold text-sm">
          {{ isOnline ? 'Connection Issues' : 'You are offline' }}
        </h4>
        <p class="text-sm mt-1">
          {{ isOnline
            ? 'Some features may not work properly. Please check your connection.'
            : 'Please check your internet connection to continue using all features.'
          }}
        </p>
      </div>

      <template v-if="hasNetworkErrors" #actions>
        <UButton
          color="warning"
          variant="ghost"
          size="xs"
          @click="clearNetworkErrors"
        >
          Dismiss
        </UButton>
      </template>
    </UAlert>
  </div>
</template>
