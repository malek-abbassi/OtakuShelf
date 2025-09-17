<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import { useAnimeUtils } from '~/composables/use-anime-utils';

type Props = {
  anime: Readonly<Anime>;
};

defineProps<Props>();

const { cleanDescription } = useAnimeUtils();
</script>

<template>
  <UCard>
    <template #header>
      <h2 class="text-xl font-semibold">
        Synopsis
      </h2>
    </template>
    <div
      v-if="anime.description"
      class="prose prose-sm max-w-none dark:prose-invert"
      v-html="cleanDescription(anime.description)"
    />
    <p v-else class="text-gray-500 italic">
      No description available.
    </p>
  </UCard>
</template>
