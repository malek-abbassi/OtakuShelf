<script lang="ts" setup>
type UserProfileProps = {
  userInfo: any;
};

type UserProfileEmits = {
  signOut: [];
};

defineProps<UserProfileProps>();
const emit = defineEmits<UserProfileEmits>();

function handleSignOut() {
  emit('signOut');
}
</script>

<template>
  <UCard class="w-full max-w-md">
    <template #header>
      <div class="text-center">
        <div class="w-16 h-16 bg-success-100 dark:bg-success-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <UIcon name="i-heroicons-check-circle" class="text-success-600 dark:text-success-400 text-2xl" />
        </div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          Welcome!
        </h2>
        <p class="text-gray-500 dark:text-gray-400 mt-1">
          You're successfully signed in
        </p>
      </div>
    </template>

    <div class="space-y-4">
      <UCard class="bg-gray-50 dark:bg-gray-800/50">
        <div class="flex items-center space-x-3">
          <UIcon name="i-heroicons-user-circle" class="text-gray-400" />
          <div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">
              User ID
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ userInfo }}
            </p>
          </div>
        </div>
      </UCard>

      <UButton
        block
        variant="outline"
        color="error"
        size="lg"
        @click="handleSignOut"
      >
        <UIcon name="i-heroicons-arrow-right-on-rectangle" class="mr-2" />
        Sign Out
      </UButton>
    </div>
  </UCard>
</template>
