<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <h2>你的屏幕尺寸较小</h2>
      </template>
      <p>
        你的屏幕宽度或高度小于我们设计的最小尺寸, 这可能导致意料之外的显示错误,
        建议检查你的屏幕缩放设置/ 更换设备查看。
      </p>
      <br />
      <p>你也可以选择继续使用此设备查看, 但是显示效果可能不如预期。</p>
      <template #footer>
        <UButton @click="$emit('close')">我已知晓</UButton>
      </template>
    </UCard>
  </UModal>
</template>

<style scoped>
h2 {
  font-size: var(--fs-500);
}
</style>
