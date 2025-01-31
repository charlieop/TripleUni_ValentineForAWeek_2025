<template>
  <div class="index-wrapper">
    <div class="logo">
      <img
        class="b"
        :src="IMAGE_BASE_URL + 'logo-b.webp'"
        alt="Valentine For A Week Logo"
        v-if="!isDarkMode"
      />
      <img
        class="b"
        :src="IMAGE_BASE_URL + 'logo-w.webp'"
        alt="Valentine For A Week Logo"
        v-else
      />
    </div>
    <div class="decor-chat">
      <img :src="IMAGE_BASE_URL + 'chat.gif'" alt="Decor Chat" />
    </div>
    <div class="decor-couple">
      <img class="a" :src="IMAGE_BASE_URL + 'couple3.webp'" alt="" />
    </div>
    <div class="content-wrapper">
      <div>
        <button class="btn primary" disabled v-if="state === States.UNKNOWN">
          加载中...
        </button>
        <button class="btn primary" disabled v-if="state === States.DELETE">
          已取消报名
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
    <UButton
      @click="openHelpModal = true"
      class="help"
      variant="link"
      icon="ic:round-help-outline"
      square
      size="sm"
    ></UButton>
  </div>
  <ModalHelp :model-value="openHelpModal" @close="openHelpModal = false" />
  <ModalCancelApplication :model-value="openModal" @close="openModal = false" />
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2025 | 首页",
});

enum States {
  APPLICATION_OPEN = 0,
  APPLICATION_SUBMITTED = 1,
  APPLICATION_END = 2,
  MATCH_RESULT_AVALIABLE = 3,
  EVENT_START = 4,
  EVENT_END = 5,
  NO_MATCH = 6,
  DELETE = 7,
  UNKNOWN = -1,
}

const router = useRouter();
const { getApplicantId, getDeleted, getMatchInfo } = useStore();
const { CONFIG } = useReactive();
const openModal = ref(false);
const openHelpModal = ref(false);

const state = computed(() => {
  if (!CONFIG.value) return States.UNKNOWN;
  if (getDeleted()) return States.DELETE;
  const now = new Date();
  if (now < new Date(CONFIG.value.APPLICATION_DEADLINE)) {
    return getApplicantId() === null
      ? States.APPLICATION_OPEN
      : States.APPLICATION_SUBMITTED;
  }
  if (now < new Date(CONFIG.value.FIRST_ROUND_MATCH_RESULTS_RELEASE)) {
    return States.APPLICATION_END;
  }

  if (now < new Date(CONFIG.value.EVENT_START)) {
    return States.MATCH_RESULT_AVALIABLE;
  }

  if (getMatchInfo() === null) {
    return States.NO_MATCH;
  }

  if (now < new Date(CONFIG.value.EVENT_END)) {
    return States.EVENT_START;
  }
  return States.EVENT_END;
});
</script>

<style scoped>
.help {
  position: absolute;
  width: fit-content;
  top: -0.375rem;
  left: 0.25rem;
  scale: 1.5;
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
  button.secondary {
    background: var(--clr-background);
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
