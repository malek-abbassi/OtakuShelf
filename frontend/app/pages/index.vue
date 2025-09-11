<template>
  <NuxtLayout>
    <div class="flex-1">
      <!-- Hero Section -->
      <section class="py-20 anime-gradient dark:from-violet-900 dark:to-blue-900">
        <div class="container mx-auto px-4 text-center">
          <h2 class="text-5xl font-bold text-white mb-6">
            Your Personal Anime & Manga Collection
          </h2>
          <p class="text-xl text-violet-100 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            Organize, track, and discover your favorite anime series and manga volumes with ease.
            Keep your otaku journey organized and never lose track of what you've watched or read.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <UButton to="/anime" size="lg" color="neutral" variant="solid">
              <UIcon name="i-heroicons-magnifying-glass" class="mr-2" />
              Discover Anime
            </UButton>
            <UButton to="/auth" size="lg" variant="outline" color="neutral">
              <UIcon name="i-heroicons-rocket-launch" class="mr-2" />
              Get Started
            </UButton>
            <UButton to="/about" size="lg" variant="outline" color="neutral">
              <UIcon name="i-heroicons-play" class="mr-2" />
              Learn More
            </UButton>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="py-20 bg-white dark:bg-gray-900">
        <div class="container mx-auto px-4">
          <div class="text-center mb-16">
            <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Everything You Need
            </h3>
            <p class="text-lg text-gray-600 dark:text-gray-400">
              Powerful features to manage your otaku collection
            </p>
          </div>

          <div class="grid md:grid-cols-3 gap-8">
            <UCard class="text-center">
              <template #header>
                <div class="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mx-auto">
                  <UIcon name="i-heroicons-rectangle-stack" class="text-primary-600 dark:text-primary-400 text-2xl" />
                </div>
              </template>
              <h4 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                Collection Management
              </h4>
              <p class="text-gray-600 dark:text-gray-400">
                Organize your anime and manga collection with custom tags, ratings, and status tracking.
              </p>
            </UCard>

            <UCard class="text-center">
              <template #header>
                <div class="w-16 h-16 bg-secondary-100 dark:bg-secondary-900/30 rounded-full flex items-center justify-center mx-auto">
                  <UIcon name="i-heroicons-chart-bar" class="text-secondary-600 dark:text-secondary-400 text-2xl" />
                </div>
              </template>
              <h4 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                Progress Tracking
              </h4>
              <p class="text-gray-600 dark:text-gray-400">
                Keep track of episodes watched, chapters read, and get insights into your viewing habits.
              </p>
            </UCard>

            <UCard class="text-center">
              <template #header>
                <div class="w-16 h-16 bg-error-100 dark:bg-error-900/30 rounded-full flex items-center justify-center mx-auto">
                  <UIcon name="i-heroicons-sparkles" class="text-error-600 dark:text-error-400 text-2xl" />
                </div>
              </template>
              <h4 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                Recommendations
              </h4>
              <p class="text-gray-600 dark:text-gray-400">
                Discover new anime and manga based on your preferences and viewing history.
              </p>
            </UCard>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="py-20 bg-primary-600 dark:bg-primary-800">
        <div class="container mx-auto px-4 text-center">
          <h3 class="text-3xl font-bold text-white mb-4">
            Ready to Start Your Journey?
          </h3>
          <p class="text-xl text-primary-100 dark:text-primary-200 mb-8 max-w-2xl mx-auto">
            Join thousands of anime and manga enthusiasts who trust OtakuShelf to manage their collections.
          </p>
          <UButton to="/auth" size="lg" color="neutral" variant="solid">
            <UIcon name="i-heroicons-arrow-right" class="mr-2" />
            Create Your Account
          </UButton>
        </div>
      </section>
    </div>
  </NuxtLayout>
</template>
