<template>
  <h1>Hi</h1>
  <p>Here is some text</p>
  <router-link to="/login"><UButton>Go to Login</UButton></router-link>
  <UButton @click="logout">Log Out</UButton>
  <router-link to="/application"
    ><UButton>Go to Application</UButton></router-link
  >
</template>

<script setup>
function logout() {
  localStorage.removeItem("openId");
}

onMounted(() => {});
</script>

<style scoped>
button {
  margin: 10px;
}
</style>
