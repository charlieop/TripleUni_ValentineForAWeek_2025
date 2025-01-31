export const API_URL = "https://api.charlieop.com/api/v1/";
export const CONFIG_URL = "https://api.charlieop.com/media/config.json";
export const API_HOST = "https://api.charlieop.com";
// export const API_URL = "http://192.168.71.91:8000/api/v1/";
// export const CONFIG_URL = "http://192.168.71.91:8000/media/config.json";
// export const API_HOST = "http://192.168.71.91:8000";

export const isWechat = computed(() => {
  var ua = window.navigator.userAgent.toLowerCase();
  if (ua.match(/MicroMessenger/i) !== null) {
    return true;
  } else {
    return false;
  }
});

export function refresh() {
  const url = new URL(window.location.href);
  window.location.href = url.origin + url.pathname;
}

export const isDarkMode = ref(false);
isDarkMode.value =
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: dark)").matches;
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    isDarkMode.value = e.matches;
  });

export const IMAGE_BASE_URL = "https://i.boatonland.com/valentine/2025/";

export interface MatchDetail {
  round: number;
  discarded: boolean;
  discard_reason: string;
  my_status: "A" | "R" | "P";
  partner_status: "A" | "R" | "P";
  partner_info: {
    nickname: string;
    head_image: string;
    head_image_url: string;
  };
  partner_paid: boolean;
  partner_sex: "M" | "F";
  partner_school: "HKUST" | "HKU" | "CUHK";
}

export interface VueformInstance {
  data: Record<string, any>;
  load(data: Record<string, any>): void;
}

export interface Config {
  APPLICATION_DEADLINE: string;
  FIRST_ROUND_MATCH_RESULTS_RELEASE: string;
  FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE: string;
  SECOND_ROUND_MATCH_RESULTS_RELEASE: string;
  SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE: string;
  EVENT_START: string;
  FIRST_TASK_START: string;
  FIRST_TASK_DEADLINE: string;
  EVENT_END: string;
}

export interface Match {
  id: number;
  name: string;
  start: string;
  end: string;
}
