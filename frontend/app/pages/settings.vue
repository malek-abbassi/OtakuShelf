<script setup lang="ts">
import { z } from 'zod';

// Authentication and user management
const { userProfile, updateProfile, isLoading } = useAuth();
const toast = useToast();

// Reactive data
const profileForm = ref({
  username: '',
  fullName: '',
  email: '',
});

const isEditingProfile = ref(false);
const profileErrors = ref<Record<string, string>>({});

// Theme management
const colorMode = useColorMode();

// Profile validation schema
const profileSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .regex(/^\w+$/, 'Username can only contain letters, numbers, and underscores'),
  fullName: z.string()
    .min(2, 'Full name must be at least 2 characters')
    .max(50, 'Full name must be less than 50 characters'),
});

// Initialize form with current user data
watchEffect(() => {
  if (userProfile.value) {
    profileForm.value = {
      username: userProfile.value.username || '',
      fullName: userProfile.value.fullName || '',
      email: userProfile.value.email || '',
    };
  }
});

// Theme options
const themeOptions = [
  { label: 'Light', value: 'light', icon: 'i-heroicons-sun' },
  { label: 'Dark', value: 'dark', icon: 'i-heroicons-moon' },
  { label: 'System', value: 'system', icon: 'i-heroicons-computer-desktop' },
];

// Methods
function startEditing() {
  isEditingProfile.value = true;
  profileErrors.value = {};
}

function cancelEditing() {
  isEditingProfile.value = false;
  profileErrors.value = {};
  // Reset form to original values
  if (userProfile.value) {
    profileForm.value = {
      username: userProfile.value.username || '',
      fullName: userProfile.value.fullName || '',
      email: userProfile.value.email || '',
    };
  }
}

async function saveProfile() {
  try {
    // Validate form
    const validatedData = profileSchema.parse({
      username: profileForm.value.username,
      fullName: profileForm.value.fullName,
    });

    // Update profile
    const result = await updateProfile({
      username: validatedData.username,
      fullName: validatedData.fullName,
    });

    if (result.success) {
      isEditingProfile.value = false;
      profileErrors.value = {};
      toast.add({
        title: 'Success',
        description: 'Profile updated successfully',
        color: 'success',
      });
    }
    else {
      toast.add({
        title: 'Update Failed',
        description: result.message || 'Failed to update profile',
        color: 'error',
      });
    }
  }
  catch (error) {
    console.error('Save profile error:', error); // Enhanced error logging
    if (error instanceof z.ZodError) {
      // Handle validation errors
      profileErrors.value = {};
      error.issues.forEach((err) => {
        if (err.path[0]) {
          profileErrors.value[err.path[0] as string] = err.message;
        }
      });
    }
    else {
      console.error('Profile update error:', error);
      toast.add({
        title: 'Error',
        description: 'An unexpected error occurred',
        color: 'error',
      });
    }
  }
}

function changeTheme(theme: string) {
  colorMode.preference = theme;
  toast.add({
    title: 'Theme Updated',
    description: `Switched to ${theme} theme`,
    color: 'success',
  });
}

// Page meta
definePageMeta({
  middleware: ['auth'],
  layout: 'default',
});
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Page Header -->
    <div class="mb-8">
      <div class="flex items-center space-x-4 mb-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Settings
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">
            Manage your account settings and preferences
          </p>
        </div>
      </div>
    </div>

    <div class="grid gap-8">
      <!-- Profile Settings -->
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <UIcon name="i-heroicons-user-circle" class="text-2xl text-primary-600 dark:text-primary-400" />
              <div>
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                  Profile Information
                </h2>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Update your account profile information
                </p>
              </div>
            </div>
            <UButton
              v-if="!isEditingProfile"
              icon="i-heroicons-pencil"
              variant="outline"
              @click="startEditing"
            >
              Edit Profile
            </UButton>
          </div>
        </template>

        <div class="space-y-6">
          <!-- Email (Read-only) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Email Address
            </label>
            <UInput
              v-model="profileForm.email"
              type="email"
              disabled
              icon="i-heroicons-envelope"
              placeholder="Email address"
            />
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Email cannot be changed. Contact support if you need to update your email.
            </p>
          </div>

          <!-- Username -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Username
            </label>
            <UInput
              v-model="profileForm.username"
              :disabled="!isEditingProfile"
              icon="i-heroicons-user"
              placeholder="Username"
              :color="profileErrors.username ? 'error' : 'primary'"
            />
            <p v-if="profileErrors.username" class="text-sm text-red-600 dark:text-red-400 mt-1">
              {{ profileErrors.username }}
            </p>
          </div>

          <!-- Full Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Full Name
            </label>
            <UInput
              v-model="profileForm.fullName"
              :disabled="!isEditingProfile"
              icon="i-heroicons-identification"
              placeholder="Full name"
              :color="profileErrors.fullName ? 'error' : 'primary'"
            />
            <p v-if="profileErrors.fullName" class="text-sm text-red-600 dark:text-red-400 mt-1">
              {{ profileErrors.fullName }}
            </p>
          </div>

          <!-- Action Buttons -->
          <div v-if="isEditingProfile" class="flex items-center space-x-3 pt-4">
            <UButton
              color="primary"
              :loading="isLoading"
              @click="saveProfile"
            >
              Save Changes
            </UButton>
            <UButton
              variant="outline"
              color="neutral"
              @click="cancelEditing"
            >
              Cancel
            </UButton>
          </div>
        </div>
      </UCard>

      <!-- Theme Settings -->
      <UCard>
        <template #header>
          <div class="flex items-center space-x-3">
            <UIcon name="i-heroicons-paint-brush" class="text-2xl text-primary-600 dark:text-primary-400" />
            <div>
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                Appearance
              </h2>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                Customize the look and feel of your application
              </p>
            </div>
          </div>
        </template>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
              Theme Preference
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div
                v-for="theme in themeOptions"
                :key="theme.value"
                class="relative"
              >
                <input
                  :id="theme.value"
                  v-model="colorMode.preference"
                  :value="theme.value"
                  type="radio"
                  class="sr-only"
                  @change="changeTheme(theme.value)"
                >
                <label
                  :for="theme.value"
                  class="flex items-center justify-center p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 hover:bg-gray-50 dark:hover:bg-gray-800"
                  :class="[
                    colorMode.preference === theme.value
                      ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                      : 'border-gray-200 dark:border-gray-700',
                  ]"
                >
                  <div class="text-center">
                    <UIcon :name="theme.icon" class="text-2xl mb-2 mx-auto" />
                    <div class="text-sm font-medium">{{ theme.label }}</div>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Account Management -->
      <UCard>
        <template #header>
          <div class="flex items-center space-x-3">
            <UIcon name="i-heroicons-shield-check" class="text-2xl text-primary-600 dark:text-primary-400" />
            <div>
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                Account Management
              </h2>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                Manage your account security and data
              </p>
            </div>
          </div>
        </template>

        <div class="space-y-6">
          <!-- Account Statistics -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div class="flex items-center space-x-3">
                <UIcon name="i-heroicons-calendar" class="text-lg text-blue-600 dark:text-blue-400" />
                <div>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    Member Since
                  </p>
                  <p class="font-semibold text-gray-900 dark:text-white">
                    {{ userProfile?.createdAt ? new Date(userProfile.createdAt).toLocaleDateString() : 'N/A' }}
                  </p>
                </div>
              </div>
            </div>
            <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div class="flex items-center space-x-3">
                <UIcon name="i-heroicons-clock" class="text-lg text-green-600 dark:text-green-400" />
                <div>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    Last Updated
                  </p>
                  <p class="font-semibold text-gray-900 dark:text-white">
                    {{ userProfile?.createdAt ? new Date(userProfile.createdAt).toLocaleDateString() : 'N/A' }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Danger Zone -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <div class="flex items-start space-x-3">
                <UIcon name="i-heroicons-exclamation-triangle" class="text-red-600 dark:text-red-400 mt-0.5" />
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
                    Danger Zone
                  </h3>
                  <p class="text-sm text-red-700 dark:text-red-300 mt-1">
                    These actions cannot be undone. Please be careful.
                  </p>
                  <div class="mt-4 space-y-3">
                    <UButton
                      color="error"
                      variant="outline"
                      size="sm"
                      @click="console.error('Password change not implemented')"
                    >
                      Change Password
                    </UButton>
                    <UButton
                      color="error"
                      variant="outline"
                      size="sm"
                      @click="console.error('Account deletion not implemented')"
                    >
                      Delete Account
                    </UButton>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Privacy & Data -->
      <UCard>
        <template #header>
          <div class="flex items-center space-x-3">
            <UIcon name="i-heroicons-lock-closed" class="text-2xl text-primary-600 dark:text-primary-400" />
            <div>
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                Privacy & Data
              </h2>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                Control your data and privacy settings
              </p>
            </div>
          </div>
        </template>

        <div class="space-y-6">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">
                  Data Export
                </p>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Download a copy of your data including watchlists and preferences
                </p>
              </div>
              <UButton
                variant="outline"
                size="sm"
                @click="console.error('Data export not implemented')"
              >
                Export Data
              </UButton>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">
                  Privacy Policy
                </p>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  View our privacy policy and data handling practices
                </p>
              </div>
              <UButton
                variant="outline"
                size="sm"
                @click="console.error('Privacy policy not implemented')"
              >
                View Policy
              </UButton>
            </div>
          </div>
        </div>
      </UCard>
    </div>
  </div>
</template>
