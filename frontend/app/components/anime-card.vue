<script setup lang="ts">
import type { Anime } from '../composables/use-ani-list';

import { useAnimeUtils } from '../composables/use-anime-utils';

type Props = {
  anime: Anime;
};

defineProps<Props>();

const {
  getAnimeTitle,
  formatStatus,
  getStatusColor,
  formatScore,
} = useAnimeUtils();

function getYear(anime: Anime): string {
  return anime.startDate?.year?.toString() || 'Unknown';
}
</script>

<template>
  <UCard class="hover:shadow-lg transition-all duration-300 cursor-pointer group overflow-hidden">
    <!-- Cover Image -->
    <div class="relative overflow-hidden -m-6 mb-4">
      <NuxtImg
        :src="anime.coverImage.large || anime.coverImage.medium"
        :alt="getAnimeTitle(anime.title)"
        class="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
        loading="lazy"
        :placeholder="[300, 400, 75, 5]"
      />

      <!-- Overlay with score and status -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />

      <div class="absolute bottom-3 left-3 right-3">
        <div class="flex items-center justify-between text-white">
          <!-- Score -->
          <div v-if="anime.averageScore" class="flex items-center gap-1">
            <UIcon name="i-heroicons-star-solid" class="text-yellow-400 w-4 h-4" />
            <span class="text-sm font-medium">{{ formatScore(anime.averageScore) }}</span>
          </div>

          <!-- Status Badge -->
          <UBadge
            v-if="anime.status"
            :color="getStatusColor(anime.status)"
            variant="soft"
            size="xs"
          >
            {{ formatStatus(anime.status) }}
          </UBadge>
        </div>
      </div>
    </div>

    <!-- Card Content -->
    <div class="-mt-2">
      <!-- Title -->
      <h3 class="font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
        {{ getAnimeTitle(anime.title) }}
      </h3>

      <!-- Meta Information -->
      <div class="space-y-1 text-sm text-gray-600 dark:text-gray-400">
        <div class="flex items-center justify-between">
          <span class="flex items-center gap-1">
            <UIcon name="i-heroicons-calendar" class="w-4 h-4" />
            {{ getYear(anime) }}
          </span>
          <span v-if="anime.episodes" class="flex items-center gap-1">
            <UIcon name="i-heroicons-film" class="w-4 h-4" />
            {{ anime.episodes }} ep
          </span>
        </div>

        <div v-if="anime.genres.length" class="flex items-center gap-1">
          <UIcon name="i-heroicons-tag" class="w-4 h-4" />
          <span class="truncate">{{ anime.genres.slice(0, 2).join(', ') }}</span>
          <span v-if="anime.genres.length > 2" class="text-xs">+{{ anime.genres.length - 2 }}</span>
        </div>
      </div>
    </div>
  </UCard>
</template>
