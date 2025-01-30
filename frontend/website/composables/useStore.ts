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

  

  return {
    setOpenId,
    getOpenId,
    clearOpenId,

    setApplicantId,
    getApplicantId,
    clearApplicantId,
  };
};
