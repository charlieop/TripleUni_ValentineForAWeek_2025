<template>
  <div class="conten-wrapper">
    <h1>第{{ round }}轮: 未能匹配</h1>
    <p>
      很遗憾，在第{{
        round
      }}轮中我们未能为你找到一个合适的匹配人选。这并不代表你有任何不足，只是我们还未找到最特别的那个ta。
    </p>
    <template v-if="round === 1">
      <p>不要灰心，我们为第二轮匹配保留了充足的名额。请耐心等待，我们将在一天后再次启动匹配, 为你寻找合适的人选。</p>
      <p>
        祝你好运，我们<br />
        <strong>
          {{
            new Date(
              CONFIG.SECOND_ROUND_MATCH_RESULTS_RELEASE
            ).toLocaleDateString("zh-CN", {
              year: "numeric",
              month: "long",
              day: "numeric",
              hour: "numeric",
              minute: "numeric",
            })
          }}</strong
        >
        <br />
        不见不散。
      </p>
    </template>
    <template v-else>
      <p>
        请不要为此感到沮丧，合适的缘分需要时间和耐心。
        我们感谢你对本次活动的关注与支持。缘分或许就在不经意间悄然降临，
        愿你在未来的日常生活中遇见那个对的人。
      </p>
      <p>
        祝你一切顺利， <br />
        幸福常在！
      </p>
    </template>
  </div>
</template>

<script setup lang="ts">
const { getMatchInfo } = useStore();
const { CONFIG } = useReactive();
const round = getMatchInfo()?.round || 1;
</script>

<style scoped>
h1 {
  font-size: var(--fs-800);
  text-align: center;
  margin-block: 1rem 1em;
}
p {
  padding: 0 0.75rem;
  font-size: var(--fs-400);
  text-align: center;
  margin-bottom: 1.25em;
}
strong {
  color: var(--clr-accent);
  text-decoration: underline;
  text-underline-position: under;
  text-decoration-thickness: 1px;
  font-size: 1.1em;
}

.conten-wrapper {
  position: relative;
}
</style>
