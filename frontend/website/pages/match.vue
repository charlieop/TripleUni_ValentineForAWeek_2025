<template>
  <div class="match-bg">
    <img src="/imgs/heart1.svg" alt="" class="decor" />
    <img :src="IMAGE_BASE_URL + 'heart3.webp'" alt="" class="decor-heart" />
    <div class="match-wrapper">
      <h2 @click="showChangeNameModal = true">
        {{ match?.id }}组 -
        <span class="name"
          >{{ match?.name }}
          <span class="hint" v-if="match?.name == '取一个组名吧!'"
            >点我更改组名</span
          >
        </span>
      </h2>
      <ul class="tasks-scroller">
        <li>
          <div
            class="task-item"
            :style="{ '--_bg-color': '#f9edd1aa' }"
            @click="showSecretMissionModal = true"
          >
            秘密任务
          </div>
          <div class="text">请查看</div>
        </li>
        <li
          v-for="i in 7"
          :key="i"
          :id="'day-' + i"
          @click="
            () => {
              if (getState(i) !== 'active') return;
              showMissionModal = true;
            }
          "
        >
          <div
            class="task-item"
            :style="{ '--_bg-color': STATE_TO_COLOR[getState(i)] }"
          >
            第{{ i }}天
          </div>
          <div class="text">{{ STATE_TO_TEXT[getState(i)] }}</div>
        </li>
      </ul>
      <h1>我的CP组:</h1>
      <div class="participant-group" v-if="match">
        <div class="participant">
          <img :src="API_HOST + match.my_info.head_image" alt="" />
          <div class="participant-nickname">
            {{ match.my_info.nickname }}<br />你
          </div>
        </div>
        <div class="score-level">{{ score_level_emoji }}</div>
        <div class="participant">
          <img :src="API_HOST + match.partner_info.head_image" alt="" />
          <div class="participant-nickname">
            {{ match.partner_info.nickname }}<br />
            {{ match.partner_wxid }}
          </div>
        </div>
      </div>
      <div class="text-wrapper">
        <h3>注意事项:</h3>
        <p>- 添加微信时请先向对方<strong>屏蔽朋友圈</strong></p>
        <p>- 请点击上方对应的天数查看每日任务</p>
        <p>
          - 每天的任务公布时间为 00:00, 提交截止时间为:
          当日23:59。错过截止日期将<strong>无法提交</strong>，当日算做没有完成任务
        </p>
        <p>- 必须完成每日的主线任务才能够完整返还押金</p>
        <p>
          - 请在
          <a href="https://hkupootal.feishu.cn/docx/YZkqdJaTwoDZnZxmnHdcihmin6f"
            >这里</a
          >
          查看具体规则
        </p>
      </div>
    </div>
  </div>
  <ModalLoading :model-value="loading" :text="modalText" />
  <ModalChangeMatchName
    :model-value="showChangeNameModal"
    :match="match"
    @close="showChangeNameModal = false"
    @update="
      () => {
        updateMatch();
        showChangeNameModal = false;
      }
    "
  />
  <ModalSecretMission
    :model-value="showSecretMissionModal"
    @close="showSecretMissionModal = false"
  />
  <ModalMission
    :model-value="showMissionModal"
    :match="match"
    :day="day"
    @close="showMissionModal = false"
  />
</template>

<script setup lang="ts">
import { ModalChangeMatchName } from "#components";

useHead({
  title: "一周CP 2025 | 我的CP组",
});

const { fetchMatchResult, fetchMatch, patchMatchName } = useHttp();
const { setMatchInfo, getMatchInfo } = useStore();
const { CONFIG } = useReactive();

const loading = ref(false);
const modalText = ref<string | null>(null);
const match = ref<Match | null>(null);
const router = useRouter();
const showChangeNameModal = ref(false);
const showSecretMissionModal = ref(false);
const showMissionModal = ref(false);
const day = ref(0);

const score_level_emoji = computed(() => {
  if (match.value === null) {
    return "👋";
  }
  const score = match.value.total_score;
  switch (true) {
    case score > 80:
      return "❤️‍🔥";
    case score > 60:
      return "💖";
    case score > 40:
      return "💌";
    case score > 20:
      return "🔥";
    case score > 6:
      return "👀";
    default:
      return "👋";
  }
});

const STATE_TO_COLOR = {
  active: "var(--clr-primary-dark)",
  future: "var(--clr-primary-light)",
  completed: "#b8de4a99",
  missing: "var(--clr-failed)",
};
const STATE_TO_TEXT = {
  active: "进行中",
  future: "未开始",
  completed: "已完成",
  missing: "未完成",
};

function getState(i: number): "active" | "future" | "completed" | "missing" {
  if (match.value === null) {
    return "missing";
  }
  switch (true) {
    case i === day.value:
      return "active";
    case i > day.value:
      return "future";
    case i < day.value && !match.value.tasks.some((task) => task.day === i):
      return "missing";
    case i < day.value && match.value.tasks.some((task) => task.day === i):
      return "completed";
    default:
      return "missing";
  }
}

async function updateMatch() {
  modalText.value = "小红娘正在寻找你的对象";
  loading.value = true;
  let storedMatchInfo = getMatchInfo();
  if (storedMatchInfo === null) {
    await fetchMatchResult()
      .then((matchInfo) => {
        if (matchInfo) {
          setMatchInfo(matchInfo.id, 2);
          return;
        }
        setMatchInfo(-1, 2);
      })
      .catch((error: Error) => {
        alert("获取匹配结果失败: " + error.message);
      });
    storedMatchInfo = getMatchInfo();
  }
  if (storedMatchInfo === null) {
    alert("意料之外的错误: 找不到本地 matchinfo");
    router.push("/");
    return;
  }
  if (storedMatchInfo.matchId <= 0) {
    alert("找不到你的匹配记录");
    router.push("/");
    return;
  }
  await fetchMatch(storedMatchInfo.matchId)
    .then((matchInfo) => {
      console.log(matchInfo);
      match.value = matchInfo;
      loading.value = false;
      modalText.value = null;
    })
    .catch((error: Error) => {
      alert("获取匹配结果失败: " + error.message);
      router.push("/");
    });
}

onMounted(async () => {
  await updateMatch();
  const now = new Date();
  const day1 = convertToLocalTime(CONFIG.value.FIRST_TASK_START);
  const diffTime = now.getTime() - day1.getTime();
  day.value = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  const element = document.getElementById(`day-${day.value}`);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
  }
});
</script>

<style scoped>
.text-wrapper a {
  color: var(--clr-secondary-dark);
  font-weight: bold;
  text-underline-offset: 2px;
  text-decoration: underline;
  cursor: pointer;
}
.text-wrapper p {
  padding: 0 1rem;
  margin-bottom: 0.5em;
}
h3 {
  font-size: var(--fs-600);
  color: var(--clr-primary-dark);
  padding-block: 1rem 0.25em;
}

.text-wrapper {
  padding: 0 1.5rem;
}

.participant-group {
  position: relative;
  padding: 0 3rem;
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  margin-block: 1rem 4rem;
}
.participant {
  position: relative;
}
.participant img {
  width: 4.5rem;
  height: 4.5rem;
  border-radius: 0.75rem;
}
.participant-nickname {
  font-size: var(--fs-300);
  text-align: center;
  position: absolute;
  top: 105%;
  left: 50%;
  width: max-content;
  max-width: 180%;
  word-break: break-word;
  transform: translateX(-50%);
}

.score-level {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 3.25rem;
}

.tasks-scroller {
  display: flex;
  gap: 1rem;
  margin-block: 2rem;
  padding-inline: 1.5rem;
  overflow-y: hidden;
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
  scroll-padding-inline: 1.5rem;

  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
.tasks-scroller > * {
  flex-shrink: 0;
  scroll-snap-align: center;
}

.tasks-scroller::-webkit-scrollbar {
  display: none;
}

.task-item {
  --_bg-color: var(--clr-failed);
  position: relative;
  width: 5.5rem;
  height: 5.5rem;
  border-radius: 1rem;
  font-size: var(--fs-400);
  text-align: center;
  padding: 0.5rem 0;

  background-color: var(--_bg-color);
}

.text {
  font-size: var(--fs-200);
  color: var(--clr-text--muted);
  text-align: center;
}
h1 {
  font-size: var(--fs-800);
  color: var(--clr-primary-dark);
  text-align: center;
}

h2 {
  display: flex;
  gap: 0.5ch;
  align-items: center;
  justify-content: center;
  font-size: var(--fs-500);
  color: var(--clr-primary);
}
.name {
  position: relative;
  font-size: var(--fs-700);
  color: var(--clr-primary-dark);
}
.name .hint {
  position: absolute;
  font-size: var(--fs-200);
  top: 85%;
  left: 50%;
  width: fit-content;
  transform: translateX(-50%);
  color: var(--clr-text--muted);
}

.match-wrapper {
  position: relative;
  z-index: 1;
  padding: 1rem 0 5rem 0;
}

.match-bg {
  width: 100%;
  min-height: 100%;
  position: relative;
}
.match-bg::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
}
@media (prefers-color-scheme: dark) {
  .match-bg::before {
    background-image: radial-gradient(
        circle 40vh at -20% -10%,
        var(--clr-primary-light) 0%,
        transparent 100%
      ),
      radial-gradient(
        circle 50vh at 120% 110%,
        var(--clr-primary-light) 0%,
        transparent 100%
      );
  }
}
@media (prefers-color-scheme: light) {
  .match-bg::before {
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
  .task-item {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
}
.decor {
  position: fixed;
  top: 45%;
  left: -23%;
  width: 75%;
  transform: rotate(35deg);
  opacity: 0.6;
  transition: all 0.3s;
}
@media (prefers-color-scheme: dark) {
  .decor {
    opacity: 0.2;
  }
}
.decor-heart {
  position: fixed;
  top: 10rem;
  right: -0.25rem;
  width: 10rem;
  transform: rotate(40deg);
  opacity: 0.3;
}
</style>
