<script lang="ts" setup>
import type { WatchlistItem } from '~/types/watchlist';

import { getStatusInfo } from '~/types/watchlist';

type WatchlistCardProps = {
  item: WatchlistItem;
  showActions?: boolean;
};

type WatchlistCardEmits = {
  edit: [item: WatchlistItem];
  remove: [item: WatchlistItem];
  statusChange: [item: WatchlistItem, newStatus: string];
};

const props = withDefaults(defineProps<WatchlistCardProps>(), {
  showActions: true,
});

const emit = defineEmits<WatchlistCardEmits>();

// Get status info for display
const statusInfo = computed(() => getStatusInfo(props.item.status));

// Format date for display
const addedDate = computed(() => {
  return new Date(props.item.createdAt).toLocaleDateString();
});

// Handle status change
function handleStatusChange(newStatus: string) {
  emit('statusChange', props.item, newStatus);
}

// Handle edit
function handleEdit() {
  emit('edit', props.item);
}

// Handle remove
function handleRemove() {
  emit('remove', props.item);
}

// Score display
const scoreDisplay = computed(() => {
  return props.item.animeScore ? `${props.item.animeScore}/10` : 'Not rated';
});
</script>

<template>
  <UCard class="hover:shadow-lg transition-shadow duration-200">
    <div class="flex gap-4">
      <!-- Anime Image -->
      <div class="flex-shrink-0">
        <NuxtImg
          v-if="item.animePictureUrl"
          :src="item.animePictureUrl"
          :alt="item.animeTitle"
          class="w-20 h-28 object-cover rounded-lg"
          loading="lazy"
        />
        <div
          v-else
          class="w-20 h-28 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center"
        >
          <UIcon
            name="i-heroicons-photo"
            class="w-8 h-8 text-gray-400"
          />
        </div>
      </div>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <div class="flex items-start justify-between gap-2">
          <h3 class="font-semibold text-gray-900 dark:text-white truncate">
            {{ item.animeTitle }}
          </h3>

          <!-- Status Badge -->
          <UBadge
            :color="statusInfo.color"
            variant="subtle"
            size="sm"
          >
            {{ statusInfo.label }}
          </UBadge>
        </div>

        <div class="mt-2 space-y-1 text-sm text-gray-600 dark:text-gray-300">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-star" class="w-4 h-4" />
            <span>{{ scoreDisplay }}</span>
          </div>

          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-calendar" class="w-4 h-4" />
            <span>Added {{ addedDate }}</span>
          </div>
        </div>

        <!-- Notes -->
        <div
          v-if="item.notes"
          class="mt-2"
        >
          <p class="text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
            {{ item.notes }}
          </p>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <template v-if="showActions" #footer>
      <div class="flex items-center justify-between">
        <UDropdown
          :items="[
            [
              {
                label: 'Plan to Watch',
                icon: 'i-heroicons-clock',
                click: () => handleStatusChange('plan_to_watch'),
              },
              {
                label: 'Watching',
                icon: 'i-heroicons-play',
                click: () => handleStatusChange('watching'),
              },
              {
                label: 'Completed',
                icon: 'i-heroicons-check-circle',
                click: () => handleStatusChange('completed'),
              },
              {
                label: 'On Hold',
                icon: 'i-heroicons-pause',
                click: () => handleStatusChange('on_hold'),
              },
              {
                label: 'Dropped',
                icon: 'i-heroicons-x-circle',
                click: () => handleStatusChange('dropped'),
              },
            ],
          ]"
        >
          <UButton
            variant="outline"
            size="sm"
            icon="i-heroicons-arrow-path"
            trailing-icon="i-heroicons-chevron-down"
          >
            Change Status
          </UButton>
        </UDropdown>

        <div class="flex gap-2">
          <UButton
            variant="ghost"
            size="sm"
            icon="i-heroicons-pencil"
            @click="handleEdit"
          >
            Edit
          </UButton>

          <UButton
            variant="ghost"
            size="sm"
            icon="i-heroicons-trash"
            color="error"
            @click="handleRemove"
          >
            Remove
          </UButton>
        </div>
      </div>
    </template>
  </UCard>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
