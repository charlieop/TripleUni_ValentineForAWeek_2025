<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <h2>帮助</h2>
      </template>
      <p>如果遇到了问题，可以先尝试通过[清除页面缓存]解决。</p>
      <br />
      <p>如果问题持续存在，请联系负责人、你的Mentor或是网站维护者。</p>
      <br />
      <p>
        活动负责人: <br />
        - 微信号: Xanaduwithinzenith-
      </p>
      <p>
        网站维护者: <br />
        - 微信号: charlieop_
      </p>
      <br />
      <template #footer>
        <div class="button-group">
          <UButton @click="clearCache" color="amber" variant="solid"
            >清除页面缓存</UButton
          >
          <UButton @click="$emit('close')">我已知晓</UButton>
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
const router = useRouter();
const mentorWechat = ref("加载中...");

function clearCache() {
  const {
    clearApplicantId,
    clearDeleted,
    clearOpenId,
    clearMatchInfo,
    clearPaid,
  } = useStore();
  const { clearConfig } = useReactive();
  clearApplicantId();
  clearDeleted();
  clearOpenId();
  clearMatchInfo();
  clearConfig();
  clearPaid();
  router.push("/login");
}
</script>

<style scoped>
h2 {
  font-size: var(--fs-500);
}
.button-group {
  display: flex;
  justify-content: space-between;
  padding-inline: 0.5rem;
}
</style>
