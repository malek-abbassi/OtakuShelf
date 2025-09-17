<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

type Props = {
  anime: Readonly<Anime>;
};

defineProps<Props>();
</script>

<template>
  <UCard v-if="anime.studios.nodes.length">
    <template #header>
      <h2 class="text-xl font-semibold">
        Studios
      </h2>
    </template>
    <div class="space-y-2">
      <div
        v-for="studio in anime.studios.nodes"
        :key="studio.name"
        class="text-sm"
      >
        <span class="font-medium">{{ studio.name }}</span>
        <UBadge
          v-if="studio.isMain"
          color="primary"
          variant="soft"
          size="xs"
          class="ml-2"
        >
          Main
        </UBadge>
      </div>
    </div>
  </UCard>
</template>
