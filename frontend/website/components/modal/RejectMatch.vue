<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <h2>你正在拒绝第一轮的匹配结果</h2>
      </template>
      <p>
        如果你选择拒绝此轮匹配结果，
        你与对方的匹配结果<strong>即刻作废</strong>，双方都将进入第二轮重新进行匹配。
      </p>
      <p>
        此选择是<strong>不可反悔</strong>的: 一旦拒绝此匹配,
        你将<strong>无法</strong>重新选择接受。
      </p>
      <p>
        请注意: <br />

        我们<strong>不能保证</strong>在第二轮匹配中为你找到合适的对象。
        在第二轮匹配中你可能：匹配失败、仍然匹配到对方、匹配到其他不愿意接受的对象。
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
            >拒绝此匹配</UButton
          >
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
const $emit = defineEmits(["close"]);
const loading = ref(false);

const { postMatchConfirmation } = useHttp();
const { getMatchInfo, setMatchInfo } = useStore();
const router = useRouter();

function handleCancelApplication() {
  const matchInfo = getMatchInfo();
  if (matchInfo === null) {
    alert("意料之外的错误: 找不到本地match info");
    router.push("/");
    return;
  }
  loading.value = true;
  postMatchConfirmation(matchInfo.matchId, false)
    .then(() => {
      setMatchInfo(matchInfo.matchId, matchInfo.round, true);
      refresh();
    })
    .catch((error: Error) => {
      alert("取消配对失败: " + error.message);
      loading.value = false;
      $emit("close");
    });
}
</script>

<style scoped>
h2 {
  font-size: var(--fs-500);
}
p {
  margin-bottom: 1rem;
}

.button-group {
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-between;
  padding-inline: 0.5rem;
}
</style>
