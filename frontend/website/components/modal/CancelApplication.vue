<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <h2>你正在取消提交的报名</h2>
      </template>
      <p>请注意:</p>
      <p>如果你选择取消报名, 你将不会被匹配算法选中。</p>
      <p>
        此选择是 <strong>不可反悔</strong> 的: 一旦报名取消, 你将
        <strong>无法</strong> 重新报名。
      </p>
      <template #footer>
        <div class="button-group">
          <UButton
            @click="$emit('close')"
            color="lime"
            variant="solid"
            :disabled="loading"
            >返回</UButton
          >
          <UButton
            @click="handleCancelApplication"
            color="red"
            variant="outline"
            :loading="loading"
            :disabled="loading"
            >取消我的报名</UButton
          >
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
const { deleteApplicant } = useHttp();
const { getApplicantId } = useStore();

const $emit = defineEmits(["close"]);
const loading = ref(false);

function handleCancelApplication() {
  const id = getApplicantId();
  if (id == null) {
    alert("无法获取报名者ID");
    return;
  }
  loading.value = true;
  deleteApplicant(id)
    .then(() => {
      $emit("close");
    })
    .catch((error: Error) => {
      alert("取消报名失败: " + error.message);
      loading.value = false;
    });
}
</script>

<style scoped>
h2 {
  font-size: var(--fs-500);
}

.button-group {
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-between;
  padding-inline: 0.5rem;
}
</style>
