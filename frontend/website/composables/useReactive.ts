interface Config {
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

export const useReactive = () => {
  const setMatchId = (matchId: number): void => {
    sessionStorage.setItem("matchId", matchId.toString());
  };
  const getMatchId = (): number | null => {
    const matchId = sessionStorage.getItem("matchId");
    return matchId ? parseInt(matchId, 10) : null;
  };
  const clearMatchId = (): void => {
    sessionStorage.removeItem("matchId");
  };

  const setConfig = (config: Config): void => {
    sessionStorage.setItem("config", JSON.stringify(config));
    CONFIG.value = config;
  };
  const getConfig = (): Config | null => {
    const config = sessionStorage.getItem("config");
    return config ? JSON.parse(config) : null;
  };
  const clearConfig = (): void => {
    sessionStorage.removeItem("config");
    CONFIG.value = null;
  };
  const CONFIG = useState<Config | null>("config", () => getConfig());

  return {
    setMatchId,
    getMatchId,
    clearMatchId,

    setConfig,
    getConfig,
    clearConfig,
    CONFIG,
  };
};
