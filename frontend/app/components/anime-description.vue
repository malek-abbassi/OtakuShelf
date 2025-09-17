<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';

type Props = {
  anime: Anime;
  maxLines?: number;
  showReadMore?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  maxLines: 3,
  showReadMore: false,
});

const cleanDescription = computed(() => {
  return props.anime.description?.replace(/<[^>]*>/g, '') || '';
});

const shouldShowReadMore = computed(() => {
  return props.showReadMore && cleanDescription.value.length > 150;
});
</script>

<template>
  <div v-if="anime.description" class="text-sm text-gray-600 dark:text-gray-400">
    <p :class="`line-clamp-${maxLines}`">
      {{ cleanDescription }}
    </p>
    <button
      v-if="shouldShowReadMore"
      class="text-primary-600 dark:text-primary-400 hover:underline mt-1 text-xs"
    >
      Read more
    </button>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
