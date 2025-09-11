<template>
  <NuxtLayout>
    <div class="py-12 anime-gradient dark:from-violet-900 dark:to-blue-900 flex-1">
      <div class="container mx-auto px-4">
        <div class="text-center mb-8">
          <h1 class="text-4xl font-bold text-white mb-2">
            Welcome to OtakuShelf
          </h1>
          <p class="text-lg text-violet-100 dark:text-gray-300">
            Sign in to manage your personal anime and manga collection
          </p>
        </div>

        <ClientOnly fallback-tag="div" fallback="Loading authentication...">
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
      </div>
    </div>
  </NuxtLayout>
</template>
