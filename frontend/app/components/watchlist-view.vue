<script lang="ts" setup>
import type { WatchlistItem } from '~/types/watchlist';

import { useWatchlist } from '~/composables/use-watchlist';
import { WATCH_STATUS_OPTIONS } from '~/types/watchlist';

// Composables
const { isLoggedIn } = useAuth();
const {
  watchlistItems,
  statusCounts,
  totalCount,
  isLoading,
  fetchWatchlist,
  updateWatchlistItem,
  removeFromWatchlist,
} = useWatchlist();

const error = ref<string | null>(null);

// Reactive state
const selectedStatus = ref<string>('all');
const searchQuery = ref('');
const viewMode = ref<'grid' | 'list'>('grid');
const editingItem = ref<WatchlistItem | null>(null);
const showEditModal = ref(false);

// Computed properties
const statusOptions = computed(() => [
  { value: 'all', label: 'All', count: totalCount.value || 0 },
  ...WATCH_STATUS_OPTIONS.map(option => ({
    ...option,
    count: statusCounts.value[option.value] || 0,
  })),
]);

const filteredItems = computed(() => {
  if (!watchlistItems.value)
    return [];

  let items = watchlistItems.value;

  // Filter by status
  if (selectedStatus.value !== 'all') {
    items = items.filter((item: WatchlistItem) => item.status === selectedStatus.value);
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    items = items.filter((item: WatchlistItem) => {
      const title = item.animeTitle || item.anime_title || '';
      return title.toLowerCase().includes(query)
        || (item.notes && item.notes.toLowerCase().includes(query));
    });
  }

  return items;
});

const hasItems = computed(() => filteredItems.value.length > 0);

// Client-side initialization for Nuxt 4
const mounted = ref(false);

onMounted(async () => {
  // Safety timeout to prevent infinite loading
  const timeoutId = setTimeout(() => {
    if (!mounted.value) {
      console.error('WatchlistView: Initialization timeout, forcing mount');
      mounted.value = true;
    }
  }, 5000);

  try {
    // Check auth status and fetch data
    const { checkAuth } = useAuth();
    await checkAuth();

    if (isLoggedIn.value) {
      await fetchWatchlist();
    }
    else {
      await navigateTo('/auth');
    }
  }
  catch (error) {
    console.error('WatchlistView: Error during initialization:', error);
  }
  finally {
    clearTimeout(timeoutId);
    mounted.value = true;
  }
});

// Methods
async function handleStatusChange(item: WatchlistItem, newStatus: string) {
  try {
    await updateWatchlistItem(item.id, { status: newStatus });
    await fetchWatchlist(); // Refresh to get updated counts
  }
  catch (err) {
    console.error('Error updating status:', err);
  }
}

async function handleEdit(item: WatchlistItem) {
  editingItem.value = item;
  showEditModal.value = true;
}

async function handleRemove(item: WatchlistItem) {
  // Simple confirmation without using browser confirm
  const shouldRemove = true; // TODO: Replace with modal confirmation
  if (shouldRemove) {
    try {
      await removeFromWatchlist(item.id);
      await fetchWatchlist(); // Refresh to get updated counts
    }
    catch (err) {
      console.error('Error removing item:', err);
    }
  }
}

function handleStatusFilter(status: string) {
  selectedStatus.value = status;
}

async function handleEditUpdated() {
  showEditModal.value = false;
  editingItem.value = null;
  await fetchWatchlist(); // Refresh to get updated data
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          My Watchlist
        </h1>
        <p class="text-gray-600 dark:text-gray-300">
          Manage your anime collection and track your progress
        </p>
      </div>

      <div class="flex items-center gap-2">
        <!-- View Mode Toggle -->
        <UButtonGroup>
          <UButton
            :variant="viewMode === 'grid' ? 'solid' : 'outline'"
            icon="i-heroicons-squares-2x2"
            @click="viewMode = 'grid'"
          />
          <UButton
            :variant="viewMode === 'list' ? 'solid' : 'outline'"
            icon="i-heroicons-list-bullet"
            @click="viewMode = 'list'"
          />
        </UButtonGroup>
      </div>
    </div>

    <!-- Status Filters -->
    <div class="flex flex-wrap gap-2">
      <UButton
        v-for="option in statusOptions"
        :key="option.value"
        :variant="selectedStatus === option.value ? 'solid' : 'outline'"
        size="sm"
        @click="handleStatusFilter(option.value)"
      >
        {{ option.label }}
        <UBadge
          v-if="option.count > 0"
          :color="selectedStatus === option.value ? 'neutral' : 'neutral'"
          variant="subtle"
          size="xs"
          class="ml-1"
        >
          {{ option.count }}
        </UBadge>
      </UButton>
    </div>

    <!-- Search -->
    <div class="max-w-md">
      <UInput
        v-model="searchQuery"
        placeholder="Search your watchlist..."
        icon="i-heroicons-magnifying-glass"
        size="lg"
      />
    </div>

    <!-- Loading State -->
    <LoadingState
      v-if="isLoading && mounted"
      message="Loading your watchlist..."
    />

    <!-- Initialization State -->
    <LoadingState
      v-else-if="!mounted"
      message="Initializing..."
    />

    <!-- Error State -->
    <ErrorState
      v-else-if="error"
      :message="error"
      @retry="fetchWatchlist"
    />

    <!-- Empty State -->
    <div
      v-else-if="!hasItems && !isLoading"
      class="text-center py-12"
    >
      <div class="mx-auto w-24 h-24 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
        <UIcon
          name="i-heroicons-film"
          class="w-12 h-12 text-gray-400"
        />
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
        {{ searchQuery ? 'No results found' : 'Your watchlist is empty' }}
      </h3>
      <p class="text-gray-600 dark:text-gray-300 mb-4">
        {{ searchQuery
          ? 'Try adjusting your search or filter criteria'
          : 'Start by adding some anime to track your viewing progress'
        }}
      </p>
      <UButton
        v-if="!searchQuery"
        to="/anime"
        icon="i-heroicons-plus"
      >
        Browse Anime
      </UButton>
    </div>

    <!-- Watchlist Items -->
    <div v-else-if="hasItems">
      <!-- Grid View -->
      <div
        v-if="viewMode === 'grid'"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <WatchlistCard
          v-for="item in filteredItems"
          :key="item.id"
          :item="item"
          @status-change="handleStatusChange"
          @edit="handleEdit"
          @remove="handleRemove"
        />
      </div>

      <!-- List View -->
      <div
        v-else
        class="space-y-4"
      >
        <WatchlistCard
          v-for="item in filteredItems"
          :key="item.id"
          :item="item"
          @status-change="handleStatusChange"
          @edit="handleEdit"
          @remove="handleRemove"
        />
      </div>
    </div>

    <!-- Edit Modal -->
    <EditWatchlistModal
      v-model:open="showEditModal"
      :item="editingItem"
      @updated="handleEditUpdated"
    />
  </div>
</template>
