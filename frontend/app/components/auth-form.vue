<script lang="ts" setup>
import type { FormSubmitEvent } from '@nuxt/ui';

import type { SignInSchema, SignUpSchema } from '~/types/auth';

import { signInSchema, signUpSchema } from '~/types/auth';

type AuthFormProps = {
  isSignUp: boolean;
  isLoading: boolean;
};

type AuthFormEmits = {
  submit: [data: SignInSchema | SignUpSchema];
  toggleMode: [];
};

const props = defineProps<AuthFormProps>();
const emit = defineEmits<AuthFormEmits>();

// Form state
const state = reactive({
  email: '',
  password: '',
  username: '',
  fullName: '',
});

// Password visibility state
const showPassword = ref(false);

// Computed schema based on mode
const currentSchema = computed(() => props.isSignUp ? signUpSchema : signInSchema);

// Form submission handler
async function onSubmit(event: FormSubmitEvent<SignInSchema | SignUpSchema>) {
  emit('submit', event.data);
}

// Toggle between sign in and sign up
function handleToggleMode() {
  // Clear form state when switching modes
  state.email = '';
  state.password = '';
  state.username = '';
  state.fullName = '';
  showPassword.value = false;
  emit('toggleMode');
}

// Watch for mode changes to clear form
watch(() => props.isSignUp, () => {
  state.email = '';
  state.password = '';
  state.username = '';
  state.fullName = '';
  showPassword.value = false;
});
</script>

<template>
  <UCard class="w-full max-w-md mx-auto" data-testid="auth-form-card">
    <template #header>
      <div class="text-center" data-testid="auth-form-header">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ isSignUp ? 'Create Account' : 'Welcome Back' }}
        </h2>
        <p class="text-gray-500 dark:text-gray-400 mt-1">
          {{ isSignUp ? 'Sign up for your account' : 'Sign in to your account' }}
        </p>
      </div>
    </template>

    <UForm
      :schema="currentSchema"
      :state="state"
      class="space-y-6"
      data-testid="auth-form"
      @submit="onSubmit"
    >
      <UFormField
        label="Email"
        name="email"
        required
        data-testid="email-field"
      >
        <UInput
          v-model="state.email"
          type="email"
          placeholder="Enter your email"
          icon="i-heroicons-envelope"
          size="lg"
          :disabled="isLoading"
          class="w-full"
          data-testid="email-input"
        />
      </UFormField>

      <UFormField
        v-if="isSignUp"
        label="Username"
        name="username"
        required
        data-testid="username-field"
      >
        <UInput
          v-model="state.username"
          type="text"
          placeholder="Choose a username"
          icon="i-heroicons-user"
          size="lg"
          :disabled="isLoading"
          class="w-full"
          data-testid="username-input"
        />
      </UFormField>

      <UFormField
        v-if="isSignUp"
        label="Full Name"
        name="fullName"
        data-testid="fullname-field"
      >
        <UInput
          v-model="state.fullName"
          type="text"
          placeholder="Enter your full name (optional)"
          icon="i-heroicons-identification"
          size="lg"
          :disabled="isLoading"
          class="w-full"
          data-testid="fullname-input"
        />
      </UFormField>

      <UFormField
        label="Password"
        name="password"
        required
        data-testid="password-field"
      >
        <UInput
          v-model="state.password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Enter your password"
          icon="i-heroicons-lock-closed"
          size="lg"
          :disabled="isLoading"
          class="w-full"
          data-testid="password-input"
        >
          <template #trailing>
            <UButton
              :icon="showPassword ? 'i-heroicons-eye-slash' : 'i-heroicons-eye'"
              size="xs"
              color="neutral"
              variant="link"
              :padded="false"
              data-testid="password-toggle"
              @click="showPassword = !showPassword"
            />
          </template>
        </UInput>
      </UFormField>

      <UButton
        type="submit"
        block
        size="lg"
        :loading="isLoading"
        data-testid="auth-submit-button"
      >
        {{ isSignUp ? 'Create Account' : 'Sign In' }}
      </UButton>
    </UForm>

    <template #footer>
      <div class="text-center" data-testid="auth-form-footer">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          {{ isSignUp ? 'Already have an account?' : "Don't have an account?" }}
        </p>
        <UButton
          variant="ghost"
          size="sm"
          class="mt-1"
          :disabled="isLoading"
          data-testid="auth-toggle-mode"
          @click="handleToggleMode"
        >
          {{ isSignUp ? 'Sign In' : 'Sign Up' }}
        </UButton>
      </div>
    </template>
  </UCard>
</template>
