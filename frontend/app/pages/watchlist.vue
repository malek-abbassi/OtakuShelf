<script lang="ts" setup>
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
</script>

<template>
  <NuxtLayout>
    <div class="container mx-auto px-4 py-8">
      <WatchlistView />
    </div>
  </NuxtLayout>
</template>
