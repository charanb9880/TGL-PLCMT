import axios from "axios";


const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

const client = axios.create({ baseURL: API_BASE });


const compactParams = (params) => {
  const cleaned = {};
  Object.entries(params || {}).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      cleaned[key] = value;
    }
  });
  return cleaned;
};


const translateCompanyParams = (params) => {
  const mapping = {
    focus_sectors: "focusSector",
    employee_size: "employeeSize",
    profitability_status: "profitabilityStatus",
    remote_policy_details: "remoteWorkPolicy",
    hiring_velocity: "hiringVelocity",
    sort_by: "sortBy",
  };

  return Object.entries(params || {}).reduce((accumulator, [key, value]) => {
    accumulator[mapping[key] || key] = value;
    return accumulator;
  }, {});
};


export const fetchDatasetStatus = async () => {
  const { data } = await client.get("/dataset/status");
  return data;
};

export const fetchImportPreview = async () => {
  const { data } = await client.get("/import/preview");
  return data;
};

export const fetchCompanies = async (params = {}) => {
  const { data } = await client.get("/companies", { params: compactParams(translateCompanyParams(params)) });
  return data;
};

export const fetchCompany = async (companyId) => {
  const { data } = await client.get(`/companies/${encodeURIComponent(companyId)}`);
  return data;
};

export const fetchCategories = async () => {
  const { data } = await client.get("/categories");
  return data;
};

export const fetchAnalytics = async () => {
  const { data } = await client.get("/analytics");
  return data;
};

export const fetchComparison = async (leftCompanyId, rightCompanyId) => {
  const { data } = await client.get("/compare", { 
    params: { left_company_id: leftCompanyId, right_company_id: rightCompanyId } 
  });
  return data;
};

export const runSkillMatch = async (payload) => {
  const { data } = await client.post("/skill-match", payload);
  return data;
};

export default client;