<script setup lang="ts">
type NavigationItem = {
  label: string;
  to: string;
  icon: string;
  requiresAuth?: boolean;
  hideWhenAuth?: boolean;
};

// Composables
const { isLoggedIn, userProfile, signOut } = useAuth();
const router = useRouter();
const route = useRoute();

// Navigation items
const navigationItems: NavigationItem[] = [
  {
    label: 'Home',
    to: '/',
    icon: 'i-heroicons-home',
  },
  {
    label: 'Discover',
    to: '/anime',
    icon: 'i-heroicons-magnifying-glass',
  },
  {
    label: 'My Watchlist',
    to: '/watchlist',
    icon: 'i-heroicons-list-bullet',
    requiresAuth: true,
  },
  {
    label: 'Sign In',
    to: '/auth',
    icon: 'i-heroicons-arrow-right-end-on-rectangle',
    hideWhenAuth: true,
  },
];

// Filter navigation based on auth status
const visibleNavItems = computed(() => {
  return navigationItems.filter((item) => {
    if (item.requiresAuth && !isLoggedIn.value)
      return false;
    if (item.hideWhenAuth && isLoggedIn.value)
      return false;
    return true;
  });
});

// User dropdown items
const userDropdownItems = computed(() => [
  [
    {
      label: userProfile.value?.fullName || userProfile.value?.username || 'Profile',
      icon: 'i-heroicons-user',
      disabled: true,
    },
  ],
  [
    {
      label: 'My Watchlist',
      icon: 'i-heroicons-list-bullet',
      to: '/watchlist',
    },
    {
      label: 'Settings',
      icon: 'i-heroicons-cog-6-tooth',
      to: '/settings',
    },
  ],
  [
    {
      label: 'Sign Out',
      icon: 'i-heroicons-arrow-left-start-on-rectangle',
      onClick: handleSignOut,
    },
  ],
]);

// Mobile menu state
const isMobileMenuOpen = ref(false);

// Methods
async function handleSignOut() {
  try {
    await signOut();
    await router.push('/');
  }
  catch (err) {
    console.error('Error signing out:', err);
  }
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false;
}

// Close mobile menu on route change
watch(() => route.path, () => {
  closeMobileMenu();
});
</script>

<template>
  <header class="sticky top-0 z-40 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-lg border-b border-neutral-200 dark:border-neutral-800">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo/Brand -->
        <NuxtLink
          to="/"
          class="flex items-center space-x-2 font-bold text-xl text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
        >
          <UIcon name="i-heroicons-film" class="text-2xl" />
          <span>OtakuShelf</span>
        </NuxtLink>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-1">
          <UButton
            v-for="item in visibleNavItems"
            :key="item.to"
            :to="item.to"
            :variant="route.path === item.to ? 'solid' : 'ghost'"
            :color="route.path === item.to ? 'primary' : 'neutral'"
            size="sm"
          >
            <UIcon :name="item.icon" class="mr-2" />
            {{ item.label }}
          </UButton>
        </nav>

        <!-- Desktop User Actions -->
        <div class="hidden md:flex items-center space-x-3">
          <ClientOnly>
            <!-- User dropdown for authenticated users -->
            <UDropdownMenu
              v-if="isLoggedIn && userProfile"
              :items="userDropdownItems"
            >
              <UAvatar
                :alt="userProfile.fullName || userProfile.username"
                size="sm"
                class="cursor-pointer hover:ring-2 hover:ring-primary-400 transition-all"
              />
            </UDropdownMenu>

            <!-- Sign in button for non-authenticated users -->
            <div v-else class="flex items-center space-x-2">
              <UButton to="/auth" variant="outline" size="sm">
                Sign In
              </UButton>
            </div>
          </ClientOnly>
        </div>

        <!-- Mobile menu button -->
        <UButton
          class="md:hidden"
          variant="ghost"
          color="neutral"
          size="sm"
          icon="i-heroicons-bars-3"
          @click="isMobileMenuOpen = !isMobileMenuOpen"
        />
      </div>
    </div>

    <!-- Mobile Navigation Menu -->
    <div v-if="isMobileMenuOpen" class="md:hidden border-t border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900">
      <div class="px-4 py-4 space-y-2">
        <!-- Mobile Navigation Items -->
        <UButton
          v-for="item in visibleNavItems"
          :key="item.to"
          :to="item.to"
          :variant="route.path === item.to ? 'solid' : 'ghost'"
          :color="route.path === item.to ? 'primary' : 'neutral'"
          size="lg"
          block
          justify="start"
          @click="closeMobileMenu"
        >
          <UIcon :name="item.icon" class="mr-3" />
          {{ item.label }}
        </UButton>

        <!-- Mobile User Section -->
        <ClientOnly>
          <div v-if="isLoggedIn && userProfile" class="border-t border-neutral-200 dark:border-neutral-800 pt-4 mt-4">
            <div class="mb-4 p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
              <div class="flex items-center space-x-3">
                <UAvatar
                  :alt="userProfile.fullName || userProfile.username"
                  size="sm"
                />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-neutral-900 dark:text-white truncate">
                    {{ userProfile.fullName || userProfile.username }}
                  </p>
                  <p class="text-xs text-neutral-500 dark:text-neutral-400 truncate">
                    {{ userProfile.email }}
                  </p>
                </div>
              </div>
            </div>

            <div class="space-y-2">
              <UButton
                to="/settings"
                variant="ghost"
                color="neutral"
                size="sm"
                block
                justify="start"
                @click="closeMobileMenu"
              >
                <UIcon name="i-heroicons-cog-6-tooth" class="mr-3" />
                Settings
              </UButton>
              <UButton
                variant="ghost"
                color="error"
                size="sm"
                block
                justify="start"
                @click="handleSignOut"
              >
                <UIcon name="i-heroicons-arrow-left-start-on-rectangle" class="mr-3" />
                Sign Out
              </UButton>
            </div>
          </div>
        </ClientOnly>
      </div>
    </div>
  </header>
</template>
