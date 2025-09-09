<template>
  <div>
    <h1>Auth Page</h1>
    <ClientOnly fallback-tag="span" fallback="Loading comments...">
      <AuthView />
    </ClientOnly>
  </div>
</template>
