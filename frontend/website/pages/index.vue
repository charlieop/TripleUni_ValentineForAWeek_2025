<template>
  <div class="index-wrapper">
    <div class="decor-chat">
      <img :src="IMAGE_BASE_URL + 'chat.gif'" alt="Decor Chat" />
    </div>
    <div class="logo">
      <img
        :src="IMAGE_BASE_URL + 'logo-b.webp'"
        alt="Valentine For A Week Logo"
        v-if="!isDarkMode"
      />
      <img :src="IMAGE_BASE_URL + 'logo-w.webp'" alt="Valentine For A Week Logo" v-else />
    </div>
    <div class="decor-couple">
      <img :src="IMAGE_BASE_URL + 'couple3.webp'" alt="" />
    </div>
    <div class="content-wrapper">
      <div>
        <button class="btn primary" disabled v-if="state === States.UNKNOWN">
          加载中...
        </button>
        <router-link to="/application" v-if="state === States.APPLICATION_OPEN">
          <button class="btn primary">立即报名</button>
        </router-link>
        <div class="btn-group" v-if="state === States.APPLICATION_SUBMITTED">
          <router-link to="/application">
            <button class="btn primary">修改报名</button>
          </router-link>
          <button class="btn primary danger" @click="openModal = true">
            取消报名
          </button>
        </div>
        <button
          class="btn primary"
          disabled
          v-if="state === States.APPLICATION_END"
        >
          报名已截止
        </button>
        <router-link
          to="/match-result"
          v-if="state === States.MATCH_RESULT_AVALIABLE"
        >
          <button class="btn primary">查看匹配结果</button>
        </router-link>
        <router-link to="/match" v-if="state === States.EVENT_START">
          <button class="btn primary">进行活动</button>
        </router-link>
        <router-link to="/match" v-if="state === States.EVENT_END">
          <button class="btn primary">回看记录</button>
        </router-link>
        <button class="btn primary" disabled v-if="state === States.NO_MATCH">
          无匹配记录
        </button>
      </div>
      <a
        href="https://hkupootal.feishu.cn/docx/YZkqdJaTwoDZnZxmnHdcihmin6f"
        target="_blank"
      >
        <button class="btn secondary" style="--_color: var(--clr-accent)">
          查看活动规则
        </button>
      </a>
    </div>

    <!-- XXX: to be removed -->
    <button class="test primary" @click="logout">测试用: 清缓存</button>
  </div>
  <ModalCancelApplication :model-value="openModal" @close="openModal = false" />
</template>

<script setup lang="ts">
enum States {
  APPLICATION_OPEN = 0,
  APPLICATION_SUBMITTED = 1,
  APPLICATION_END = 2,
  MATCH_RESULT_AVALIABLE = 3,
  EVENT_START = 4,
  EVENT_END = 5,
  NO_MATCH = 6,
  UNKNOWN = -1,
}

const { getApplicantId } = useStore();
const { CONFIG, getMatchId } = useReactive();
const openModal = ref(false);

useHead({
  title: "一周CP 2025 | 首页",
});

// XXX: to be removed
function logout() {
  localStorage.removeItem("openId");
  localStorage.removeItem("applicantId");
  sessionStorage.removeItem("matchId");
  sessionStorage.removeItem("config");
}

const state = computed(() => {
  if (!CONFIG.value) return States.UNKNOWN;
  const now = new Date();
  if (now < new Date(CONFIG.value.APPLICATION_DEADLINE)) {
    return getApplicantId() === null
      ? States.APPLICATION_OPEN
      : States.APPLICATION_SUBMITTED;
  }
  if (now < new Date(CONFIG.value.FIRST_ROUND_MATCH_RESULTS_RELEASE)) {
    return States.APPLICATION_END;
  }
  // XXX: 无匹配记录处理
  if (now < new Date(CONFIG.value.EVENT_START)) {
    return States.MATCH_RESULT_AVALIABLE;
  }

  if (now < new Date(CONFIG.value.EVENT_END)) {
    return getMatchId() === null ? States.NO_MATCH : States.EVENT_START;
  }
  return States.EVENT_END;
});

onMounted(() => {});
</script>

<style scoped>
.test {
  position: absolute;
  z-index: 999;
  bottom: 0.25rem;
  right: 1rem;
  --_color: var(--clr-accent);
  font-size: 14px;
  width: fit-content;
  padding: 0.25rem;
}

.index-wrapper {
  width: 100%;
  height: 100%;
  padding: 0.5rem 1rem;
  position: relative;
  overflow: hidden;
  overflow-y: scroll;
}
@media (prefers-color-scheme: dark) {
  .index-wrapper {
    background-image: radial-gradient(
        circle 40vh at -20% -10%,
        var(--clr-primary-light) 0%,
        transparent 100%
      ),
      radial-gradient(
        circle 40vh at 110% 100%,
        var(--clr-primary-light) 0%,
        transparent 100%
      );
  }
}
@media (prefers-color-scheme: light) {
  .index-wrapper {
    background-color: var(--clr-primary-light);
    background-image: radial-gradient(
        circle 40vh at -20% -10%,
        var(--clr-primary) 0%,
        transparent 100%
      ),
      radial-gradient(
        circle 40vh at 110% 100%,
        var(--clr-primary) 0%,
        transparent 100%
      );
  }
}

.decor-chat {
  position: absolute;
  top: 1.25rem;
  right: 8%;
  width: 3rem;
  height: 3rem;
  transform: rotate(10deg);
}
.content-wrapper {
  line-height: 1.5;
  padding: 0 1.5rem;
}

.btn-group {
  display: grid;
  grid-template-columns: 2fr 1fr;
}
.danger {
  --_color: var(--clr-danger);
  font-size: var(--fs-300);
  padding-inline: 0.125rem;
}

.logo img {
  width: 100%;
  transform: translateX(-2%);
  margin-bottom: -0.5rem;
}

button {
  display: block;
  margin: 1.5vh auto;
  width: 90%;
  font-size: var(--fs-500);
  font-weight: bold;
  cursor: pointer;
}

.decor-couple {
  position: absolute;
  width: 90%;
  left: 5%;
  bottom: 0.5rem;
}
</style>
