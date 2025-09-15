<script setup lang="ts">
type InternalLink = {
  label: string;
  to: string;
};

type ExternalLink = {
  label: string;
  href: string;
  external?: boolean;
};

type FooterLink = InternalLink | ExternalLink;

type FooterSection = {
  title: string;
  links: FooterLink[];
};

const config = useRuntimeConfig();
const appVersion = config.public.appVersion || '1.0.0';

const currentYear = new Date().getFullYear();

// Color mode composable
const { $colorMode } = useNuxtApp();
const isDark = computed({
  get: () => $colorMode.value === 'dark',
  set: (value: boolean) => {
    $colorMode.preference = value ? 'dark' : 'light';
  },
});

// Type guards
function isInternalLink(link: FooterLink): link is InternalLink {
  return 'to' in link;
}

function isExternalLink(link: FooterLink): link is ExternalLink {
  return 'href' in link;
}

const footerLinks: FooterSection[] = [
  {
    title: 'Product',
    links: [
      { label: 'Features', to: '/#features' },
      { label: 'Discover Anime', to: '/anime' },
      { label: 'Watchlist', to: '/watchlist' },
    ],
  },
  {
    title: 'Support',
    links: [
      { label: 'About', to: '/about' },
      { label: 'Contact', href: 'mailto:support@otakushelf.com' },
      { label: 'Privacy Policy', to: '/privacy' },
    ],
  },
  {
    title: 'Connect',
    links: [
      { label: 'GitHub', href: 'https://github.com/malek-abbassi/OtakuShelf', external: true },
      { label: 'AniList', href: 'https://anilist.co/', external: true },
    ],
  },
];
</script>

<template>
  <footer class="bg-white dark:bg-neutral-900 border-t border-neutral-200 dark:border-neutral-800">
    <div class="container mx-auto px-4 py-12">
      <!-- Main Footer Content -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Brand Section -->
        <div class="lg:col-span-1">
          <div class="flex items-center space-x-2 mb-4">
            <UIcon name="i-heroicons-film" class="text-2xl text-primary-600 dark:text-primary-400" />
            <span class="font-bold text-xl text-neutral-900 dark:text-white">OtakuShelf</span>
          </div>
          <p class="text-neutral-600 dark:text-neutral-400 text-sm mb-4">
            Your personal anime collection manager. Organize, track, and discover your favorite series with ease.
          </p>
          <p class="text-xs text-neutral-500 dark:text-neutral-500">
            Version {{ appVersion }}
          </p>
        </div>

        <!-- Footer Links -->
        <div
          v-for="section in footerLinks"
          :key="section.title"
          class="space-y-4"
        >
          <h3 class="text-sm font-semibold text-neutral-900 dark:text-white uppercase tracking-wider">
            {{ section.title }}
          </h3>
          <ul class="space-y-2">
            <li v-for="link in section.links" :key="link.label">
              <ULink
                v-if="isInternalLink(link)"
                :to="link.to"
                class="text-neutral-600 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors"
              >
                {{ link.label }}
              </ULink>
              <ULink
                v-else-if="isExternalLink(link)"
                :to="link.href"
                :target="link.external ? '_blank' : undefined"
                :rel="link.external ? 'noopener noreferrer' : undefined"
                class="text-neutral-600 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm transition-colors inline-flex items-center"
              >
                {{ link.label }}
                <UIcon
                  v-if="link.external"
                  name="i-heroicons-arrow-top-right-on-square"
                  class="ml-1 text-xs"
                />
              </ULink>
            </li>
          </ul>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="mt-12 pt-8 border-t border-neutral-200 dark:border-neutral-800">
        <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <p class="text-sm text-neutral-600 dark:text-neutral-400">
            © {{ currentYear }} OtakuShelf. All rights reserved.
          </p>
          <div class="flex items-center space-x-4">
            <UButton
              to="/privacy"
              variant="link"
              size="xs"
              color="neutral"
            >
              Privacy
            </UButton>
            <UButton
              to="/terms"
              variant="link"
              size="xs"
              color="neutral"
            >
              Terms
            </UButton>
            <ClientOnly>
              <UButton
                :icon="isDark ? 'i-heroicons-sun' : 'i-heroicons-moon'"
                variant="ghost"
                size="sm"
                color="neutral"
                :aria-label="`Switch to ${isDark ? 'light' : 'dark'} mode`"
                @click="isDark = !isDark"
              />
              <template #fallback>
                <UButton
                  icon="i-heroicons-sun"
                  variant="ghost"
                  size="sm"
                  color="neutral"
                  disabled
                  aria-label="Loading theme toggle"
                />
              </template>
            </ClientOnly>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
