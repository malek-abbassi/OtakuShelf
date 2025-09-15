<script setup lang="ts">
type AnimeSearchResult = {
  id: number;
  title: string;
  coverImage?: string;
  averageScore?: number;
  status?: string;
  format?: string;
  episodes?: number;
  startDate?: {
    year?: number;
    month?: number;
    day?: number;
  };
  genres?: string[];
  description?: string;
};

type Props = {
  placeholder?: string;
  debounceMs?: number;
  minSearchLength?: number;
  showFilters?: boolean;
  variant?: 'default' | 'compact';
  autoFocus?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Search for anime...',
  debounceMs: 300,
  minSearchLength: 2,
  showFilters: false,
  variant: 'default',
  autoFocus: false,
});

const emit = defineEmits<{
  select: [anime: AnimeSearchResult];
  search: [query: string];
}>();

// Composables
const { searchAnime } = useAniList();

// State
const searchQuery = ref('');
const isDropdownOpen = ref(false);
const searchInput = ref<HTMLInputElement>();
const searchResults = ref<AnimeSearchResult[]>([]);
const isSearching = ref(false);
const searchError = ref('');

// Filters (when enabled)
const selectedGenres = ref<string[]>([]);
const selectedFormat = ref<{ label: string; value: string }>({ label: 'Any Format', value: '' });
const selectedStatus = ref<{ label: string; value: string }>({ label: 'Any Status', value: '' });

// Available filter options
const formatOptions = [
  { label: 'Any Format', value: '' },
  { label: 'TV', value: 'TV' },
  { label: 'Movie', value: 'MOVIE' },
  { label: 'OVA', value: 'OVA' },
  { label: 'ONA', value: 'ONA' },
  { label: 'Special', value: 'SPECIAL' },
];

const statusOptions = [
  { label: 'Any Status', value: '' },
  { label: 'Releasing', value: 'RELEASING' },
  { label: 'Finished', value: 'FINISHED' },
  { label: 'Not Yet Released', value: 'NOT_YET_RELEASED' },
  { label: 'Cancelled', value: 'CANCELLED' },
];

const popularGenres = [
  'Action',
  'Adventure',
  'Comedy',
  'Drama',
  'Fantasy',
  'Romance',
  'Sci-Fi',
  'Slice of Life',
  'Sports',
  'Supernatural',
];

// Debounced search
let searchTimeout: NodeJS.Timeout | null = null;

async function performSearch(query: string) {
  if (query.length >= props.minSearchLength) {
    isSearching.value = true;
    searchError.value = '';
    emit('search', query);

    try {
      const result = await searchAnime(query);

      // Transform API results to match our component interface
      searchResults.value = result.media.map(anime => ({
        id: anime.id,
        title: anime.title.romaji || anime.title.english || anime.title.native || 'Unknown Title',
        coverImage: anime.coverImage?.large,
        averageScore: anime.averageScore ?? undefined,
        status: anime.status ?? undefined,
        format: anime.format ?? undefined,
        episodes: anime.episodes ?? undefined,
        startDate: {
          year: anime.startDate.year ?? undefined,
          month: anime.startDate.month ?? undefined,
          day: anime.startDate.day ?? undefined,
        },
        genres: anime.genres,
        description: anime.description ?? undefined,
      }));

      isDropdownOpen.value = true;
    }
    catch (error: any) {
      console.error('Search error:', error);
      searchError.value = error.message || 'Search failed';
      searchResults.value = [];
    }
    finally {
      isSearching.value = false;
    }
  }
  else {
    isDropdownOpen.value = false;
    searchResults.value = [];
  }
}

function debouncedSearch(query: string) {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  searchTimeout = setTimeout(() => {
    performSearch(query);
  }, props.debounceMs);
}

// Watchers
watch(searchQuery, (newQuery) => {
  debouncedSearch(newQuery);
});

// Auto-focus input
onMounted(() => {
  if (props.autoFocus && searchInput.value) {
    searchInput.value.focus();
  }
});

// Methods
function handleSelect(anime: AnimeSearchResult) {
  emit('select', anime);
  isDropdownOpen.value = false;
  searchQuery.value = anime.title;
}

function clearSearch() {
  searchQuery.value = '';
  isDropdownOpen.value = false;
}

function handleInputFocus() {
  if (searchResults.value.length > 0 && searchQuery.value.length >= props.minSearchLength) {
    isDropdownOpen.value = true;
  }
}

function handleInputBlur() {
  // Delay closing to allow for clicks on dropdown items
  setTimeout(() => {
    isDropdownOpen.value = false;
  }, 200);
}

function applyFilters() {
  if (searchQuery.value.length >= props.minSearchLength) {
    debouncedSearch(searchQuery.value);
  }
}

function clearFilters() {
  selectedGenres.value = [];
  selectedFormat.value = { label: 'Any Format', value: '' };
  selectedStatus.value = { label: 'Any Status', value: '' };
  if (searchQuery.value.length >= props.minSearchLength) {
    debouncedSearch(searchQuery.value);
  }
}
</script>

<template>
  <div class="relative w-full">
    <!-- Search Input -->
    <div class="relative">
      <UInput
        ref="searchInput"
        v-model="searchQuery"
        :placeholder="placeholder"
        icon="i-heroicons-magnifying-glass"
        size="lg"
        :loading="isSearching"
        @focus="handleInputFocus"
        @blur="handleInputBlur"
      >
        <template #trailing>
          <UButton
            v-if="searchQuery"
            variant="ghost"
            color="neutral"
            size="xs"
            icon="i-heroicons-x-mark"
            @click="clearSearch"
          />
        </template>
      </UInput>
    </div>

    <!-- Filters (when enabled) -->
    <div
      v-if="showFilters"
      class="mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg space-y-4"
    >
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-medium text-gray-900 dark:text-white">
          Filters
        </h4>
        <UButton
          variant="ghost"
          size="xs"
          @click="clearFilters"
        >
          Clear All
        </UButton>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Format Filter -->
        <USelectMenu
          v-model="selectedFormat"
          :items="formatOptions"
          placeholder="Select format"
          @change="applyFilters"
        />

        <!-- Status Filter -->
        <USelectMenu
          v-model="selectedStatus"
          :items="statusOptions"
          placeholder="Select status"
          @change="applyFilters"
        />
      </div>

      <!-- Genre Filter -->
      <div>
        <label class="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2 block">
          Genres
        </label>
        <div class="flex flex-wrap gap-2">
          <UButton
            v-for="genre in popularGenres"
            :key="genre"
            :variant="selectedGenres.includes(genre) ? 'solid' : 'outline'"
            :color="selectedGenres.includes(genre) ? 'primary' : 'neutral'"
            size="xs"
            @click="() => {
              const index = selectedGenres.indexOf(genre)
              if (index > -1) {
                selectedGenres.splice(index, 1)
              }
              else {
                selectedGenres.push(genre)
              }
              applyFilters()
            }"
          >
            {{ genre }}
          </UButton>
        </div>
      </div>
    </div>

    <!-- Search Results Dropdown -->
    <div
      v-if="isDropdownOpen"
      class="absolute top-full left-0 right-0 z-50 mt-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg max-h-96 overflow-y-auto"
    >
      <!-- Loading State -->
      <div
        v-if="isSearching"
        class="p-4"
      >
        <UiLoadingState
          variant="skeleton"
          size="sm"
        />
      </div>

      <!-- Error State -->
      <div
        v-else-if="searchError"
        class="p-4"
      >
        <UiErrorState
          :message="searchError"
          variant="warning"
          :show-retry="false"
        />
      </div>

      <!-- No Results -->
      <div
        v-else-if="searchResults.length === 0 && searchQuery.length >= minSearchLength"
        class="p-4"
      >
        <UiEmptyState
          title="No anime found"
          :description="`No results for &quot;${searchQuery}&quot;`"
          icon="i-heroicons-face-frown"
          :show-action="false"
        />
      </div>

      <!-- Results List -->
      <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
        <button
          v-for="anime in searchResults"
          :key="anime.id"
          class="w-full p-4 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors focus:outline-none focus:bg-gray-50 dark:focus:bg-gray-700"
          @click="handleSelect(anime)"
        >
          <UiAnimeCard
            :anime="anime"
            variant="compact"
            :show-watchlist-button="false"
          />
        </button>
      </div>

      <!-- Show more results hint -->
      <div
        v-if="searchResults.length > 0"
        class="p-3 bg-gray-50 dark:bg-gray-800 text-center border-t border-gray-200 dark:border-gray-700"
      >
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Showing {{ searchResults.length }} results
        </p>
      </div>
    </div>
  </div>
</template>
