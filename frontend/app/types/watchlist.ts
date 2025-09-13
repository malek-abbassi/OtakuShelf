import { z } from 'zod';

// Watchlist item schemas
export const watchlistAddSchema = z.object({
  animeId: z.number().positive('Anime ID must be a positive number'),
  animeTitle: z.string().min(1, 'Anime title is required').max(200, 'Title too long'),
  animePictureUrl: z.string().url('Invalid image URL').optional(),
  animeScore: z.number().min(0).max(10).optional(),
  status: z.string().default('plan_to_watch'),
  notes: z.string().max(1000, 'Notes too long').optional(),
});

export const watchlistUpdateSchema = z.object({
  status: z.string().optional(),
  notes: z.string().max(1000, 'Notes too long').optional(),
  animeScore: z.number().min(0).max(10).optional(),
});

// Type definitions
export type WatchlistAddSchema = z.output<typeof watchlistAddSchema>;
export type WatchlistUpdateSchema = z.output<typeof watchlistUpdateSchema>;

// API response types
export type WatchlistItem = {
  id: number;
  animeId: number;
  animeTitle: string;
  animePictureUrl?: string;
  animeScore?: number;
  status: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
};

export type WatchlistResponse = {
  items: WatchlistItem[];
  totalCount: number;
  statusCounts: Record<string, number>;
};

export type AnimeSearchResult = {
  id: number;
  title: string;
  coverImage?: string;
  score?: number;
  genres: string[];
  status?: string;
};

// Watch status options
export const WATCH_STATUS_OPTIONS = [
  { value: 'plan_to_watch', label: 'Plan to Watch', color: 'info' },
  { value: 'watching', label: 'Watching', color: 'success' },
  { value: 'completed', label: 'Completed', color: 'primary' },
  { value: 'on_hold', label: 'On Hold', color: 'warning' },
  { value: 'dropped', label: 'Dropped', color: 'error' },
] as const;

export type WatchStatus = typeof WATCH_STATUS_OPTIONS[number]['value'];

// Utility function to get status info
export function getStatusInfo(status: string) {
  return WATCH_STATUS_OPTIONS.find(option => option.value === status)
    || { value: status, label: status, color: 'neutral' as const };
}
