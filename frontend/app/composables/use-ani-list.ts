import type { Ref } from 'vue';

import { GET_ANIME_DETAILS, SEARCH_ANIME } from '../../queries/anime';

export type AnimeTitle = {
  romaji: string | null;
  english: string | null;
  native: string | null;
};

export type AnimeDate = {
  year: number | null;
  month: number | null;
  day: number | null;
};

export type AnimeStudio = {
  name: string;
  isMain?: boolean;
};

export type AnimeTag = {
  name: string;
  description: string | null;
  rank: number | null;
};

export type AnimeRelation = {
  id: number;
  title: AnimeTitle;
  type: string;
  format: string;
};

export type AnimeTrailer = {
  id: string;
  site: string;
  thumbnail: string;
};

export type AnimeExternalLink = {
  site: string;
  url: string;
};

export type NextAiringEpisode = {
  airingAt: number;
  episode: number;
  timeUntilAiring?: number;
};

export type Anime = {
  id: number;
  title: AnimeTitle;
  description: string | null;
  coverImage: {
    extraLarge?: string;
    large: string;
    medium: string;
    color: string | null;
  };
  bannerImage: string | null;
  format: string | null;
  status: string | null;
  episodes: number | null;
  duration: number | null;
  startDate: AnimeDate;
  endDate: AnimeDate;
  season: string | null;
  seasonYear: number | null;
  averageScore: number | null;
  meanScore?: number | null;
  popularity: number | null;
  favourites?: number | null;
  genres: string[];
  tags?: AnimeTag[];
  studios: {
    nodes: AnimeStudio[];
  };
  source?: string | null;
  relations?: {
    nodes: AnimeRelation[];
  };
  nextAiringEpisode: NextAiringEpisode | null;
  trailer?: AnimeTrailer | null;
  isAdult: boolean;
  externalLinks?: AnimeExternalLink[];
};

export type SearchResult = {
  pageInfo: {
    total: number;
    currentPage: number;
    lastPage: number;
    hasNextPage: boolean;
  };
  media: Anime[];
};

export function useAniList() {
  const _config = useRuntimeConfig();

  // Search anime with Nuxt's useFetch for better SSR and caching
  const searchAnime = async (
    search: string,
    page: number = 1,
    perPage: number = 20,
  ): Promise<SearchResult> => {
    try {
      const response = await $fetch<{
        data: { Page: SearchResult };
        errors?: any[];
      }>('https://graphql.anilist.co', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: {
          query: SEARCH_ANIME,
          variables: {
            search,
            page,
            perPage,
          },
        },
      });

      if (response.errors) {
        throw new Error(response.errors[0]?.message || 'Failed to search anime');
      }

      return response.data.Page;
    }
    catch (error) {
      console.error('Error searching anime:', error);
      throw error;
    }
  };

  // Get anime details with Nuxt's useFetch
  const getAnimeDetails = async (id: number): Promise<Anime> => {
    try {
      const response = await $fetch<{
        data: { Media: Anime };
        errors?: any[];
      }>('https://graphql.anilist.co', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: {
          query: GET_ANIME_DETAILS,
          variables: { id },
        },
      });

      if (response.errors) {
        throw new Error(response.errors[0]?.message || 'Failed to fetch anime details');
      }

      return response.data.Media;
    }
    catch (error) {
      console.error('Error fetching anime details:', error);
      throw error;
    }
  };

  // Get anime details with useFetch composable for reactive data
  const useAnimeDetails = (id: Ref<number | null>) => {
    const { data, error, pending, refresh } = useFetch<{
      data: { Media: Anime };
      errors?: any[];
    }>('https://graphql.anilist.co', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: computed(() => ({
        query: GET_ANIME_DETAILS,
        variables: { id: id.value },
      })),
      watch: [id],
      server: true,
      lazy: true,
      default: () => ({
        data: {
          Media: {} as Anime,
        },
        errors: undefined,
      }),
    });

    // Computed property to get the anime data with error handling
    const anime = computed(() => {
      if (data.value?.errors) {
        throw new Error(data.value.errors[0]?.message || 'Failed to fetch anime details');
      }
      return data.value?.data.Media;
    });

    return {
      data: anime,
      error,
      pending,
      refresh,
    };
  };

  return {
    searchAnime,
    getAnimeDetails,
    useAnimeDetails,
  };
}
