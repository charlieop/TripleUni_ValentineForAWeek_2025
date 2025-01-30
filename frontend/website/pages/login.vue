<template>
  <div class="login-wrapper">
    <div class="logo">
      <img
        src="/imgs/logo-b.webp"
        alt="Valentine For A Week Logo"
        v-if="!isDarkMode"
      />
      <img src="/imgs/logo-p.webp" alt="Valentine For A Week Logo" v-else />
    </div>
    <div class="content-wrapper">
      <h1>{{ jump ? "正在转跳授权中..." : "请点击下方授权登陆" }}</h1>
      <p>注意: 请不要使用虚拟账户 (momo)</p>
      <p class="push">
        我们需要获取你的<strong>真实</strong>用户昵称及头像用作匹配目的
      </p>
    </div>
    <div class="decor-heart">
      <img src="/imgs/heart2.webp" alt="" />
    </div>
    <div class="decor-couple">
      <img src="/imgs/couple1.webp" alt="" />
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const router = useRouter();
const jump = computed(() => isWechat.value && !queryParams.code);
const { setOpenId } = useStore();
const { fetchOpenId } = useHttp();

const queryParams = route.query;
const requestURL = "http://wechat-oauth.uuunnniii.com";
const appID = "wx09ec18a3cf830379";
let url =
  requestURL +
  "?appid=" +
  appID +
  "&redirect_uri=" +
  encodeURIComponent(window.location.href) +
  "&response_type=code&scope=snsapi_userinfo#wechat_redirect";

onMounted(() => {
  if (jump.value) {
    setTimeout(() => {
      window.location.href = url;
    }, 1500);
  }

  const code = queryParams.code;
  if (typeof code === "string") {
    fetchOpenId(code)
      .then((openid) => {
        if (openid) {
          setOpenId(openid);
          router.push("/");
        }
      })
      .catch((error: Error) => {
        alert("获取OpenId失败: " + error.message);
      });
  }
});
</script>

<style scoped>
.login-wrapper {
  width: 100%;
  height: 100%;
  padding: 0.5rem 1rem;
  position: relative;
  overflow: hidden;
}

.logo img {
  width: 100%;
  transform: translateX(-2%);
}
.content-wrapper {
  line-height: 1.5;
  padding: 0 1.5rem;
}

h1 {
  font-size: var(--fs-600);
  color: var(--clr-primary);
  text-align: center;
  margin-bottom: 0.75em;
  letter-spacing: 2px;
}
.push {
  padding-left: 4ch;
}

.decor-couple {
  position: absolute;
  width: 80%;
  left: 10%;
  bottom: -0.5rem;
}
.decor-heart {
  position: absolute;
  width: 40%;
  left: 27%;
  bottom: 14%;
  animation: updown 7s infinite ease-in-out;
}
@keyframes updown {
  0% {
    transform: translateY(0.25rem);
  }
  50% {
    transform: translateY(-0.25rem) scale(1.05);
  }
  100% {
    transform: translateY(0.25rem);
  }
}
</style>
