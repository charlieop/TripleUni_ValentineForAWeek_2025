import Match from "~/pages/match.vue";

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

  const setDeleted = (): void => {
    localStorage.setItem("deleted", "true");
  };
  const getDeleted = (): boolean => {
    return localStorage.getItem("deleted") === "true";
  };
  const clearDeleted = (): void => {
    localStorage.removeItem("deleted");
  };

  const setMatchInfo = (
    matchId: number,
    round: 1 | 2,
    discarded: boolean = false
  ): void => {
    const matchInfo = JSON.stringify({ matchId, round, discarded });
    sessionStorage.setItem("matchInfo", matchInfo);
  };
  const getMatchInfo = (): MatchInfo | null => {
    const matchInfo = sessionStorage.getItem("matchInfo");
    if (matchInfo) {
      return JSON.parse(matchInfo) as { matchId: number; round: 1 | 2; discarded: boolean };
    }
    return null;
  };
  const clearMatchInfo = (): void => {
    localStorage.removeItem("matchInfo");
    sessionStorage.removeItem("matchInfo");
  };

  const setMatch = (match: Match) => {
    sessionStorage.setItem("match", JSON.stringify(match));
  }
  const getMatch = (): Match | null => {
    const match = sessionStorage.getItem("match");
    if (match) {
      return JSON.parse(match) as Match;
    }
    return null;
  }
  const clearMatch = () => {
    sessionStorage.removeItem("match");
  }

  const setPaid = (): void => {
    localStorage.setItem("paid", "true");
  }
  const getPaid = (): boolean => {
    return localStorage.getItem("paid") === "true";
  }
  const clearPaid = (): void => {
    localStorage.removeItem("paid");
  }

  return {
    setOpenId,
    getOpenId,
    clearOpenId,

    setApplicantId,
    getApplicantId,
    clearApplicantId,

    setDeleted,
    getDeleted,
    clearDeleted,

    setMatchInfo,
    getMatchInfo,
    clearMatchInfo,

    setPaid,
    getPaid,
    clearPaid,

    setMatch,
    getMatch,
    clearMatch,
  };
};
