<script setup lang="ts">
import type { Anime, SearchResult } from '~/composables/use-ani-list';
import type { WatchlistAddSchema } from '~/types/watchlist';

import AnimeCard from '~/components/anime-card.vue';
import { useAniList } from '~/composables/use-ani-list';
import { useAuth } from '~/composables/use-auth';
import { useWatchlist } from '~/composables/use-watchlist';

type Props = {
  initialQuery?: string;
  showWatchlistActions?: boolean;
  debounceMs?: number;
  showFilters?: boolean;
  variant?: 'default' | 'compact';
};

type Emits = {
  selectAnime: [anime: Anime];
  addedToWatchlist: [anime: Anime];
};

const props = withDefaults(defineProps<Props>(), {
  initialQuery: '',
  showWatchlistActions: true,
  debounceMs: 300,
  showFilters: false,
  variant: 'default',
});

const emit = defineEmits<Emits>();

// Composables
const { searchAnime } = useAniList();
const { addToWatchlist, checkAnimeInWatchlist } = useWatchlist();
const { isLoggedIn } = useAuth();

// Reactive state
const searchQuery = ref(props.initialQuery);
const searchResults = ref<SearchResult | null>(null);
const currentPage = ref(1);
const pending = ref(false);
const error = ref<Error | null>(null);
const searched = ref(false);

// Watchlist state for each anime
const watchlistItems = ref<Map<number, any>>(new Map());
const addingToWatchlist = ref<Set<number>>(new Set());

// Debounce timer
let debounceTimer: NodeJS.Timeout | null = null;

// Debounced search function
function debouncedSearch(query: string) {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }

  debounceTimer = setTimeout(() => {
    if (query.trim()) {
      performSearch(1);
    }
  }, props.debounceMs);
}

// Watch for search query changes for auto-search
watch(searchQuery, (newQuery) => {
  if (newQuery.trim()) {
    debouncedSearch(newQuery);
  }
});

// Search functionality
async function performSearch(page = 1) {
  if (!searchQuery.value.trim())
    return;

  try {
    pending.value = true;
    error.value = null;
    currentPage.value = page;

    searchResults.value = await searchAnime(searchQuery.value.trim(), page, 20);
    searched.value = true;

    // Check watchlist status for each anime
    if (isLoggedIn.value && searchResults.value?.media) {
      await checkWatchlistStatus(searchResults.value.media);
    }
  }
  catch (err) {
    error.value = err as Error;
    searchResults.value = null;
  }
  finally {
    pending.value = false;
  }
}

// Check if anime are in watchlist
async function checkWatchlistStatus(animeList: Anime[]) {
  if (!isLoggedIn.value)
    return;

  const checks = animeList.map(async (anime) => {
    try {
      const item = await checkAnimeInWatchlist(anime.id);
      if (item) {
        watchlistItems.value.set(anime.id, item);
      }
    }
    catch (err) {
      console.error(`Error checking watchlist for anime ${anime.id}:`, err);
    }
  });

  await Promise.allSettled(checks);
}

// Add anime to watchlist with dropdown selection
async function handleAddToWatchlistDropdown(anime: Anime) {
  if (!isLoggedIn.value) {
    navigateTo('/auth');
    return;
  }

  addingToWatchlist.value.add(anime.id);

  try {
    const score = anime.averageScore || anime.meanScore;
    const imageUrl = anime.coverImage.large || anime.coverImage.medium;
    const animeData: WatchlistAddSchema = {
      animeId: anime.id,
      animeTitle: anime.title.romaji || anime.title.english || anime.title.native || 'Unknown Title',
      animePictureUrl: imageUrl && imageUrl.startsWith('http') ? imageUrl : undefined,
      animeScore: score ? score / 10 : undefined,
      status: 'plan_to_watch',
      notes: '',
    };

    const result = await addToWatchlist(animeData);

    if (result.success && result.item) {
      watchlistItems.value.set(anime.id, result.item);
      emit('addedToWatchlist', anime);
    }
  }
  catch (err) {
    console.error('Error adding to watchlist:', err);
  }
  finally {
    addingToWatchlist.value.delete(anime.id);
  }
}

// Event handlers
function handleSearchClick() {
  performSearch(1);
}

function changePage(page: number) {
  performSearch(page);
}

function selectAnime(anime: Anime) {
  emit('selectAnime', anime);
}

// Helper functions
function isInWatchlist(animeId: number): boolean {
  return watchlistItems.value.has(animeId);
}

function isAdding(animeId: number): boolean {
  return addingToWatchlist.value.has(animeId);
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
      <UInput v-model="searchQuery" placeholder="Search for anime..." size="lg" class="flex-1" :loading="pending"
        @keyup.enter="handleSearchClick">
        <template #leading>
          <UIcon name="i-heroicons-magnifying-glass" />
        </template>
      </UInput>
      <UButton size="lg" :loading="pending" :disabled="!searchQuery.trim()" @click="handleSearchClick">
        Search
      </UButton>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="flex flex-col items-center justify-center py-12">
      <ULoading class="mb-4" />
      <p class="text-gray-600 dark:text-gray-400">
        Searching anime...
      </p>
    </div>

    <!-- Error State -->
    <UAlert v-if="error" color="error" variant="soft" title="Search Error" :description="error.message" />

    <!-- Results -->
    <div v-if="searchResults && !pending" class="space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold">
          Found {{ searchResults.pageInfo.total }} results
        </h3>
        <div v-if="searchResults.pageInfo.lastPage > 1" class="flex gap-2">
          <UButton variant="outline" size="sm" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
            Previous
          </UButton>
          <span class="flex items-center px-3 text-sm">
            Page {{ currentPage }} of {{ searchResults.pageInfo.lastPage }}
          </span>
          <UButton variant="outline" size="sm" :disabled="!searchResults.pageInfo.hasNextPage"
            @click="changePage(currentPage + 1)">
            Next
          </UButton>
        </div>
      </div>

      <!-- Anime Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <AnimeCard v-for="anime in searchResults.media" :key="anime.id" :anime="anime"
          :is-in-watchlist="isInWatchlist(anime.id)" :is-loading="isAdding(anime.id)"
          :show-watchlist-button="showWatchlistActions && isLoggedIn" @click="selectAnime"
          @add-to-watchlist="handleAddToWatchlistDropdown" />
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

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
