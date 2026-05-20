export const formatValue = (value) => {
  if (value === null || value === undefined || value === "") {
    return "Not available";
  }

  if (typeof value === "string" && value.startsWith("http")) {
    return value;
  }

  if (typeof value === "object") {
    // Check if it's an InnovX-style JSON (with job_role_details)
    const roles = value.job_role_details || (Array.isArray(value) ? value : null);
    if (roles && Array.isArray(roles)) {
      return roles.map(r => r.role_title || r.role_category).filter(Boolean).join(", ") || "Details available in JSON";
    }
    return JSON.stringify(value);
  }

  return String(value);
};


export const isUrl = (value) => typeof value === "string" && /^https?:\/\//i.test(value);


export const extractPrimaryUrl = (value) => {
  if (!value) {
    return null;
  }

  const parts = String(value)
    .split(/[;,]/)
    .map((part) => part.trim())
    .filter((part) => /^https?:\/\//i.test(part));

  return parts[0] || null;
};


export const extractDomain = (url) => {
  if (!url) return null;
  try {
    const cleanUrl = String(url).split(/[;,]/)[0].trim();
    const parsed = new URL(cleanUrl.startsWith("http") ? cleanUrl : `https://${cleanUrl}`);
    return parsed.hostname.replace(/^www\./i, "");
  } catch {
    return null;
  }
};


/**
 * Higher-order utility to get the best possible logo URL.
 * Extracts the first URL from a composite string and validates it.
 */
export function getLogoUrl(value) {
  const primary = extractPrimaryUrl(value);
  if (primary && isUrl(primary)) return primary;
  return null;
}


export const truncate = (value, maxLength = 140) => {
  const text = formatValue(value);
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength)}…`;
};


export const getCompanyIdentifier = (company) => company?.company_id ?? company?.["Company Name"];


export const getCompanyHeadline = (company) => company?.["Company Name"] || company?.["Short Name"] || "Company";


export const toOptions = (values = []) => values.map((value) => ({ label: value, value }));


export const buildChartPalette = () => ["#0055ff", "#1f2937", "#71717a", "#d4d4d8", "#cbd5e1", "#10b981"];