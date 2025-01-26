<template>
  <h1>Hi</h1>
  <p>Here is some text</p>
  <p>Is WeChat: {{ isWechat }}</p>
  <br />
  <a :href="url">TEST</a>
  <h2>Query Params:</h2>
  <p>{{ queryParams }}</p>
  <h2>Res:</h2>
  <p>{{ res }}</p>
</template>

<script setup>
// let fromURL = "http://api.charlieop.com:8000";
let fromURL = "http://192.168.71.85:3000";

let appID = "wx04ddbc9e6bebf0e5";

let url =
  "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" +
  appID +
  "&redirect_uri=" +
  encodeURIComponent(fromURL) +
  "&response_type=code&scope=snsapi_userinfo#wechat_redirect";

const route = useRoute();
const queryParams = route.query;
const isWechat = computed(() => {
  var ua = window.navigator.userAgent.toLowerCase();
  if (ua.match(/MicroMessenger/i) == "micromessenger") {
    return true;
  } else {
    return false;
  }
});
const res = ref();

onMounted(() => {
  if (isWechat.value && !queryParams.code) {
    window.location.href = url;
  }

  const code = queryParams.code;
  if (!code) {
    return;
  }

  const result = fetch(`http:///192.168.71.85:8000/api/v1/oauth/wechat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code }),
  })
    .then((res) => res.json())
    .then((data) => {
      res.value = data;
      console.log(data);
      return data;
    });
});
</script>
