// https://nuxt.com/docs/api/configuration/nuxt-config
import { resolve } from "path";

const IMAGE_BASE_URL = "https://i.boatonland.com/valentine/2025/";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: false },
  alias: {
    "@": resolve(__dirname, "."),
  },
  css: [
    "@/assets/css/fonts.css",
    "@/assets/css/resets.css",
    "@/assets/css/style.css",
  ],
  modules: ["@vueform/nuxt", "@nuxt/ui"],
  ssr: false,
  app: {
    baseURL: "/",
    head: {
      title: "一周CP 2025",
      viewport:
        "width=device-width, initial-scale=1, user-scalable=no, viewport-fit=cover",
      link: [
        {
          rel: "icon",
          type: "image/x-icon",
          href: "https://tripleuni.com/img/logo-512.461b29bd.png",
        },
      ],
    },
  },
});
