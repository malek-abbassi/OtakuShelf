<script setup lang="ts">
// Composables
const { isLoggedIn, userProfile } = useAuth();

// Enhanced SEO Meta
useSeoMeta({
  title: 'OtakuShelf - Your Personal Anime & Manga Collection Manager',
  ogTitle: 'OtakuShelf - Your Personal Anime & Manga Collection Manager',
  description: 'Organize, track, and discover your favorite anime series and manga volumes with ease. Keep your otaku journey organized with smart watchlists, detailed stats, and seamless anime discovery.',
  ogDescription: 'Organize, track, and discover your favorite anime series and manga volumes with ease. Keep your otaku journey organized with smart watchlists, detailed stats, and seamless anime discovery.',
  ogImage: '/favicon.ico',
  ogImageAlt: 'OtakuShelf - Anime Collection Manager',
  twitterCard: 'summary_large_image',
  twitterTitle: 'OtakuShelf - Your Personal Anime & Manga Collection Manager',
  twitterDescription: 'Organize, track, and discover your favorite anime series and manga volumes with ease.',
  keywords: 'anime, manga, watchlist, collection, tracker, otaku, anilist, anime database, anime manager',
  robots: 'index, follow',
});

// Add canonical link
useHead({
  link: [
    { rel: 'canonical', href: 'https://otakushelf.com' },
  ],
});

// Structured Data for SEO
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebApplication',
        'name': 'OtakuShelf',
        'description': 'Personal anime and manga collection manager with smart watchlists and discovery features',
        'url': 'https://otakushelf.com',
        'applicationCategory': 'Entertainment',
        'operatingSystem': 'Web',
        'offers': {
          '@type': 'Offer',
          'price': '0',
          'priceCurrency': 'USD',
        },
        'featureList': [
          'Smart Watchlist Management',
          'Anime Discovery',
          'Personal Profile & Stats',
          'Progress Tracking',
        ],
      }),
    },
  ],
});
</script>

<template>
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

        <!-- Authenticated User Actions -->
        <div v-if="isLoggedIn" class="flex flex-col sm:flex-row gap-4 justify-center">
          <UButton to="/watchlist" size="lg" color="neutral" variant="solid">
            <UIcon name="i-heroicons-list-bullet" class="mr-2" />
            My Watchlist
          </UButton>
          <UButton to="/anime" size="lg" variant="outline" color="neutral">
            <UIcon name="i-heroicons-magnifying-glass" class="mr-2" />
            Discover Anime
          </UButton>
        </div>

        <!-- Non-authenticated User Actions -->
        <div v-else class="flex flex-col sm:flex-row gap-4 justify-center">
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

        <!-- User Welcome Message -->
        <div v-if="isLoggedIn && userProfile" class="mt-8">
          <p class="text-lg text-violet-100">
            Welcome back, {{ userProfile.fullName || userProfile.username }}!
            <span v-if="userProfile.watchlistCount > 0">
              You have {{ userProfile.watchlistCount }} anime in your watchlist.
            </span>
            <span v-else>
              Ready to start your anime journey?
            </span>
          </p>
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
          <UCard class="text-center hover:shadow-lg transition-shadow">
            <template #header>
              <div class="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mx-auto">
                <UIcon name="i-heroicons-list-bullet" class="text-primary-600 dark:text-primary-400 text-2xl" />
              </div>
            </template>
            <h4 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              Smart Watchlist
            </h4>
            <p class="text-gray-600 dark:text-gray-400">
              Keep track of anime you're watching, planning to watch, completed, or dropped. Never lose track of your progress.
            </p>
          </UCard>

          <UCard class="text-center hover:shadow-lg transition-shadow">
            <template #header>
              <div class="w-16 h-16 bg-secondary-100 dark:bg-secondary-900/30 rounded-full flex items-center justify-center mx-auto">
                <UIcon name="i-heroicons-magnifying-glass" class="text-secondary-600 dark:text-secondary-400 text-2xl" />
              </div>
            </template>
            <h4 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              Discover Anime
            </h4>
            <p class="text-gray-600 dark:text-gray-400">
              Search through thousands of anime titles from AniList. Get detailed information, ratings, and add them to your watchlist instantly.
            </p>
          </UCard>

          <UCard class="text-center hover:shadow-lg transition-shadow">
            <template #header>
              <div class="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto">
                <UIcon name="i-heroicons-user-circle" class="text-green-600 dark:text-green-400 text-2xl" />
              </div>
            </template>
            <h4 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">
              Personal Profile
            </h4>
            <p class="text-gray-600 dark:text-gray-400">
              Create your profile, track your viewing statistics, and share your anime taste with the community.
            </p>
          </UCard>
        </div>
      </div>
    </section>

    <!-- Call to Action Section -->
    <section v-if="!isLoggedIn" class="py-20 bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-700 dark:to-secondary-700">
      <div class="container mx-auto px-4 text-center">
        <h3 class="text-3xl font-bold text-white mb-4">
          Ready to Start Your Journey?
        </h3>
        <p class="text-lg text-primary-100 mb-8 max-w-xl mx-auto">
          Join thousands of anime fans who are already organizing their collections with OtakuShelf.
        </p>
        <UButton to="/auth" size="lg" color="neutral" variant="solid">
          <UIcon name="i-heroicons-rocket-launch" class="mr-2" />
          Create Your Account
        </UButton>
      </div>
    </section>

    <!-- Quick Stats Section for Logged In Users -->
    <section v-else-if="userProfile" class="py-20 bg-gray-50 dark:bg-gray-800">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Your Anime Stats
          </h3>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            Here's your anime journey so far
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8 max-w-3xl mx-auto">
          <UCard class="text-center">
            <div class="p-6">
              <div class="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-2">
                {{ userProfile.watchlistCount }}
              </div>
              <div class="text-gray-600 dark:text-gray-400">
                Anime in Watchlist
              </div>
            </div>
          </UCard>

          <UCard class="text-center">
            <div class="p-6">
              <div class="text-3xl font-bold text-secondary-600 dark:text-secondary-400 mb-2">
                {{ userProfile.username }}
              </div>
              <div class="text-gray-600 dark:text-gray-400">
                Your Username
              </div>
            </div>
          </UCard>

          <UCard class="text-center">
            <div class="p-6">
              <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
                {{ new Date(userProfile.createdAt).getFullYear() }}
              </div>
              <div class="text-gray-600 dark:text-gray-400">
                Member Since
              </div>
            </div>
          </UCard>
        </div>

        <div class="text-center mt-12">
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <UButton to="/watchlist" size="lg" color="primary">
              <UIcon name="i-heroicons-list-bullet" class="mr-2" />
              View My Watchlist
            </UButton>
            <UButton to="/anime" size="lg" variant="outline" color="primary">
              <UIcon name="i-heroicons-plus" class="mr-2" />
              Add More Anime
            </UButton>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
