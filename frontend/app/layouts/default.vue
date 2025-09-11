<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Navigation Header -->
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-8">
            <div class="flex items-center space-x-2">
              <UIcon name="i-heroicons-book-open" class="text-3xl text-primary-600" />
              <NuxtLink to="/" class="text-2xl font-bold text-gray-900 hover:text-primary-600 transition-colors">
                OtakuShelf
              </NuxtLink>
            </div>
            <nav class="hidden md:flex items-center space-x-6">
              <NuxtLink
                to="/anime"
                class="text-gray-700 hover:text-primary-600 transition-colors font-medium"
              >
                Discover Anime
              </NuxtLink>
              <NuxtLink
                to="/about"
                class="text-gray-700 hover:text-primary-600 transition-colors font-medium"
              >
                About
              </NuxtLink>
            </nav>
          </div>
          <UButton to="/auth" color="primary" variant="solid">
            <UIcon name="i-heroicons-user-circle" class="mr-2" />
            Sign In
          </UButton>
        </div>
      </div>
    </header>

    <!-- Page Content -->
    <main class="flex flex-1">
      <slot />
    </main>

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
              <li>
                <NuxtLink to="/about" class="hover:text-white transition-colors">
                  About
                </NuxtLink>
              </li>
              <li><a href="#" class="hover:text-white transition-colors">Features</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Pricing</a></li>
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
