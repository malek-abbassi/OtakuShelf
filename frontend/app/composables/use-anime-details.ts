import type { Anime } from './use-ani-list';

import { useAniList } from './use-ani-list';

/**
 * Composable for managing anime details state and functionality
 * Simplified for use with UModal's v-model:open
 */
export function useAnimeDetails() {
  const { getAnimeDetails } = useAniList();

  const selectedAnime = ref<Anime | null>(null);
  const selectedAnimeDetails = ref<Anime | null>(null);
  const error = ref<Error | null>(null);
  const isModalOpen = ref(false);
  const isLoading = ref(false);

  /**
   * Show anime details in modal
   */
  async function showAnimeDetails(anime: Anime) {
    if (!anime) {
      console.error('No anime provided to showAnimeDetails');
      return;
    }

    selectedAnime.value = anime;
    selectedAnimeDetails.value = null;
    error.value = null;
    isModalOpen.value = true;
    isLoading.value = true;

    try {
      selectedAnimeDetails.value = await getAnimeDetails(anime.id);
    }
    catch (err) {
      console.error('Error loading anime details for ID', anime.id, ':', err);
      error.value = err as Error;
      // Fallback to basic info if detailed fetch fails
      selectedAnimeDetails.value = anime;
    }
    finally {
      isLoading.value = false;
    }
  }

  /**
   * Retry loading anime details
   */
  async function retryLoadDetails() {
    if (!selectedAnime.value)
      return;
    await showAnimeDetails(selectedAnime.value);
  }

  // Watch for modal close to clear data
  watch(isModalOpen, (isOpen) => {
    if (!isOpen && !isLoading.value) {
      nextTick(() => {
        selectedAnime.value = null;
        selectedAnimeDetails.value = null;
        error.value = null;
      });
    }
  });

  return {
    // State
    selectedAnime: readonly(selectedAnime),
    selectedAnimeDetails: computed(() => selectedAnimeDetails.value),
    error: readonly(error),
    isModalOpen,
    isLoading: readonly(isLoading),

    // Actions
    showAnimeDetails,
    retryLoadDetails,
  };
}
