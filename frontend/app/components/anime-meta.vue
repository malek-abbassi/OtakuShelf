<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

type Props = {
  anime: Anime;
  variant?: 'default' | 'compact' | 'detailed';
  showDate?: boolean;
  showEpisodes?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  showDate: true,
  showEpisodes: true,
});

const formattedDate = computed(() => {
  const date = props.anime.startDate;
  if (!date?.year)
    return 'TBA';
  return date.year.toString();
});
</script>

<template>
  <!-- Meta Information -->
  <div
    v-if="variant !== 'compact'"
    class="space-y-2 text-sm text-gray-600 dark:text-gray-400"
  >
    <div class="flex items-center justify-between">
      <span v-if="showDate" class="flex items-center gap-1">
        <UIcon name="i-heroicons-calendar" class="w-4 h-4" />
        {{ formattedDate }}
      </span>
      <span v-if="showEpisodes && anime.episodes" class="flex items-center gap-1">
        <UIcon name="i-heroicons-film" class="w-4 h-4" />
        {{ anime.episodes }} ep
      </span>
    </div>
  </div>

  <!-- Compact version meta -->
  <div
    v-if="variant === 'compact'"
    class="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400"
  >
    <span v-if="showDate">{{ formattedDate }}</span>
    <span v-if="showEpisodes && anime.episodes">{{ anime.episodes }} ep</span>
  </div>
</template>
