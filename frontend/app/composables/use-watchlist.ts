import type {
  WatchlistAddSchema,
  WatchlistItem,
  WatchlistResponse,
  WatchlistUpdateSchema,
} from '~/types/watchlist';

export function useWatchlist() {
  const toast = useToast();
  const config = useRuntimeConfig();
  const API_BASE_URL = ((config.public?.apiBaseUrl as string) || 'http://localhost:8000')
    .replace('127.0.0.1', 'localhost'); // Ensure consistent domain for cookies

  // Reactive filters for dynamic data fetching
  const statusFilter = ref<string | undefined>(undefined);
  const skip = ref<number>(0);
  const limit = ref<number>(50);

  // Use useAsyncData for automatic caching and SSR support
  const {
    data: watchlistData,
    status,
    refresh: refreshWatchlist,
  } = useAsyncData<WatchlistResponse>(
    'watchlist',
    () => {
      const params = new URLSearchParams();
      if (statusFilter.value)
        params.append('status_filter', statusFilter.value);
      if (skip.value !== undefined)
        params.append('skip', skip.value.toString());
      if (limit.value !== undefined)
        params.append('limit', limit.value.toString());

      return $fetch<WatchlistResponse>(
        `${API_BASE_URL}/api/v1/watchlist?${params.toString()}`,
        {
          credentials: 'include',
        },
      );
    },
    {
      // Watch these refs to automatically refetch when they change
      watch: [statusFilter, skip, limit],
      // Don't fetch on server if user isn't authenticated
      server: false,
      // Lazy load to prevent blocking navigation
      lazy: true,
      // Transform the response to ensure consistent property names
      transform: (data: WatchlistResponse) => ({
        items: data.items,
        status_counts: data.status_counts || data.statusCounts || {},
        total_count: data.total_count || data.totalCount || 0,
      }),
      // Default empty state
      default: () => ({
        items: [],
        status_counts: {},
        total_count: 0,
      }),
    },
  );

  // Computed properties for easier access
  const watchlistItems = computed(() => watchlistData.value?.items || []);
  const statusCounts = computed(() => watchlistData.value?.status_counts || {});
  const totalCount = computed(() => watchlistData.value?.total_count || 0);
  const isLoading = computed(() => status.value === 'pending');
  const isAddingItem = ref(false);

  // Fetch watchlist with filters (updates reactive refs)
  function fetchWatchlist(options: {
    statusFilter?: string;
    skip?: number;
    limit?: number;
  } = {}) {
    statusFilter.value = options.statusFilter;
    if (options.skip !== undefined)
      skip.value = options.skip;
    if (options.limit !== undefined)
      limit.value = options.limit;

    // The data will automatically refetch due to watchers
    return refreshWatchlist();
  }

  // Add anime to watchlist
  async function addToWatchlist(animeData: WatchlistAddSchema) {
    isAddingItem.value = true;
    try {
      const requestBody = {
        animeId: animeData.animeId,
        animeTitle: animeData.animeTitle,
        animePictureUrl: animeData.animePictureUrl,
        animeScore: animeData.animeScore,
        status: animeData.status,
        notes: animeData.notes,
      };

      const response = await $fetch<WatchlistItem>(
        `${API_BASE_URL}/api/v1/watchlist`,
        {
          method: 'POST',
          body: requestBody,
          credentials: 'include',
        },
      );

      // Refresh the watchlist to get updated data
      await refreshWatchlist();

      toast.add({
        title: 'Success',
        description: 'Anime added to watchlist',
        color: 'success',
      });

      return { success: true, item: response };
    }
    catch (error: any) {
      console.error('Failed to add to watchlist:', error);

      // Handle validation errors specifically
      let errorMessage = 'Failed to add anime to watchlist';
      if (error?.data?.detail) {
        if (Array.isArray(error.data.detail)) {
          // FastAPI validation errors are usually arrays
          errorMessage = error.data.detail.map((err: any) => err.msg || err).join(', ');
        }
        else {
          errorMessage = error.data.detail;
        }
      }
      else if (error?.message) {
        errorMessage = error.message;
      }

      toast.add({
        title: 'Error',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
    finally {
      isAddingItem.value = false;
    }
  }

  // Update watchlist item
  async function updateWatchlistItem(itemId: number, updateData: WatchlistUpdateSchema) {
    console.warn('updateWatchlistItem called:', { itemId, updateData, API_BASE_URL });

    try {
      const requestBody = {
        status: updateData.status,
        notes: updateData.notes,
        animeScore: updateData.animeScore,
      };

      console.warn('Making PUT request to:', `${API_BASE_URL}/api/v1/watchlist/${itemId}`);
      console.warn('Request body:', requestBody);

      const response = await $fetch<WatchlistItem>(
        `${API_BASE_URL}/api/v1/watchlist/${itemId}`,
        {
          method: 'PUT',
          body: requestBody,
          credentials: 'include',
        },
      );

      console.warn('PUT response received:', response);

      // Refresh the watchlist to get updated data
      await refreshWatchlist();

      toast.add({
        title: 'Success',
        description: 'Watchlist item updated',
        color: 'success',
      });

      return { success: true, item: response };
    }
    catch (error: any) {
      console.error('Failed to update watchlist item:', error);
      console.error('Error details:', {
        status: error?.status,
        statusCode: error?.statusCode,
        data: error?.data,
        message: error?.message,
        cause: error?.cause,
      });

      const errorMessage = error?.data?.detail || error.message || 'Failed to update item';
      toast.add({
        title: 'Error',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
  }

  // Remove from watchlist
  async function removeFromWatchlist(itemId: number) {
    try {
      await $fetch(`${API_BASE_URL}/api/v1/watchlist/${itemId}`, {
        method: 'DELETE',
        credentials: 'include',
      });

      // Refresh the watchlist to get updated data
      await refreshWatchlist();

      toast.add({
        title: 'Success',
        description: 'Anime removed from watchlist',
        color: 'success',
      });

      return { success: true };
    }
    catch (error: any) {
      console.error('Failed to remove from watchlist:', error);
      const errorMessage = error?.data?.detail || error.message || 'Failed to remove anime';
      toast.add({
        title: 'Error',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
  }

  // Check if anime is in watchlist
  async function checkAnimeInWatchlist(animeId: number): Promise<WatchlistItem | null> {
    try {
      const response = await $fetch<WatchlistItem | null>(
        `${API_BASE_URL}/api/v1/watchlist/anime/${animeId}`,
        {
          credentials: 'include',
        },
      );
      return response;
    }
    catch (error) {
      console.error('Failed to check anime in watchlist:', error);
      return null;
    }
  }

  // Bulk update status
  async function bulkUpdateStatus(itemIds: number[], newStatus: string) {
    try {
      await $fetch(`${API_BASE_URL}/api/v1/watchlist/bulk`, {
        method: 'POST',
        body: {
          item_ids: itemIds,
          new_status: newStatus,
        },
        credentials: 'include',
      });

      // Refresh the watchlist to get updated data
      await refreshWatchlist();

      toast.add({
        title: 'Success',
        description: `Updated ${itemIds.length} items`,
        color: 'success',
      });

      return { success: true };
    }
    catch (error: any) {
      console.error('Failed to bulk update status:', error);
      const errorMessage = error?.data?.detail || error.message || 'Failed to update items';
      toast.add({
        title: 'Error',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
  }

  // Get watchlist item by ID
  function getWatchlistItem(itemId: number): WatchlistItem | undefined {
    return watchlistItems.value.find(item => item.id === itemId);
  }

  // Filter watchlist by status
  const getItemsByStatus = computed(() => {
    return (status: string) => watchlistItems.value.filter(item => item.status === status);
  });

  // Clear watchlist state (triggers refetch with empty filters)
  function clearWatchlist() {
    statusFilter.value = undefined;
    skip.value = 0;
    limit.value = 50;
    return refreshWatchlist();
  }

  return {
    // State
    watchlistItems: readonly(watchlistItems),
    statusCounts: readonly(statusCounts),
    totalCount: readonly(totalCount),
    isLoading: readonly(isLoading),
    isAddingItem: readonly(isAddingItem),

    // Computed
    getItemsByStatus,

    // Methods
    fetchWatchlist,
    addToWatchlist,
    updateWatchlistItem,
    removeFromWatchlist,
    checkAnimeInWatchlist,
    bulkUpdateStatus,
    getWatchlistItem,
    clearWatchlist,
  };
}
