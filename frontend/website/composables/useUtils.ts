export const API_URL = "https://api.charlieop.com/api/v1/";
export const CONFIG_URL = "https://api.charlieop.com/media/config.json";
export const API_HOST = "https://api.charlieop.com";
// export const API_URL = "http://192.168.3.4:8000/api/v1/";
// export const CONFIG_URL = "http://192.168.3.4:8000/media/config.json";
// export const API_HOST = "http://192.168.3.4:8000";

export const APPID = "wx09ec18a3cf830379";

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

export interface PaymentDetails {
  appId: string;
  timeStamp: string;
  nonceStr: string;
  package: string;
  signType: string;
  paySign: string;
}

export interface MatchInfo {
  matchId: number;
  round: 1 | 2;
  discarded: boolean;
}

export interface MentorInfo {
  name: string;
  wechat: string;
  wechat_qrcode: string;
}

export function convertToLocalTime(dateString: string): Date {
  const offset = new Date().getTimezoneOffset() * 60 * 1000;
  const LocalTime =
    new Date(dateString).getTime() - offset - 8 * 60 * 60 * 1000;
  return new Date(LocalTime);
}

export interface Task {
  day: number;
  submit_text: string;
  basic_score: number;
  bonus_score: number;
  daily_score: number;
  imgs: Array<{ id: string; path: string }>;
}

export interface Match {
  id: number;
  name: string;
  my_info: {
    nickname: string;
    head_image: string;
    head_image_url: string;
  };
  partner_info: {
    nickname: string;
    head_image: string;
    head_image_url: string;
  };
  partner_wxid: string;
  tasks: Task[];
  total_score: number;
}

export interface Mission {
  title: string;
  content: string;
  link: string;
}
