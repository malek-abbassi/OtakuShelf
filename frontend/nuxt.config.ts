// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  // SSR Configuration
  ssr: true,
  nitro: {
    prerender: {
      routes: ['/privacy', '/terms', '/about'],
      crawlLinks: true,
    },
    // Add caching headers for static assets
    routeRules: {
      // Homepage pre-rendered at build time
      '/': { prerender: true },
      // Privacy and Terms pre-rendered at build time
      '/privacy': { prerender: true },
      '/terms': { prerender: true },
      '/about': { prerender: true },
      // Auth page - CSR for better UX with authentication
      '/auth': { ssr: false },
      // API routes - cache for 1 hour
      '/api/**': { headers: { 'cache-control': 's-maxage=3600' } },
      // Static assets - cache for 1 year
      '/_nuxt/**': { headers: { 'cache-control': 's-maxage=31536000' } },
    },
  },

  // Performance optimizations
  experimental: {
    payloadExtraction: false, // Disable payload extraction for better performance
    typedPages: true, // Enable typed pages for better DX
    // Add compatibility for Nuxt UI with Nuxt 4
    clientNodeCompat: true,
  },

  modules: ['@nuxt/eslint', '@nuxt/image', '@nuxt/test-utils', '@nuxt/ui', '@nuxt/scripts'],
  css: ['~/assets/css/main.css'],

  // Image optimization configuration
  image: {
    format: ['webp', 'avif'],
    quality: 80,
    screens: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      xxl: 1536,
    },
    presets: {
      cover: {
        modifiers: {
          format: 'webp',
          quality: 85,
          fit: 'cover',
        },
      },
      avatar: {
        modifiers: {
          format: 'webp',
          quality: 85,
          width: 128,
          height: 128,
          fit: 'cover',
        },
      },
    },
  },

  colorMode: {
    preference: 'system',
    fallback: 'light',
    hid: 'nuxt-color-mode-script',
    globalName: '__NUXT_COLOR_MODE__',
    componentName: 'ColorScheme',
    classPrefix: '',
    classSuffix: '',
    storageKey: 'nuxt-color-mode',
  },

  eslint: {
    config: {
      standalone: false,
    },
  },

  // Runtime config
  runtimeConfig: {
    public: {
      apiBaseUrl: 'http://localhost:8000',
      apiDomain: 'http://localhost:8000',
      websiteDomain: 'http://localhost:3000',
    },
  },

  // App head configuration for SEO
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'OtakuShelf - Your Personal Anime Collection Manager',
      meta: [
        { name: 'description', content: 'Organize, track, and discover your favorite anime series with OtakuShelf. The ultimate personal anime collection manager for otaku enthusiasts.' },
        { name: 'format-detection', content: 'telephone=no' },
        // Open Graph
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'OtakuShelf' },
        { property: 'og:locale', content: 'en_US' },
        // Twitter
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:site', content: '@otakushelf' },
        // Theme
        { name: 'theme-color', content: '#3b82f6' },
        { name: 'msapplication-TileColor', content: '#3b82f6' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'canonical', href: 'https://otakushelf.com' },
        // Preconnect to external domains
        { rel: 'preconnect', href: 'https://s4.anilist.co' },
        { rel: 'dns-prefetch', href: 'https://graphql.anilist.co' },
      ],
    },
  },
});
