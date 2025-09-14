// Global middleware to check authentication status on every route change
// This ensures the auth state is always up to date across the application

export default defineNuxtRouteMiddleware(async (_to, _from) => {
  // Only run on client-side to avoid hydration issues
  if (import.meta.server) {
    return;
  }

  const { checkAuth } = useAuth();

  // Check authentication status on every route change
  // This ensures reactive state is updated properly
  try {
    await checkAuth();
  }
  catch (error) {
    console.error('Global auth check failed:', error);
  }
});
