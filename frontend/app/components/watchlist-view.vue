<script lang="ts" setup>
import type { WatchlistItem } from '~/types/watchlist';

// Component imports
import EditWatchlistModal from '~/components/edit-watchlist-modal.vue';
import WatchlistCard from '~/components/watchlist-card.vue';
import { useErrorHandler } from '~/composables/use-error-handler';
import { useWatchlist } from '~/composables/use-watchlist';
import { WATCH_STATUS_OPTIONS } from '~/types/watchlist';

// Composables
const { isLoggedIn } = useAuth();
const { showErrorToast } = useErrorHandler();
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

// Computed properties with performance optimizations
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
  console.warn('watchlist-view: handleStatusChange called:', { itemId: item.id, currentStatus: item.status, newStatus });

  try {
    console.warn('Calling updateWatchlistItem...');
    const result = await updateWatchlistItem(item.id, { status: newStatus });
    console.warn('updateWatchlistItem result:', result);

    console.warn('Refreshing watchlist...');
    await fetchWatchlist(); // Refresh to get updated counts
    console.warn('Watchlist refreshed successfully');
  }
  catch (err: any) {
    console.error('Error updating status:', err);
    console.error('Error details:', {
      message: err?.message,
      data: err?.data,
      statusCode: err?.statusCode,
      response: err?.response,
    });
    showErrorToast(err, 'Update Watchlist Status');
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
      showErrorToast(err, 'Remove from Watchlist');
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
  <div class="space-y-6" data-testid="watchlist-view">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4" data-testid="watchlist-header">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
          My Watchlist
        </h1>
        <p class="text-gray-600 dark:text-gray-300 text-sm sm:text-base">
          Manage your anime collection and track your progress
        </p>
      </div>

      <div class="flex items-center gap-2 self-start sm:self-auto" data-testid="watchlist-controls">
        <!-- View Mode Toggle -->
        <UButtonGroup data-testid="view-mode-toggle">
          <UButton
            :variant="viewMode === 'grid' ? 'solid' : 'outline'" icon="i-heroicons-squares-2x2"
            data-testid="grid-view-button"
            @click="viewMode = 'grid'"
          />
          <UButton
            :variant="viewMode === 'list' ? 'solid' : 'outline'" icon="i-heroicons-list-bullet"
            data-testid="list-view-button"
            @click="viewMode = 'list'"
          />
        </UButtonGroup>
      </div>
    </div>

    <!-- Status Filters -->
    <div class="flex flex-wrap gap-2 overflow-x-auto pb-2" data-testid="status-filters">
      <UButton
        v-for="option in statusOptions" :key="option.value"
        :variant="selectedStatus === option.value ? 'solid' : 'outline'" size="sm"
        :data-testid="`status-filter-${option.value}`"
        @click="handleStatusFilter(option.value)"
      >
        {{ option.label }}
        <UBadge
          v-if="option.count > 0" :color="selectedStatus === option.value ? 'neutral' : 'neutral'"
          variant="subtle" size="xs" class="ml-1"
        >
          {{ option.count }}
        </UBadge>
      </UButton>
    </div>

    <!-- Search -->
    <div class="max-w-md" data-testid="watchlist-search">
      <UInput
        v-model="searchQuery" placeholder="Search your watchlist..." icon="i-heroicons-magnifying-glass"
        size="lg"
        data-testid="watchlist-search-input"
      />
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && mounted" class="flex items-center justify-center py-12" data-testid="watchlist-loading">
      <LoadingState size="lg" text="Loading your watchlist..." />
    </div>

    <!-- Initialization State -->
    <div v-else-if="!mounted" class="flex items-center justify-center py-12" data-testid="watchlist-initializing">
      <LoadingState size="lg" text="Initializing..." />
    </div>

    <!-- Error State -->
    <UAlert v-else-if="error" color="error" variant="soft" :description="error" data-testid="watchlist-error">
      <template #actions>
        <UButton color="primary" data-testid="watchlist-retry-button" @click="() => fetchWatchlist()">
          Try Again
        </UButton>
      </template>
    </UAlert>

    <!-- Empty State -->
    <div v-else-if="!hasItems && !isLoading" class="text-center py-12" data-testid="watchlist-empty">
      <div class="mx-auto w-24 h-24 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
        <UIcon name="i-heroicons-film" class="w-12 h-12 text-gray-400" />
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
      <UButton v-if="!searchQuery" to="/anime" icon="i-heroicons-plus" data-testid="browse-anime-button">
        Browse Anime
      </UButton>
    </div>

    <!-- Watchlist Items -->
    <div v-else-if="hasItems" data-testid="watchlist-items">
      <!-- Grid View -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6" data-testid="watchlist-grid">
        <WatchlistCard
          v-for="item in filteredItems" :key="item.id" :item="item" @status-change="handleStatusChange"
          @edit="handleEdit" @remove="handleRemove"
        />
      </div>

      <!-- List View -->
      <div v-else class="space-y-4" data-testid="watchlist-list">
        <WatchlistCard
          v-for="item in filteredItems" :key="item.id" :item="item" @status-change="handleStatusChange"
          @edit="handleEdit" @remove="handleRemove"
        />
      </div>
    </div>

    <!-- Edit Modal -->
    <EditWatchlistModal v-model:open="showEditModal" :item="editingItem" data-testid="edit-watchlist-modal" @updated="handleEditUpdated" />
  </div>
</template>
