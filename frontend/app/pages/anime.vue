<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import { useAnimeDetails } from '~/composables/use-anime-details';
import { useAnimeUtils } from '~/composables/use-anime-utils';

// Meta
definePageMeta({
  title: 'Discover Anime',
  description: 'Search and discover anime titles with detailed information from AniList',
});

// Enhanced SEO
useSeoMeta({
  title: 'Discover Anime - OtakuShelf | Browse Thousands of Anime Titles',
  ogTitle: 'Discover Anime - OtakuShelf | Browse Thousands of Anime Titles',
  description: 'Search through thousands of anime titles with detailed information including ratings, air dates, genres, and more. Discover your next favorite anime with comprehensive search and filtering.',
  ogDescription: 'Search through thousands of anime titles with detailed information including ratings, air dates, genres, and more. Discover your next favorite anime with comprehensive search and filtering.',
  ogImage: '/favicon.ico',
  ogImageAlt: 'OtakuShelf Anime Discovery',
  twitterCard: 'summary_large_image',
  keywords: 'anime search, discover anime, anime database, anime titles, anime ratings, anilist search, anime genres',
  robots: 'index, follow',
});

// Add canonical link
useHead({
  link: [
    { rel: 'canonical', href: 'https://otakushelf.com/anime' },
  ],
});

// Structured Data for Anime Discovery Page
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'name': 'Discover Anime - OtakuShelf',
        'description': 'Search and discover anime titles with detailed information from AniList',
        'url': 'https://otakushelf.com/anime',
        'mainEntity': {
          '@type': 'SearchAction',
          'target': 'https://otakushelf.com/anime?q={search_term_string}',
          'query-input': 'required name=search_term_string',
        },
      }),
    },
  ],
});

const route = useRoute();
const { getAnimeTitle } = useAnimeUtils();

// Use the anime details composable
const {
  selectedAnime,
  selectedAnimeDetails,
  isModalOpen,
  isLoading,
  showAnimeDetails,
  retryLoadDetails,
} = useAnimeDetails();

// Handle anime selection
function handleAnimeSelect(anime: Anime) {
  showAnimeDetails(anime);
}

// Handle successful watchlist addition
function handleWatchlistAdd(anime: Anime) {
  // You could show a toast notification here
  console.error('Added to watchlist:', getAnimeTitle(anime.title));
}

// Update URL when search is performed
watch(() => route.query.q, (newQuery) => {
  if (newQuery) {
    useSeoMeta({
      title: `Search: ${newQuery} - OtakuShelf`,
      ogTitle: `Search: ${newQuery} - OtakuShelf`,
    });
  }
});
</script>

<template>
  <NuxtLayout>
    <div class="container mx-auto px-4 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Discover Anime
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Search through thousands of anime titles from the AniList database
        </p>
      </div>

      <!-- Search Component -->
      <AnimeSearchEnhanced
        :initial-query="(route.query.q as string) || ''"
        @select-anime="handleAnimeSelect"
        @added-to-watchlist="handleWatchlistAdd"
      />

      <!-- Anime Details Modal - Official UModal Implementation -->
      <UModal
        v-model:open="isModalOpen"
        :title="selectedAnime ? getAnimeTitle(selectedAnime.title) : 'Anime Details'"
        :dismissible="!isLoading"
        :ui="{
          content: 'max-w-4xl w-full max-h-[90vh]',
          body: 'p-0',
        }"
      >
        <template #body="{ close }">
          <!-- Loading State -->
          <div v-if="isLoading" class="p-6">
            <LoadingState
              message="Loading anime details..."
              size="lg"
            />
          </div>

          <!-- Anime Details -->
          <div v-else-if="selectedAnimeDetails">
            <AnimeDetails :anime="selectedAnimeDetails" />
          </div>

          <!-- Error State -->
          <div v-else class="p-6">
            <ErrorState
              title="Failed to load anime details"
              message="We couldn't load the detailed information for this anime. This might be a temporary issue."
              @retry="retryLoadDetails"
            >
              <template #actions>
                <UButton
                  color="primary"
                  @click="retryLoadDetails"
                >
                  Try Again
                </UButton>
                <UButton
                  color="neutral"
                  variant="outline"
                  @click="close"
                >
                  Close
                </UButton>
              </template>
            </ErrorState>
          </div>
        </template>
      </UModal>
    </div>
  </NuxtLayout>
</template>
