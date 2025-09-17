<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import { useAnimeUtils } from '~/composables/use-anime-utils';

type Props = {
  anime: Anime;
  variant?: 'default' | 'compact' | 'detailed';
  showScore?: boolean;
  showStatus?: boolean;
  showWatchlistIndicator?: boolean;
  isInWatchlist?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  showScore: true,
  showStatus: true,
  showWatchlistIndicator: true,
  isInWatchlist: false,
});

const { getAnimeTitle, formatStatus, getStatusColor, formatScore } = useAnimeUtils();

const imageUrl = computed(() => {
  return props.anime.coverImage.large || props.anime.coverImage.medium;
});

const imageHeight = computed(() => {
  switch (props.variant) {
    case 'compact': return 'h-48';
    case 'detailed': return 'h-80';
    default: return 'h-64';
  }
});
</script>

<template>
  <div
    class="relative overflow-hidden -m-6 mb-4"
    :class="imageHeight"
  >
    <NuxtImg
      :src="imageUrl"
      :alt="getAnimeTitle(anime.title)"
      class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      loading="lazy"
      placeholder="/placeholder-anime.svg"
    />

    <!-- Overlay with score and status -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />

    <div class="absolute bottom-3 left-3 right-3">
      <div class="flex items-center justify-between text-white">
        <!-- Score -->
        <div v-if="showScore && (anime.averageScore || anime.meanScore)" class="flex items-center gap-1">
          <UIcon name="i-heroicons-star-solid" class="text-yellow-400 w-4 h-4" />
          <span class="text-sm font-medium">{{ formatScore((anime.averageScore || anime.meanScore) ?? null) }}</span>
        </div>

        <!-- Status Badge -->
        <UBadge
          v-if="showStatus && anime.status"
          :color="getStatusColor(anime.status)"
          variant="soft"
          size="xs"
        >
          {{ formatStatus(anime.status) }}
        </UBadge>
      </div>
    </div>

    <!-- Watchlist Status Indicator -->
    <div v-if="showWatchlistIndicator && isInWatchlist" class="absolute top-3 right-3">
      <UBadge color="success" variant="solid" size="xs">
        <UIcon name="i-heroicons-check" class="w-3 h-3" />
      </UBadge>
    </div>
  </div>
</template>
