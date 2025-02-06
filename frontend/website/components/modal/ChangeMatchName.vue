<template>
  <UModal
    prevent-close
    :ui="{
      container: 'items-start',
    }"
  >
    <UCard>
      <template #header>
        <h2>更改组名</h2>
      </template>
      <div class="modal-wrapper">
        <p>想给你们的CP组合起一个什么样的名字呢?</p>
        <UInput
          color="primary"
          variant="outline"
          placeholder="我们的组名叫:"
          :disabled="loading"
          v-model="groupName"
        />
      </div>
      <template #footer>
        <div class="button-group">
          <UButton @click="$emit('close')" :disabled="loading">取消</UButton>

          <UButton
            @click="handleChanegMatchName"
            color="green"
            variant="solid"
            :disabled="loading"
            >修改组名</UButton
          >
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
const { patchMatchName } = useHttp();

const router = useRouter();
const loading = ref(false);
const groupName = ref("");
const $emit = defineEmits(["close", "update"]);
const props = defineProps<{
  match: Match | null;
}>();

function handleChanegMatchName() {
  if (groupName.value === "") {
    alert("组名不能为空");
    return;
  }
  if (groupName.value.length > 8) {
    alert("组名长度不能超过8个字");
    return;
  }

  loading.value = true;
  if (props.match === null) {
    alert("意料之外的错误: 找不到match");
    router.push("/");
    return;
  }
  patchMatchName(props.match.id, groupName.value)
    .then(() => {
      $emit("update");
    })
    .catch((error: Error) => {
      alert("修改组名失败: " + error.message);
    })
    .finally(() => {
      groupName.value = "";
      loading.value = false;
    });

  console.log("change match name" + groupName.value);
}
</script>

<style scoped>
h2 {
  font-size: var(--fs-500);
}
p {
  margin-bottom: 1rem;
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
