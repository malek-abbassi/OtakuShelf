<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

type Props = {
  anime: Readonly<Anime>;
};

defineProps<Props>();
</script>

<template>
  <UCard v-if="anime.externalLinks?.length">
    <template #header>
      <h2 class="text-xl font-semibold">
        External Links
      </h2>
    </template>
    <div class="space-y-2">
      <UButton
        v-for="link in anime.externalLinks.slice(0, 5)"
        :key="link.site"
        :to="link.url"
        target="_blank"
        variant="outline"
        size="sm"
        class="w-full justify-start"
      >
        <UIcon name="i-heroicons-arrow-top-right-on-square" class="mr-2" />
        {{ link.site }}
      </UButton>
    </div>
  </UCard>
</template>
