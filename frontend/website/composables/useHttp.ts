const { getOpenId, setDeleted } = useStore();

export const useHttp = () => {
  const _fetch = (endpoint: string, options: RequestInit = {}) => {
    const openId = getOpenId();
    if (!openId) {
      throw new Error("OpenId 未初始化");
    }
    return fetch(API_URL + endpoint, {
      ...options,
      headers: {
        ...options.headers,
        "Content-Type": "application/json",
        Authorization: openId,
      },
    });
  };

  const fetchConfig = async (): Promise<any> => {
    const response = await fetch(CONFIG_URL);
    if (response.status === 200) {
      return await response.json();
    }
    throw new Error("配置文件加载失败");
  };

  const fetchOpenId = async (code: string): Promise<string | null> => {
    const response = await fetch(API_URL + "oauth/wechat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: code }),
    });
    const data = await response.json();
    if (response.status === 200) {
      const openid = data?.data?.openid;
      return openid;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const fetchApplicantId = async (): Promise<string | null> => {
    const response = await _fetch("applicants/", {
      method: "GET",
    });
    if (response.status === 200) {
      const data = await response.json();
      return data.data.id;
    }
    if (response.status === 204) {
      return null;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };
  const postApplicant = async (applicant: any): Promise<string> => {
    const response = await _fetch("applicants/", {
      method: "POST",
      body: JSON.stringify(applicant),
    });
    const data = await response.json();
    if (response.status === 201) {
      return data.data.id;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const fetchApplicantDetail = async (applicant_id: string): Promise<any> => {
    const response = await _fetch(`applicants/${applicant_id}/`, {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data;
    }
    if (response.status === 410) {
      setDeleted();
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };
  const patchApplicant = async (
    applicant_id: string,
    applicant: any
  ): Promise<boolean> => {
    const response = await _fetch(`applicants/${applicant_id}/`, {
      method: "PATCH",
      body: JSON.stringify(applicant),
    });
    if (response.status === 200) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };
  const deleteApplicant = async (applicant_id: string): Promise<boolean> => {
    const response = await _fetch(`applicants/${applicant_id}/`, {
      method: "DELETE",
    });
    if (response.status === 204) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const getApplicantHasPaid = async (
    applicant_id: string
  ): Promise<boolean> => {
    const response = await _fetch(`applicants/${applicant_id}/deposit/`, {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data.paid;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const fetchMatchResult = async (): Promise<{
    id: number;
    round: 1 | 2;
  } | null> => {
    const response = await _fetch("matches/result/", {
      method: "GET",
    });
    if (response.status === 204) {
      return null;
    }
    const data = await response.json();
    if (response.status === 200) {
      return data.data;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };
  const fetchMatchMentor = async (match_id: number): Promise<MentorInfo> => {
    const response = await _fetch(`matches/${match_id}/mentor/`, {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data as MentorInfo;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };
  const fetchMatchPartner = async (match_id: number): Promise<MatchDetail> => {
    const response = await _fetch(`matches/${match_id}/partner/`, {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data as MatchDetail;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };
  const postMatchConfirmation = async (
    match_id: number,
    confirmation: boolean
  ): Promise<boolean> => {
    const action = confirmation ? "A" : "R";
    const response = await _fetch(`matches/${match_id}/partner/`, {
      method: "POST",
      body: JSON.stringify({ action }),
    });
    if (response.status === 200) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const requestPayment = async (): Promise<PaymentDetails> => {
    const response = await _fetch("wechat/payment/", {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data as PaymentDetails;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const fetchMatch = async (match_id: number): Promise<Match> => {
    const response = await _fetch(`matches/${match_id}/`, {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data as Match;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const patchMatchName = async (
    match_id: number,
    name: string
  ): Promise<boolean> => {
    const response = await _fetch(`matches/${match_id}/`, {
      method: "PATCH",
      body: JSON.stringify({ name }),
    });
    if (response.status === 200) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const fetchSecretMission = async (): Promise<Mission> => {
    const response = await _fetch("secret-missions/", {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data as Mission;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const fetchMission = async (): Promise<Mission> => {
    const response = await _fetch("missions/", {
      method: "GET",
    });
    const data = await response.json();
    if (response.status === 200) {
      return data.data as Mission;
    }
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const fetchTask = async (
    matchId: number,
    day: number
  ): Promise<Task | null> => {
    const response = await _fetch(`matches/${matchId}/tasks/day${day}/`, {
      method: "GET",
    });
    if (response.status === 200) {
      const data = await response.json();
      return data.data as Task;
    }
    if (response.status === 204) {
      return null;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const postTask = async (
    matchId: number,
    day: number,
    submit_text: string
  ): Promise<boolean> => {
    const response = await _fetch(`matches/${matchId}/tasks/day${day}/`, {
      method: "POST",
      body: JSON.stringify({ submit_text }),
    });
    if (response.status === 201) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const postTaskImages = async (
    matchId: number,
    day: number,
    imgs: File[]
  ): Promise<boolean> => {
    const formData = new FormData();
    imgs.forEach((img, index) => {
      formData.append("images", img, `image${index}.jpg`);
    });
    const response = await fetch(
      API_URL + `matches/${matchId}/tasks/day${day}/images/`,
      {
        method: "POST",
        headers: {
          Authorization: getOpenId()!,
          "Accept-Encoding": "gzip, deflate, br",
        },
        body: formData,
      }
    );
    if (response.status === 201) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };
  const patchTask = async (
    matchId: number,
    day: number,
    submit_text: string
  ): Promise<boolean> => {
    const response = await _fetch(`matches/${matchId}/tasks/day${day}/`, {
      method: "PATCH",
      body: JSON.stringify({ submit_text }),
    });
    if (response.status === 200) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  const deleteImage = async (matchId: number, day: number, imgId: string) => {
    const response = await _fetch(
      `matches/${matchId}/tasks/day${day}/images/${imgId}/`,
      {
        method: "DELETE",
      }
    );
    if (response.status === 204) {
      return true;
    }
    const data = await response.json();
    throw new Error(`${JSON.stringify(data?.detail || data)}`);
  };

  return {
    fetchConfig,
    fetchOpenId,

    fetchApplicantId,
    postApplicant,

    fetchApplicantDetail,
    patchApplicant,
    deleteApplicant,

    getApplicantHasPaid,

    fetchMatchResult,
    fetchMatchMentor,
    fetchMatchPartner,
    postMatchConfirmation,

    requestPayment,

    fetchMatch,
    patchMatchName,

    fetchSecretMission,
    fetchMission,

    fetchTask,
    postTask,
    patchTask,
    postTaskImages,
    deleteImage,
  };
};
