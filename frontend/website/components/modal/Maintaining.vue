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
        小红娘正在查看你的申请资料并为你匹配最合适的人选中...
      </p>
      <br />
      <p>请耐心等候, 我们将于今晚19:00在本网址公布匹配结果。</p>
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
