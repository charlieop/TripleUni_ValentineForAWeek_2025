<template>
  <div class="conten-wrapper">
    <h1>
      第{{ matchDetail?.round || "..." }}轮 -
      <span>
        {{ matchStatus }}
      </span>
    </h1>
    <h2>你的CP:</h2>

    <div
      class="head-img-frame"
      :style="{
        '--_color':
          matchDetail?.partner_sex === 'F'
            ? 'var(--clr-primary)'
            : 'var(--clr-accent)',
      }"
    >
      <div
        class="partner-status"
        :style="{ '--_status-color': StatusToColor[partnerStatus] }"
      >
        <div class="dot"></div>
        <span>{{ matchDetail?.partner_sex === "F" ? "她" : "他" }}:</span>
        <span>{{ partnerStatus }}</span>
      </div>
      <img
        :src="API_HOST + matchDetail?.partner_info.head_image"
        :class="{
          darken:
            !matchDetail?.partner_paid || matchStatus == MatchStatus.DISCARDED,
        }"
        alt=""
      />
      <div class="img-overlay" v-if="matchDetail?.my_status != 'A'">
        你需要接受匹配方可查看清晰头像
      </div>
      <div class="partner-info">
        <p v-if="matchDetail?.my_status == 'A'">
          微信昵称: {{ matchDetail?.partner_info.nickname }}
        </p>
        <p v-else>
          微信昵称:
          {{ matchDetail?.partner_info.nickname.substring(0, 1) + "*****" }}
        </p>
        <p>
          {{ matchDetail?.partner_school }} |
          {{ matchDetail?.partner_sex === "F" ? "女生" : "男生" }}
        </p>
      </div>
    </div>

    <template v-if="matchStatus == MatchStatus.DISCARDED">
      <div class="action">
        <h2>此轮匹配已作废, 原因:</h2>
        <h3>
          {{ matchDetail?.discard_reason || "未知" }}
        </h3>
        <p v-if="matchDetail?.round === 1">
          请耐心等候, 我们将很快为你进行第二轮匹配。结果公布时间为:<br />
          <strong>
            北京时间{{
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
          <br />
          请注意：我们不能保证在第二轮中为你找到合适的匹配人选。
          如果你在第二轮匹配结果公布后你仍然看到此界面，
          即说明第二轮匹配失败。我们将在活动结束后退还你的全部押金。
        </p>
        <div v-else>
          <p>
            鉴于第二轮配对失败。我们的mentor可能在稍后为你进行第三轮匹配，请及时查看微信消息(mentor可能会添加你)。<br />
            如果你是拒绝匹配的一方或我们的mentor无法为你进行第三轮匹配,
            你将无法参与本次活动。 我们将在活动结束后返还你的全部押金。
          </p>
          <p>
            我们理解这可能会让你感到失望，但请相信，合适的缘分需要时间和耐心。
            我们感谢你对本次活动的关注与支持。缘分或许就在不经意间悄然降临，
            愿你在未来的日常生活中遇见那个对的人。
          </p>
          <p>
            祝你一切顺利， <br />
            幸福常在！
          </p>
        </div>
      </div>
    </template>
    <template v-else-if="matchDetail?.my_status == 'P'">
      <h2>请选择是否接受此轮匹配结果:</h2>
      <div class="action">
        <div class="btn-group">
          <button
            class="btn primary"
            style="--_color: var(--clr-success)"
            @click="handleAcceptMatch"
            :disabled="loading"
          >
            接受匹配
          </button>
          <button
            class="btn primary danger"
            @click="openModal = true"
            :disabled="loading"
          >
            不接受
          </button>
        </div>
      </div>
    </template>
    <template v-else>
      <h2>活动即将开始:</h2>
      <div class="action">
        <p>距离开始还有: {{ countdown }}</p>
        <p>
          在活动开始后你将可以查看对方的微信号。
          请在第一天<strong>向对方屏蔽你的朋友圈</strong>,
          我们将在第二天有相关任务。
        </p>
        <p>准备好了吗? 祝你好运!</p>
      </div>
      <h2>你的负责Mentor:</h2>
      <div class="action">
        <p>
          以下是负责Mentor的微信，在添加时请备注你的组号:
          <strong>「第{{ match?.matchId }}组」</strong>
        </p>
      </div>
      <div class="wechat-info" v-if="mentor">
        <div class="hint">长按图片识别二维码</div>
        <img
          :src="API_HOST + mentor?.wechat_qrcode"
          :alt="'微信号:' + mentor?.wechat"
        />
        <p>微信号: {{ mentor.wechat }}</p>
      </div>
    </template>
  </div>
  <ModalRejectMatchRoundOne
    v-model="openModal"
    @close="openModal = false"
    v-if="matchDetail?.round === 1"
  />
  <ModalRejectMatchRoundTwo
    v-model="openModal"
    @close="openModal = false"
    v-if="matchDetail?.round === 2"
  />
</template>

<script setup lang="ts">
enum MatchStatus {
  UNKNOWN = "加载中",
  DISCARDED = "已作废",
  CONFIRMED = "已确认",
  PENDING = "待确认",
}
enum PartnerStatus {
  UNKNOWN = "加载中",
  UNPAID = "未提交押金",
  REJECTED = "选择放弃",
  CONFIRMED = "确认匹配",
  PENDING = "待确认",
}

const StatusToColor = {
  [PartnerStatus.UNKNOWN]: "var(--clr-text--muted)",
  [PartnerStatus.REJECTED]: "var(--clr-danger)",
  [PartnerStatus.CONFIRMED]: "var(--clr-success)",
  [PartnerStatus.UNPAID]: "var(--clr-text--muted)",
  [PartnerStatus.PENDING]: "var(--clr-primary-dark)",
};

const { fetchMatchPartner, postMatchConfirmation, fetchMatchMentor } =
  useHttp();
const { setMatchInfo, getMatchInfo } = useStore();
const { CONFIG } = useReactive();
const router = useRouter();
const host = "http://192.168.71.91:8000";
const openModal = ref(false);
const loading = ref(false);
const countdown = ref("加载中...");

const matchDetail = ref<MatchDetail | null>(null);
const match = ref<MatchInfo | null>(null);
const mentor = ref<MentorInfo | null>(null);

const matchStatus = computed(() => {
  if (matchDetail.value === null) {
    return MatchStatus.UNKNOWN;
  }
  if (matchDetail.value.discarded) {
    return MatchStatus.DISCARDED;
  }
  if (
    matchDetail.value.my_status === "A" &&
    matchDetail.value.partner_status === "A"
  ) {
    return MatchStatus.CONFIRMED;
  }
  return MatchStatus.PENDING;
});

const partnerStatus = computed(() => {
  if (matchDetail.value === null) {
    return PartnerStatus.UNKNOWN;
  }
  if (!matchDetail.value.partner_paid) {
    return PartnerStatus.UNPAID;
  }
  if (matchDetail.value.partner_status === "R") {
    return PartnerStatus.REJECTED;
  }
  if (matchDetail.value.partner_status === "A") {
    return PartnerStatus.CONFIRMED;
  }
  if (matchDetail.value.partner_status === "P") {
    return PartnerStatus.PENDING;
  }
  return PartnerStatus.UNKNOWN;
});

async function handleAcceptMatch() {
  const matchInfo = getMatchInfo();
  if (matchInfo === null || matchInfo.matchId <= 0) {
    alert("意料之外的错误: 找不到本地match info");
    router.push("/");
    return;
  }
  loading.value = true;

  postMatchConfirmation(matchInfo.matchId, true)
    .then(() => {
      refresh();
    })
    .catch((error: Error) => {
      alert("确认匹配失败: " + error.message);
      loading.value = false;
    });
}

onMounted(() => {
  const matchInfo = getMatchInfo();
  if (matchInfo === null || matchInfo.matchId <= 0) {
    alert("意料之外的错误: 找不到本地match info");
    router.push("/");
    return;
  }
  match.value = matchInfo;

  fetchMatchPartner(matchInfo.matchId)
    .then((fetchedMatchDetail: MatchDetail) => {
      matchDetail.value = fetchedMatchDetail;
      if (fetchedMatchDetail.discarded) {
        setMatchInfo(matchInfo.matchId, matchInfo.round, true);
      }
    })
    .catch((error: Error) => {
      alert("获取匹配结果失败: " + error.message);
      router.push("/");
    });

  fetchMatchMentor(matchInfo.matchId).then(
    (m) => {
      if (m === null) {
        alert("意料之外的错误: 无Mentor信息");
        router.push("/");
        return;
      }
      mentor.value = m;
    },
    (error) => {
      alert("获取Mentor信息出错: " + error.message);
      router.push("/");
    }
  );

  const interval = setInterval(() => {
    const now = new Date();
    const eventStart = convertToLocalTime(CONFIG.value.EVENT_START);
    const diff = eventStart.getTime() - now.getTime();
    if (diff < 0) {
      router.push("/");
      return;
    }
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    countdown.value = `${days}天 ${hours}时 ${minutes}分 ${seconds}秒`;
  }, 1000);
});
</script>

<style scoped>
.conten-wrapper {
  position: relative;
  padding-inline: 1rem;
  user-select: none;
  padding-bottom: 7rem;
}
h1 {
  font-size: var(--fs-700);
  margin-block: 0.5em 0;
}

.head-img-frame {
  --_color: var(--clr-primary);
  box-sizing: border-box;
  position: relative;
  aspect-ratio: 1;
  width: 80%;
  margin: 3rem auto 5rem auto;
  border: 5px solid var(--_color);
  border-radius: 30px 2px 30% 3px / 4px 10px 3px 30px;
}

.head-img-frame::before,
.head-img-frame::after {
  z-index: 1;
  content: "";
  position: absolute;
  top: -2%;
  left: -2%;
  width: 104%;
  height: 104%;
  border: 4px solid var(--_color);
  border-radius: 30px 2px 30% 3px / 4px 10px 3px 30px;
}

.head-img-frame::before {
  opacity: 0.7;
  transform: rotate(-13deg);
}
.head-img-frame::after {
  filter: brightness(0.9);
  border-width: 2.5px;
  transform: rotate(-4deg);
}

.head-img-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 40px 15px 40% 15px / 15px 25px 15px 40px;
  overflow: hidden;
  position: relative;
}

.img-overlay {
  position: absolute;
  padding: 2rem 3rem;
  text-align: center;
  text-wrap: balance;
  color: var(--clr-primary-dark);
  display: grid;
  font-size: var(--fs-400);
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  background: radial-gradient(
    circle,
    rgba(0, 0, 0, 0.4) 0%,
    rgba(0, 0, 0, 0.5) 100%
  );
  z-index: 2;
  border-radius: 40px 15px 40% 15px / 15px 25px 15px 40px;
}

.head-img-frame img.darken {
  filter: brightness(0.4);
}
@media (prefers-color-scheme: dark) {
  .head-img-frame img {
    filter: brightness(0.8);
  }
  .head-img-frame img.darken {
    filter: brightness(0.3);
  }
}

h2 {
  font-size: var(--fs-600);
  margin-block: 1em 0;
}
.partner-info {
  display: flex;
  flex-direction: column;
  text-align: right;
  position: absolute;
  bottom: -0.5rem;
  right: 0;
  transform: translate(0, 100%);
  font-size: var(--fs-400);
}
.partner-status {
  --_status-color: var(--clr-background);
  position: absolute;
  top: -0.25rem;
  left: -1rem;
  width: 80%;
  padding: 0.25rem 0.5rem;
  transform: translate(0, -100%);
  display: flex;
  align-items: center;
  gap: 0.5ch;
}
.dot {
  display: inline-block;
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 50%;
  background-color: var(--_status-color);
  box-shadow: 0 0 10px
      color-mix(in lab, var(--_status-color) 90%, rgba(255, 255, 255, 1)),
    0 0 15px color-mix(in lab, var(--_status-color) 50%, rgba(255, 255, 255, 1));
}

.action p {
  padding-inline: 2rem;
  margin-top: 1rem;
}
.action h3 {
  font-size: var(--fs-500);
  font-weight: bold;
}
.btn-group {
  font-size: var(--fs-400);
  margin-block: 1rem;
  display: grid;
  gap: 1rem;
  grid-template-columns: 3fr 1fr;
}

.wechat-info {
  position: relative;
  margin: 2rem 1rem;
  border-radius: 5px;
  border: 5px solid var(--clr-primary);
}
.wechat-info p {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 100%;
  text-align: center;
  font-size: var(--fs-600);
  color: var(--clr-text--muted);
  z-index: -1;
  transform: translate(-50%, -50%);
}
.hint {
  position: absolute;
  color: var(--clr-text--muted);
  bottom: -0.5rem;
  left: 50%;
  width: max-content;
  transform: translate(-50%, 100%);
}
</style>
