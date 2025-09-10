// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/test-utils',
    '@nuxt/ui',
    '@nuxt/content',
    '@nuxt/scripts',
  ],
  css: ['~/assets/css/main.css'],
  eslint: {
    config: {
      standalone: false,
    },
  },
});
