<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

type Props = {
  anime: Readonly<Anime>;
};

defineProps<Props>();

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
</template>
