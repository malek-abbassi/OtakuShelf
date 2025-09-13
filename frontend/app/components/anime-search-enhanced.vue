<script setup lang="ts">
import type { Anime, SearchResult } from '~/composables/use-ani-list';
import type { WatchlistAddSchema } from '~/types/watchlist';

import { useAniList } from '~/composables/use-ani-list';
import { useWatchlist } from '~/composables/use-watchlist';
import { WATCH_STATUS_OPTIONS } from '~/types/watchlist';

type Props = {
  initialQuery?: string;
  showWatchlistActions?: boolean;
};

type Emits = {
  selectAnime: [anime: Anime];
  addedToWatchlist: [anime: Anime];
};

const props = withDefaults(defineProps<Props>(), {
  initialQuery: '',
  showWatchlistActions: true,
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

// Add anime to watchlist
async function handleAddToWatchlist(anime: Anime, status: string = 'plan_to_watch') {
  if (!isLoggedIn.value) {
    navigateTo('/auth');
    return;
  }

  addingToWatchlist.value.add(anime.id);

  try {
    const animeData: WatchlistAddSchema = {
      animeId: anime.id,
      animeTitle: anime.title.romaji || anime.title.english || anime.title.native || 'Unknown Title',
      animePictureUrl: anime.coverImage.large || anime.coverImage.medium,
      animeScore: anime.averageScore || anime.meanScore || undefined,
      status,
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

function getWatchlistStatus(animeId: number): string | null {
  const item = watchlistItems.value.get(animeId);
  return item?.status || null;
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
        <UCard
          v-for="anime in searchResults.media"
          :key="anime.id"
          class="hover:shadow-lg transition-shadow duration-200 cursor-pointer"
          @click="selectAnime(anime)"
        >
          <div class="space-y-3">
            <!-- Cover Image -->
            <div class="relative aspect-[3/4] overflow-hidden rounded-lg">
              <NuxtImg
                :src="anime.coverImage.large || anime.coverImage.medium"
                :alt="anime.title.romaji || anime.title.english || 'Anime cover'"
                class="w-full h-full object-cover"
                loading="lazy"
              />

              <!-- Watchlist Status Badge -->
              <div
                v-if="isInWatchlist(anime.id)"
                class="absolute top-2 right-2"
              >
                <UBadge
                  :color="WATCH_STATUS_OPTIONS.find(opt => opt.value === getWatchlistStatus(anime.id))?.color || 'neutral'"
                  variant="solid"
                  size="sm"
                >
                  {{ WATCH_STATUS_OPTIONS.find(opt => opt.value === getWatchlistStatus(anime.id))?.label || 'In List' }}
                </UBadge>
              </div>
            </div>

            <!-- Title -->
            <div>
              <h4 class="font-medium text-sm line-clamp-2 min-h-[2.5rem]">
                {{ anime.title.romaji || anime.title.english || anime.title.native }}
              </h4>
            </div>

            <!-- Score and Year -->
            <div class="flex items-center justify-between text-xs text-gray-600 dark:text-gray-300">
              <div class="flex items-center gap-1">
                <UIcon name="i-heroicons-star" class="w-3 h-3" />
                <span>{{ anime.averageScore || anime.meanScore || 'N/A' }}</span>
              </div>
              <span>{{ anime.seasonYear || 'Unknown' }}</span>
            </div>

            <!-- Genres -->
            <div class="flex flex-wrap gap-1">
              <UBadge
                v-for="genre in anime.genres.slice(0, 2)"
                :key="genre"
                variant="subtle"
                size="xs"
              >
                {{ genre }}
              </UBadge>
            </div>
          </div>

          <!-- Watchlist Actions -->
          <template v-if="showWatchlistActions && isLoggedIn" #footer>
            <div v-if="!isInWatchlist(anime.id)" class="flex gap-2">
              <UDropdown
                :items="[
                  WATCH_STATUS_OPTIONS.map(option => ({
                    label: option.label,
                    icon: 'i-heroicons-plus',
                    click: () => handleAddToWatchlist(anime, option.value),
                  })),
                ]"
              >
                <UButton
                  variant="outline"
                  size="sm"
                  :loading="isAdding(anime.id)"
                  :disabled="isAdding(anime.id)"
                  block
                >
                  <template v-if="isAdding(anime.id)">
                    Adding...
                  </template>
                  <template v-else>
                    <UIcon name="i-heroicons-plus" class="w-4 h-4 mr-1" />
                    Add to Watchlist
                  </template>
                </UButton>
              </UDropdown>
            </div>
            <div v-else class="text-center">
              <UBadge
                :color="WATCH_STATUS_OPTIONS.find(opt => opt.value === getWatchlistStatus(anime.id))?.color || 'neutral'"
                variant="subtle"
                size="sm"
              >
                <UIcon name="i-heroicons-check" class="w-3 h-3 mr-1" />
                In Watchlist
              </UBadge>
            </div>
          </template>

          <!-- Login prompt for non-authenticated users -->
          <template v-else-if="showWatchlistActions && !isLoggedIn" #footer>
            <UButton
              variant="outline"
              size="sm"
              block
              @click.stop="navigateTo('/auth')"
            >
              Login to Add
            </UButton>
          </template>
        </UCard>
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
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
