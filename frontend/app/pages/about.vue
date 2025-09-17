<template>
  <div class="py-20 flex-1 bg-white dark:bg-gray-900">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold text-center mb-8 text-gray-900 dark:text-white">
        About OtakuShelf
      </h1>
      <div class="max-w-3xl mx-auto">
        <p class="text-lg text-gray-600 dark:text-gray-400 mb-6">
          OtakuShelf is a personal anime and manga collection manager designed to help enthusiasts organize, track, and discover new titles. Whether you're a casual viewer or a hardcore fan, OtakuShelf provides the tools you need to manage your otaku collection effectively.
        </p>

        <div class="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-6 mb-8 border border-primary-200 dark:border-primary-800">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
            What We Offer
          </h2>
          <ul class="space-y-3 text-gray-600 dark:text-gray-400">
            <li class="flex items-start">
              <UIcon name="i-heroicons-check-circle" class="text-success-500 dark:text-success-400 mt-1 mr-3 flex-shrink-0" />
              <span><strong class="text-gray-900 dark:text-white">Collection Management:</strong> Organize your anime and manga with custom tags, ratings, and status tracking</span>
            </li>
            <li class="flex items-start">
              <UIcon name="i-heroicons-check-circle" class="text-success-500 dark:text-success-400 mt-1 mr-3 flex-shrink-0" />
              <span><strong class="text-gray-900 dark:text-white">Progress Tracking:</strong> Keep track of episodes watched and chapters read with detailed insights</span>
            </li>
            <li class="flex items-start">
              <UIcon name="i-heroicons-check-circle" class="text-success-500 dark:text-success-400 mt-1 mr-3 flex-shrink-0" />
              <span><strong class="text-gray-900 dark:text-white">Smart Recommendations:</strong> Discover new titles based on your preferences and viewing history</span>
            </li>
          </ul>
        </div>

        <div class="text-center mb-8">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
            Ready to Get Started?
          </h2>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            Join thousands of anime and manga enthusiasts who trust OtakuShelf to manage their collections.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <UButton to="/auth" size="lg" color="primary">
              <UIcon name="i-heroicons-user-plus" class="mr-2" />
              Create Your Account
            </UButton>
            <UButton to="/" size="lg" variant="outline" color="primary">
              <UIcon name="i-heroicons-arrow-left" class="mr-2" />
              Back to Home
            </UButton>
          </div>
        </div>

        <div class="border-t border-gray-200 dark:border-gray-700 pt-8">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
            Learn More
          </h2>
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            Want to see all the features in action? Visit our <NuxtLink to="/" class="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium">
              homepage
            </NuxtLink> to explore everything OtakuShelf has to offer, or <NuxtLink to="/auth" class="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium">
              sign up
            </NuxtLink> to start building your collection today.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
