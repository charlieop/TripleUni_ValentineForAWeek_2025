const defaultConfig: Config = {
  APPLICATION_DEADLINE: "2025-02-04T10:00",
  FIRST_ROUND_MATCH_RESULTS_RELEASE: "2025-02-04T20:00",
  FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE: "2025-02-05T23:59",
  SECOND_ROUND_MATCH_RESULTS_RELEASE: "2025-02-06T09:00",
  SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE: "2025-02-07T12:00",
  EVENT_START: "2025-02-07T23:00",
  FIRST_TASK_START: "2025-02-08T00:00",
  FIRST_TASK_DEADLINE: "2025-02-09T01:00",
  EVENT_END: "2025-02-15T02:00",
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
