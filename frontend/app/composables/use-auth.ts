import SuperTokens from 'supertokens-web-js';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';

import type { SignInSchema, SignUpSchema, UserProfile } from '~/types/auth';

export function useAuth() {
  const isLoggedIn = ref(false);
  const userProfile = ref<UserProfile | null>(null);
  const isInitialized = ref(false);
  const isLoading = ref(false);

  const toast = useToast();

  const config = useRuntimeConfig();
  const API_BASE_URL = (config.public?.apiBaseUrl as string) || 'http://localhost:8000';

  // Initialize SuperTokens if not already done
  function initSuperTokensIfNeeded() {
    if (!isInitialized.value) {
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
      isInitialized.value = true;
    }
  }

  // Fetch user profile from our backend
  async function fetchUserProfile(): Promise<UserProfile | null> {
    try {
      const response = await $fetch<UserProfile>(`${API_BASE_URL}/api/v1/users/me`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response;
    }
    catch (error) {
      console.error('Failed to fetch user profile:', error);
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
          isLoggedIn.value = true;
          userProfile.value = profile;
        }
        else {
          isLoggedIn.value = false;
          userProfile.value = null;
        }
      }
      else {
        isLoggedIn.value = false;
        userProfile.value = null;
      }
    }
    catch (error) {
      console.error('Auth check failed:', error);
      isLoggedIn.value = false;
      userProfile.value = null;
    }
  }

  // Sign up function using our backend API
  async function signUp(data: SignUpSchema) {
    isLoading.value = true;
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
      isLoading.value = false;
    }
  }

  // Sign in function using our backend API
  async function signIn(data: SignInSchema) {
    isLoading.value = true;
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
      isLoading.value = false;
    }
  }

  // Sign out function
  async function signOut() {
    try {
      initSuperTokensIfNeeded();
      await Session.signOut();
      isLoggedIn.value = false;
      userProfile.value = null;
      toast.add({
        title: 'Signed Out',
        description: 'You have been successfully signed out.',
        color: 'info',
      });
    }
    catch (error) {
      console.error('Sign out error:', error);
      toast.add({
        title: 'Error',
        description: 'An error occurred during sign out',
        color: 'error',
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
    isLoading.value = true;
    try {
      const response = await $fetch(`${API_BASE_URL}/api/v1/users/me`, {
        method: 'PUT',
        body: {
          username: data.username,
          full_name: data.fullName,
        },
        credentials: 'include',
      });

      if (response) {
        // Refresh user profile
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
      const errorMessage = error?.data?.detail || error.message || 'An error occurred';
      toast.add({
        title: 'Update Failed',
        description: errorMessage,
        color: 'error',
      });
      return { success: false, message: errorMessage };
    }
    finally {
      isLoading.value = false;
    }
  }

  // Initialize auth on composable creation
  onMounted(() => {
    checkAuth();
  });

  return {
    // State
    isLoggedIn: readonly(isLoggedIn),
    userProfile: readonly(userProfile),
    isLoading: readonly(isLoading),

    // Methods
    signUp,
    signIn,
    signOut,
    checkAuth,
    checkUsernameAvailability,
    updateProfile,
  };
}
