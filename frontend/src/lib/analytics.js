const FIXED_CATEGORY_LABELS = {
  "Tech Giants": ["tech giant", "enterprise", "platform", "cloud", "data"],
  "Product Companies": ["product", "saas", "platform", "fintech"],
  "Service Companies": ["service", "consulting", "outsourcing", "agency"],
  Startups: ["startup", "unicorn", "scale-up", "scale up"],
};


const normalizeValue = (value) => String(value || "").trim();


const countByField = (companies, field) => {
  const counts = new Map();
  companies.forEach((company) => {
    const label = normalizeValue(company[field]);
    if (!label) {
      return;
    }
    counts.set(label, (counts.get(label) || 0) + 1);
  });
  return Array.from(counts.entries())
    .map(([label, value]) => ({ label, value }))
    .sort((left, right) => right.value - left.value);
};


export const buildAnalyticsFromCompanies = (companies = []) => ({
  total_companies: companies.length,
  category_distribution: countByField(companies, "Category"),
  hiring_velocity_distribution: countByField(companies, "Hiring Velocity"),
  profitability_mix: countByField(companies, "Profitability Status"),
  work_mode_distribution: countByField(companies, "Remote Work Policy"),
  category_tiles: Object.entries(FIXED_CATEGORY_LABELS).map(([label, keywords]) => ({
    label,
    count: companies.filter((company) => keywords.some((keyword) => normalizeValue(company.Category).toLowerCase().includes(keyword))).length,
  })),
});


export const ANALYTICS_FILTER_MAP = {
  category_distribution: "category",
  hiring_velocity_distribution: "hiring_velocity",
  profitability_mix: "profitability_status",
  work_mode_distribution: "remote_policy_details",
};