from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime

def save_to_supabase(record: dict) -> bool:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[MOCK SUPABASE] Keys not found. Pretending to save record to DB.")
        return True
        
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 1. MAP RESEARCH FIELDS TO SQL COLUMN NAMES
        # Based on the provided public.company schema
        mapping = {
            "Company Name": "name",
            "Short Name": "short_name",
            "Logo": "logo_url",
            "Category": "category",
            "Year of Incorporation": "incorporation_year",
            "Overview of the Company": "overview_text",
            "Nature of Company": "nature_of_company",
            "Company Headquarters": "headquarters_address",
            "Countries Operating In": "operating_countries",
            "Number of Offices (beyond HQ)": "office_count",
            "Office Locations": "office_locations",
            "Employee Size": "employee_size",
            "Vision": "vision_statement",
            "Mission": "mission_statement",
            "Values": "core_values",
            "Interesting Facts": "interesting_facts",
            "Recent News": "recent_news",
            "Website URL": "website_url",
            "LinkedIn Profile URL": "linkedin_url",
            "Twitter (X) Handle": "twitter_handle",
            "Facebook Page URL": "facebook_url",
            "Instagram Page URL": "instagram_url",
            "Company Contact Email": "primary_contact_email",
            "Company Phone Number": "primary_phone_number",
            "Regulatory & Compliance Status": "regulatory_compliance_status",
            "Legal Issues / Controversies": "legal_issues_controversies",
            "ESG Practices or Ratings": "esg_ratings",
            "Supply Chain Dependencies": "supply_chain_dependencies",
            "Geopolitical Risks": "geopolitical_risks",
            "Macro Risks": "macro_risks",
            "Carbon Footprint/Environmental Impact": "carbon_footprint",
            "Ethical Sourcing Practices": "ethical_sourcing",
            "Company Introduction / Marketing videos": "marketing_videos",
            "Customer testimonial": "customer_testimonials",
            "Quality of Website": "website_quality",
            "Website Rating": "website_rating",
            "Website Traffic Rank": "website_traffic_rank",
            "Social Media Followers – Combined": "social_followers_combined",
            "Glassdoor Rating": "glassdoor_rating",
            "Indeed Rating": "indeed_rating",
            "Google Reviews Rating": "google_reviews_rating",
            "Awards & Recognitions": "awards_recognitions",
            "Brand Sentiment Score": "brand_sentiment_score",
            "Event Participation": "event_participation",
            "Pain Points Being Addressed": "pain_points_addressed",
            "Focus Sectors / Industries": "focus_sectors",
            "Services / Offerings / Products": "services_products",
            "Top Customers by Client Segments": "top_customers",
            "Core Value Proposition": "core_value_proposition",
            "Unique Differentiators": "unique_differentiators",
            "Competitive Advantages": "competitive_advantages",
            "Weaknesses / Gaps in Offering": "weaknesses_gaps",
            "Key Challenges and Unmet Needs": "key_challenges_needs",
            "Key Competitors": "key_competitors",
            "Market Share (%)": "market_share_percent",
            "Sales Motion": "sales_motion",
            "Customer Concentration Risk": "customer_concentration_risk",
            "Exit Strategy/History": "exit_strategy",
            "Benchmark vs. Peers": "benchmark_vs_peers",
            "Future Projections": "future_projections",
            "Strategic Priorities": "strategic_priorities",
            "Industry Associations / Memberships": "industry_associations",
            "Case Studies / Public Success Stories": "case_studies",
            "Go-to-Market Strategy": "gtm_strategy",
            "Innovation Roadmap": "innovation_roadmap",
            "Product Pipeline": "product_pipeline",
            "Total Addressable Market (TAM)": "tam",
            "Serviceable Addressable Market (SAM)": "sam",
            "Serviceable Obtainable Market (SOM)": "som",
            "Leave policy": "leave_policy",
            "Health support": "health_support",
            "Fixed vs variable pay": "fixed_vs_variable_pay",
            "Bonus predictability": "bonus_predictability",
            "ESOPs and long-term incentives": "esops_incentives",
            "Family health insurance": "family_health_insurance",
            "Relocation support": "relocation_support",
            "Lifestyle and wellness benefits": "lifestyle_wellness_benefits",
            "Hiring Velocity": "hiring_velocity",
            "Employee Turnover": "employee_turnover",
            "Average Retention Tenure": "average_retention_tenure",
            "Diversity Metrics": "diversity_metrics",
            "Work culture": "work_culture",
            "Manager quality": "manager_quality",
            "Psychological safety": "psychological_safety",
            "Feedback culture": "feedback_culture",
            "Diversity & inclusion": "diversity_inclusion",
            "Ethical standards": "ethical_standards",
            "Burnout risk": "burnout_risk",
            "Layoff history": "layoff_history",
            "Mission clarity": "mission_clarity",
            "Sustainability and CSR": "sustainability_csr",
            "Crisis behavior": "crisis_behavior",
            "Annual Revenues": "annual_revenues",
            "Annual Profits": "annual_profits",
            "Revenue Mix": "revenue_mix",
            "Company Valuation": "company_valuation",
            "Year-over-Year Growth Rate": "yoy_growth_rate",
            "Profitability Status": "profitability_status",
            "Key Investors / Backers": "key_investors",
            "Recent Funding Rounds": "recent_funding_rounds",
            "Total Capital Raised": "total_capital_raised",
            "Customer Acquisition Cost (CAC)": "cac",
            "Customer Lifetime Value (CLV)": "clv",
            "CAC:LTV Ratio": "cac_clv_ratio",
            "Churn Rate": "churn_rate",
            "Net Promoter Score (NPS)": "nps",
            "Burn Rate": "burn_rate",
            "Runway": "runway",
            "Burn Multiplier": "burn_multiplier",
            "Remote Work Policy": "remote_work_policy",
            "Typical working hours": "typical_working_hours",
            "Overtime expectations": "overtime_expectations",
            "Weekend work": "weekend_work",
            "Remote / hybrid / on-site flexibility": "flexibility_mode",
            "Central vs peripheral location": "location_centrality",
            "Public transport access": "public_transport_access",
            "Cab availability and company cab policy": "cab_policy",
            "Commute time from airport": "airport_commute_time",
            "Office zone type": "office_zone_type",
            "Area safety": "area_safety",
            "Company safety policies": "company_safety_policies",
            "Office infrastructure safety": "office_infrastructure_safety",
            "Emergency response preparedness": "emergency_preparedness",
            "CEO Name": "ceo_name",
            "CEO LinkedIn URL": "ceo_linkedin_url",
            "Key Business Leaders": "key_business_leaders",
            "Warm Introduction Pathways": "warm_intro_pathways",
            "Decision Maker Accessibility": "decision_maker_accessibility",
            "Primary Contact Person's Name": "primary_contact_name",
            "Primary Contact Person's Title": "primary_contact_title",
            "Primary Contact Person's Email": "contact_person_email",
            "Primary Contact Person's Phone Number": "contact_person_phone",
            "Board of Directors / Advisors": "board_of_directors",
            "Training/Development Spend": "training_dev_spend",
            "Onboarding and training quality": "onboarding_quality",
            "Learning culture": "learning_culture",
            "Exposure quality": "exposure_quality",
            "Mentorship availability": "mentorship_availability",
            "Internal mobility": "internal_mobility",
            "Promotion clarity": "promotion_clarity",
            "Tools and technology access": "tools_tech_access",
            "Role clarity": "role_clarity",
            "Early ownership": "early_ownership",
            "Work impact": "work_impact",
            "Execution vs thinking balance": "execution_vs_thinking",
            "Automation level": "automation_level",
            "Cross-functional exposure": "cross_functional_exposure",
            "Company maturity": "company_maturity",
            "Brand value": "brand_value",
            "Client quality": "client_quality",
            "Exit opportunities": "exit_opportunities",
            "Skill relevance": "skill_relevance",
            "External recognition": "external_recognition",
            "Network strength": "network_strength",
            "Global exposure": "global_exposure",
            "Technology Partners": "technology_partners",
            "Intellectual Property": "intellectual_property",
            "R&D Investment": "r_d_investment",
            "AI/ML Adoption Level": "ai_ml_adoption_level",
            "Tech Stack/Tools Used": "tech_stack_tools",
            "Cybersecurity Posture": "cybersecurity_posture",
            "Partnership Ecosystem": "partnership_ecosystem",
            "Industry Benchmark Technology Adoption Rating": "industry_benchmark_tech_rating"
        }

        # Create the SQL-ready record
        db_record = {}
        for research_key, sql_key in mapping.items():
            if research_key in record:
                # Ensure we only send strings for text columns
                val = record[research_key]
                db_record[sql_key] = str(val) if val is not None else None
        
        # 2. GENERATE DETERMINISTIC COMPANY_ID
        # Since the database requires a non-null company_id, we generate one from the name
        import hashlib
        company_name_str = record.get("Company Name", "Unknown")
        # Create a stable integer ID from the name string
        db_record["company_id"] = int(hashlib.md5(company_name_str.encode()).hexdigest(), 16) % 10**8
        
        if len(db_record) <= 1: # Only has company_id
            print("   ⚠️ No fields matched the database schema. Skipping DB save.")
            return True

        # 3. ATTEMPT UPSERT INTO 'company' TABLE
        try:
            supabase.table("company").upsert(db_record).execute()
            print(f"✅ Successfully saved/updated golden record (ID: {db_record['company_id']}) in public.company!")
        except Exception as e:
            print(f"❌ Supabase Insertion Error: {e}")
            
            # Fallback to JSONB if you have a table for that
            # supabase.table("research_logs").insert({"company": record.get("Company Name"), "data": record}).execute()

        return True
    except Exception as e:
        print(f"❌ Supabase Final Error: {e}")
        return False
