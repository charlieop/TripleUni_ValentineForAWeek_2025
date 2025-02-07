<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
  >
    <UCard>
      <template #header>
        <div class="header-group">
          <h2>你上传的图片</h2>
          <UButton @click="handleDeleteImage" variant="outline"
            >删除此图片</UButton
          >
        </div>
      </template>
      <div class="img-wrapper">
        <img :src="API_HOST + props.image?.path" alt="" />
      </div>
      <template #footer>
        <div class="btn-group">
          <UButton @click="$emit('close')" color="lime">关闭</UButton>
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
const { getMatchInfo } = useStore();
const { deleteImage } = useHttp();
const props = defineProps<{
  image: { id: string; path: string } | null;
  day: number;
}>();

const $emit = defineEmits(["close", "deleted"]);

function handleDeleteImage() {
  if (!props.image) {
    return;
  }

  if (!confirm("确定删除此图片吗?")) {
    return;
  }

  const matchInfo = getMatchInfo();
  if (!matchInfo) {
    alert("意料之外的错误: 未找到匹配信息");
    return;
  }

  deleteImage(matchInfo.matchId, props.day, props.image.id)
    .then(() => {
      alert("删除成功");
      $emit("deleted");
    })
    .catch((err: Error) => {
      alert("删除失败: " + err.message);
    });
}
</script>

<style scoped>
h2 {
  font-size: var(--fs-500);
}
.img-wrapper {
  width: 100%;
  height: 60vh;
  overflow: scroll;
}
img {
  width: auto;
  height: auto;
}
.btn-group {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-inline: 0.5rem;
}
.header-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-inline: 0.5rem;
}
</style>
