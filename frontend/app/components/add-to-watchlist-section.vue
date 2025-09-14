<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';
import type { WatchlistAddSchema } from '~/types/watchlist';

import { useAuth } from '~/composables/use-auth';
import { useWatchlist } from '~/composables/use-watchlist';
import { WATCH_STATUS_OPTIONS } from '~/types/watchlist';

type Props = {
  anime: Anime;
};

type Emits = {
  addedToWatchlist: [anime: Anime];
};

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// Composables
const { addToWatchlist, checkAnimeInWatchlist } = useWatchlist();
const { isLoggedIn } = useAuth();

// State
const isModalOpen = ref(false);
const selectedStatus = ref('plan_to_watch');
const userNotes = ref('');
const isSubmitting = ref(false);
const isInWatchlist = ref(false);

// Computed
const animeTitle = computed(() => {
  return props.anime.title.romaji || props.anime.title.english || props.anime.title.native || 'Unknown Title';
});

// Check if anime is in watchlist
async function checkWatchlistStatus() {
  if (isLoggedIn.value) {
    try {
      const result = await checkAnimeInWatchlist(props.anime.id);
      isInWatchlist.value = result !== null;
    }
    catch (error) {
      console.error('Error checking watchlist status:', error);
    }
  }
}

// Add to watchlist with modal
async function handleQuickAdd(status: string) {
  if (!isLoggedIn.value) {
    navigateTo('/auth');
    return;
  }

  isSubmitting.value = true;

  try {
    const score = props.anime.averageScore || props.anime.meanScore;
    const imageUrl = props.anime.coverImage.large || props.anime.coverImage.medium;
    const animeData: WatchlistAddSchema = {
      animeId: props.anime.id,
      animeTitle: animeTitle.value,
      animePictureUrl: imageUrl && imageUrl.startsWith('http') ? imageUrl : undefined,
      animeScore: score ? score / 10 : undefined,
      status,
      notes: '',
    };

    const result = await addToWatchlist(animeData);

    if (result.success) {
      isInWatchlist.value = true;
      emit('addedToWatchlist', props.anime);
    }
  }
  catch (err) {
    console.error('Error adding to watchlist:', err);
  }
  finally {
    isSubmitting.value = false;
  }
}

// Add to watchlist with custom notes
async function handleModalSubmit() {
  if (!props.anime)
    return;

  isSubmitting.value = true;

  try {
    const score = props.anime.averageScore || props.anime.meanScore;
    const imageUrl = props.anime.coverImage.large || props.anime.coverImage.medium;
    const animeData: WatchlistAddSchema = {
      animeId: props.anime.id,
      animeTitle: animeTitle.value,
      animePictureUrl: imageUrl && imageUrl.startsWith('http') ? imageUrl : undefined,
      animeScore: score ? score / 10 : undefined,
      status: selectedStatus.value,
      notes: userNotes.value.trim() || undefined,
    };

    const result = await addToWatchlist(animeData);

    if (result.success) {
      isInWatchlist.value = true;
      emit('addedToWatchlist', props.anime);
      handleCloseModal();
    }
  }
  catch (err) {
    console.error('Error adding to watchlist:', err);
  }
  finally {
    isSubmitting.value = false;
  }
}

function handleCloseModal() {
  isModalOpen.value = false;
  selectedStatus.value = 'plan_to_watch';
  userNotes.value = '';
}

// Check watchlist status on mount and when anime changes
watch(() => props.anime, checkWatchlistStatus, { immediate: true });
watch(isLoggedIn, checkWatchlistStatus);
</script>

<template>
  <UCard v-if="!isInWatchlist">
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold">
          Add to Watchlist
        </h3>
        <UIcon name="i-heroicons-plus" class="w-5 h-5 text-gray-500" />
      </div>
    </template>

    <div v-if="isLoggedIn" class="space-y-4">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Track your progress and save this anime to your watchlist.
      </p>

      <!-- Quick Add Buttons -->
      <div class="flex flex-wrap gap-2">
        <UButton
          v-for="option in WATCH_STATUS_OPTIONS.slice(0, 3)"
          :key="option.value"
          :color="option.color || 'primary'"
          variant="soft"
          size="sm"
          :loading="isSubmitting"
          :disabled="isSubmitting"
          @click="handleQuickAdd(option.value)"
        >
          {{ option.label }}
        </UButton>
      </div>

      <!-- Custom Add Button -->
      <UButton
        variant="outline"
        :loading="isSubmitting"
        :disabled="isSubmitting"
        @click="isModalOpen = true"
      >
        <UIcon name="i-heroicons-cog-6-tooth" class="w-4 h-4 mr-2" />
        Add with Custom Options
      </UButton>
    </div>

    <div v-else class="text-center py-4">
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Sign in to add anime to your watchlist
      </p>
      <UButton @click="navigateTo('/auth')">
        Sign In
      </UButton>
    </div>
  </UCard>

  <!-- Already in Watchlist -->
  <UCard v-else>
    <div class="text-center py-4">
      <UIcon name="i-heroicons-check-circle" class="w-12 h-12 mx-auto text-green-500 mb-2" />
      <h3 class="text-lg font-semibold text-green-600 dark:text-green-400 mb-1">
        In Your Watchlist
      </h3>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        This anime is already saved to your watchlist
      </p>
    </div>
  </UCard>

  <!-- Custom Add Modal -->
  <UModal
    v-model:open="isModalOpen"
    title="Add to Watchlist"
    :ui="{ content: 'max-w-md w-full' }"
  >
    <template #body="{ close }">
      <div class="space-y-6">
        <!-- Anime Info -->
        <div class="flex gap-4">
          <div class="flex-shrink-0">
            <NuxtImg
              :src="anime.coverImage.medium || anime.coverImage.large"
              :alt="animeTitle"
              class="w-16 h-20 object-cover rounded-lg"
            />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-medium text-gray-900 dark:text-white truncate">
              {{ animeTitle }}
            </h3>
            <div class="text-sm text-gray-600 dark:text-gray-300 mt-1">
              <div class="flex items-center gap-2">
                <UIcon name="i-heroicons-star" class="w-3 h-3" />
                <span>{{ anime.averageScore || anime.meanScore || 'N/A' }}/100</span>
              </div>
              <div class="flex items-center gap-2 mt-1">
                <UIcon name="i-heroicons-calendar" class="w-3 h-3" />
                <span>{{ anime.seasonYear || 'Unknown' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Status Selection -->
        <UFormGroup label="Watch Status" required>
          <USelectMenu
            v-model="selectedStatus"
            :options="WATCH_STATUS_OPTIONS.map(option => ({
              value: option.value,
              label: option.label,
            }))"
            option-attribute="label"
            value-attribute="value"
          />
        </UFormGroup>

        <!-- Notes -->
        <UFormGroup label="Notes (Optional)">
          <UTextarea
            v-model="userNotes"
            placeholder="Add your thoughts about this anime..."
            :rows="3"
            :maxlength="500"
          />
          <template #help>
            <span class="text-xs text-gray-500">
              {{ userNotes.length }}/500 characters
            </span>
          </template>
        </UFormGroup>

        <!-- Actions -->
        <div class="flex gap-3 justify-end">
          <UButton
            variant="outline"
            @click="close"
          >
            Cancel
          </UButton>
          <UButton
            :loading="isSubmitting"
            :disabled="isSubmitting"
            @click="handleModalSubmit"
          >
            Add to Watchlist
          </UButton>
        </div>
      </div>
    </template>
  </UModal>
</template>
