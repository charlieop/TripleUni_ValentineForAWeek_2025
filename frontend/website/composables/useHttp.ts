const API_URL = "https://api.charlieop.com/api/v1/";
const CONFIG_URL = "https://api.charlieop.com/media/config.json";
// const API_URL = "http://192.168.71.91:8000/api/v1/";
// const CONFIG_URL = "http://192.168.71.91:8000/media/config.json";



const { getOpenId } = useStore();

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

  const postApplicantPaymentVoucher = async (
    applicant_id: string,
    voucher_id: string
  ): Promise<boolean> => {
    const response = await _fetch(`applicants/${applicant_id}/deposit/`, {
      method: "POST",
      body: JSON.stringify({ code: voucher_id }),
    });
    if (response.status === 200) {
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
    postApplicantPaymentVoucher,
  };
};
