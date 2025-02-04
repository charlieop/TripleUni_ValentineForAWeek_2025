<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <h2>你正在拒绝第二轮的匹配结果</h2>
      </template>
      <p>
        我们不建议你在第二轮拒绝匹配。 <br>
        如果你选择拒绝此轮匹配，
        你与对方的匹配<strong>即刻作废</strong>，你将立刻退出本次活动。
      </p>
      <p>
        此选择是<strong>不可反悔</strong>的: 一旦拒绝此匹配,
        你将<strong>无法</strong>重新选择接受。
      </p>
      <p>
        请注意: <br />

        如果你不接受本次匹配结果，我们<strong>不会</strong>再为你匹配任何人选。
        你将会自动退出本次活动，你支付的押金将在活动结束后统一退还。 <br>
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
  if (matchInfo === null || matchInfo.matchId <= 0) {
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
