import SuperTokens from 'supertokens-web-js';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';

import type { SignInSchema, SignUpSchema, UserProfile } from '~/types/auth';

// Global state for authentication - shared across all instances
const globalAuthState = {
  isLoggedIn: ref(false),
  userProfile: ref<UserProfile | null>(null),
  isLoading: ref(false),
  isInitialized: ref(false),
};

export function useAuth() {
  const toast = useToast();

  const config = useRuntimeConfig();
  const API_BASE_URL = ((config.public?.apiBaseUrl as string) || 'http://localhost:8000')
    .replace('127.0.0.1', 'localhost'); // Ensure consistent domain for cookies

  // Initialize SuperTokens if not already done
  function initSuperTokensIfNeeded() {
    if (!globalAuthState.isInitialized.value) {
      SuperTokens.init({
        appInfo: {
          appName: 'OtakuShelf',
          apiDomain: API_BASE_URL,
          apiBasePath: '/auth',
        },
        recipeList: [
          EmailPassword.init(),
          Session.init(),
        ],
      });
      globalAuthState.isInitialized.value = true;
    }
  }

  // Fetch user profile from our backend
  async function fetchUserProfile(): Promise<UserProfile | null> {
    try {
      initSuperTokensIfNeeded();

      // First check if we have a valid session
      if (!(await Session.doesSessionExist())) {
        console.warn('No session exists');
        return null;
      }

      // Use native fetch with credentials to ensure cookies are sent
      const response = await fetch(`${API_BASE_URL}/api/v1/users/me`, {
        method: 'GET',
        credentials: 'include', // This is crucial for sending cookies
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        console.error('Failed to fetch user profile:', response.status, response.statusText);

        // If we get 401, the session might be expired
        if (response.status === 401) {
          console.warn('Session appears to be invalid, clearing local session');
          await Session.signOut();
        }
        return null;
      }

      const data = await response.json();

      // Transform backend snake_case to frontend camelCase
      return {
        id: data.id,
        username: data.username,
        email: data.email,
        fullName: data.full_name,
        isActive: data.is_active,
        createdAt: data.created_at,
        watchlistCount: data.watchlist_count || 0,
      };
    }
    catch (error: any) {
      console.error('Failed to fetch user profile:', error);

      // If we get 401, the session might be expired
      if (error.status === 401 || error.statusCode === 401) {
        console.warn('Session appears to be invalid, clearing local session');
        await Session.signOut();
      }
      return null;
    }
  }

  // Check authentication status
  async function checkAuth() {
    try {
      initSuperTokensIfNeeded();
      if (await Session.doesSessionExist()) {
        const profile = await fetchUserProfile();
        if (profile) {
          globalAuthState.isLoggedIn.value = true;
          globalAuthState.userProfile.value = profile;
        }
        else {
          globalAuthState.isLoggedIn.value = false;
          globalAuthState.userProfile.value = null;
        }
      }
      else {
        globalAuthState.isLoggedIn.value = false;
        globalAuthState.userProfile.value = null;
      }
    }
    catch (error) {
      console.error('Auth check failed:', error);
      globalAuthState.isLoggedIn.value = false;
      globalAuthState.userProfile.value = null;
    }
  }

  // Sign up function using our backend API
  async function signUp(data: SignUpSchema) {
    globalAuthState.isLoading.value = true;
    try {
      // First register with our backend
      const response = await $fetch(`${API_BASE_URL}/api/v1/users/signup`, {
        method: 'POST',
        body: {
          email: data.email,
          password: data.password,
          username: data.username,
          full_name: data.fullName,
        },
      });

      if (response) {
        // After successful backend registration, sign in with SuperTokens
        initSuperTokensIfNeeded();
        const authResponse = await EmailPassword.signIn({
          formFields: [
            { id: 'email', value: data.email },
            { id: 'password', value: data.password },
          ],
        });

        if (authResponse.status === 'OK') {
          await checkAuth();
          toast.add({
            title: 'Success',
            description: 'Account created successfully! You are now signed in.',
            color: 'success',
          });
          return { success: true };
        }
      }

      toast.add({
        title: 'Sign Up Failed',
        description: 'Failed to complete sign up process',
        color: 'error',
      });
      return { success: false, message: 'Failed to complete sign up process' };
    }
    catch (error: any) {
      console.error('Sign up error:', error);
      const errorMessage = error?.data?.detail || error.message || 'An error occurred during sign up';
      toast.add({
        title: 'Sign Up Failed',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
    finally {
      globalAuthState.isLoading.value = false;
    }
  }

  // Sign in function using our backend API
  async function signIn(data: SignInSchema) {
    globalAuthState.isLoading.value = true;
    try {
      // First sign in with our backend to validate credentials
      const response = await $fetch(`${API_BASE_URL}/api/v1/users/signin`, {
        method: 'POST',
        body: {
          email: data.email,
          password: data.password,
        },
      });

      if (response) {
        // After successful backend validation, sign in with SuperTokens
        initSuperTokensIfNeeded();
        const authResponse = await EmailPassword.signIn({
          formFields: [
            { id: 'email', value: data.email },
            { id: 'password', value: data.password },
          ],
        });

        if (authResponse.status === 'OK') {
          await checkAuth();
          toast.add({
            title: 'Success',
            description: 'Welcome back! You are now signed in.',
            color: 'success',
          });
          return { success: true };
        }
      }

      toast.add({
        title: 'Sign In Failed',
        description: 'Invalid email or password',
        color: 'error',
      });
      return { success: false, message: 'Invalid credentials' };
    }
    catch (error: any) {
      console.error('Sign in error:', error);
      const errorMessage = error?.data?.detail || error.message || 'An error occurred during sign in';
      toast.add({
        title: 'Sign In Failed',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
    finally {
      globalAuthState.isLoading.value = false;
    }
  }

  // Sign out function
  async function signOut() {
    try {
      initSuperTokensIfNeeded();
      await Session.signOut();
      globalAuthState.isLoggedIn.value = false;
      globalAuthState.userProfile.value = null;
      toast.add({
        title: 'Signed Out',
        description: 'You have been successfully signed out.',
        color: 'info',
      });
    }
    catch (error) {
      console.error('Sign out error:', error);
      // Even if there's an error, clear the local state
      globalAuthState.isLoggedIn.value = false;
      globalAuthState.userProfile.value = null;
      toast.add({
        title: 'Signed Out',
        description: 'You have been signed out.',
        color: 'info',
      });
    }
  }

  // Check username availability
  async function checkUsernameAvailability(username: string) {
    try {
      const response = await $fetch(`${API_BASE_URL}/api/v1/users/check-username/${username}`);
      return response;
    }
    catch (error) {
      console.error('Username check error:', error);
      return { username, available: false, message: 'Error checking username' };
    }
  }

  // Update user profile
  async function updateProfile(data: { username?: string; fullName?: string }) {
    globalAuthState.isLoading.value = true;
    try {
      const requestBody = {
        username: data.username,
        full_name: data.fullName,
      };

      // Use native fetch to ensure proper cookie handling
      const response = await fetch(`${API_BASE_URL}/api/v1/users/me`, {
        method: 'PUT',
        credentials: 'include', // This is crucial for sending cookies
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData?.detail || 'Failed to update profile';
        throw new Error(errorMessage);
      }

      const responseData = await response.json();

      if (responseData) {
        // Refresh user profile to get updated data
        await checkAuth();
        toast.add({
          title: 'Success',
          description: 'Profile updated successfully',
          color: 'success',
        });
        return { success: true };
      }

      return { success: false, message: 'Failed to update profile' };
    }
    catch (error: any) {
      console.error('Profile update error:', error);
      const errorMessage = error?.message || 'An error occurred';
      toast.add({
        title: 'Update Failed',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
    finally {
      globalAuthState.isLoading.value = false;
    }
  }

  // Initialize auth on composable creation - but only on client side
  if (import.meta.client) {
    nextTick(() => {
      checkAuth();
    });
  }

  return {
    // State
    isLoggedIn: readonly(globalAuthState.isLoggedIn),
    userProfile: readonly(globalAuthState.userProfile),
    isLoading: readonly(globalAuthState.isLoading),

    // Methods
    signUp,
    signIn,
    signOut,
    checkAuth,
    fetchUserProfile,
    checkUsernameAvailability,
    updateProfile,
  };
}
