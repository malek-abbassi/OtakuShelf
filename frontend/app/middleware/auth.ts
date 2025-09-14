// Auth middleware to protect routes that require authentication
// Usage: Add `middleware: ['auth']` to definePageMeta in any page that needs protection

export default defineNuxtRouteMiddleware(async (_to, _from) => {
  // Skip middleware on server-side rendering to avoid hydration issues
  if (import.meta.server)
    return;

  const { isLoggedIn, checkAuth } = useAuth();

  // Check authentication status
  await checkAuth();

  // Redirect to auth page if not logged in
  if (!isLoggedIn.value) {
    return navigateTo('/auth');
  }
});
