<template>
  <UModal
    :ui="{
      padding: 'p-0 sm:p-0',
      margin: 'my-0 sm:my-0',
      width: '',
      container: 'items-center',
      overlay: {
        background: 'bg-gray-700/90 dark:bg-gray-900/90',
      },
      background: 'bg-transparent dark:bg-transparent',
      shadow: 'shadow-none',
    }"
    preventClose
  >
    <div class="loading-wrapper">
      <div class="logo">
        <img
          :src="IMAGE_BASE_URL + 'logo-w.webp'"
          alt="Valentine For A Week Logo"
          v-if="!isDarkMode"
        />
        <img
          :src="IMAGE_BASE_URL + 'logo-p.webp'"
          alt="Valentine For A Week Logo"
          v-else
        />
      </div>
      <h3>
        {{ text || "正在联系月老" }}
        <span class="dots">...</span>
      </h3>

      <div class="decor-hearts">
        <div class="heart">
          <svg
            width="80"
            height="80"
            viewBox="0 0 800 700"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="m263.42 235.15c-66.24 0-120 53.76-120 120 0 134.76 135.93 170.09 228.56 303.31 87.574-132.4 228.56-172.86 228.56-303.31 0-66.24-53.76-120-120-120-48.048 0-89.402 28.37-108.56 69.188-19.161-40.817-60.514-69.188-108.56-69.188z"
            />
          </svg>
        </div>
        <div class="heart">
          <svg
            width="70"
            height="70"
            viewBox="0 0 800 700"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="m263.42 235.15c-66.24 0-120 53.76-120 120 0 134.76 135.93 170.09 228.56 303.31 87.574-132.4 228.56-172.86 228.56-303.31 0-66.24-53.76-120-120-120-48.048 0-89.402 28.37-108.56 69.188-19.161-40.817-60.514-69.188-108.56-69.188z"
            />
          </svg>
        </div>
        <div class="heart">
          <svg
            width="68"
            height="68"
            viewBox="0 0 800 700"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="m263.42 235.15c-66.24 0-120 53.76-120 120 0 134.76 135.93 170.09 228.56 303.31 87.574-132.4 228.56-172.86 228.56-303.31 0-66.24-53.76-120-120-120-48.048 0-89.402 28.37-108.56 69.188-19.161-40.817-60.514-69.188-108.56-69.188z"
            />
          </svg>
        </div>
      </div>
      <div class="decor-couple">
        <img :src="IMAGE_BASE_URL + 'couple2.webp'" alt="" />
      </div>
    </div>
  </UModal>
</template>

<script setup lang="ts">
const props = defineProps<{
  text: string | null;
}>();

const text = ref(props.text);
</script>

<style scoped>
.loading-wrapper {
  height: var(--height);
  max-width: var(--max-width);
  /* background-color: red; */
  padding: 0.5rem 1rem;
  position: relative;
  overflow: hidden;
}
.logo img {
  margin-inline: auto;
  transform: translateX(-2%);
}
h3 {
  display: flex;
  justify-content: center;
  align-items: baseline;
  margin-top: 3vh;
  font-size: var(--fs-600);
  font-weight: 500;
  color: var(--clr-primary);
  text-align: center;
  margin-bottom: 1rem;
}
.dots {
  display: inline-block;
  width: fit-content;
  font-weight: bold;
  font-family: monospace;
  font-size: 20px;
  clip-path: inset(0 3ch 0 0);
  animation: l4 3s steps(4) infinite;
}
@keyframes l4 {
  to {
    clip-path: inset(0 -1ch 0 0);
  }
}

.decor-couple {
  position: absolute;
  width: 80%;
  bottom: -0.25rem;
  left: 53%;
  transform: translateX(-50%);
}

.decor-couple img {
  width: 100%;
}

.decor-hearts {
  width: 4rem;
  margin-inline: auto;
  position: absolute;
  bottom: 26%;
  left: 45%;
  transform: translateX(-50%);
}
.heart {
  position: relative;
}
.heart:nth-child(1) svg {
  opacity: 0;
  -webkit-animation: heartUp 2s infinite ease-in;
  animation: heartUp 2s infinite ease-in;
}
.heart:nth-child(2) svg {
  position: absolute;
  left: 1rem;
  bottom: 0;
  opacity: 0;
  -webkit-animation: heartUp 2s 0.3s infinite ease-in;
  animation: heartUp 2s 0.3s infinite ease-in;
}
.heart:nth-child(3) svg {
  position: absolute;
  left: 0.5rem;
  bottom: 0;
  opacity: 0;
  -webkit-animation: heartUp 2s 0.6s infinite ease-in;
  animation: heartUp 2s 0.6s infinite ease-in;
}

svg {
  fill: #f58d9c;
}

@-webkit-keyframes heartUp {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, 0, 0) rotate(10deg);
    transform: translate3d(0, 0, 0) rotate(10deg);
  }
  50% {
    opacity: 1;
  }
  65% {
    opacity: 1;
  }
  80% {
    opacity: 0;
    -webkit-transform: translate3d(0, -28vh, 0) scale(1.2) rotate(-10deg);
    transform: translate3d(0, -28vh, 0) scale(1.2) rotate(-10deg);
  }
  100% {
    opacity: 0;
  }
}
@keyframes heartUp {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, 0, 0) rotate(10deg);
    transform: translate3d(0, 0, 0) rotate(10deg);
  }
  40% {
    opacity: 1;
  }
  55% {
    opacity: 1;
  }
  80% {
    opacity: 0;
    -webkit-transform: translate3d(0, -28vh, 0) scale(1.2) rotate(-10deg);
    transform: translate3d(0, -28vh, 0) scale(1.2) rotate(-10deg);
  }
  100% {
    opacity: 0;
  }
}
</style>
