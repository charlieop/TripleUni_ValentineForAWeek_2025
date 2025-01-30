<template>
  <div class="app-wrapper">
    <NuxtRouteAnnouncer />

    <div class="app">
      <NuxtPage />
    </div>
    <ModalScreenSizeWarning
      :model-value="displayScreenSizeWarning"
      @close="displayScreenSizeWarning = false"
    />
    <ModalRequireWeChat :model-value="!isWechat" />

    <UNotifications />
    <UModals />
  </div>
</template>

<script setup lang="ts">
import { ModalRequireWeChat } from "#components";

const displayScreenSizeWarning = ref(false);

onMounted(() => {
  if (window.innerWidth < 375 || window.innerHeight < 650) {
    displayScreenSizeWarning.value = true;
  }
});
</script>

<style scoped>
.app-wrapper {
  background-color: rgb(238, 235, 235);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  height: 100svh;
}

.app {
  background-color: var(--clr-background);
  width: var(--width);
  height: var(--height);
}
</style>
