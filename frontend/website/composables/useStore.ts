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

export const useStore = () => {
  const setOpenId = (openId: string): void => {
    localStorage.setItem("openId", openId);
  };
  const getOpenId = (): string | null => {
    return localStorage.getItem("openId");
  };
  const clearOpenId = (): void => {
    localStorage.removeItem("openId");
  };

  const setApplicantId = (applicationId: string): void => {
    if (
      !/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(
        applicationId
      )
    ) {
      throw new Error("Invalid UUID format");
    }
    localStorage.setItem("applicantId", applicationId);
  };
  const getApplicantId = (): string | null => {
    return localStorage.getItem("applicantId");
  };
  const clearApplicantId = (): void => {
    localStorage.removeItem("applicantId");
  };

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
  };
  const getConfig = (): Config | null => {
    const config = sessionStorage.getItem("config");
    return config ? JSON.parse(config) : null;
  };
  const clearConfig = (): void => {
    sessionStorage.removeItem("config");
  };

  return {
    setOpenId,
    getOpenId,
    clearOpenId,

    setApplicantId,
    getApplicantId,
    clearApplicantId,

    setMatchId,
    getMatchId,
    clearMatchId,

    setConfig,
    getConfig,
    clearConfig,
  };
};
