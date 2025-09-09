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
  <div class="auth-container">
    <div v-if="!isLoggedIn" class="auth-form">
      <h2>{{ isSignUp ? 'Sign Up' : 'Sign In' }}</h2>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email:</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label for="password">Password:</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="form-input"
          >
        </div>

        <button type="submit" class="submit-btn">
          {{ isSignUp ? 'Sign Up' : 'Sign In' }}
        </button>
      </form>

      <p class="toggle-mode">
        {{ isSignUp ? 'Already have an account?' : "Don't have an account?" }}
        <button class="toggle-btn" @click="isSignUp = !isSignUp">
          {{ isSignUp ? 'Sign In' : 'Sign Up' }}
        </button>
      </p>

      <p v-if="message" class="message">
        {{ message }}
      </p>
    </div>

    <div v-else class="user-dashboard">
      <h2>Welcome!</h2>
      <p>User ID: {{ userInfo }}</p>
      <button class="logout-btn" @click="signOut">
        Sign Out
      </button>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.auth-form {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-btn,
.logout-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.submit-btn:hover,
.logout-btn:hover {
  background-color: #0056b3;
}

.toggle-mode {
  text-align: center;
  margin-top: 1rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
}

.message {
  text-align: center;
  margin-top: 1rem;
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #e9ecef;
}

.user-dashboard {
  text-align: center;
}
</style>
