<script setup lang="ts">
type Props = {
  modelValue: string;
  placeholder?: string;
  loading?: boolean;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
};

type Emits = {
  'update:modelValue': [value: string];
  'search': [];
};

const _props = withDefaults(defineProps<Props>(), {
  placeholder: 'Search...',
  loading: false,
  disabled: false,
  size: 'md',
});

const emit = defineEmits<Emits>();

function handleKeyup(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    emit('search');
  }
}

function handleSearch() {
  emit('search');
}
</script>

<template>
  <div class="flex gap-4" data-testid="search-input-container">
    <UInput
      :model-value="modelValue"
      :placeholder="placeholder"
      :size="size"
      :loading="loading"
      :disabled="disabled"
      class="flex-1"
      data-testid="search-input-field"
      @update:model-value="$emit('update:modelValue', $event)"
      @keyup="handleKeyup"
    >
      <template #leading>
        <UIcon name="i-heroicons-magnifying-glass" />
      </template>
    </UInput>
    <UButton
      :size="size"
      :loading="loading"
      :disabled="disabled || !modelValue.trim()"
      data-testid="search-button"
      @click="handleSearch"
    >
      Search
    </UButton>
  </div>
</template>
