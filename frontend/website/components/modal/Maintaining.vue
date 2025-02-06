<template>
  <UModal
    :ui="{
      container: 'items-center',
    }"
    preventClose
  >
    <UCard>
      <template #header>
        <h2>服务器正在维护中</h2>
      </template>
      <p>
        2025 Triple Uni 一周CP 活动报名已经截止啦!
        小红娘正在处理第一轮的匹配结果以及匹配第二轮中...
      </p>
      <br />
      <p>请耐心等候, 我们将于2月6日早上8:00在本网址公布第二轮匹配结果。</p>
      <br />
      <p>不见不散!<br />操劳的小红娘</p>
      <template #footer> </template>
    </UCard>
  </UModal>
</template>

<style scoped>
h2 {
  font-size: var(--fs-500);
  font-weight: bold;
}
</style>
