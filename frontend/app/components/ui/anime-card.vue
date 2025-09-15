<script setup lang="ts">
type AnimeData = {
  id: number;
  title: string;
  coverImage?: string;
  averageScore?: number;
  status?: string;
  format?: string;
  episodes?: number;
  startDate?: {
    year?: number;
    month?: number;
    day?: number;
  };
  genres?: string[];
  description?: string;
};

type Props = {
  anime: AnimeData;
  variant?: 'default' | 'compact' | 'detailed';
  showWatchlistButton?: boolean;
  isInWatchlist?: boolean;
  isLoading?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  showWatchlistButton: true,
  isInWatchlist: false,
  isLoading: false,
});

const emit = defineEmits<{
  addToWatchlist: [anime: AnimeData];
  removeFromWatchlist: [animeId: number];
  click: [anime: AnimeData];
}>();

// Computed properties
const formattedScore = computed(() => {
  if (!props.anime.averageScore)
    return 'N/A';
  return `${(props.anime.averageScore / 10).toFixed(1)}/10`;
});

const formattedDate = computed(() => {
  const date = props.anime.startDate;
  if (!date?.year)
    return 'TBA';

  const months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
  ];

  const month = date.month ? months[date.month - 1] : '';
  return `${month} ${date.year}`.trim();
});

const statusColor = computed(() => {
  switch (props.anime.status?.toUpperCase()) {
    case 'RELEASING':
      return 'success';
    case 'FINISHED':
      return 'neutral';
    case 'NOT_YET_RELEASED':
      return 'warning';
    case 'CANCELLED':
      return 'error';
    default:
      return 'neutral';
  }
});

const truncatedDescription = computed(() => {
  if (!props.anime.description)
    return '';
  const maxLength = props.variant === 'detailed' ? 200 : 100;
  return props.anime.description.length > maxLength
    ? `${props.anime.description.slice(0, maxLength)}...`
    : props.anime.description;
});

// Methods
function handleWatchlistToggle() {
  if (props.isInWatchlist) {
    emit('removeFromWatchlist', props.anime.id);
  }
  else {
    emit('addToWatchlist', props.anime);
  }
}

function handleCardClick() {
  emit('click', props.anime);
}
</script>

<template>
  <UCard
    class="group transition-all duration-200 hover:shadow-lg hover:-translate-y-1 cursor-pointer"
    :class="{
      'h-full': variant !== 'compact',
    }"
    @click="handleCardClick"
  >
    <!-- Compact variant -->
    <template v-if="variant === 'compact'">
      <div class="flex space-x-3">
        <!-- Cover Image -->
        <div class="flex-shrink-0">
          <NuxtImg
            :src="anime.coverImage || '/placeholder-anime.jpg'"
            :alt="anime.title"
            class="w-16 h-20 rounded-lg object-cover"
            loading="lazy"
            placeholder
            :modifiers="{ width: 64, height: 80, quality: 80 }"
          />
        </div>

        <!-- Content -->
        <div class="flex-1 min-w-0">
          <h3 class="font-semibold text-gray-900 dark:text-white text-sm line-clamp-2 mb-1">
            {{ anime.title }}
          </h3>

          <div class="flex items-center space-x-2 mb-2">
            <UBadge
              v-if="anime.status"
              :color="statusColor"
              variant="subtle"
              size="xs"
            >
              {{ anime.status.replace('_', ' ') }}
            </UBadge>
            <span class="text-xs text-gray-500">{{ formattedDate }}</span>
          </div>

          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-primary-600 dark:text-primary-400">
              {{ formattedScore }}
            </span>

            <UButton
              v-if="showWatchlistButton"
              :color="isInWatchlist ? 'error' : 'primary'"
              variant="ghost"
              size="xs"
              :loading="isLoading"
              @click.stop="handleWatchlistToggle"
            >
              <UIcon :name="isInWatchlist ? 'i-heroicons-heart-solid' : 'i-heroicons-heart'" />
            </UButton>
          </div>
        </div>
      </div>
    </template>

    <!-- Default and detailed variants -->
    <template v-else>
      <div class="flex flex-col h-full">
        <!-- Cover Image -->
        <div class="relative overflow-hidden rounded-lg mb-3">
          <NuxtImg
            :src="anime.coverImage || '/placeholder-anime.jpg'"
            :alt="anime.title"
            class="w-full h-48 object-cover transition-transform duration-200 group-hover:scale-105"
            loading="lazy"
            placeholder
            preset="cover"
          />

          <!-- Score overlay -->
          <div
            v-if="anime.averageScore"
            class="absolute top-2 right-2 bg-black/70 text-white text-xs font-semibold px-2 py-1 rounded-full"
          >
            {{ formattedScore }}
          </div>

          <!-- Watchlist button overlay -->
          <div
            v-if="showWatchlistButton"
            class="absolute top-2 left-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200"
          >
            <UButton
              :color="isInWatchlist ? 'error' : 'primary'"
              variant="solid"
              size="xs"
              :loading="isLoading"
              @click.stop="handleWatchlistToggle"
            >
              <UIcon :name="isInWatchlist ? 'i-heroicons-heart-solid' : 'i-heroicons-heart'" />
            </UButton>
          </div>
        </div>

        <!-- Content -->
        <div class="flex-1 flex flex-col">
          <!-- Title -->
          <h3 class="font-semibold text-gray-900 dark:text-white text-sm line-clamp-2 mb-2">
            {{ anime.title }}
          </h3>

          <!-- Metadata -->
          <div class="flex items-center justify-between mb-2">
            <UBadge
              v-if="anime.status"
              :color="statusColor"
              variant="subtle"
              size="xs"
            >
              {{ anime.status.replace('_', ' ') }}
            </UBadge>

            <span class="text-xs text-gray-500">{{ formattedDate }}</span>
          </div>

          <!-- Format and Episodes -->
          <div v-if="anime.format || anime.episodes" class="text-xs text-gray-500 mb-2">
            <span v-if="anime.format">{{ anime.format }}</span>
            <span v-if="anime.format && anime.episodes"> • </span>
            <span v-if="anime.episodes">{{ anime.episodes }} episodes</span>
          </div>

          <!-- Genres (detailed variant only) -->
          <div v-if="variant === 'detailed' && anime.genres?.length" class="mb-2">
            <div class="flex flex-wrap gap-1">
              <UBadge
                v-for="genre in anime.genres.slice(0, 3)"
                :key="genre"
                variant="soft"
                size="xs"
              >
                {{ genre }}
              </UBadge>
              <UBadge
                v-if="anime.genres.length > 3"
                variant="soft"
                size="xs"
                color="neutral"
              >
                +{{ anime.genres.length - 3 }}
              </UBadge>
            </div>
          </div>

          <!-- Description (detailed variant only) -->
          <p
            v-if="variant === 'detailed' && truncatedDescription"
            class="text-xs text-gray-600 dark:text-gray-400 line-clamp-3 flex-1"
          >
            {{ truncatedDescription }}
          </p>

          <!-- Footer spacer -->
          <div class="flex-1" />
        </div>
      </div>
    </template>
  </UCard>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
