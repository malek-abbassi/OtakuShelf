<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import { WATCH_STATUS_OPTIONS } from '~/types/watchlist';

type Props = {
  anime: Anime;
  isInWatchlist?: boolean;
  isLoading?: boolean;
  showWatchlistButton?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  isInWatchlist: false,
  isLoading: false,
  showWatchlistButton: true,
});

const emit = defineEmits<{
  addToWatchlist: [anime: Anime, status: string];
  removeFromWatchlist: [animeId: number];
}>();

function handleAddToWatchlist(status: string) {
  emit('addToWatchlist', props.anime, status);
}

function handleRemoveFromWatchlist() {
  emit('removeFromWatchlist', props.anime.id);
}
</script>

<template>
  <div v-if="showWatchlistButton" class="flex gap-2">
    <UDropdownMenu
      v-if="!isInWatchlist"
      :items="WATCH_STATUS_OPTIONS.map(option => ({
        label: option.label,
        icon: 'i-heroicons-plus',
        onSelect: () => handleAddToWatchlist(option.value),
      }))"
      @click.stop
    >
      <UButton
        variant="outline"
        size="sm"
        block
        :disabled="isLoading"
        trailing-icon="i-heroicons-chevron-down"
        @click.stop
      >
        Add to Watchlist
      </UButton>
    </UDropdownMenu>

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
