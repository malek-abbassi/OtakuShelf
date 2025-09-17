<script lang="ts" setup>
import type { SignInSchema, SignUpSchema } from '~/types/auth';

// Local state for form mode
const isSignUp = ref(false);

// Use auth composable
const { isLoggedIn, userProfile, isLoading, signUp, signIn, signOut } = useAuth();

// Handle form submission
async function handleSubmit(data: SignInSchema | SignUpSchema) {
  if (isSignUp.value) {
    await signUp(data as SignUpSchema);
    await navigateTo('/anime');
  }
  else {
    await signIn(data as SignInSchema);
    await navigateTo('/watchlist');
  }
}

// Toggle between sign in and sign up
function toggleMode() {
  isSignUp.value = !isSignUp.value;
}

// Handle sign out
async function handleSignOut() {
  await signOut();
  await navigateTo('/');
}
</script>

<template>
  <div class="flex justify-center items-center p-4" data-testid="auth-view">
    <AuthForm
      v-if="!isLoggedIn"
      :is-sign-up="isSignUp"
      :is-loading="isLoading"
      data-testid="auth-form"
      @submit="handleSubmit"
      @toggle-mode="toggleMode"
    />

    <UserProfile
      v-else
      :user-info="userProfile"
      data-testid="user-profile"
      @sign-out="handleSignOut"
    />
  </div>
</template>
