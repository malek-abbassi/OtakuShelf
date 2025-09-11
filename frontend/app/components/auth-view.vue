<script lang="ts" setup>
import SuperTokens from 'supertokens-web-js';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';
import { onMounted, ref } from 'vue';

const isLoggedIn = ref(false);
const userInfo = ref<any>(null);
const isInitialized = ref(false);

// Initialize SuperTokens if not already done (fallback)
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

async function signUp(email: string, password: string) {
  try {
    initSuperTokensIfNeeded();
    const response = await EmailPassword.signUp({
      formFields: [
        { id: 'email', value: email },
        { id: 'password', value: password },
      ],
    });

    if (response.status === 'OK') {
      // Sign up successful, redirect or update UI
      await checkAuth();
      return { success: true, message: 'Sign up successful!' };
    }
    else if (response.status === 'FIELD_ERROR') {
      return { success: false, message: response.formFields?.[0]?.error || 'Sign up failed' };
    }
    else {
      return { success: false, message: 'Sign up not allowed' };
    }
  }
  catch {
    return { success: false, message: 'An error occurred during sign up' };
  }
}

async function signIn(email: string, password: string) {
  try {
    initSuperTokensIfNeeded();
    const response = await EmailPassword.signIn({
      formFields: [
        { id: 'email', value: email },
        { id: 'password', value: password },
      ],
    });

    if (response.status === 'OK') {
      // Sign in successful
      await checkAuth();
      return { success: true, message: 'Sign in successful!' };
    }
    else {
      return { success: false, message: 'Invalid credentials' };
    }
  }
  catch (error) {
    console.error('Error during sign in:', error);
    return { success: false, message: 'An error occurred during sign in' };
  }
}

async function signOut() {
  initSuperTokensIfNeeded();
  await Session.signOut();
  isLoggedIn.value = false;
  userInfo.value = null;
}

onMounted(() => {
  checkAuth();
});

// Form handling
const email = ref('');
const password = ref('');
const isSignUp = ref(false);
const message = ref('');

async function handleSubmit() {
  if (isSignUp.value) {
    const result = await signUp(email.value, password.value);
    message.value = result.message;
  }
  else {
    const result = await signIn(email.value, password.value);
    message.value = result.message;
  }
}
</script>

<template>
  <div class="flex justify-center items-center  p-4">
    <UCard v-if="!isLoggedIn" class="w-full max-w-md">
      <template #header>
        <h2 class="text-2xl font-bold text-center">
          {{ isSignUp ? 'Create Account' : 'Welcome Back' }}
        </h2>
        <p class="text-gray-500 text-center mt-1">
          {{ isSignUp ? 'Sign up for your account' : 'Sign in to your account' }}
        </p>
      </template>

      <UForm :state="{ email, password }" class="space-y-4" @submit="handleSubmit">
        <UFormGroup label="Email" name="email" required>
          <UInput
            v-model="email"
            type="email"
            placeholder="Enter your email"
            icon="i-heroicons-envelope"
            size="lg"
          />
        </UFormGroup>

        <UFormGroup label="Password" name="password" required>
          <UInput
            v-model="password"
            type="password"
            placeholder="Enter your password"
            icon="i-heroicons-lock-closed"
            size="lg"
          />
        </UFormGroup>

        <UButton
          type="submit"
          block
          size="lg"
          :loading="false"
        >
          {{ isSignUp ? 'Create Account' : 'Sign In' }}
        </UButton>
      </UForm>

      <template #footer>
        <div class="text-center">
          <p class="text-sm text-gray-600">
            {{ isSignUp ? 'Already have an account?' : "Don't have an account?" }}
          </p>
          <UButton
            variant="ghost"
            size="sm"
            class="mt-1"
            @click="isSignUp = !isSignUp"
          >
            {{ isSignUp ? 'Sign In' : 'Sign Up' }}
          </UButton>
        </div>

        <UAlert
          v-if="message"
          :color="message.includes('successful') ? 'success' : 'error'"
          variant="soft"
          :title="message"
          class="mt-4"
        />
      </template>
    </UCard>

    <UCard v-else class="w-full max-w-md">
      <template #header>
        <div class="text-center">
          <div class="w-16 h-16 bg-success-100 dark:bg-success-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-check-circle" class="text-success-600 dark:text-success-400 text-2xl" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            Welcome!
          </h2>
          <p class="text-gray-500 dark:text-gray-400 mt-1">
            You're successfully signed in
          </p>
        </div>
      </template>

      <div class="space-y-4">
        <UCard class="bg-gray-50">
          <div class="flex items-center space-x-3">
            <UIcon name="i-heroicons-user-circle" class="text-gray-400" />
            <div>
              <p class="text-sm font-medium text-gray-900">
                User ID
              </p>
              <p class="text-sm text-gray-500">
                {{ userInfo }}
              </p>
            </div>
          </div>
        </UCard>

        <UButton
          block
          variant="outline"
          color="error"
          size="lg"
          @click="signOut"
        >
          <UIcon name="i-heroicons-arrow-right-on-rectangle" class="mr-2" />
          Sign Out
        </UButton>
      </div>
    </UCard>
  </div>
</template>
