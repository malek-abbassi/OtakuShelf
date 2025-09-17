<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import { useAnimeUtils } from '~/composables/use-anime-utils';

type Props = {
  anime: Readonly<Anime>;
};

defineProps<Props>();

const { formatSource, formatEpisodes, formatDuration } = useAnimeUtils();
</script>

<template>
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
</template>
