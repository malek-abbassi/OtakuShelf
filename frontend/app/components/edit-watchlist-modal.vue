<script setup lang="ts">
import type { WatchlistItem } from '~/types/watchlist';

import { useWatchlist } from '~/composables/use-watchlist';
import { WATCH_STATUS_OPTIONS } from '~/types/watchlist';

type Props = {
  item: WatchlistItem | null;
  open: boolean;
};

type Emits = {
  'update:open': [value: boolean];
  'updated': [];
};

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// Composables
const { updateWatchlistItem } = useWatchlist();
const toast = useToast();

// Form state
const form = ref({
  status: '',
  notes: '',
  animeScore: null as number | null,
});

const isSubmitting = ref(false);

// Status options for dropdown
const statusOptions = computed(() => [
  [
    {
      label: 'Plan to Watch',
      icon: 'i-heroicons-clock',
      value: 'plan_to_watch',
      onSelect() {
        form.value.status = 'plan_to_watch';
      },
    },
    {
      label: 'Watching',
      icon: 'i-heroicons-play',
      value: 'watching',
      onSelect() {
        form.value.status = 'watching';
      },
    },
    {
      label: 'Completed',
      icon: 'i-heroicons-check-circle',
      value: 'completed',
      onSelect() {
        form.value.status = 'completed';
      },
    },
    {
      label: 'On Hold',
      icon: 'i-heroicons-pause',
      value: 'on_hold',
      onSelect() {
        form.value.status = 'on_hold';
      },
    },
    {
      label: 'Dropped',
      icon: 'i-heroicons-x-circle',
      value: 'dropped',
      onSelect() {
        form.value.status = 'dropped';
      },
    },
  ],
]);

// Get current status info for display
const currentStatusInfo = computed(() => {
  const statusIconMap = {
    plan_to_watch: 'i-heroicons-clock',
    watching: 'i-heroicons-play',
    completed: 'i-heroicons-check-circle',
    on_hold: 'i-heroicons-pause',
    dropped: 'i-heroicons-x-circle',
  };

  const currentStatus = WATCH_STATUS_OPTIONS.find(option => option.value === form.value.status);
  const status = currentStatus || WATCH_STATUS_OPTIONS[0];

  return {
    ...status,
    icon: statusIconMap[status.value as keyof typeof statusIconMap] || 'i-heroicons-question-mark-circle',
  };
});

// Computed
const isOpen = computed({
  get: () => props.open,
  set: value => emit('update:open', value),
});

// Watch for item changes to update form
watch(() => props.item, (newItem) => {
  if (newItem) {
    const animeScore = newItem.animeScore || (newItem as any).anime_score || null;
    form.value = {
      status: newItem.status || 'plan_to_watch',
      notes: newItem.notes || '',
      animeScore,
    };
  }
}, { immediate: true });

// Computed properties to handle field name variations
const animeTitle = computed(() => {
  return props.item?.animeTitle || (props.item as any)?.anime_title || '';
});

const animePictureUrl = computed(() => {
  return props.item?.animePictureUrl || (props.item as any)?.anime_picture_url || null;
});

const createdAt = computed(() => {
  return props.item?.createdAt || (props.item as any)?.created_at;
});

const addedDate = computed(() => {
  const date = createdAt.value;
  if (!date)
    return 'Unknown';
  try {
    return new Date(date).toLocaleDateString();
  }
  catch {
    return 'Invalid Date';
  }
});

// Methods
async function handleSubmit() {
  if (!props.item)
    return;

  isSubmitting.value = true;
  try {
    await updateWatchlistItem(props.item.id, {
      status: form.value.status,
      notes: form.value.notes.trim() || undefined,
      animeScore: form.value.animeScore || undefined,
    });

    toast.add({
      title: 'Success',
      description: 'Watchlist item updated successfully',
      color: 'success',
    });

    emit('updated');
    handleClose();
  }
  catch (error) {
    console.error('Error updating watchlist item:', error);
    toast.add({
      title: 'Error',
      description: 'Failed to update watchlist item',
      color: 'error',
    });
  }
  finally {
    isSubmitting.value = false;
  }
}

function handleClose() {
  isOpen.value = false;
}
</script>

<template>
  <UModal
    v-model:open="isOpen"
    title="Edit Watchlist Item"
    :ui="{
      content: 'max-w-md w-full',
    }"
  >
    <template v-if="item" #body>
      <div class="space-y-6">
        <!-- Anime Info -->
        <div class="flex gap-4">
          <NuxtImg
            v-if="animePictureUrl"
            :src="animePictureUrl"
            :alt="animeTitle"
            class="w-16 h-20 object-cover rounded-lg flex-shrink-0"
            loading="lazy"
          />
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-gray-900 dark:text-white truncate">
              {{ animeTitle }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
              Added {{ addedDate }}
            </p>
          </div>
        </div>

        <!-- Form -->
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <!-- Status -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Status
            </label>
            <UDropdownMenu :items="statusOptions">
              <UButton
                variant="outline"
                class="w-full justify-between"
                :icon="currentStatusInfo.icon"
                trailing-icon="i-heroicons-chevron-down"
              >
                {{ currentStatusInfo.label }}
              </UButton>
            </UDropdownMenu>
          </div>

          <!-- Score -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Your Rating (1-10)
            </label>
            <UInput
              v-model.number="form.animeScore"
              type="number"
              min="0"
              max="10"
              step="0.1"
              placeholder="Optional rating"
            />
          </div>

          <!-- Notes -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Notes
            </label>
            <UTextarea
              v-model="form.notes"
              placeholder="Add your thoughts about this anime..."
              :maxlength="1000"
              :rows="3"
            />
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-3 pt-4">
            <UButton
              variant="ghost"
              :disabled="isSubmitting"
              @click="handleClose"
            >
              Cancel
            </UButton>
            <UButton
              type="submit"
              :loading="isSubmitting"
              :disabled="isSubmitting"
            >
              Update
            </UButton>
          </div>
        </form>
      </div>
    </template>
  </UModal>
</template>
