import type { Anime } from '~/composables/use-ani-list';

export function useAnimeSearchWithWatchlist() {
  // Reactive state for watchlist
  const watchlistItems = ref<Map<number, any>>(new Map());
  const addingToWatchlist = ref<Set<number>>(new Set());

  // Composables
  const { addToWatchlist, checkAnimeInWatchlist } = useWatchlist();
  const { isLoggedIn } = useAuth();

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
  async function handleAddToWatchlist(anime: Anime, status: string, emit: (event: 'addedToWatchlist', anime: Anime) => void) {
    if (!isLoggedIn.value) {
      await navigateTo('/auth');
      return;
    }

    addingToWatchlist.value.add(anime.id);

    try {
      const score = anime.averageScore || anime.meanScore;
      const imageUrl = anime.coverImage.large || anime.coverImage.medium;
      const animeData = {
        animeId: anime.id,
        animeTitle: anime.title.romaji || anime.title.english || anime.title.native || 'Unknown Title',
        animePictureUrl: imageUrl && imageUrl.startsWith('http') ? imageUrl : undefined,
        animeScore: score ? score / 10 : undefined,
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

  // Helper functions
  function isInWatchlist(animeId: number): boolean {
    return watchlistItems.value.has(animeId);
  }

  function isAdding(animeId: number): boolean {
    return addingToWatchlist.value.has(animeId);
  }

  return {
    watchlistItems: readonly(watchlistItems),
    addingToWatchlist: readonly(addingToWatchlist),
    checkWatchlistStatus,
    handleAddToWatchlist,
    isInWatchlist,
    isAdding,
  };
}
