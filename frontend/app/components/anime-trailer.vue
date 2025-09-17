<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

type Props = {
  anime: Readonly<Anime>;
};

defineProps<Props>();
</script>

<template>
  <UCard v-if="anime.trailer">
    <template #header>
      <h2 class="text-xl font-semibold">
        Trailer
      </h2>
    </template>
    <div class="aspect-video">
      <iframe
        v-if="anime.trailer.site === 'youtube'"
        :src="`https://www.youtube.com/embed/${anime.trailer.id}`"
        class="w-full h-full rounded"
        frameborder="0"
        allowfullscreen
      />
    </div>
  </UCard>
</template>
