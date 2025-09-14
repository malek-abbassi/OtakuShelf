<script setup lang="ts">
// Composables
const { isLoggedIn, userProfile, signOut } = useAuth();
const router = useRouter();

// Methods
async function handleSignOut() {
  try {
    await signOut();
    await router.push('/');
  }
  catch (err) {
    console.error('Error signing out:', err);
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col transition-colors duration-200">
    <!-- Navigation Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-8">
            <div class="flex items-center space-x-2">
              <UIcon name="i-heroicons-book-open" class="text-3xl text-primary-600 dark:text-primary-400" />
              <NuxtLink to="/" class="text-2xl font-bold text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                OtakuShelf
              </NuxtLink>
            </div>
            <nav class="hidden md:flex items-center space-x-6">
              <NuxtLink
                to="/anime"
                class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors font-medium"
              >
                Discover Anime
              </NuxtLink>
              <NuxtLink
                v-if="isLoggedIn"
                to="/watchlist"
                class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors font-medium"
              >
                My Watchlist
              </NuxtLink>
              <NuxtLink
                to="/about"
                class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors font-medium"
              >
                About
              </NuxtLink>
            </nav>
          </div>
          <div class="flex items-center space-x-3">
            <!-- Color Mode Toggle -->
            <UButton
              :icon="$colorMode.value === 'dark' ? 'i-heroicons-sun' : 'i-heroicons-moon'"
              variant="ghost"
              color="neutral"
              @click="$colorMode.preference = $colorMode.value === 'dark' ? 'light' : 'dark'"
            />

            <!-- Authentication Actions -->
            <div v-if="!isLoggedIn">
              <UButton to="/auth" color="primary" variant="solid">
                <UIcon name="i-heroicons-user-circle" class="mr-2" />
                Sign In
              </UButton>
            </div>
            <div v-else class="flex items-center space-x-2">
              <UDropdownMenu
                :items="[
                  [
                    {
                      label: userProfile?.fullName || userProfile?.username || 'Profile',
                      icon: 'i-heroicons-user',
                      disabled: true,
                    },
                  ],
                  [
                    {
                      label: 'My Watchlist',
                      icon: 'i-heroicons-list-bullet',
                      click: () => $router.push('/watchlist'),
                    },
                    {
                      label: 'Settings',
                      icon: 'i-heroicons-cog-6-tooth',
                      click: () => console.error('Settings not implemented'),
                    },
                  ],
                  [
                    {
                      label: 'Sign Out',
                      icon: 'i-heroicons-arrow-right-on-rectangle',
                      click: handleSignOut,
                    },
                  ],
                ]"
              >
                <UButton variant="ghost" color="neutral">
                  <UIcon name="i-heroicons-user-circle" class="text-xl" />
                </UButton>
              </UDropdownMenu>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Page Content -->
    <main class="flex flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 dark:bg-gray-950 text-white py-12 border-t border-gray-800 dark:border-gray-700">
      <div class="container mx-auto px-4">
        <div class="grid md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <UIcon name="i-heroicons-book-open" class="text-2xl text-primary-400" />
              <span class="text-lg font-bold">OtakuShelf</span>
            </div>
            <p class="text-gray-400 dark:text-gray-500">
              Your personal anime and manga collection manager.
            </p>
          </div>

          <div>
            <h5 class="font-semibold mb-4 text-white">
              Product
            </h5>
            <ul class="space-y-2 text-gray-400 dark:text-gray-500">
              <li>
                <NuxtLink to="/about" class="hover:text-white dark:hover:text-gray-300 transition-colors">
                  About
                </NuxtLink>
              </li>
              <li><a href="#" class="hover:text-white dark:hover:text-gray-300 transition-colors">Features</a></li>
              <li><a href="#" class="hover:text-white dark:hover:text-gray-300 transition-colors">Pricing</a></li>
            </ul>
          </div>

          <div>
            <h5 class="font-semibold mb-4 text-white">
              Support
            </h5>
            <ul class="space-y-2 text-gray-400 dark:text-gray-500">
              <li><a href="#" class="hover:text-white dark:hover:text-gray-300 transition-colors">Help Center</a></li>
              <li><a href="#" class="hover:text-white dark:hover:text-gray-300 transition-colors">Contact</a></li>
              <li><a href="#" class="hover:text-white dark:hover:text-gray-300 transition-colors">Community</a></li>
            </ul>
          </div>

          <div>
            <h5 class="font-semibold mb-4 text-white">
              Connect
            </h5>
            <div class="flex space-x-4">
              <UButton icon="i-heroicons-link" variant="ghost" color="neutral" size="sm" />
              <UButton icon="i-heroicons-chat-bubble-left-ellipsis" variant="ghost" color="neutral" size="sm" />
              <UButton icon="i-heroicons-heart" variant="ghost" color="neutral" size="sm" />
            </div>
          </div>
        </div>

        <div class="border-t border-gray-800 dark:border-gray-700 mt-8 pt-8 text-center text-gray-400 dark:text-gray-500">
          <p>&copy; 2025 OtakuShelf. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>
