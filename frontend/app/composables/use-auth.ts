import SuperTokens from 'supertokens-web-js';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';

import type { SignInSchema, SignUpSchema } from '~/types/auth';

export function useAuth() {
  const isLoggedIn = ref(false);
  const userInfo = ref<any>(null);
  const isInitialized = ref(false);
  const isLoading = ref(false);

  const toast = useToast();

  // Initialize SuperTokens if not already done
  function initSuperTokensIfNeeded() {
    if (!isInitialized.value) {
      SuperTokens.init({
        appInfo: {
          appName: 'OtakuShelf',
          apiDomain: 'http://127.0.0.1:8000',
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

  // Check authentication status
  async function checkAuth() {
    try {
      initSuperTokensIfNeeded();
      if (await Session.doesSessionExist()) {
        isLoggedIn.value = true;
        userInfo.value = await Session.getUserId();
      }
      else {
        isLoggedIn.value = false;
      }
    }
    catch (error) {
      console.error('Auth check failed:', error);
      isLoggedIn.value = false;
    }
  }

  // Sign up function
  async function signUp(data: SignUpSchema) {
    isLoading.value = true;
    try {
      initSuperTokensIfNeeded();
      const response = await EmailPassword.signUp({
        formFields: [
          { id: 'email', value: data.email },
          { id: 'password', value: data.password },
        ],
      });

      if (response.status === 'OK') {
        await checkAuth();
        toast.add({
          title: 'Success',
          description: 'Account created successfully! You are now signed in.',
          color: 'success',
        });
        return { success: true };
      }
      else if (response.status === 'FIELD_ERROR') {
        const errorMessage = response.formFields?.[0]?.error || 'Sign up failed';
        toast.add({
          title: 'Sign Up Failed',
          description: errorMessage,
          color: 'error',
        });
        return { success: false, message: errorMessage };
      }
      else {
        toast.add({
          title: 'Sign Up Failed',
          description: 'Sign up not allowed',
          color: 'error',
        });
        return { success: false, message: 'Sign up not allowed' };
      }
    }
    catch (error) {
      console.error('Sign up error:', error);
      const errorMessage = error instanceof Error ? error.message : String(error);
      toast.add({
        title: 'Error',
        description: `An error occurred during sign up: ${errorMessage}`,
        color: 'error',
      });
      return { success: false, message: 'An error occurred during sign up' };
    }
    finally {
      isLoading.value = false;
    }
  }

  // Sign in function
  async function signIn(data: SignInSchema) {
    isLoading.value = true;
    try {
      initSuperTokensIfNeeded();
      const response = await EmailPassword.signIn({
        formFields: [
          { id: 'email', value: data.email },
          { id: 'password', value: data.password },
        ],
      });

      if (response.status === 'OK') {
        await checkAuth();
        toast.add({
          title: 'Success',
          description: 'Welcome back! You are now signed in.',
          color: 'success',
        });
        return { success: true };
      }
      else {
        toast.add({
          title: 'Sign In Failed',
          description: 'Invalid email or password',
          color: 'error',
        });
        return { success: false, message: 'Invalid credentials' };
      }
    }
    catch (error) {
      console.error('Sign in error:', error);
      const errorMessage = error instanceof Error ? error.message : String(error);
      toast.add({
        title: 'Error',
        description: `An error occurred during sign in: ${errorMessage}`,
        color: 'error',
      });
      return { success: false, message: 'An error occurred during sign in' };
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
      userInfo.value = null;
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

  // Initialize auth on composable creation
  onMounted(() => {
    checkAuth();
  });

  return {
    // State
    isLoggedIn: readonly(isLoggedIn),
    userInfo: readonly(userInfo),
    isLoading: readonly(isLoading),

    // Methods
    signUp,
    signIn,
    signOut,
    checkAuth,
  };
}
