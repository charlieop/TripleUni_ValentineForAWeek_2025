<template>
  <div class="match-wrapper">
    <img src="/imgs/heart1.svg" alt="" class="decor" />
    <div class="logo">
      <img
        :src="IMAGE_BASE_URL + 'logo-b.webp'"
        alt="Valentine For A Week Logo"
        v-if="!isDarkMode"
      />
      <img
        :src="IMAGE_BASE_URL + 'logo-w.webp'"
        alt="Valentine For A Week Logo"
        v-else
      />
    </div>
    <template v-if="!matched">
      <MatchNotFound />
    </template>
    <template v-else>
      <template v-if="!paid">
        <MatchPayDeposit />
      </template>
      <template v-else>
        <MatchViewResult />
      </template>
    </template>
  </div>

  <ModalLoading :model-value="loading" :text="modalText" />
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2025 | 查看匹配结果",
});

const {
  fetchApplicantId,
  getApplicantHasPaid,
  fetchMatchResult,
  fetchMatchMentor,
} = useHttp();
const {
  setMatchInfo,
  getMatchInfo,
  setPaid,
  getPaid,
  setApplicantId,
  getApplicantId,
} = useStore();
const { CONFIG } = useReactive();

const loading = ref(false);
const modalText = ref<string | null>(null);
const matched = ref(false);
const paid = ref(false);
const router = useRouter();

async function updateMatchInfo() {
  const storedMatchInfo = getMatchInfo();
  const roundNow =
    new Date() < new Date(CONFIG.value.SECOND_ROUND_MATCH_RESULTS_RELEASE)
      ? 1
      : 2;
  if (
    storedMatchInfo === null ||
    (storedMatchInfo.round === 1 && roundNow === 2)
  ) {
    await fetchMatchResult()
      .then((matchInfo) => {
        if (matchInfo) {
          setMatchInfo(matchInfo.id, roundNow);
          return;
        }
        setMatchInfo(-1, roundNow);
      })
      .catch((error: Error) => {
        alert("获取匹配结果失败: " + error.message);
      });
  }
}

async function updatePaymentInfo() {
  let hasPaid = getPaid();
  if (hasPaid) return;

  let applicantId = getApplicantId();
  if (applicantId === null) {
    await fetchApplicantId()
      .then((id) => {
        if (id === null) {
          alert("获取报名信息失败");
          router.push("/");
          return;
        }
        applicantId = id;
        setApplicantId(id);
      })
      .catch((error: Error) => {
        alert("获取报名信息失败: " + error.message);
        router.push("/");
      });
  }

  await getApplicantHasPaid(applicantId!)
    .then((result) => {
      hasPaid = result;
    })
    .catch((error: Error) => {
      alert("获取支付信息失败: " + error.message);
      router.push("/");
    });
  if (hasPaid) {
    setPaid();
  }
}

onMounted(async () => {
  modalText.value = "月老正在寻找你的对象";
  loading.value = true;
  await updateMatchInfo();
  modalText.value = "月老正在检查你的押金";
  await updatePaymentInfo();
  loading.value = false;
  modalText.value = null;

  const storedMatchInfo = getMatchInfo();
  matched.value = storedMatchInfo !== null && storedMatchInfo.matchId > 0;

  paid.value = getPaid();
});
</script>

<style scoped>
.match-wrapper {
  width: 100%;
  min-height: 100%;
  padding: 0.5rem 1rem;
  position: relative;
}
.match-wrapper::before {
  content: "";
  position: fixed;
  inset: 0;
}
@media (prefers-color-scheme: dark) {
  .match-wrapper::before {
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
  .match-wrapper::before {
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

.decor {
  position: fixed;
  top: 40%;
  left: -20%;
  width: 75%;
  transform: rotate(35deg);
  opacity: 0.6;
  transition: all 0.3s;
}

@media (prefers-color-scheme: dark) {
  .decor {
    top: 45%;
    left: -25%;
    opacity: 0.2;
  }
}
</style>
