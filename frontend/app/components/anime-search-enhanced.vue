<script setup lang="ts">
import type { Anime, SearchResult } from '~/composables/use-ani-list';

import AnimeCard from '~/components/anime-card.vue';
import AnimeSkeleton from '~/components/anime-skeleton.vue';
import EmptyState from '~/components/empty-state.vue';
import Pagination from '~/components/pagination.vue';
import SearchInput from '~/components/search-input.vue';
import { useAniList } from '~/composables/use-ani-list';
import { useAnimeSearchWithWatchlist } from '~/composables/use-anime-search-with-watchlist';

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
const { isLoggedIn } = useAuth();
const {
  checkWatchlistStatus,
  handleAddToWatchlist,
  isInWatchlist,
  isAdding,
} = useAnimeSearchWithWatchlist();

// Reactive state
const searchQuery = ref(props.initialQuery);
const searchResults = ref<SearchResult | null>(null);
const currentPage = ref(1);
const pending = ref(false);
const error = ref<Error | null>(null);
const searched = ref(false);

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

function handleAddToWatchlistClick(anime: Anime, status: string) {
  handleAddToWatchlist(anime, status, emit);
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
    <SearchInput
      v-model="searchQuery"
      placeholder="Search for anime..."
      :loading="pending"
      size="lg"
      @search="handleSearchClick"
    />

    <!-- Loading State -->
    <div v-if="pending" class="flex flex-col items-center justify-center py-12">
      <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary-600 mb-4" />
      <p class="text-gray-600 dark:text-gray-400">
        Searching anime...
      </p>
      <div class="mt-8 w-full">
        <AnimeSkeleton />
      </div>
    </div>

    <!-- Error State -->
    <UAlert v-if="error" color="error" variant="soft" title="Search Error" :description="error.message" />

    <!-- Results -->
    <div v-if="searchResults && !pending" class="space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold">
          Found {{ searchResults.pageInfo.total }} results
        </h3>
        <Pagination
          :current-page="currentPage"
          :total-pages="searchResults.pageInfo.lastPage"
          :has-next-page="searchResults.pageInfo.hasNextPage"
          @change-page="changePage"
        />
      </div>

      <!-- Anime Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 animate-in fade-in-0 duration-300">
        <AnimeCard
          v-for="anime in searchResults.media" :key="anime.id" :anime="anime"
          :is-in-watchlist="isInWatchlist(anime.id)" :is-loading="isAdding(anime.id)"
          :show-watchlist-button="showWatchlistActions && isLoggedIn" @click="selectAnime"
          @add-to-watchlist="handleAddToWatchlistClick"
        />
      </div>
    </div>

    <!-- Empty State -->
    <EmptyState
      v-if="searched && !searchResults?.media.length && !pending"
      title="No anime found"
      description="Try searching with different keywords or check your spelling."
      icon="i-heroicons-face-frown"
    />
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
