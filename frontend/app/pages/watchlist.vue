<script lang="ts" setup>
import { useAuth } from '~/composables/use-auth';

// Meta
useHead({
  title: 'My Watchlist - OtakuShelf',
  meta: [
    {
      name: 'description',
      content: 'Manage your anime watchlist and track your viewing progress',
    },
  ],
});

// Auth check
const { isLoggedIn } = useAuth();

// Redirect to auth if not logged in
watchEffect(() => {
  if (!isLoggedIn.value) {
    navigateTo('/auth');
  }
});
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <ClientOnly>
      <WatchlistView />
      <template #fallback>
        <LoadingState message="Loading watchlist..." />
      </template>
    </ClientOnly>
  </div>
</template>
