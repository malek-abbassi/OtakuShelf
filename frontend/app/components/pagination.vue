<script setup lang="ts">
type Props = {
  currentPage: number;
  totalPages: number;
  hasNextPage: boolean;
  hasPreviousPage?: boolean;
};

type Emits = {
  changePage: [page: number];
};

const { currentPage, hasNextPage } = defineProps<Props>();
const emit = defineEmits<Emits>();

function goToPrevious() {
  if (currentPage > 1) {
    emit('changePage', currentPage - 1);
  }
}

function goToNext() {
  if (hasNextPage) {
    emit('changePage', currentPage + 1);
  }
}
</script>

<template>
  <div v-if="totalPages > 1" class="flex gap-2 justify-center items-center">
    <UButton
      variant="outline"
      size="sm"
      :disabled="currentPage === 1"
      @click="goToPrevious"
    >
      Previous
    </UButton>
    <span class="flex items-center px-3 text-sm">
      Page {{ currentPage }} of {{ totalPages }}
    </span>
    <UButton
      variant="outline"
      size="sm"
      :disabled="!hasNextPage"
      @click="goToNext"
    >
      Next
    </UButton>
  </div>
</template>
