<template>
  <div class="py-8 sm:py-12 anime-gradient dark:from-violet-900 dark:to-blue-900 flex-1" data-testid="auth-page">
    <ResponsiveContainer size="md" padding="sm">
      <div class="text-center mb-6 sm:mb-8" data-testid="auth-page-header">
        <h1 class="text-3xl sm:text-4xl font-bold text-white mb-2">
          Welcome to OtakuShelf
        </h1>
        <p class="text-base sm:text-lg text-violet-100 dark:text-gray-300 px-4">
          Sign in to manage your personal anime and manga collection
        </p>
      </div>

      <ClientOnly fallback-tag="div" fallback="Loading authentication..." data-testid="auth-client-only">
        <template #fallback>
          <div class="flex justify-center items-center py-8">
            <UCard class="w-full max-w-md">
              <div class="flex items-center justify-center p-8">
                <UIcon name="i-heroicons-arrow-path" class="animate-spin text-2xl text-primary-500" />
                <span class="ml-3 text-gray-600 dark:text-gray-400">Loading authentication...</span>
              </div>
            </UCard>
          </div>
        </template>
        <AuthView />
      </ClientOnly>
    </ResponsiveContainer>
  </div>
</template>
