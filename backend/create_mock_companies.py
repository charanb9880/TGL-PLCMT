import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(".env")
engine = create_engine(os.environ["DATABASE_URL"])

companies_data = [
    {
        "name": "Datadog, Inc.",
        "short_name": "Datadog",
        "category": "Cloud Monitoring & Analytics",
        "overview_text": "Datadog is an observability service for cloud-scale applications, providing monitoring of servers, databases, tools, and services, through a SaaS-based data analytics platform.",
        "headquarters_address": "New York, NY",
        "employee_size": "1,000-5,000",
        "website_url": "https://www.datadoghq.com",
        "logo_url": "https://logo.clearbit.com/datadoghq.com",
        "brand_value": "Very High",
        "profitability_status": "Profitable",
        "hiring_velocity": "High",
        "remote_policy_details": "Hybrid / Remote-friendly",
        "nature_of_company": "Public SaaS",
        "incorporation_year": "2010"
    },
    {
        "name": "Scale AI, Inc.",
        "short_name": "Scale AI",
        "category": "Artificial Intelligence / Data Infrastructure",
        "overview_text": "Scale AI provides the data infrastructure for AI, providing high-quality training data for leading machine learning teams.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "500-1,000",
        "website_url": "https://scale.com",
        "logo_url": "https://logo.clearbit.com/scale.com",
        "brand_value": "Very High",
        "profitability_status": "Growth-stage / Pre-IPO",
        "hiring_velocity": "Very High",
        "remote_policy_details": "In-office heavily encouraged",
        "nature_of_company": "Private Tech",
        "incorporation_year": "2016"
    },
    {
        "name": "Canva Pty Ltd",
        "short_name": "Canva",
        "category": "Design Software",
        "overview_text": "Canva is a free-to-use online graphic design tool. Use it to create social media posts, presentations, posters, videos, logos and more.",
        "headquarters_address": "Sydney, Australia",
        "employee_size": "1,000-5,000",
        "website_url": "https://www.canva.com",
        "logo_url": "https://logo.clearbit.com/canva.com",
        "brand_value": "Exceptional",
        "profitability_status": "Profitable",
        "hiring_velocity": "High",
        "remote_policy_details": "Remote-first",
        "nature_of_company": "Private Tech",
        "incorporation_year": "2012"
    },
    {
        "name": "Plaid Inc.",
        "short_name": "Plaid",
        "category": "Financial Technology",
        "overview_text": "Plaid is a financial technology company that builds a data transfer network that powers Fintech and digital finance products.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "500-1,000",
        "website_url": "https://plaid.com",
        "logo_url": "https://logo.clearbit.com/plaid.com",
        "brand_value": "High",
        "profitability_status": "Growth-stage / Pre-IPO",
        "hiring_velocity": "Moderate",
        "remote_policy_details": "Hybrid",
        "nature_of_company": "Private Fintech",
        "incorporation_year": "2013"
    },
    {
        "name": "Brex Inc.",
        "short_name": "Brex",
        "category": "Financial Technology",
        "overview_text": "Brex is a financial service and technology company that offers business credit cards and cash management accounts to technology companies.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "1,000-5,000",
        "website_url": "https://www.brex.com",
        "logo_url": "https://logo.clearbit.com/brex.com",
        "brand_value": "High",
        "profitability_status": "Growth-stage / Pre-IPO",
        "hiring_velocity": "Moderate",
        "remote_policy_details": "Remote-first",
        "nature_of_company": "Private Fintech",
        "incorporation_year": "2017"
    },
    {
        "name": "Snowflake Inc.",
        "short_name": "Snowflake",
        "category": "Cloud Computing / Data Warehousing",
        "overview_text": "Snowflake offers a cloud-based data storage and analytics service, generally termed data-as-a-service.",
        "headquarters_address": "Bozeman, MT",
        "employee_size": "5,000+",
        "website_url": "https://www.snowflake.com",
        "logo_url": "https://logo.clearbit.com/snowflake.com",
        "brand_value": "Exceptional",
        "profitability_status": "Profitable",
        "hiring_velocity": "High",
        "remote_policy_details": "Hybrid / Flexible",
        "nature_of_company": "Public Tech",
        "incorporation_year": "2012"
    },
    {
        "name": "Rippling",
        "short_name": "Rippling",
        "category": "HR & IT Management",
        "overview_text": "Rippling makes it easy to manage your company's Payroll, Benefits, HR, and IT—all in one modern platform.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "1,000-5,000",
        "website_url": "https://www.rippling.com",
        "logo_url": "https://logo.clearbit.com/rippling.com",
        "brand_value": "High",
        "profitability_status": "Growth-stage / Pre-IPO",
        "hiring_velocity": "Very High",
        "remote_policy_details": "Hybrid",
        "nature_of_company": "Private SaaS",
        "incorporation_year": "2016"
    },
    {
        "name": "Figma, Inc.",
        "short_name": "Figma",
        "category": "Design Software",
        "overview_text": "Figma is a collaborative web application for interface design, with additional offline features enabled by desktop applications for macOS and Windows.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "500-1,000",
        "website_url": "https://www.figma.com",
        "logo_url": "https://logo.clearbit.com/figma.com",
        "brand_value": "Exceptional",
        "profitability_status": "Profitable",
        "hiring_velocity": "Moderate",
        "remote_policy_details": "Hybrid",
        "nature_of_company": "Private Tech",
        "incorporation_year": "2012"
    },
    {
        "name": "Vercel Inc.",
        "short_name": "Vercel",
        "category": "Cloud Platform",
        "overview_text": "Vercel is a platform for frontend frameworks and static sites, built to integrate with headless content, commerce, or database.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "100-500",
        "website_url": "https://vercel.com",
        "logo_url": "https://logo.clearbit.com/vercel.com",
        "brand_value": "High",
        "profitability_status": "Growth-stage",
        "hiring_velocity": "High",
        "remote_policy_details": "Remote-first",
        "nature_of_company": "Private Tech",
        "incorporation_year": "2015"
    },
    {
        "name": "Stripe, Inc.",
        "short_name": "Stripe",
        "category": "Financial Technology",
        "overview_text": "Stripe is an Irish-American financial services and software as a service company dual-headquartered in San Francisco and Dublin.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "5,000+",
        "website_url": "https://stripe.com",
        "logo_url": "https://logo.clearbit.com/stripe.com",
        "brand_value": "Exceptional",
        "profitability_status": "Profitable",
        "hiring_velocity": "High",
        "remote_policy_details": "Remote-friendly / Hybrid",
        "nature_of_company": "Private Fintech",
        "incorporation_year": "2010"
    },
    {
        "name": "Notion Labs Inc.",
        "short_name": "Notion",
        "category": "Productivity Software",
        "overview_text": "Notion is a single space where you can think, write, and plan. Capture thoughts, manage projects, or even run an entire company.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "500-1,000",
        "website_url": "https://www.notion.so",
        "logo_url": "https://logo.clearbit.com/notion.so",
        "brand_value": "Exceptional",
        "profitability_status": "Growth-stage",
        "hiring_velocity": "Moderate",
        "remote_policy_details": "Hybrid",
        "nature_of_company": "Private SaaS",
        "incorporation_year": "2016"
    },
    {
        "name": "Airtable",
        "short_name": "Airtable",
        "category": "Productivity Software",
        "overview_text": "Airtable is a cloud collaboration service. It is a spreadsheet-database hybrid, with the features of a database but applied to a spreadsheet.",
        "headquarters_address": "San Francisco, CA",
        "employee_size": "500-1,000",
        "website_url": "https://airtable.com",
        "logo_url": "https://logo.clearbit.com/airtable.com",
        "brand_value": "High",
        "profitability_status": "Growth-stage",
        "hiring_velocity": "Moderate",
        "remote_policy_details": "Hybrid",
        "nature_of_company": "Private SaaS",
        "incorporation_year": "2012"
    }
]

df = pd.DataFrame(companies_data)

# Fetch valid columns from DB to pad missing values with None
with engine.connect() as conn:
    res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"))
    valid_cols = [r[0] for r in res.fetchall()]

# Fill missing columns with None
for col in valid_cols:
    if col not in df.columns and col != "company_id":
        df[col] = None

# Reorder columns to match valid_cols (excluding company_id)
cols_to_insert = [c for c in valid_cols if c != "company_id"]
df = df[cols_to_insert]

df.to_sql("company", engine, if_exists="append", index=False)
print(f"Successfully inserted {len(df)} synthetic companies with clearbit logos!")
