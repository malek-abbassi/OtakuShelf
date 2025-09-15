<script setup lang="ts">
type Props = {
  title?: string;
  description?: string;
  icon?: string;
  actionText?: string;
  showAction?: boolean;
  illustration?: string;
};

const _props = withDefaults(defineProps<Props>(), {
  title: 'No items found',
  description: 'Get started by adding your first item.',
  icon: 'i-heroicons-inbox',
  actionText: 'Get Started',
  showAction: true,
});

const emit = defineEmits<{
  action: [];
}>();

function handleAction() {
  emit('action');
}
</script>

<template>
  <div class="text-center py-12">
    <!-- Illustration or Icon -->
    <div class="mx-auto mb-6">
      <NuxtImg
        v-if="illustration"
        :src="illustration"
        :alt="title"
        class="w-48 h-48 mx-auto opacity-60"
        loading="lazy"
      />
      <div
        v-else
        class="w-16 h-16 mx-auto rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center"
      >
        <UIcon
          :name="icon"
          class="text-2xl text-gray-400 dark:text-gray-600"
        />
      </div>
    </div>

    <!-- Title -->
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
      {{ title }}
    </h3>

    <!-- Description -->
    <p class="text-gray-600 dark:text-gray-400 text-sm mb-8 max-w-md mx-auto">
      {{ description }}
    </p>

    <!-- Action -->
    <div v-if="showAction" class="flex justify-center">
      <UButton
        color="primary"
        variant="solid"
        @click="handleAction"
      >
        <UIcon name="i-heroicons-plus" class="mr-2" />
        {{ actionText }}
      </UButton>
    </div>

    <!-- Additional content slot -->
    <slot />
  </div>
</template>
