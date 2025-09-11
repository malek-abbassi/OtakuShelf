import { gql } from 'graphql-request';

export const SEARCH_ANIME = gql`
  query SearchAnime($search: String!, $page: Int = 1, $perPage: Int = 20) {
    Page(page: $page, perPage: $perPage) {
      pageInfo {
        total
        currentPage
        lastPage
        hasNextPage
      }
      media(search: $search, type: ANIME) {
        id
        title {
          romaji
          english
          native
        }
        description
        coverImage {
          large
          medium
          color
        }
        bannerImage
        format
        status
        episodes
        duration
        startDate {
          year
          month
          day
        }
        endDate {
          year
          month
          day
        }
        season
        seasonYear
        averageScore
        popularity
        genres
        studios {
          nodes {
            name
          }
        }
        nextAiringEpisode {
          airingAt
          episode
        }
        isAdult
      }
    }
  }
`;

export const GET_ANIME_DETAILS = gql`
  query GetAnimeDetails($id: Int!) {
    Media(id: $id, type: ANIME) {
      id
      title {
        romaji
        english
        native
      }
      description
      coverImage {
        extraLarge
        large
        medium
        color
      }
      bannerImage
      format
      status
      episodes
      duration
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      season
      seasonYear
      averageScore
      meanScore
      popularity
      favourites
      genres
      tags {
        name
        description
        rank
      }
      studios {
        nodes {
          name
          isMain
        }
      }
      source
      relations {
        nodes {
          id
          title {
            romaji
            english
          }
          type
          format
        }
      }
      nextAiringEpisode {
        airingAt
        episode
        timeUntilAiring
      }
      trailer {
        id
        site
        thumbnail
      }
      isAdult
      externalLinks {
        site
        url
      }
    }
  }
`;
