<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

type Props = {
  anime: Anime;
  variant?: 'default' | 'compact' | 'detailed';
  maxGenres?: number;
};

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  maxGenres: 2,
});

const genres = computed(() => {
  return props.anime.genres || [];
});

const displayGenres = computed(() => {
  return genres.value.slice(0, props.maxGenres);
});

const remainingCount = computed(() => {
  return Math.max(0, genres.value.length - props.maxGenres);
});
</script>

<template>
  <!-- Default/Compact version -->
  <div
    v-if="variant !== 'detailed' && genres.length"
    class="flex items-center gap-1"
  >
    <UIcon name="i-heroicons-tag" class="w-4 h-4" />
    <span class="truncate">{{ displayGenres.join(', ') }}</span>
    <span v-if="remainingCount > 0" class="text-xs">+{{ remainingCount }}</span>
  </div>

  <!-- Detailed version: Genres -->
  <div v-if="variant === 'detailed' && genres.length" class="flex flex-wrap gap-1">
    <UBadge
      v-for="genre in displayGenres"
      :key="genre"
      variant="subtle"
      size="xs"
    >
      {{ genre }}
    </UBadge>
    <UBadge
      v-if="remainingCount > 0"
      variant="outline"
      size="xs"
    >
      +{{ remainingCount }}
    </UBadge>
  </div>
</template>
