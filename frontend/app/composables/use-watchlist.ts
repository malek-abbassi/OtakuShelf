import type {
  WatchlistAddSchema,
  WatchlistItem,
  WatchlistResponse,
  WatchlistUpdateSchema,
} from '~/types/watchlist';

export function useWatchlist() {
  const watchlistItems = ref<WatchlistItem[]>([]);
  const statusCounts = ref<Record<string, number>>({});
  const totalCount = ref(0);
  const isLoading = ref(false);
  const isAddingItem = ref(false);

  const toast = useToast();

  const config = useRuntimeConfig();
  const API_BASE_URL = ((config.public?.apiBaseUrl as string) || 'http://localhost:8000')
    .replace('127.0.0.1', 'localhost'); // Ensure consistent domain for cookies

  // Fetch user's watchlist
  async function fetchWatchlist(options: {
    statusFilter?: string;
    skip?: number;
    limit?: number;
  } = {}) {
    isLoading.value = true;
    try {
      const params = new URLSearchParams();
      if (options.statusFilter)
        params.append('status_filter', options.statusFilter);
      if (options.skip !== undefined)
        params.append('skip', options.skip.toString());
      if (options.limit !== undefined)
        params.append('limit', options.limit.toString());

      const response = await $fetch<WatchlistResponse>(
        `${API_BASE_URL}/api/v1/watchlist?${params.toString()}`,
        {
          credentials: 'include',
        },
      );

      watchlistItems.value = response.items;
      statusCounts.value = response.status_counts || response.statusCounts || {};
      totalCount.value = response.total_count || response.totalCount || 0;

      return response;
    }
    catch (error: any) {
      console.error('Failed to fetch watchlist:', error);
      toast.add({
        title: 'Error',
        description: 'Failed to load watchlist',
        color: 'error',
      });
      throw error;
    }
    finally {
      isLoading.value = false;
    }
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

      // Add to local state
      watchlistItems.value.unshift(response);
      totalCount.value += 1;

      // Update status counts
      const status = response.status;
      statusCounts.value[status] = (statusCounts.value[status] || 0) + 1;

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
    try {
      const response = await $fetch<WatchlistItem>(
        `${API_BASE_URL}/api/v1/watchlist/${itemId}`,
        {
          method: 'PUT',
          body: {
            status: updateData.status,
            notes: updateData.notes,
            animeScore: updateData.animeScore,
          },
          credentials: 'include',
        },
      );

      // Update local state
      const index = watchlistItems.value.findIndex(item => item.id === itemId);
      if (index !== -1 && watchlistItems.value[index]) {
        const oldStatus = watchlistItems.value[index].status;
        watchlistItems.value[index] = response;

        // Update status counts if status changed
        if (oldStatus !== response.status) {
          statusCounts.value[oldStatus] = Math.max(0, (statusCounts.value[oldStatus] || 0) - 1);
          statusCounts.value[response.status] = (statusCounts.value[response.status] || 0) + 1;
        }
      }

      toast.add({
        title: 'Success',
        description: 'Watchlist item updated',
        color: 'success',
      });

      return { success: true, item: response };
    }
    catch (error: any) {
      console.error('Failed to update watchlist item:', error);
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

      // Remove from local state
      const index = watchlistItems.value.findIndex(item => item.id === itemId);
      if (index !== -1) {
        const item = watchlistItems.value[index];
        if (item) {
          watchlistItems.value.splice(index, 1);
          totalCount.value -= 1;

          // Update status counts
          const status = item.status;
          statusCounts.value[status] = Math.max(0, (statusCounts.value[status] || 0) - 1);
        }
      }

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

      // Update local state
      const updatedItems = watchlistItems.value.filter(item => itemIds.includes(item.id));
      const oldStatuses: Record<string, number> = {};

      updatedItems.forEach((item) => {
        const oldStatus = item.status;
        oldStatuses[oldStatus] = (oldStatuses[oldStatus] || 0) + 1;
        item.status = newStatus;
      });

      // Update status counts
      Object.entries(oldStatuses).forEach(([status, count]) => {
        statusCounts.value[status] = Math.max(0, (statusCounts.value[status] || 0) - count);
      });
      statusCounts.value[newStatus] = (statusCounts.value[newStatus] || 0) + itemIds.length;

      toast.add({
        title: 'Success',
        description: `Updated ${itemIds.length} items to ${newStatus}`,
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

  // Clear watchlist state
  function clearWatchlist() {
    watchlistItems.value = [];
    statusCounts.value = {};
    totalCount.value = 0;
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
