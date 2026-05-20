import { getFieldValue } from "./fieldMapper";
const normalizeValue = (value) => String(value || "").toLowerCase();


export const buildCompanyHighlights = (company = {}) => {
  const strengths = [];
  const risks = [];

  const getV = (field) => getFieldValue(company, field);

  if (normalizeValue(getV("Brand value")).includes("high")) {
    strengths.push(`Brand value: ${getV("Brand value")}`);
  }
  if (normalizeValue(getV("Profitability Status")).includes("profit")) {
    strengths.push(`Profitability: ${getV("Profitability Status")}`);
  }
  if (normalizeValue(getV("AI/ML Adoption Level")).includes("high")) {
    strengths.push(`Technology adoption: ${getV("AI/ML Adoption Level")}`);
  }
  if (normalizeValue(getV("Learning culture")).includes("strong")) {
    strengths.push(`Learning culture: ${getV("Learning culture")}`);
  }

  if (normalizeValue(getV("Burnout risk")).includes("high")) {
    risks.push(`Burnout risk: ${getV("Burnout risk")}`);
  }
  if (normalizeValue(getV("Profitability Status")).includes("not profitable")) {
    risks.push(`Profitability risk: ${getV("Profitability Status")}`);
  }
  if (normalizeValue(getV("Customer Concentration Risk")).includes("yes")) {
    risks.push(`Customer concentration risk: ${getV("Customer Concentration Risk")}`);
  }
  if (getV("Legal Issues / Controversies")) {
    risks.push(`Legal issues / controversies: ${getV("Legal Issues / Controversies")}`);
  }

  return {
    strengths: strengths.slice(0, 4),
    weaknesses: risks.slice(0, 2),
    risks: risks.slice(0, 4),
  };
};