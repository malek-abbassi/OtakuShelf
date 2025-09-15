<script lang="ts" setup>
// Enhanced SEO Meta
useSeoMeta({
  title: 'My Watchlist - OtakuShelf | Track Your Anime Progress',
  ogTitle: 'My Watchlist - OtakuShelf | Track Your Anime Progress',
  description: 'Manage your anime watchlist, track viewing progress, and organize your anime collection. Keep track of what you are watching, planning to watch, completed, and dropped.',
  ogDescription: 'Manage your anime watchlist, track viewing progress, and organize your anime collection. Keep track of what you are watching, planning to watch, completed, and dropped.',
  ogImage: '/favicon.ico',
  keywords: 'anime watchlist, track anime progress, anime collection, watching anime, anime tracker',
  robots: 'noindex, follow', // Private user content
});

// Add canonical link
useHead({
  title: 'My Watchlist - OtakuShelf',
  link: [
    { rel: 'canonical', href: 'https://otakushelf.com/watchlist' },
  ],
});

// Structured Data for Watchlist Page
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'name': 'My Watchlist - OtakuShelf',
        'description': 'Personal anime watchlist and progress tracker',
        'url': 'https://otakushelf.com/watchlist',
        'isPartOf': {
          '@type': 'WebApplication',
          'name': 'OtakuShelf',
        },
      }),
    },
  ],
});
</script>

<template>
  <NuxtLayout>
    <div class="container mx-auto px-4 py-8">
      <WatchlistView />
    </div>
  </NuxtLayout>
</template>
