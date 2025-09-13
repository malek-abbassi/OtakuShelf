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
  }
  else {
    await signIn(data as SignInSchema);
  }
}

// Toggle between sign in and sign up
function toggleMode() {
  isSignUp.value = !isSignUp.value;
}

// Handle sign out
function handleSignOut() {
  signOut();
}
</script>

<template>
  <div class="flex justify-center items-center p-4">
    <AuthForm
      v-if="!isLoggedIn"
      :is-sign-up="isSignUp"
      :is-loading="isLoading"
      @submit="handleSubmit"
      @toggle-mode="toggleMode"
    />

    <UserProfile
      v-else
      :user-info="userProfile"
      @sign-out="handleSignOut"
    />
  </div>
</template>
