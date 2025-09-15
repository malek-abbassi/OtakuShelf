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

  // Initialize SuperTokens
  async function initSuperTokensIfNeeded() {
    if (globalAuthState.isInitialized.value)
      return;

    try {
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
    catch (error) {
      console.error('SuperTokens initialization failed:', error);
    }
  }

  // Fetch user profile from API
  async function fetchUserProfile(): Promise<UserProfile | null> {
    try {
      // First verify we have a session
      const sessionExists = await Session.doesSessionExist();
      if (!sessionExists) {
        console.warn('No SuperTokens session exists when trying to fetch profile');
        globalAuthState.isLoggedIn.value = false;
        globalAuthState.userProfile.value = null;
        return null;
      }

      const response = await $fetch<any>('/api/v1/users/me', {
        baseURL: API_BASE_URL,
        credentials: 'include',
        // Add retry logic to the request
        retry: 2,
        retryDelay: 500,
      });

      if (response) {
        const profile: UserProfile = {
          id: response.id,
          username: response.username,
          email: response.email,
          fullName: response.full_name || response.fullName,
          isActive: response.is_active ?? response.isActive,
          createdAt: response.created_at || response.createdAt,
          watchlistCount: response.watchlist_count || response.watchlistCount || 0,
        };
        globalAuthState.userProfile.value = profile;
        globalAuthState.isLoggedIn.value = true;
        return profile;
      }
    }
    catch (error: any) {
      console.error('Failed to fetch user profile:', error);
      if (error?.status === 401) {
        console.warn('Profile fetch returned 401, clearing session state');
        globalAuthState.isLoggedIn.value = false;
        globalAuthState.userProfile.value = null;

        // Try to refresh the session if it exists in SuperTokens
        try {
          const sessionExists = await Session.doesSessionExist();
          if (sessionExists) {
            await Session.attemptRefreshingSession();
            // If refresh succeeds, try fetching profile again (but avoid infinite recursion)
            const refreshedResponse = await $fetch<any>('/api/v1/users/me', {
              baseURL: API_BASE_URL,
              credentials: 'include',
            });
            if (refreshedResponse) {
              const profile: UserProfile = {
                id: refreshedResponse.id,
                username: refreshedResponse.username,
                email: refreshedResponse.email,
                fullName: refreshedResponse.full_name || refreshedResponse.fullName,
                isActive: refreshedResponse.is_active ?? refreshedResponse.isActive,
                createdAt: refreshedResponse.created_at || refreshedResponse.createdAt,
                watchlistCount: refreshedResponse.watchlist_count || refreshedResponse.watchlistCount || 0,
              };
              globalAuthState.userProfile.value = profile;
              globalAuthState.isLoggedIn.value = true;
              return profile;
            }
          }
        }
        catch (refreshError) {
          console.error('Session refresh failed:', refreshError);
        }
      }
    }
    return null;
  }

  // Check authentication status
  async function checkAuth() {
    if (!import.meta.client)
      return;

    try {
      globalAuthState.isLoading.value = true;
      await initSuperTokensIfNeeded();

      const sessionExists = await Session.doesSessionExist();
      if (sessionExists) {
        await fetchUserProfile();
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
    finally {
      globalAuthState.isLoading.value = false;
    }
  }

  // Sign up function using SuperTokens
  async function signUp(data: SignUpSchema) {
    globalAuthState.isLoading.value = true;
    try {
      await initSuperTokensIfNeeded();

      const response = await EmailPassword.signUp({
        formFields: [
          { id: 'email', value: data.email },
          { id: 'password', value: data.password },
        ],
      });

      if (response.status === 'OK') {
        // Create user profile in our database
        try {
          await $fetch('/api/v1/users/signup', {
            baseURL: API_BASE_URL,
            method: 'POST',
            body: {
              email: data.email,
              password: data.password, // This will be ignored by backend since user already exists in SuperTokens
              username: data.username,
              full_name: data.fullName,
            },
            credentials: 'include',
          });

          // Fetch the updated profile
          await fetchUserProfile();

          toast.add({
            title: 'Success',
            description: 'Account created successfully! You are now signed in.',
            color: 'success',
          });
          return { success: true };
        }
        catch (profileError: any) {
          console.error('Profile creation error:', profileError);
          const errorMessage = profileError?.data?.detail || 'Failed to create user profile';
          toast.add({
            title: 'Profile Creation Failed',
            description: errorMessage,
            color: 'error',
          });
          return { success: false, message: errorMessage };
        }
      }
      else if (response.status === 'FIELD_ERROR') {
        const emailError = response.formFields.find(field => field.id === 'email')?.error;
        const passwordError = response.formFields.find(field => field.id === 'password')?.error;
        const errorMessage = emailError || passwordError || 'Sign up failed';

        toast.add({
          title: 'Sign Up Failed',
          description: errorMessage,
          color: 'error',
        });
        return { success: false, message: errorMessage };
      }
      else {
        throw new Error('Unexpected response status');
      }
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

  // Sign in function using SuperTokens
  async function signIn(data: SignInSchema) {
    globalAuthState.isLoading.value = true;
    try {
      await initSuperTokensIfNeeded();

      const response = await EmailPassword.signIn({
        formFields: [
          { id: 'email', value: data.email },
          { id: 'password', value: data.password },
        ],
      });

      if (response.status === 'OK') {
        // Give SuperTokens a moment to set up the session
        await new Promise(resolve => setTimeout(resolve, 100));

        // Verify session was created successfully
        const sessionExists = await Session.doesSessionExist();
        if (!sessionExists) {
          throw new Error('Session was not created after successful sign-in');
        }

        // Update user profile in our database if needed
        try {
          await $fetch('/api/v1/users/signin', {
            baseURL: API_BASE_URL,
            method: 'POST',
            body: {
              email: data.email,
              password: data.password,
            },
            credentials: 'include',
          });
        }
        catch (signinError) {
          // This might fail if the endpoint doesn't exist, but the SuperTokens auth still succeeded
          console.warn('Backend signin call failed, but SuperTokens auth succeeded:', signinError);
        }

        // Fetch the user profile with retry logic
        let retries = 3;
        let profileFetched = false;

        while (retries > 0 && !profileFetched) {
          try {
            await fetchUserProfile();
            profileFetched = globalAuthState.userProfile.value !== null;
            if (!profileFetched) {
              retries--;
              if (retries > 0) {
                await new Promise(resolve => setTimeout(resolve, 200));
              }
            }
          }
          catch (error) {
            console.warn('Profile fetch attempt failed:', error);
            retries--;
            if (retries > 0) {
              await new Promise(resolve => setTimeout(resolve, 200));
            }
          }
        }

        if (!profileFetched) {
          throw new Error('Failed to fetch user profile after sign-in');
        }

        toast.add({
          title: 'Success',
          description: 'Welcome back! You are now signed in.',
          color: 'success',
        });
        return { success: true };
      }
      else if (response.status === 'FIELD_ERROR') {
        const emailError = response.formFields.find(field => field.id === 'email')?.error;
        const passwordError = response.formFields.find(field => field.id === 'password')?.error;
        const errorMessage = emailError || passwordError || 'Invalid email or password';

        toast.add({
          title: 'Sign In Failed',
          description: errorMessage,
          color: 'error',
        });
        return { success: false, message: errorMessage };
      }
      else if (response.status === 'WRONG_CREDENTIALS_ERROR') {
        const errorMessage = 'Invalid email or password';
        toast.add({
          title: 'Sign In Failed',
          description: errorMessage,
          color: 'error',
        });
        return { success: false, message: errorMessage };
      }
      else {
        throw new Error('Unexpected response status');
      }
    }
    catch (error: any) {
      console.error('Sign in error:', error);
      const errorMessage = error?.data?.detail || error.message || 'Invalid email or password';
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

  // Sign out function using SuperTokens
  async function signOut() {
    try {
      await initSuperTokensIfNeeded();
      await Session.signOut();

      // Try to notify backend about signout
      try {
        await $fetch('/api/v1/users/signout', {
          baseURL: API_BASE_URL,
          method: 'POST',
          credentials: 'include',
        });
      }
      catch (error) {
        console.error('Sign out API error:', error);
        // Continue with local cleanup even if API call fails
      }
    }
    catch (error) {
      console.error('SuperTokens sign out error:', error);
    }
    finally {
      // Clear local state
      globalAuthState.isLoggedIn.value = false;
      globalAuthState.userProfile.value = null;
      toast.add({
        title: 'Signed Out',
        description: 'You have been successfully signed out.',
        color: 'info',
      });
    }
  }

  // Check username availability
  async function checkUsernameAvailability(username: string) {
    try {
      const response = await $fetch<{ username: string; available: boolean; message?: string }>(
        `/api/v1/users/check-username/${username}`,
        {
          baseURL: API_BASE_URL,
        },
      );
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
      await initSuperTokensIfNeeded();

      const response = await $fetch<UserProfile>('/api/v1/users/me', {
        baseURL: API_BASE_URL,
        method: 'PUT',
        body: {
          username: data.username,
          full_name: data.fullName,
        },
        credentials: 'include',
      });

      if (response) {
        // Refresh profile to get updated data
        await fetchUserProfile();
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
      const errorMessage = error?.data?.detail || error.message || 'An error occurred';
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

  // Auto-initialize on client-side
  if (import.meta.client && !globalAuthState.isInitialized.value) {
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
