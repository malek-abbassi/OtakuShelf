<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import { useAnimeUtils } from '~/composables/use-anime-utils';

type Props = {
  anime: Readonly<Anime>;
};

defineProps<Props>();

const { getAnimeTitle, formatStatus, getStatusColor, getAirDate, formatScore } = useAnimeUtils();
</script>

<template>
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
</template>
