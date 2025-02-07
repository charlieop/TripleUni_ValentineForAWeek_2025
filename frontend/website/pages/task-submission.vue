<template>
  <div class="form-wrapper">
    <Vueform
      ref="form"
      validate-on="step|change"
      add-class="vf-task-submit-form"
      :upload-temp-endpoint="false"
      @submit="handleFormSubmit"
    >
      <StaticElement name="h1" tag="h1" :content="`第${day}天任务提交`" />
      <StaticElement
        name="p"
        tag="p"
        content="<div>在提交截止前, 你可以不限次数的修改你提交的内容.<br>参与双方都可以看到此界面的提交/ 修改</div>"
      />
      <StaticElement name="divider_1" tag="hr" />
      <StaticElement name="h2" tag="h2" content="图片上传" />
      <StaticElement
        name="quote"
        tag="blockquote"
        content="<div>每张图片大小不能超过5MB。<br>
          <strong>建议先通过微信给对方发送图片(非原图)进行压缩, 再保存发送后的压缩图片进行上传。</strong><br>
        </div>"
      />
      <template v-if="uploadedImagesUrls.length > 0">
        <StaticElement name="h3" tag="h3" content="已经提交的图片" top="1" />
        <ul class="uploaded-img-wrapper">
          <li
            v-for="(img, index) in uploadedImagesUrls"
            :key="index"
            class="uploaded-img"
            @click="
              () => {
                current_img = img;
                showImageDetailModal = true;
              }
            "
          >
            <img
              :src="API_HOST + img.path"
              alt="uploaded image"
              :data-img-id="img.id"
            />
          </li>
        </ul>
        <StaticElement
          name="p1"
          tag="p"
          content="<div>你可以左右滑动, 点击图片可查看大图。</div>"
        />
      </template>
      <StaticElement name="h3-1" tag="h3" content="在此上传你的图片" top="1" />
      <MultifileElement
        name="images"
        view="gallery"
        accept="image/*"
        :upload-temp-endpoint="false"
        :file="{
          rules: [
            'mimetypes:image/jpeg,image/png,image/heic',
            'mimes:png,jpg,jpeg,heic',
            'max:5120',
          ],
        }"
        :urls="{}"
        :disabled="loading"
        description="注意: 每张图片大小不可以超过5MB"
      />
      <StaticElement name="divider" tag="hr" />
      <TextareaElement
        name="submit_text"
        label="提交内容描述"
        :rows="5"
        :rules="['max:300']"
        :disabled="loading"
      />
      <StaticElement name="divider_2" tag="hr" />
      <ButtonElement
        name="submit"
        :button-label="taskExist ? '修改任务' : '提交任务'"
        :submits="true"
        :loading="loading"
        align="right"
      />
    </Vueform>
    <div class="images-wrapper"></div>
  </div>

  <ModalImageView
    :image="current_img"
    :day="day"
    @close="showImageDetailModal = false"
    @deleted="
      () => {
        showImageDetailModal = false
        uploadedImagesUrls = uploadedImagesUrls.filter(
          (img) => current_img && img.id !== current_img.id
        );
        current_img = null;
      }
    "
    :model-value="showImageDetailModal"
  />
</template>

<script setup lang="ts">
const { CONFIG } = useReactive();
const { getMatchInfo } = useStore();
const { fetchTask, postTask, patchTask, postTaskImages } = useHttp();
const form = ref<{ update: (data: any) => void } | null>(null);
const router = useRouter();

const loading = ref(true);
const uploadedImagesUrls = ref<{ id: string; path: string }[]>([]);
const day = ref(0);
const current_img = ref<{ id: string; path: string } | null>(null);
const showImageDetailModal = ref(false);
const taskExist = ref(false);

const handleFormSubmit = async (form$: { data: any }, FormData: any) => {
  const data = form$.data;
  const imgs = data.images;
  if (imgs.length === 0 && !data.submit_text) {
    alert("请至少提交一张图片或者文字描述");
    return;
  }

  const matchInfo = getMatchInfo();
  if (!matchInfo) {
    alert("意料之外的错误: 未找到匹配信息");
    router.push("/match");
    return;
  }
  loading.value = true;
  const compressedImages: File[] = await Promise.all(
    imgs.map(async (img: File) => {
      const compressedImg = await compressImage(img);
      return new File([compressedImg], img.name, { type: "image/jpeg" });
    })
  );

  let success = true;
  if (!taskExist.value) {
    await postTask(matchInfo.matchId, day.value, data.submit_text).catch(
      (err: Error) => {
        alert("修改任务失败: " + err.message);
        success = false;
        router.push("/match");
      }
    );
  } else {
    await patchTask(matchInfo.matchId, day.value, data.submit_text).catch(
      (err: Error) => {
        alert("修改任务失败: " + err.message);
        success = false;
        router.push("/match");
      }
    );
  }
  if (!success) return;
  await postTaskImages(matchInfo.matchId, day.value, compressedImages).catch(
    (err: Error) => {
      alert("上传图片失败: " + err.message);
      router.push("/match");
    }
  );
  loading.value = false;
  alert("提交成功");
  router.push("/match");
};

onMounted(async () => {
  const now = new Date();
  const day1 = convertToLocalTime(CONFIG.value.FIRST_TASK_START);
  const diffTime = now.getTime() - day1.getTime();
  day.value = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  const matchInfo = getMatchInfo();
  if (!matchInfo) {
    alert("意料之外的错误: 未找到匹配信息");
    router.push("/match");
    return;
  }
  await fetchTask(matchInfo.matchId, day.value)
    .then((task: Task | null) => {
      loading.value = false;
      if (!task) {
        taskExist.value = false;
        return;
      }
      taskExist.value = true;
      if (!form.value) return;
      form.value.update({
        submit_text: task.submit_text,
      });
      uploadedImagesUrls.value = task.imgs;
    })
    .catch((err: Error) => {
      alert("获取任务失败: " + err.message);
      router.push("/match");
    });
});
</script>

<style scoped>
.uploaded-img-wrapper {
  display: flex;
  gap: 1rem;
  overflow-x: scroll;

  width: calc(100vw - 4rem);
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}
.uploaded-img-wrapper::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}

.uploaded-img-wrapper > * {
  flex-shrink: 0;
}

.uploaded-img img {
  width: 7rem;
  height: 10rem;
  object-fit: cover;
  overflow: hidden;
  border-radius: 6px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.form-wrapper {
  padding: 3rem 2rem;
}

.vf-task-submit-form *,
.vf-task-submit-form *:before,
.vf-task-submit-form *:after,
.vf-task-submit-form:root {
  --vf-primary: var(--clr-primary);
  --vf-primary-darker: var(--clr-primary-dark);
  --vf-color-on-primary: #ffffff;

  --vf-color-passive: var(--clr-text--muted);

  /* slider */
  --vf-ring-width: 2px;
  --vf-ring-color: var(--clr-primary-light);
  --vf-slider-handle-size-lg: 1.75rem;

  --vf-font-size-h1: 2.125rem;
  --vf-font-size-h2: 1.875rem;
  --vf-font-size-h3: 1.5rem;
  --vf-font-size-h1-mobile: var(--fs-600);
  --vf-font-size-h2-mobile: var(--fs-600);
  --vf-font-size-h3-mobile: var(--fs-500);

  --vf-line-height: 1.5;
  --vf-line-height-headings: 1.2;
}
</style>
