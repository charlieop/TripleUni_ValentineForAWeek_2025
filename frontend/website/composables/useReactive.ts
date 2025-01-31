const defaultConfig: Config = {
  APPLICATION_DEADLINE: "2025/02/04 10:00:00",
  FIRST_ROUND_MATCH_RESULTS_RELEASE: "2025/02/04 20:00:00",
  FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE: "2025/02/05 23:59:59",
  SECOND_ROUND_MATCH_RESULTS_RELEASE: "2025/02/06 09:00:00",
  SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE: "2025/02/07 12:00:00",
  EVENT_START: "2025/02/07 23:00:00",
  FIRST_TASK_START: "2025/02/08 00:00:00",
  FIRST_TASK_DEADLINE: "2025/02/09 01:00:00",
  EVENT_END: "2025/02/15 02:00:00",
};

export const useReactive = () => {
  const setConfig = (config: Config): void => {
    localStorage.setItem("config", JSON.stringify(config));
    CONFIG.value = config;
  };
  const getConfig = (): Config => {
    const config = localStorage.getItem("config");
    return config ? JSON.parse(config) : defaultConfig;
  };
  const clearConfig = (): void => {
    localStorage.removeItem("config");
    CONFIG.value = defaultConfig;
  };
  const CONFIG = useState<Config>("config", () => getConfig());

  return {
    setConfig,
    getConfig,
    clearConfig,
    CONFIG,
  };
};
