<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
    preventClose
  >
    <UCard>
      <template #header>
        <h2>服务器正在维护中</h2>
      </template>
      <p>服务器正在维护中，暂时无法响应你的操作。</p>
      <br />
      <p>请在稍后重试。</p>
      <template #footer> </template>
    </UCard>
  </UModal>
</template>

<style scoped>
h2 {
  font-size: var(--fs-500);
  font-weight: bold;
}
</style>
