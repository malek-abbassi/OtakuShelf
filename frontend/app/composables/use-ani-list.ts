import { GraphQLClient } from 'graphql-request';

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
  const client = new GraphQLClient('https://graphql.anilist.co');

  const searchAnime = async (
    search: string,
    page: number = 1,
    perPage: number = 20,
  ): Promise<SearchResult> => {
    try {
      const data = await client.request(SEARCH_ANIME, {
        search,
        page,
        perPage,
      }) as { Page: SearchResult };
      return data.Page;
    }
    catch (error) {
      console.error('Error searching anime:', error);
      throw error;
    }
  };

  const getAnimeDetails = async (id: number): Promise<Anime> => {
    try {
      const data = await client.request(GET_ANIME_DETAILS, { id }) as { Media: Anime };
      return data.Media;
    }
    catch (error) {
      console.error('Error fetching anime details:', error);
      throw error;
    }
  };

  return {
    searchAnime,
    getAnimeDetails,
  };
}
