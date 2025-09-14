import { beforeEach, describe, expect, it, vi } from 'vitest';

describe('useWatchlist composable', () => {
  let useWatchlist: any;

  beforeEach(async () => {
    // Reset modules before each test
    vi.resetModules();

    // Import the composable after mocking
    const { useWatchlist: importedUseWatchlist } = await import('../../app/composables/use-watchlist');
    useWatchlist = importedUseWatchlist;
  });

  it('should initialize watchlist state correctly', () => {
    const watchlist = useWatchlist();

    expect(watchlist.watchlistItems).toBeDefined();
    expect(watchlist.statusCounts).toBeDefined();
    expect(watchlist.totalCount).toBeDefined();
    expect(watchlist.isLoading).toBeDefined();
    expect(watchlist.isAddingItem).toBeDefined();
  });

  it('should fetch watchlist successfully', async () => {
    const mockResponse = {
      items: [
        {
          id: 1,
          anime_id: 123,
          anime_title: 'Test Anime',
          anime_picture_url: 'https://example.com/image.jpg',
          anime_score: 8.5,
          status: 'watching',
          notes: 'Great anime!',
          user_id: 1,
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
        },
      ],
      total_count: 1,
      status_counts: {
        watching: 1,
        completed: 0,
        plan_to_watch: 0,
        dropped: 0,
        on_hold: 0,
      },
    };

    globalThis.$fetch = vi.fn().mockResolvedValue(mockResponse);

    const watchlist = useWatchlist();
    const result = await watchlist.fetchWatchlist();

    expect(result).toEqual(mockResponse);
    expect(watchlist.watchlistItems.value).toEqual(mockResponse.items);
    expect(watchlist.totalCount.value).toBe(1);
    expect(watchlist.statusCounts.value).toEqual(mockResponse.status_counts);
  });

  it('should handle failed watchlist fetch', async () => {
    globalThis.$fetch = vi.fn().mockRejectedValue(new Error('Network error'));

    const watchlist = useWatchlist();

    await expect(watchlist.fetchWatchlist()).rejects.toThrow('Network error');
  });

  it('should add anime to watchlist successfully', async () => {
    const mockResponse = {
      id: 1,
      anime_id: 123,
      anime_title: 'Test Anime',
      anime_picture_url: 'https://example.com/image.jpg',
      anime_score: 8.5,
      status: 'watching',
      notes: 'Great anime!',
      user_id: 1,
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z',
    };

    globalThis.$fetch = vi.fn().mockResolvedValue(mockResponse);

    const watchlist = useWatchlist();
    const initialCount = watchlist.watchlistItems.value.length;

    const result = await watchlist.addToWatchlist({
      animeId: 123,
      animeTitle: 'Test Anime',
      animePictureUrl: 'https://example.com/image.jpg',
      animeScore: 8.5,
      status: 'watching',
      notes: 'Great anime!',
    });

    expect(result.success).toBe(true);
    expect(result.item).toEqual(mockResponse);
    expect(watchlist.watchlistItems.value.length).toBe(initialCount + 1);
    expect(watchlist.watchlistItems.value[0]).toEqual(mockResponse);
  });

  it('should handle failed add to watchlist', async () => {
    globalThis.$fetch = vi.fn().mockRejectedValue(new Error('Anime already in watchlist'));

    const watchlist = useWatchlist();
    const result = await watchlist.addToWatchlist({
      animeId: 123,
      animeTitle: 'Test Anime',
      status: 'watching',
    });

    expect(result.success).toBe(false);
    expect(result.message).toBe('Anime already in watchlist');
  });

  it('should update watchlist item successfully', async () => {
    const mockResponse = {
      id: 1,
      anime_id: 123,
      anime_title: 'Updated Anime Title',
      anime_picture_url: 'https://example.com/image.jpg',
      anime_score: 9.0,
      status: 'completed',
      notes: 'Updated notes',
      user_id: 1,
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-02T00:00:00Z',
    };

    globalThis.$fetch = vi.fn().mockResolvedValue(mockResponse);

    const watchlist = useWatchlist();
    const result = await watchlist.updateWatchlistItem(1, {
      animeTitle: 'Updated Anime Title',
      animeScore: 9.0,
      status: 'completed',
      notes: 'Updated notes',
    });

    expect(result.success).toBe(true);
    expect(result.item).toEqual(mockResponse);
  });

  it('should remove from watchlist successfully', async () => {
    globalThis.$fetch = vi.fn().mockResolvedValue({
      message: 'Watchlist item deleted successfully',
    });

    // Setup initial state with an item
    const watchlist = useWatchlist();
    watchlist.watchlistItems.value = [
      {
        id: 1,
        anime_id: 123,
        anime_title: 'Test Anime',
        status: 'watching',
        user_id: 1,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
      },
    ];

    const result = await watchlist.removeFromWatchlist(1);

    expect(result.success).toBe(true);
    expect(watchlist.watchlistItems.value).toHaveLength(0);
  });

  it('should handle watchlist filtering by status', async () => {
    const mockResponse = {
      items: [
        {
          id: 1,
          anime_id: 123,
          anime_title: 'Completed Anime',
          status: 'completed',
          user_id: 1,
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
        },
      ],
      total_count: 1,
      status_counts: {
        completed: 1,
      },
    };

    globalThis.$fetch = vi.fn().mockResolvedValue(mockResponse);

    const watchlist = useWatchlist();
    await watchlist.fetchWatchlist({ statusFilter: 'completed' });

    expect(globalThis.$fetch).toHaveBeenCalledWith(
      expect.stringContaining('status_filter=completed'),
      expect.any(Object),
    );
  });

  it('should handle pagination', async () => {
    const mockResponse = {
      items: [],
      total_count: 50,
      status_counts: {},
    };

    globalThis.$fetch = vi.fn().mockResolvedValue(mockResponse);

    const watchlist = useWatchlist();
    await watchlist.fetchWatchlist({ skip: 20, limit: 10 });

    expect(globalThis.$fetch).toHaveBeenCalledWith(
      expect.stringContaining('skip=20&limit=10'),
      expect.any(Object),
    );
  });
});
