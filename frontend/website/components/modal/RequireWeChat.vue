<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
    preventClose
  >
    <UCard>
      <template #header>
        <h2>请使用微信内置浏览器打开</h2>
      </template>
      <p>
        Triple Uni 需要使用你的微信信息用于<strong>登陆与验证</strong>,
        我们无法在非微信环境请求你的授权。
      </p>
      <br />
      <p>
        我们会在你授权后获取并保存你的<strong>微信昵称与头像</strong>用于展示匹配结果
        <strong>我们不会通过微信授权收集其他信息</strong>。
      </p>
      <br />
      <p>请使用微信内置浏览器打开此页面以继续。</p>
      <template #footer>
        <UButton @click="copyAndRedirect">复制链接并前往微信</UButton>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
async function copyAndRedirect() {
  const url = window.location.href;
  if (navigator.clipboard) {
    await navigator.clipboard.writeText(url);
    alert("链接已复制, 正在前往微信内置浏览器打开");
  } else {
    try {
      var textarea = document.createElement("textarea");
      document.body.appendChild(textarea);
      // 隐藏此输入框
      textarea.style.position = "fixed";
      textarea.style.clip = "rect(0 0 0 0)";
      textarea.style.top = "10px";
      // 赋值
      textarea.value = url;
      // 选中
      textarea.select();
      // 复制
      document.execCommand("copy", true);
      // 移除输入框
      document.body.removeChild(textarea);
      alert("链接已复制, 正在前往微信内置浏览器打开");
    } catch (error) {
      alert("复制失败, 请手动复制链接");
    }
  }
  window.location.href = "weixin://";
}
</script>

<style scoped>
h2 {
  font-size: var(--fs-500);
}
</style>
