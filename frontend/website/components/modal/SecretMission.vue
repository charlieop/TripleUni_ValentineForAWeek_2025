<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <h2>你的秘密任务</h2>
      </template>
      <div v-if="mission">
        <h2>
          {{ mission.title }}
        </h2>
        <p>
          每位参与者都有一定几率被分配到一个秘密任务,
          请不要告知你的CP你的秘密任务。
        </p>
        <p>
          你可以选择完成你的秘密任务并在最后一天中上传相关凭证来获取额外的分数
        </p>
        <p>
          你可以在这里查看你的秘密任务:<br />
          <a :href="mission.link" target="_blank">我的秘密任务</a>
        </p>
      </div>
      <p v-else>加载中...</p>
      <template #footer>
        <div class="button-group">
          <UButton @click="$emit('close')">我已知晓</UButton>
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
const { fetchSecretMission } = useHttp();
const mission = ref<Mission | null>(null);

onMounted(async () => {
  await fetchSecretMission()
    .then((res) => {
      mission.value = res;
    })
    .catch((err: Error) => {
      alert("获取秘密任务失败" + err.message);
    });
});
</script>

<style scoped>
h2 {
  font-size: var(--fs-500);
  margin-bottom: 0.75em;
}
p {
  font-size: var(--fs-400);
  margin-left: 0.5em;
  margin-bottom: 0.5em;
}
a {
  color: var(--clr-secondary-dark);
  font-weight: bold;
  text-decoration: underline;
  text-underline-offset: 2px;
  cursor: pointer;
}
.button-group {
  display: flex;
  justify-content: space-between;
  padding-inline: 0.5rem;
}
</style>
