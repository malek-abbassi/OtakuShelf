import { mount } from '@vue/test-utils';
import { beforeEach, describe, expect, it, vi } from 'vitest';

describe('animeCard Component', () => {
  let AnimeCard: any;

  beforeEach(async () => {
    // Reset modules before each test
    vi.resetModules();

    // Import the component after mocking
    AnimeCard = (await import('../../app/components/anime-card.vue')).default;
  });

  const mockAnime = {
    id: 1,
    title: { english: 'Test Anime', romaji: 'Test Anime' },
    coverImage: { large: 'https://example.com/image.jpg' },
    averageScore: 85,
    status: 'FINISHED',
    episodes: 12,
    genres: ['Action', 'Adventure', 'Comedy'],
  };

  const createWrapper = (props = {}) => {
    return mount(AnimeCard, {
      props: { anime: mockAnime, ...props },
      global: {
        stubs: {
          NuxtImg: {
            name: 'NuxtImg',
            template: '<img :src="src" :alt="alt" />',
            props: ['src', 'alt', 'loading', 'placeholder', 'class'],
          },
          UCard: {
            name: 'UCard',
            template: '<div class="u-card"><slot /></div>',
            props: ['class'],
          },
          UBadge: {
            name: 'UBadge',
            template: '<span class="u-badge"><slot /></span>',
            props: ['color', 'variant', 'size'],
          },
          UIcon: {
            name: 'UIcon',
            template: '<i class="u-icon"></i>',
            props: ['name', 'class'],
          },
        },
      },
    });
  };

  it('renders anime information correctly', () => {
    const wrapper = createWrapper();

    expect(wrapper.text()).toContain('Test Anime');
    expect(wrapper.text()).toContain('85');
    expect(wrapper.text()).toContain('12');
  });

  it('displays anime cover image', () => {
    const wrapper = createWrapper();

    const img = wrapper.find('img');
    expect(img.attributes('src')).toBe('https://example.com/image.jpg');
    expect(img.attributes('alt')).toContain('Test Anime');
  });

  it('handles missing title gracefully', () => {
    const animeWithoutEnglishTitle = {
      ...mockAnime,
      title: { romaji: 'Test Anime Romaji' },
    };

    const wrapper = createWrapper({ anime: animeWithoutEnglishTitle });

    expect(wrapper.text()).toContain('Test Anime Romaji');
  });

  it('displays status correctly', () => {
    const wrapper = createWrapper();

    expect(wrapper.text()).toContain('Finished');
  });

  it('handles anime without score', () => {
    const animeWithoutScore = {
      ...mockAnime,
      averageScore: null,
    };

    const wrapper = createWrapper({ anime: animeWithoutScore });

    // Should not crash and should handle missing score gracefully
    expect(wrapper.exists()).toBe(true);
  });

  it('handles anime without episodes', () => {
    const animeWithoutEpisodes = {
      ...mockAnime,
      episodes: null,
    };

    const wrapper = createWrapper({ anime: animeWithoutEpisodes });

    // Should not crash and should handle missing episodes gracefully
    expect(wrapper.exists()).toBe(true);
  });

  it('applies correct CSS classes', () => {
    const wrapper = createWrapper();

    // Check for typical card styling classes
    expect(wrapper.find('.u-card').exists()).toBe(true);
  });
});
