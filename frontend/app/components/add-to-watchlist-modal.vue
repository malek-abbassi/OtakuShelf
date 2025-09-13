<script setup lang="ts">
import type { Anime } from '~/composables/use-ani-list';
import type { WatchlistAddSchema } from '~/types/watchlist';

import { useWatchlist } from '~/composables/use-watchlist';
import { WATCH_STATUS_OPTIONS } from '~/types/watchlist';

type Props = {
  anime: Anime | null;
  open: boolean;
};

type Emits = {
  'update:open': [value: boolean];
  'added': [anime: Anime];
};

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// Composables
const { addToWatchlist } = useWatchlist();

// Form state
const selectedStatus = ref('plan_to_watch');
const userNotes = ref('');
const isSubmitting = ref(false);

// Computed
const isOpen = computed({
  get: () => props.open,
  set: value => emit('update:open', value),
});

const animeTitle = computed(() => {
  if (!props.anime)
    return '';
  return props.anime.title.romaji || props.anime.title.english || props.anime.title.native || 'Unknown Title';
});

// Methods
async function handleSubmit() {
  if (!props.anime)
    return;

  isSubmitting.value = true;

  try {
    const animeData: WatchlistAddSchema = {
      animeId: props.anime.id,
      animeTitle: animeTitle.value,
      animePictureUrl: props.anime.coverImage.large || props.anime.coverImage.medium,
      animeScore: props.anime.averageScore || props.anime.meanScore || undefined,
      status: selectedStatus.value,
      notes: userNotes.value.trim() || undefined,
    };

    const result = await addToWatchlist(animeData);

    if (result.success) {
      emit('added', props.anime);
      handleClose();
    }
  }
  catch (err) {
    console.error('Error adding to watchlist:', err);
  }
  finally {
    isSubmitting.value = false;
  }
}

function handleClose() {
  isOpen.value = false;
  // Reset form
  selectedStatus.value = 'plan_to_watch';
  userNotes.value = '';
}

// Watch for anime changes to reset form
watch(() => props.anime, () => {
  selectedStatus.value = 'plan_to_watch';
  userNotes.value = '';
});
</script>

<template>
  <UModal
    v-model:open="isOpen"
    title="Add to Watchlist"
    :ui="{
      content: 'max-w-md w-full',
    }"
  >
    <template v-if="anime" #body="{ close }">
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
            @click="handleSubmit"
          >
            Add to Watchlist
          </UButton>
        </div>
      </div>
    </template>
  </UModal>
</template>
