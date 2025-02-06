<template>
  <UModal
    prevent-close
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <h2>第{{ props.day }}天任务</h2>
      </template>
      <div class="modal-wrapper" v-if="!submit">
        <div v-if="mission">
          <h2>
            {{ mission.title }}
          </h2>
          <p>
            每日任务分为主线任务和支线任务,
            主线任务为 <strong>必须</strong> 完成的任务, 支线任务为额外任务,
            完成支线任务可以获得额外分数。
          </p>
          <p>
            请在今日的 23:59前提交任务完成的凭证,
            <strong>你将无法在截止日期后提交当日任务</strong>。
          </p>
          <p>
            你可以在这里查看你们的第{{ props.day }}天任务:<br />
            <a :href="mission.link" target="_blank">我的秘密任务</a>
          </p>
        </div>
        <p v-else>加载中...</p>
      </div>
      <div v-else>submit</div>
      <template #footer>
        <div class="button-group">
          <UButton @click="$emit('close')" :disabled="loading">关闭</UButton>

          <UButton @click="$router.push('/task-submission')" color="green" variant="solid" :disabled="loading"
          >{{ (props.match === null || props.match.tasks.every((task) => task.day != props.day)) ? '前往提交任务' : '前往查看/修改' }}</UButton>
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
const { fetchMission } = useHttp();

const loading = ref(false);
const submit = ref(false);
const mission = ref<Mission | null>(null);

const $emit = defineEmits(["close", "update"]);
const props = defineProps<{
  day: number,
  match: Match | null,
}>();

onMounted(async () => {
  await fetchMission()
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
.modal-wrapper {
  padding: 1rem 0.75rem;
}
.button-group {
  display: flex;
  justify-content: space-between;
  padding-inline: 0.5rem;
}
</style>
