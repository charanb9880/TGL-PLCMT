import { extractDomain } from "./formatters";

/**
 * Mappings between Excel-style column names (used in placement frames)
 * and snake_case database columns (used in NEW_UI schema).
 */
export const LOGO_FALLBACKS = {
  zoom: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Zoom_Communications_Logo.svg/1024px-Zoom_Communications_Logo.svg.png",
  wikimedia: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Wikimedia_Foundation_logo_-_2021.svg/1024px-Wikimedia_Foundation_logo_-_2021.svg.png",
  snap: "https://logo.clearbit.com/snapchat.com",
  discord: "https://logo.clearbit.com/discord.com",
  twitter: "https://logo.clearbit.com/twitter.com",
  x: "https://logo.clearbit.com/x.com",
  scale: "https://logo.clearbit.com/scale.com",
  datadog: "https://logo.clearbit.com/datadoghq.com",
  canva: "https://logo.clearbit.com/canva.com",
  plaid: "https://logo.clearbit.com/plaid.com",
  brex: "https://logo.clearbit.com/brex.com",
  rippling: "https://logo.clearbit.com/rippling.com",
  snowflake: "https://logo.clearbit.com/snowflake.com",
  airwallex: "https://logo.clearbit.com/airwallex.com",
  snowplow: "https://logo.clearbit.com/snowplow.io",
  wise: "https://logo.clearbit.com/wise.com",
  reddit: "https://logo.clearbit.com/reddit.com",
  block: "https://pbs.twimg.com/profile_images/1466046702636531713/GqO2X-0__400x400.jpg",
  square: "https://logo.clearbit.com/square.com",
};


export const MAPPING = {
  // Overview
  "Company Name": "name",
  "Short Name": "short_name",
  "Logo": "logo_url",
  "Logo URL": "logo_url",
  "Category": "category",
  "Year of Incorporation": "incorporation_year",
  "Nature of Company": "nature_of_company",
  "Company Headquarters": "headquarters_address",
  "Countries Operating In": "operating_countries",
  "Number of Offices (beyond HQ)": "office_count",
  "Office Locations": "office_locations",
  "Employee Size": "employee_size",
  "Overview of the Company": "overview_text",
  "Vision": "vision_statement",
  "Mission": "mission_statement",
  "Values": "core_values",
  "Interesting Facts": "unique_differentiators", // Mapping to unique_differentiators as a proxy
  "Recent News": "recent_news",

  // Business & Market
  "Pain Points Being Addressed": "pain_points_addressed",
  "Focus Sectors / Industries": "focus_sectors",
  "Services / Offerings / Products": "offerings_description",
  "Top Customers by Client Segments": "top_customers",
  "Core Value Proposition": "core_value_proposition",
  "Unique Differentiators": "unique_differentiators",
  "Competitive Advantages": "competitive_advantages",
  "Weaknesses / Gaps in Offering": "weaknesses_gaps",
  "Key Challenges and Unmet Needs": "key_challenges_needs",
  "Key Competitors": "key_competitors",
  "Market Share (%)": "market_share_percentage",
  "Sales Motion": "sales_motion",
  "Customer Concentration Risk": "customer_concentration_risk",
  "Exit Strategy/History": "exit_strategy_history",
  "Benchmark vs. Peers": "benchmark_vs_peers",
  "Future Projections": "future_projections",
  "Strategic Priorities": "strategic_priorities",
  "Industry Associations / Memberships": "industry_associations",
  "Case Studies / Public Success Stories": "case_studies",
  "Go-to-Market Strategy": "go_to_market_strategy",
  "Innovation Roadmap": "innovation_roadmap",
  "Product Pipeline": "product_pipeline",
  "Total Addressable Market (TAM)": "tam",
  "Serviceable Addressable Market (SAM)": "sam",
  "Serviceable Obtainable Market (SOM)": "som",

  // Culture & People
  "Hiring Velocity": "hiring_velocity",
  "Employee Turnover": "employee_turnover",
  "Average Retention Tenure": "avg_retention_tenure",
  "Diversity Metrics": "diversity_metrics",
  "Work culture": "work_culture_summary",
  "Manager quality": "manager_quality",
  "Psychological safety": "psychological_safety",
  "Feedback culture": "feedback_culture",
  "Diversity & inclusion": "diversity_inclusion_score",
  "Ethical standards": "ethical_standards",
  "Burnout risk": "burnout_risk",
  "Layoff history": "layoff_history",
  "Mission clarity": "mission_clarity",
  "Sustainability and CSR": "sustainability_csr",
  "Crisis behavior": "crisis_behavior",

  // Learning & Growth
  "Training/Development Spend": "training_spend",
  "Onboarding and training quality": "onboarding_quality",
  "Learning culture": "learning_culture",
  "Exposure quality": "exposure_quality",
  "Mentorship availability": "mentorship_availability",
  "Internal mobility": "internal_mobility",
  "Promotion clarity": "promotion_clarity",
  "Tools and technology access": "tools_access",
  "Role clarity": "role_clarity",
  "Early ownership": "early_ownership",
  "Work impact": "work_impact",
  "Execution vs thinking balance": "execution_thinking_balance",
  "Cross-functional exposure": "cross_functional_exposure",
  "Company maturity": "company_maturity",
  "Exit opportunities": "exit_opportunities",
  "Skill relevance": "skill_relevance",
  "External recognition": "external_recognition",
  "Network strength": "network_strength",
  "Global exposure": "global_exposure",

  // Compensation
  "Leave policy": "leave_policy",
  "Health support": "health_support",
  "Fixed vs variable pay": "fixed_vs_variable_pay",
  "Bonus predictability": "bonus_predictability",
  "ESOPs and long-term incentives": "esops_incentives",
  "Family health insurance": "family_health_insurance",
  "Relocation support": "relocation_support",
  "Lifestyle and wellness benefits": "lifestyle_benefits",

  // Work Logistics
  "Remote Work Policy": "remote_policy_details",
  "Typical working hours": "typical_hours",
  "Overtime expectations": "overtime_expectations",
  "Weekend work": "weekend_work",
  "Remote / hybrid / on-site flexibility": "flexibility_level",
  "Central vs peripheral location": "location_centrality",
  "Public transport access": "public_transport_access",
  "Cab availability and company cab policy": "cab_policy",
  "Commute time from airport": "airport_commute_time",
  "Office zone type": "office_zone_type",
  "Area safety": "area_safety",
  "Company safety policies": "safety_policies",
  "Office infrastructure safety": "infrastructure_safety",
  "Emergency response preparedness": "emergency_preparedness",

  // Financials
  "Annual Revenues": "annual_revenue",
  "Annual Profits": "annual_profit",
  "Revenue Mix": "revenue_mix",
  "Company Valuation": "valuation",
  "Year-over-Year Growth Rate": "yoy_growth_rate",
  "Profitability Status": "profitability_status",
  "Key Investors / Backers": "key_investors",
  "Recent Funding Rounds": "recent_funding_rounds",
  "Total Capital Raised": "total_capital_raised",
  "Customer Acquisition Cost (CAC)": "customer_acquisition_cost",
  "Customer Lifetime Value (CLV)": "customer_lifetime_value",
  "CAC:LTV Ratio": "cac_ltv_ratio",
  "Churn Rate": "churn_rate",
  "Net Promoter Score (NPS)": "net_promoter_score",
  "Burn Rate": "burn_rate",
  "Runway": "runway_months",
  "Burn Multiplier": "burn_multiplier",

  // Technology
  "Technology Partners": "technology_partners",
  "Intellectual Property": "intellectual_property",
  "R&D Investment": "r_and_d_investment",
  "AI/ML Adoption Level": "ai_ml_adoption_level",
  "Tech Stack/Tools Used": "tech_stack",
  "Cybersecurity Posture": "cybersecurity_posture",
  "Partnership Ecosystem": "partnership_ecosystem",
  "Industry Benchmark Technology Adoption Rating": "tech_adoption_rating",
  "Automation level": "automation_level",

  // Leadership
  "CEO Name": "ceo_name",
  "CEO LinkedIn URL": "ceo_linkedin_url",
  "Key Business Leaders": "key_leaders",
  "Warm Introduction Pathways": "warm_intro_pathways",
  "Decision Maker Accessibility": "decision_maker_access",
  "Primary Contact Person's Name": "contact_person_name",
  "Primary Contact Person's Title": "contact_person_title",
  "Primary Contact Person's Email": "contact_person_email",
  "Primary Contact Person's Phone Number": "contact_person_phone",
  "Board of Directors / Advisors": "board_members",

  // Brand & Digital
  "Website URL": "website_url",
  "LinkedIn Profile URL": "linkedin_url",
  "Twitter (X) Handle": "twitter_handle",
  "Facebook Page URL": "facebook_url",
  "Instagram Page URL": "instagram_url",
  "Company Contact Email": "primary_contact_email",
  "Company Phone Number": "primary_phone_number",
  "Regulatory & Compliance Status": "regulatory_status",
  "Legal Issues / Controversies": "legal_issues",
  "ESG Practices or Ratings": "esg_ratings",
  "Supply Chain Dependencies": "supply_chain_dependencies",
  "Geopolitical Risks": "geopolitical_risks",
  "Macro Risks": "macro_risks",
  "Carbon Footprint/Environmental Impact": "carbon_footprint",
  "Ethical Sourcing Practices": "ethical_sourcing",
  "Company Introduction / Marketing videos": "marketing_video_url",
  "Customer testimonial": "customer_testimonials",
  "Quality of Website": "website_quality",
  "Website Rating": "website_rating",
  "Website Traffic Rank": "website_traffic_rank",
  "Social Media Followers – Combined": "social_media_followers",
  "Glassdoor Rating": "glassdoor_rating",
  "Indeed Rating": "indeed_rating",
  "Google Reviews Rating": "google_rating",
  "Awards & Recognitions": "awards_recognitions",
  "Brand Sentiment Score": "brand_sentiment_score",
  "Brand value": "brand_value",
  "Client quality": "client_quality",

  // Virtual fields for Hiring Intelligence (mapped to JSON columns)
  "Job Roles (InnovX Master)": "innovx_json",
  "Hiring Rounds": "innovx_json",
  "Typical Assessment Questions": "innovx_json",
  "Compensation & Benefits": "innovx_json",
  "Skill Fit Predictors": "innovx_json",
};


/**
 * Gets the actual value for a field from the company object,
 * checking both the raw key and the snake_case mapping.
 */
export function getFieldValue(company, field) {
  if (!company) return null;

  // Handle special case for InnovX JSON fields
  if (field === "Job Roles (InnovX Master)" || field === "Hiring Rounds" || field === "Typical Assessment Questions" || field === "Compensation & Benefits" || field === "Skill Fit Predictors") {
    const rawJson = company.innovx_json || company.job_role_details || company.company_details?.job_role_details;
    if (!rawJson) return null;

    // Return the JSON object; the renderer should handle formatting
    return rawJson;
  }

  const mappedKey = MAPPING[field];
  const value = company[field] ?? (mappedKey ? company[mappedKey] : null);

  // Apply fallback logos for specific companies
  if (field === "Logo") {
    const companyName = String(company["Company Name"] || company["name"] || "").toLowerCase();
    
    // 1. Check manual fallbacks first (highly reliable)
    const fallbackKey = Object.keys(LOGO_FALLBACKS).find((key) => companyName.includes(key));
    if (fallbackKey) {
      return LOGO_FALLBACKS[fallbackKey];
    }

    // 2. If data has a value, use it (but we've already checked manual fallbacks)
    if (value && String(value).length > 5) {
      return value;
    }

    // 3. Generate from domain if available
    const website = company["Website URL"] || company["website_url"] || company["Website"];
    const domain = extractDomain(website);
    
    if (domain) {
      return `https://logo.clearbit.com/${domain}`;
    }

    // 4. Guess from name as fallback URL for icon services
    if (companyName) {
      const cleanName = String(companyName || "").replace(/(corp|inc|ltd|plc|limited|co)\.?$/i, "").trim().split(/[,\s]/)[0].replace(/[^a-z0-9]/g, "").toLowerCase();
      if (cleanName.length > 1) {
        return `https://logo.clearbit.com/${cleanName}.com`;
      }
    }
  }

  return value;
}
