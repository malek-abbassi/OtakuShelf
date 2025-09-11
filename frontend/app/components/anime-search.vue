<script setup lang="ts">
import type { Anime, SearchResult } from '../composables/use-ani-list';

import { useAniList } from '../composables/use-ani-list';

type Props = {
  initialQuery?: string;
};

type Emits = {
  selectAnime: [anime: Anime];
};

const props = withDefaults(defineProps<Props>(), {
  initialQuery: '',
});

const emit = defineEmits<Emits>();

const { searchAnime } = useAniList();

const searchQuery = ref(props.initialQuery);
const searchResults = ref<SearchResult | null>(null);
const currentPage = ref(1);
const pending = ref(false);
const error = ref<Error | null>(null);
const searched = ref(false);

async function performSearch(page = 1) {
  if (!searchQuery.value.trim())
    return;

  try {
    pending.value = true;
    error.value = null;
    currentPage.value = page;

    searchResults.value = await searchAnime(searchQuery.value.trim(), page, 20);
    searched.value = true;
  }
  catch (err) {
    error.value = err as Error;
    searchResults.value = null;
  }
  finally {
    pending.value = false;
  }
}

function handleSearchClick() {
  performSearch(1);
}

function changePage(page: number) {
  performSearch(page);
}

function selectAnime(anime: Anime) {
  emit('selectAnime', anime);
}

// Auto-search if initial query is provided
onMounted(() => {
  if (props.initialQuery.trim()) {
    performSearch();
  }
});
</script>

<template>
  <div class="space-y-6">
    <!-- Search Input -->
    <div class="flex gap-4">
      <UInput
        v-model="searchQuery"
        placeholder="Search for anime..."
        size="lg"
        class="flex-1"
        :loading="pending"
        @keyup.enter="handleSearchClick"
      >
        <template #leading>
          <UIcon name="i-heroicons-magnifying-glass" />
        </template>
      </UInput>
      <UButton
        size="lg"
        :loading="pending"
        :disabled="!searchQuery.trim()"
        @click="handleSearchClick"
      >
        Search
      </UButton>
    </div>

    <!-- Loading State -->
    <LoadingState
      v-if="pending"
      message="Searching anime..."
      size="md"
    />

    <!-- Error State -->
    <UAlert
      v-if="error"
      color="error"
      variant="soft"
      title="Search Error"
      :description="error.message"
    />

    <!-- Results -->
    <div v-if="searchResults && !pending" class="space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold">
          Found {{ searchResults.pageInfo.total }} results
        </h3>
        <div v-if="searchResults.pageInfo.lastPage > 1" class="flex gap-2">
          <UButton
            variant="outline"
            size="sm"
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            Previous
          </UButton>
          <span class="flex items-center px-3 text-sm">
            Page {{ currentPage }} of {{ searchResults.pageInfo.lastPage }}
          </span>
          <UButton
            variant="outline"
            size="sm"
            :disabled="!searchResults.pageInfo.hasNextPage"
            @click="changePage(currentPage + 1)"
          >
            Next
          </UButton>
        </div>
      </div>

      <!-- Anime Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <AnimeCard
          v-for="anime in searchResults.media"
          :key="anime.id"
          :anime="anime"
          @click="selectAnime(anime)"
        />
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="searched && !searchResults?.media.length && !pending" class="text-center py-12">
      <UIcon name="i-heroicons-face-frown" class="w-12 h-12 mx-auto text-gray-400 dark:text-gray-600 mb-4" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
        No anime found
      </h3>
      <p class="text-gray-500 dark:text-gray-400">
        Try searching with different keywords or check your spelling.
      </p>
    </div>
  </div>
</template>
