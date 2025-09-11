<script setup lang="ts">
import type { Anime } from '../composables/use-ani-list';

import { useAnimeUtils } from '../composables/use-anime-utils';

type Props = {
  anime: Readonly<Anime> | null;
};

defineProps<Props>();

const {
  getAnimeTitle,
  formatStatus,
  getStatusColor,
  getAirDate,
  formatSource,
  cleanDescription,
  formatScore,
  formatEpisodes,
  formatDuration,
} = useAnimeUtils();

function formatAiringTime(timestamp: number): string {
  return new Date(timestamp * 1000).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}
</script>

<template>
  <div v-if="anime" class="max-w-5xl mx-auto">
    <!-- Header with Banner -->
    <div
      class="relative h-64 bg-gradient-to-br from-blue-600 to-purple-700 rounded-lg overflow-hidden mb-6"
      :style="anime.bannerImage ? `background-image: url(${anime.bannerImage}); background-size: cover; background-position: center;` : ''"
    >
      <div class="absolute inset-0 bg-black/50" />
      <div class="relative z-10 flex items-end h-full p-6">
        <div class="flex gap-4 items-end">
          <NuxtImg
            :src="anime.coverImage.large || anime.coverImage.medium"
            :alt="getAnimeTitle(anime.title)"
            class="w-32 h-48 object-cover rounded-lg shadow-lg"
            loading="lazy"
          />
          <div class="text-white">
            <h1 class="text-3xl font-bold mb-2">
              {{ getAnimeTitle(anime.title) }}
            </h1>
            <div class="flex items-center gap-4 mb-2">
              <div v-if="anime.averageScore" class="flex items-center gap-1">
                <UIcon name="i-heroicons-star-solid" class="text-yellow-400" />
                <span class="font-medium">{{ formatScore(anime.averageScore) }}</span>
              </div>
              <UBadge
                v-if="anime.status"
                :color="getStatusColor(anime.status)"
                variant="soft"
              >
                {{ formatStatus(anime.status) }}
              </UBadge>
            </div>
            <div class="text-sm opacity-90">
              {{ getAirDate(anime) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Main Content -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Description -->
        <UCard>
          <template #header>
            <h2 class="text-xl font-semibold">
              Synopsis
            </h2>
          </template>
          <div
            v-if="anime.description"
            class="prose prose-sm max-w-none dark:prose-invert"
            v-html="cleanDescription(anime.description)"
          />
          <p v-else class="text-gray-500 italic">
            No description available.
          </p>
        </UCard>

        <!-- Trailer -->
        <UCard v-if="anime.trailer">
          <template #header>
            <h2 class="text-xl font-semibold">
              Trailer
            </h2>
          </template>
          <div class="aspect-video">
            <iframe
              v-if="anime.trailer.site === 'youtube'"
              :src="`https://www.youtube.com/embed/${anime.trailer.id}`"
              class="w-full h-full rounded"
              frameborder="0"
              allowfullscreen
            />
          </div>
        </UCard>

        <!-- Next Airing Episode -->
        <UCard v-if="anime.nextAiringEpisode">
          <template #header>
            <h2 class="text-xl font-semibold flex items-center gap-2">
              <UIcon name="i-heroicons-clock" />
              Next Episode
            </h2>
          </template>
          <div class="space-y-2">
            <p class="font-medium">
              Episode {{ anime.nextAiringEpisode.episode }}
            </p>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Airs {{ formatAiringTime(anime.nextAiringEpisode.airingAt) }}
            </p>
          </div>
        </UCard>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Basic Info -->
        <UCard>
          <template #header>
            <h2 class="text-xl font-semibold">
              Information
            </h2>
          </template>
          <div class="space-y-3 text-sm">
            <div v-if="anime.format">
              <span class="font-medium text-gray-700 dark:text-gray-300">Format:</span>
              <span class="ml-2">{{ anime.format }}</span>
            </div>
            <div v-if="anime.episodes">
              <span class="font-medium text-gray-700 dark:text-gray-300">Episodes:</span>
              <span class="ml-2">{{ formatEpisodes(anime.episodes) }}</span>
            </div>
            <div v-if="anime.duration">
              <span class="font-medium text-gray-700 dark:text-gray-300">Duration:</span>
              <span class="ml-2">{{ formatDuration(anime.duration) }}</span>
            </div>
            <div v-if="anime.season && anime.seasonYear">
              <span class="font-medium text-gray-700 dark:text-gray-300">Season:</span>
              <span class="ml-2">{{ anime.season }} {{ anime.seasonYear }}</span>
            </div>
            <div v-if="anime.source">
              <span class="font-medium text-gray-700 dark:text-gray-300">Source:</span>
              <span class="ml-2">{{ formatSource(anime.source) }}</span>
            </div>
          </div>
        </UCard>

        <!-- Studios -->
        <UCard v-if="anime.studios.nodes.length">
          <template #header>
            <h2 class="text-xl font-semibold">
              Studios
            </h2>
          </template>
          <div class="space-y-2">
            <div
              v-for="studio in anime.studios.nodes"
              :key="studio.name"
              class="text-sm"
            >
              <span class="font-medium">{{ studio.name }}</span>
              <UBadge
                v-if="studio.isMain"
                color="primary"
                variant="soft"
                size="xs"
                class="ml-2"
              >
                Main
              </UBadge>
            </div>
          </div>
        </UCard>

        <!-- Genres -->
        <UCard v-if="anime.genres.length">
          <template #header>
            <h2 class="text-xl font-semibold">
              Genres
            </h2>
          </template>
          <div class="flex flex-wrap gap-2">
            <UBadge
              v-for="genre in anime.genres"
              :key="genre"
              color="primary"
              variant="soft"
            >
              {{ genre }}
            </UBadge>
          </div>
        </UCard>

        <!-- External Links -->
        <UCard v-if="anime.externalLinks?.length">
          <template #header>
            <h2 class="text-xl font-semibold">
              External Links
            </h2>
          </template>
          <div class="space-y-2">
            <UButton
              v-for="link in anime.externalLinks.slice(0, 5)"
              :key="link.site"
              :to="link.url"
              target="_blank"
              variant="outline"
              size="sm"
              class="w-full justify-start"
            >
              <UIcon name="i-heroicons-arrow-top-right-on-square" class="mr-2" />
              {{ link.site }}
            </UButton>
          </div>
        </UCard>
      </div>
    </div>
  </div>
</template>
