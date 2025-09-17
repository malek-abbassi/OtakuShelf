<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

import AnimeExternalLinks from '~/components/anime-external-links.vue';
import AnimeHeader from '~/components/anime-header.vue';
import AnimeInfo from '~/components/anime-info.vue';
import AnimeNextEpisode from '~/components/anime-next-episode.vue';
import AnimeStudios from '~/components/anime-studios.vue';
import AnimeSynopsis from '~/components/anime-synopsis.vue';
import AnimeTrailer from '~/components/anime-trailer.vue';

type Props = {
  anime: Readonly<Anime> | null;
};

defineProps<Props>();
</script>

<template>
  <div v-if="anime" class="max-w-5xl mx-auto px-2 sm:px-4">
    <!-- Header with Banner -->
    <AnimeHeader :anime="anime" />

    <!-- Add to Watchlist Section -->
    <div class="mb-4 sm:mb-6">
      <AddToWatchlistSection :anime="anime" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
      <!-- Main Content -->
      <div class="lg:col-span-2 space-y-4 sm:space-y-6">
        <!-- Description -->
        <AnimeSynopsis :anime="anime" />

        <!-- Trailer -->
        <AnimeTrailer :anime="anime" />

        <!-- Next Airing Episode -->
        <AnimeNextEpisode :anime="anime" />
      </div>

      <!-- Sidebar -->
      <div class="space-y-4 sm:space-y-6 order-first lg:order-last">
        <!-- Basic Info -->
        <AnimeInfo :anime="anime" />

        <!-- Studios -->
        <AnimeStudios :anime="anime" />

        <!-- Genres -->
        <UCard v-if="anime.genres.length">
          <template #header>
            <h2 class="text-xl font-semibold">
              Genres
            </h2>
          </template>
          <div class="flex flex-wrap gap-2">
            <UBadge
              v-for="genre in anime.genres"
              :key="genre"
              color="primary"
              variant="soft"
            >
              {{ genre }}
            </UBadge>
          </div>
        </UCard>

        <!-- External Links -->
        <AnimeExternalLinks :anime="anime" />
      </div>
    </div>
  </div>
</template>
