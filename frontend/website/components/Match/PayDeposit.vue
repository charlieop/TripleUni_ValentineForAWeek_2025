<template>
  <div class="conten-wrapper">
    <h1>第{{ match?.round }}轮匹配成功！</h1>
    <p>恭喜！我们已经根据你的要求找到了一位合适的嘉宾。</p>
    <p>
      我们还为你安排了一位Mentor。活动中如有任何疑问或需要帮助，ta将非常乐意协助。
    </p>
    <p>
      以下是ta的微信，在添加时请备注你的组号:
      <strong>「第{{ match?.matchId }}组」</strong>
    </p>
    <div class="wechat-info" v-if="mentor">
      <div class="hint">长按图片识别二维码</div>
      <img
        :src="API_HOST + mentor?.wechat_qrcode"
        :alt="'微信号:' + mentor?.wechat"
      />
      <p>微信号: {{ mentor.wechat }}</p>
    </div>
    <h2>押金缴纳</h2>
    <p>
      为了让双方都拥有更好的体验，我们要求提前你缴纳<strong>70元人民币</strong>的押金作为不会中途退出活动的担保。
    </p>
    <p>
      你可以在
      <a
        href="https://mp.weixin.qq.com/s/F2IHbExetIvUc_eLENcYvw"
        target="_blank"
        >这里</a
      >
      查看具体的规则。你在缴纳押金后将可以查看匹配嘉宾的信息。
    </p>
    <button class="btn primary" @click="pay">缴纳押金</button>
    <p class="small">缴纳押金即代表你已阅读并同意遵守以上规则</p>
  </div>
  <ModalLoading :model-value="loading" :text="modalText" />
</template>

<script setup lang="ts">
const { requestPayment, getApplicantHasPaid, fetchMatchMentor } = useHttp();
const { getApplicantId, setPaid, getMatchInfo } = useStore();
const loading = ref(false);
const modalText = ref<string | null>(null);
const router = useRouter();
const match = ref<MatchInfo | null>(null);
const mentor = ref<MentorInfo | null>(null);

declare const WeixinJSBridge: {
  invoke: (
    method: string,
    paymentDetails: PaymentDetails,
    callback: (res: { err_msg: string }) => void
  ) => void;
};

function InitPayment(paymentDetails: PaymentDetails) {
  WeixinJSBridge.invoke(
    "getBrandWCPayRequest",
    paymentDetails,
    async function (res) {
      if (res.err_msg === "get_brand_wcpay_request:ok") {
        setPaid();
        alert("支付成功");
        modalText.value = "支付成功, 正在刷新";

        const applicantId = getApplicantId();
        if (applicantId === null) {
          setTimeout(() => {
            refresh();
          }, 2000);
          return;
        }

        let paid = false;
        for (let i = 0; i < 3; i++) {
          paid = await getApplicantHasPaid(applicantId);
          if (paid) {
            refresh();
            break;
          }
          await new Promise((resolve) => setTimeout(resolve, 500 * (i + 1)));
        }
      } else {
        alert("支付失败");
        loading.value = false;
        modalText.value = null;
      }
    }
  );
}

async function pay() {
  modalText.value = "正在获取支付订单";
  loading.value = true;
  requestPayment()
    .then((data) => {
      modalText.value = "等待支付中";
      if (typeof WeixinJSBridge === "undefined") {
        document.addEventListener(
          "WeixinJSBridgeReady",
          () => {
            InitPayment(data);
          },
          false
        );
      } else {
        InitPayment(data);
      }
    })
    .catch((error: Error) => {
      alert("获取微信支付订单失败: " + error.message);
    });
}

onMounted(async () => {
  const matchInfo = getMatchInfo();
  if (matchInfo === null || matchInfo.matchId <= 0) {
    alert("意料之外的错误: 找不到本地match info");
    router.push("/");
    return;
  }
  match.value = matchInfo;

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
});
</script>

<style scoped>
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
  transform: translate(-50%, 100%);
  width:max-content;
}

h1 {
  font-size: var(--fs-700);
  text-align: center;
  margin-block: 0.5rem 0.5em;
  color: var(--clr-text);
}
h2 {
  font-size: var(--fs-700);
  text-align: center;
  margin-block: 3.5rem 0.5em;
  color: var(--clr-text);
}

a {
  color: var(--clr-secondary);
  text-decoration: underline;
  text-underline-offset: 4px;
  font-size: 1.1em;
  font-weight: bold;
}
p {
  font-size: var(--fs-400);
  padding-inline: 1rem;
  margin-bottom: 0.5em;
}
strong {
  color: var(--clr-accent);
  font-size: 1.1em;
}
button {
  display: block;
  margin: 1rem auto 0.5rem auto;
  width: 90%;
  font-size: var(--fs-500);
  font-weight: bold;
  cursor: pointer;
}
.small {
  font-size: var(--fs-200);
  color: var(--clr-text--muted);
  text-align: center;
}
.conten-wrapper {
  position: relative;
  padding-bottom: 7rem;
}
</style>
