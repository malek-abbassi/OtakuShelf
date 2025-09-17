<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import AnimeDescription from '~/components/anime-description.vue';
import AnimeGenres from '~/components/anime-genres.vue';
import AnimeImage from '~/components/anime-image.vue';
import AnimeMeta from '~/components/anime-meta.vue';
import AnimeWatchlistActions from '~/components/anime-watchlist-actions.vue';
import { useAnimeUtils } from '~/composables/use-anime-utils';

type Props = {
  anime: Anime;
  variant?: 'default' | 'compact' | 'detailed';
  showWatchlistButton?: boolean;
  isInWatchlist?: boolean;
  isLoading?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  showWatchlistButton: true,
  isInWatchlist: false,
  isLoading: false,
});

const emit = defineEmits<{
  addToWatchlist: [anime: Anime, status: string];
  removeFromWatchlist: [animeId: number];
  click: [anime: Anime];
}>();

// Use anime utils
const { getAnimeTitle } = useAnimeUtils();

// Event handlers
function handleClick() {
  if (!props.isLoading) {
    emit('click', props.anime);
  }
}

function handleAddToWatchlist(anime: Anime, status: string) {
  emit('addToWatchlist', anime, status);
}

function handleRemoveFromWatchlist(animeId: number) {
  emit('removeFromWatchlist', animeId);
}
</script>

<template>
  <UCard
    class="group transition-all duration-300 cursor-pointer touch-manipulation min-h-[320px]"
    :class="{
      'hover:shadow-lg hover:scale-[1.02]': !isLoading,
      'opacity-50': isLoading,
      'h-80 sm:h-96': variant === 'compact',
      'h-auto': variant !== 'compact',
    }"
    @click="handleClick"
  >
    <!-- Loading Overlay -->
    <div
      v-if="isLoading"
      class="absolute inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-10 flex items-center justify-center"
    >
      <UIcon name="i-heroicons-arrow-path" class="w-6 h-6 animate-spin text-primary-600" />
    </div>

    <!-- Cover Image -->
    <AnimeImage
      :anime="anime"
      :variant="variant"
      :is-in-watchlist="isInWatchlist"
    />

    <!-- Card Content -->
    <div class="-mt-2 space-y-3">
      <!-- Title -->
      <h3
        class="font-semibold text-gray-900 dark:text-white line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors"
        :class="{
          'text-sm': variant === 'compact',
          'text-base': variant === 'default',
          'text-lg': variant === 'detailed',
        }"
      >
        {{ getAnimeTitle(anime.title) }}
      </h3>

      <!-- Meta Information -->
      <AnimeMeta :anime="anime" :variant="variant" />

      <!-- Genres -->
      <AnimeGenres :anime="anime" :variant="variant" />

      <!-- Detailed version: Description -->
      <AnimeDescription
        v-if="variant === 'detailed'"
        :anime="anime"
        :max-lines="3"
      />
    </div>

    <!-- Watchlist Actions Footer -->
    <template v-if="showWatchlistButton" #footer>
      <AnimeWatchlistActions
        :anime="anime"
        :is-in-watchlist="isInWatchlist"
        :is-loading="isLoading"
        @add-to-watchlist="handleAddToWatchlist"
        @remove-from-watchlist="handleRemoveFromWatchlist"
      />
    </template>
  </UCard>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
