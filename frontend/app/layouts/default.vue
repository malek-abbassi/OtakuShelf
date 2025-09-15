<script setup lang="ts">
// Ensure auth is checked on client-side
const { checkAuth } = useAuth();

// Initialize auth check on client side
onMounted(async () => {
  await checkAuth();
});
</script>

<template>
  <div class="min-h-screen flex flex-col bg-neutral-50 dark:bg-neutral-900">
    <!-- Header -->
    <AppHeader />

    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>
