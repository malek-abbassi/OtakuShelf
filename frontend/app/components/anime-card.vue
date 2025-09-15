<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

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
  addToWatchlist: [anime: Anime];
  removeFromWatchlist: [animeId: number];
  click: [anime: Anime];
}>();

// Use anime utils
const {
  getAnimeTitle,
  formatStatus,
  getStatusColor,
  formatScore,
} = useAnimeUtils();

// Computed properties
const formattedDate = computed(() => {
  const date = props.anime.startDate;
  if (!date?.year)
    return 'TBA';
  return date.year.toString();
});

const genres = computed(() => {
  return props.anime.genres || [];
});

const imageUrl = computed(() => {
  return props.anime.coverImage.large || props.anime.coverImage.medium;
});

// Event handlers
function handleClick() {
  if (!props.isLoading) {
    emit('click', props.anime);
  }
}

function handleAddToWatchlist(event: Event) {
  event.stopPropagation();
  emit('addToWatchlist', props.anime);
}

function handleRemoveFromWatchlist(event: Event) {
  event.stopPropagation();
  emit('removeFromWatchlist', props.anime.id);
}
</script>

<template>
  <UCard
    class="group overflow-hidden transition-all duration-300 cursor-pointer"
    :class="{
      'hover:shadow-lg hover:scale-[1.02]': !isLoading,
      'opacity-50': isLoading,
      'h-96': variant === 'compact',
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
    <div
      class="relative overflow-hidden -m-6 mb-4"
      :class="{
        'h-48': variant === 'compact',
        'h-64': variant === 'default',
        'h-80': variant === 'detailed',
      }"
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
          <div v-if="anime.averageScore || anime.meanScore" class="flex items-center gap-1">
            <UIcon name="i-heroicons-star-solid" class="text-yellow-400 w-4 h-4" />
            <span class="text-sm font-medium">{{ formatScore((anime.averageScore || anime.meanScore) ?? null) }}</span>
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

      <!-- Watchlist Status Indicator -->
      <div v-if="isInWatchlist" class="absolute top-3 right-3">
        <UBadge color="success" variant="solid" size="xs">
          <UIcon name="i-heroicons-check" class="w-3 h-3" />
        </UBadge>
      </div>
    </div>

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
      <div
        v-if="variant !== 'compact'"
        class="space-y-2 text-sm text-gray-600 dark:text-gray-400"
      >
        <div class="flex items-center justify-between">
          <span class="flex items-center gap-1">
            <UIcon name="i-heroicons-calendar" class="w-4 h-4" />
            {{ formattedDate }}
          </span>
          <span v-if="anime.episodes" class="flex items-center gap-1">
            <UIcon name="i-heroicons-film" class="w-4 h-4" />
            {{ anime.episodes }} ep
          </span>
        </div>

        <div v-if="genres.length" class="flex items-center gap-1">
          <UIcon name="i-heroicons-tag" class="w-4 h-4" />
          <span class="truncate">{{ genres.slice(0, 2).join(', ') }}</span>
          <span v-if="genres.length > 2" class="text-xs">+{{ genres.length - 2 }}</span>
        </div>
      </div>

      <!-- Compact version meta -->
      <div
        v-if="variant === 'compact'"
        class="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400"
      >
        <span>{{ formattedDate }}</span>
        <span v-if="anime.episodes">{{ anime.episodes }} ep</span>
      </div>

      <!-- Detailed version: Description -->
      <div v-if="variant === 'detailed' && anime.description" class="text-sm text-gray-600 dark:text-gray-400">
        <p class="line-clamp-3">
          {{ anime.description.replace(/<[^>]*>/g, '') }}
        </p>
      </div>

      <!-- Detailed version: Genres -->
      <div v-if="variant === 'detailed' && genres.length" class="flex flex-wrap gap-1">
        <UBadge
          v-for="genre in genres.slice(0, 4)"
          :key="genre"
          variant="subtle"
          size="xs"
        >
          {{ genre }}
        </UBadge>
        <UBadge
          v-if="genres.length > 4"
          variant="outline"
          size="xs"
        >
          +{{ genres.length - 4 }}
        </UBadge>
      </div>
    </div>

    <!-- Watchlist Actions Footer -->
    <template v-if="showWatchlistButton" #footer>
      <div class="flex gap-2">
        <UButton
          v-if="!isInWatchlist"
          variant="outline"
          size="sm"
          block
          :disabled="isLoading"
          @click="handleAddToWatchlist"
        >
          <UIcon name="i-heroicons-plus" class="w-4 h-4 mr-1" />
          Add to Watchlist
        </UButton>

        <UButton
          v-else
          variant="soft"
          color="success"
          size="sm"
          block
          :disabled="isLoading"
          @click="handleRemoveFromWatchlist"
        >
          <UIcon name="i-heroicons-check" class="w-4 h-4 mr-1" />
          In Watchlist
        </UButton>
      </div>
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

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
