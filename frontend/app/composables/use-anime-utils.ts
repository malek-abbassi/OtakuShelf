import type { Anime } from './use-ani-list';

/**
 * Utility composable for anime data formatting and transformation
 * Extracts common formatting logic to be reusable across components
 */
export function useAnimeUtils() {
  /**
   * Get the best available title for an anime
   */
  function getAnimeTitle(title: Anime['title']): string {
    if (!title)
      return 'Unknown Title';
    return title.english || title.romaji || title.native || 'Unknown Title';
  }

  /**
   * Format anime status with proper display names
   */
  function formatStatus(status: string | null): string {
    if (!status)
      return 'Unknown';

    const statusMap: Record<string, string> = {
      FINISHED: 'Finished',
      RELEASING: 'Airing',
      NOT_YET_RELEASED: 'Upcoming',
      CANCELLED: 'Cancelled',
      HIATUS: 'Hiatus',
    };

    return statusMap[status] || status;
  }

  /**
   * Get appropriate color for status badges
   */
  function getStatusColor(status: string | null): 'error' | 'primary' | 'secondary' | 'success' | 'info' | 'warning' | 'neutral' {
    if (!status)
      return 'neutral';

    const colorMap: Record<string, 'error' | 'primary' | 'secondary' | 'success' | 'info' | 'warning' | 'neutral'> = {
      FINISHED: 'success',
      RELEASING: 'primary',
      NOT_YET_RELEASED: 'warning',
      CANCELLED: 'error',
      HIATUS: 'info',
    };

    return colorMap[status] || 'neutral';
  }

  /**
   * Format air dates with proper display
   */
  function getAirDate(anime: Anime): string {
    if (!anime?.startDate?.year)
      return 'Unknown';

    const { startDate, endDate, status } = anime;

    const formatDate = (date: { year: number | null; month: number | null; day: number | null }) => {
      if (!date.year)
        return '';
      if (!date.month)
        return date.year.toString();

      const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      const monthName = monthNames[date.month - 1] || date.month;

      if (!date.day)
        return `${monthName} ${date.year}`;
      return `${monthName} ${date.day}, ${date.year}`;
    };

    const start = formatDate(startDate);

    if (status === 'FINISHED' && endDate?.year && endDate.year !== startDate.year) {
      const end = formatDate(endDate);
      return `${start} - ${end}`;
    }

    return start;
  }

  /**
   * Format source material with proper display names
   */
  function formatSource(source: string): string {
    const sourceMap: Record<string, string> = {
      ORIGINAL: 'Original',
      MANGA: 'Manga',
      LIGHT_NOVEL: 'Light Novel',
      VISUAL_NOVEL: 'Visual Novel',
      VIDEO_GAME: 'Video Game',
      OTHER: 'Other',
      NOVEL: 'Novel',
      DOUJINSHI: 'Doujinshi',
      ANIME: 'Anime',
      WEB_NOVEL: 'Web Novel',
      LIVE_ACTION: 'Live Action',
      GAME: 'Game',
      COMIC: 'Comic',
      MULTIMEDIA_PROJECT: 'Multimedia Project',
      PICTURE_BOOK: 'Picture Book',
    };

    return sourceMap[source] || source;
  }

  /**
   * Clean HTML description and format for display
   */
  function cleanDescription(description: string): string {
    if (!description)
      return '';

    return description
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]*>/g, '')
      .replace(/&quot;/g, '"')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .trim();
  }

  /**
   * Format score for display
   */
  function formatScore(score: number | null): string {
    if (!score)
      return 'N/A';
    return `${score}%`;
  }

  /**
   * Format episode count for display
   */
  function formatEpisodes(episodes: number | null): string {
    if (!episodes)
      return 'Unknown';
    return episodes === 1 ? '1 episode' : `${episodes} episodes`;
  }

  /**
   * Format duration for display
   */
  function formatDuration(duration: number | null): string {
    if (!duration)
      return 'Unknown';
    return `${duration} min`;
  }

  return {
    getAnimeTitle,
    formatStatus,
    getStatusColor,
    getAirDate,
    formatSource,
    cleanDescription,
    formatScore,
    formatEpisodes,
    formatDuration,
  };
}
