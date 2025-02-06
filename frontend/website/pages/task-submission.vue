<template>
  <div class="form-wrapper">
    <Vueform
      validate-on="step|change"
      add-class="vf-task-submit-form"
      :upload-temp-endpoint="false"
      @submit="handleSubmit"
    >
      <StaticElement name="h1" tag="h1" :content="`第${day}天任务提交`" />
      <StaticElement
        name="p"
        tag="p"
        content="<div>在提交截止前, 你可以不限次数的修改你提交的内容.<br>参与双方都可以看到此界面的提交/ 修改</div>"
      />
      <StaticElement name="divider" tag="hr" />
      <TextareaElement
        name="submit_text"
        label="提交内容描述"
        :rows="7"
        :rules="['max:300']"
      />
      <StaticElement name="divider_1" tag="hr" />
      <StaticElement name="h2" tag="h2" content="图片上传" />
      <StaticElement
        name="quote"
        tag="blockquote"
        content="<div>每张图片大小不能超过2MB。<br><strong>建议通过微信发送截图进行压缩, 保存发送后的压缩图片再上传。</strong></div>"
      />
      <MultifileElement
        name="images"
        view="gallery"
        accept="image/*"
        :upload-temp-endpoint="false"
        :file="{
          rules: [
            'mimetypes:image/jpeg,image/png,image/heic',
            'mimes:png,jpg,jpeg,heic',
            'max:2048',
          ],
        }"
        :urls="{}"
        label="图片上传"
        description="注意: 每张图片大小不可以超过2MB"
      />
      <StaticElement name="divider_2" tag="hr" />
      <ButtonElement
        name="submit"
        button-label="Submit"
        :submits="true"
        align="right"
      />
    </Vueform>
  </div>
</template>

<script setup lang="ts">
const { CONFIG } = useReactive();
const { setMatchInfo, getMatchInfo } = useStore();
const router = useRouter();

const loading = ref(false);
const modalText = ref<string | null>(null);
const day = ref(0);

const uploadTemp = async (value: File, el$: any) => {
  console.log(value, el$);
  const file = el$.form$.convertFormData({
    file: value,
  });
  console.log(file);
};

const handleSubmit = async (form$, FormData) => {
  console.log(form$);
  console.log(FormData);
  alert("功能暂未开放...");
};

onMounted(async () => {
  const now = new Date();
  const day1 = convertToLocalTime(CONFIG.value.FIRST_TASK_START);
  const diffTime = now.getTime() - day1.getTime();
  day.value = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
});
</script>

<style scoped>
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
