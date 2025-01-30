<template>
  <div class="application-form-wrapper">
    <FormNewApplication />
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2025 | 报名",
});
</script>

<style scoped>
.application-form-wrapper {
  height: 100%;
  padding: 3rem 2rem;
  overflow: scroll;
  overflow-x: hidden;
  overflow-x: clip;
}
</style>
