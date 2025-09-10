<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <UIcon name="i-heroicons-book-open" class="text-3xl text-primary-600" />
            <h1 class="text-2xl font-bold text-gray-900">
              OtakuShelf
            </h1>
          </div>
          <UButton to="/auth" color="primary" variant="solid">
            <UIcon name="i-heroicons-user-circle" class="mr-2" />
            Sign In
          </UButton>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="py-20 bg-gradient-to-br from-blue-50 to-indigo-100">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-5xl font-bold text-gray-900 mb-6">
          Your Personal Anime & Manga Collection
        </h2>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Organize, track, and discover your favorite anime series and manga volumes with ease.
          Keep your otaku journey organized and never lose track of what you've watched or read.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <UButton to="/auth" size="lg" color="primary">
            <UIcon name="i-heroicons-rocket-launch" class="mr-2" />
            Get Started
          </UButton>
          <UButton size="lg" variant="outline" color="primary">
            <UIcon name="i-heroicons-play" class="mr-2" />
            Learn More
          </UButton>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h3 class="text-3xl font-bold text-gray-900 mb-4">
            Everything You Need
          </h3>
          <p class="text-lg text-gray-600">
            Powerful features to manage your otaku collection
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <UCard class="text-center">
            <template #header>
              <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                <UIcon name="i-heroicons-rectangle-stack" class="text-blue-600 text-2xl" />
              </div>
            </template>
            <h4 class="text-xl font-semibold text-gray-900 mb-3">
              Collection Management
            </h4>
            <p class="text-gray-600">
              Organize your anime and manga collection with custom tags, ratings, and status tracking.
            </p>
          </UCard>

          <UCard class="text-center">
            <template #header>
              <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <UIcon name="i-heroicons-chart-bar" class="text-green-600 text-2xl" />
              </div>
            </template>
            <h4 class="text-xl font-semibold text-gray-900 mb-3">
              Progress Tracking
            </h4>
            <p class="text-gray-600">
              Keep track of episodes watched, chapters read, and get insights into your viewing habits.
            </p>
          </UCard>

          <UCard class="text-center">
            <template #header>
              <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto">
                <UIcon name="i-heroicons-sparkles" class="text-purple-600 text-2xl" />
              </div>
            </template>
            <h4 class="text-xl font-semibold text-gray-900 mb-3">
              Recommendations
            </h4>
            <p class="text-gray-600">
              Discover new anime and manga based on your preferences and viewing history.
            </p>
          </UCard>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-primary-600">
      <div class="container mx-auto px-4 text-center">
        <h3 class="text-3xl font-bold text-white mb-4">
          Ready to Start Your Journey?
        </h3>
        <p class="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
          Join thousands of anime and manga enthusiasts who trust OtakuShelf to manage their collections.
        </p>
        <UButton to="/auth" size="lg" color="neutral" variant="solid">
          <UIcon name="i-heroicons-arrow-right" class="mr-2" />
          Create Your Account
        </UButton>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="grid md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <UIcon name="i-heroicons-book-open" class="text-2xl text-primary-400" />
              <span class="text-lg font-bold">OtakuShelf</span>
            </div>
            <p class="text-gray-400">
              Your personal anime and manga collection manager.
            </p>
          </div>

          <div>
            <h5 class="font-semibold mb-4">
              Product
            </h5>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white transition-colors">Features</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Pricing</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Updates</a></li>
            </ul>
          </div>

          <div>
            <h5 class="font-semibold mb-4">
              Support
            </h5>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white transition-colors">Help Center</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Contact</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Community</a></li>
            </ul>
          </div>

          <div>
            <h5 class="font-semibold mb-4">
              Connect
            </h5>
            <div class="flex space-x-4">
              <UButton icon="i-heroicons-link" variant="ghost" color="neutral" size="sm" />
              <UButton icon="i-heroicons-chat-bubble-left-ellipsis" variant="ghost" color="neutral" size="sm" />
              <UButton icon="i-heroicons-heart" variant="ghost" color="neutral" size="sm" />
            </div>
          </div>
        </div>

        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 OtakuShelf. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>
