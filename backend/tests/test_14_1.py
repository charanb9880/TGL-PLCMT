import pytest

# Utility functions for test logic
def is_null_like(val):
    return val in [None, "N/A", "Unknown", "", "n/a"]

def is_large_company(size):
    if is_null_like(size): return False
    try:
        # Handle cases like "5000+", "~6000", "10,000"
        clean_size = str(size).replace(",", "").replace("+", "").split("-")[0].strip()
        matches = [int(s) for s in clean_size.split() if s.isdigit()]
        if matches: return matches[0] > 1000
        # Simple fallback for strings like "5000"
        num = int(''.join(filter(str.isdigit, clean_size)))
        return num > 1000
    except:
        return False

def has_social_presence(followers):
    if is_null_like(followers) or followers == 0: return False
    return True

# --- Test Cases based on TC_014 ---

# VC Product Logic (TC_014_001, TC_014_002)
def test_vc_no_products():
    # PASS case
    data_pass = { "Category": "VC", "Services / Offerings / Products": "N/A" }
    assert is_null_like(data_pass["Services / Offerings / Products"])
    
    # FAIL case
    data_fail = { "Category": "VC", "Services / Offerings / Products": "SaaS Platform" }
    # Products should not exist for VC
    assert not (data_fail["Category"] == "VC" and not is_null_like(data_fail["Services / Offerings / Products"]))

# Bootstrapped Investor Logic (TC_014_003, TC_014_004)
def test_bootstrapped_investors():
    # PASS case
    data_pass = { "Funding Status": "Bootstrapped", "Key Investors / Backers": "N/A" }
    assert is_null_like(data_pass["Key Investors / Backers"])
    
    # FAIL case
    data_fail = { "Funding Status": "Bootstrapped", "Key Investors / Backers": "Sequoia" }
    # Conflict: bootstrapped should not have investors
    assert not (data_fail["Funding Status"] == "Bootstrapped" and not is_null_like(data_fail["Key Investors / Backers"]))

# Remote Office Logic (TC_014_005, TC_014_006)
def test_remote_offices():
    # PASS case
    data_pass = { "Remote Work Policy": "Remote", "Office Locations": "N/A" }
    assert is_null_like(data_pass["Office Locations"])
    
    # FAIL case
    data_fail = { "Remote Work Policy": "Remote", "Office Locations": "New York, USA" }
    # Contradiction: remote-only shouldn't have locations
    assert not (data_fail["Remote Work Policy"] == "Remote" and not is_null_like(data_fail["Office Locations"]))

# Non-profit Profit Logic (TC_014_007, TC_014_008)
def test_nonprofit_profits():
    # PASS case
    data_pass = { "Nature of Company": "Non-Profit", "Annual Profits": "N/A" }
    assert is_null_like(data_pass["Annual Profits"])
    
    # FAIL case
    data_fail = { "Nature of Company": "Non-Profit", "Annual Profits": "$5M" }
    assert not (data_fail["Nature of Company"] == "Non-Profit" and not is_null_like(data_fail["Annual Profits"]))

# Mature Company Metrics (TC_014_009, TC_014_010)
def test_mature_metrics():
    # Mature company (5000 employees) incorrectly marking CAC as N/A
    data_fail = { "Employee Size": "5000", "Customer Acquisition Cost (CAC)": "N/A" }
    # FAIL: CAC expected for mature company
    assert not (is_large_company(data_fail["Employee Size"]) and is_null_like(data_fail["Customer Acquisition Cost (CAC)"]))

# Social Sentiment Logic (TC_014_011, TC_014_12)
def test_sentiment_social_dependency():
    # FAIL: High social presence but sentiment marked N/A
    data_fail = { "Social Media Followers – Combined": "1M", "Brand Sentiment Score": "N/A" }
    assert not (has_social_presence(data_fail["Social Media Followers – Combined"]) and is_null_like(data_fail["Brand Sentiment Score"]))

# Government Entity Logic (TC_014_013, TC_014_014)
def test_govt_investors():
    data_fail = { "Nature of Company": "Govt", "Key Investors / Backers": "VC Fund" }
    assert not (data_fail["Nature of Company"] == "Govt" and not is_null_like(data_fail["Key Investors / Backers"]))

# Industry Supply Chain Logic (TC_014_015, TC_014_016, TC_014_017)
def test_industry_supply_chain():
    # Manufacturing missing supply chain
    data_fail = { "Industry": "Manufacturing", "Supply Chain Dependencies": "N/A" }
    assert not (data_fail["Industry"] == "Manufacturing" and is_null_like(data_fail["Supply Chain Dependencies"]))

# Product Role Requirement (TC_014_018)
def test_product_company_requirement():
    # Product company missing product details
    data_fail = { "Category": "Enterprise", "Services / Offerings / Products": "N/A" }
    assert not (data_fail["Category"] == "Enterprise" and is_null_like(data_fail["Services / Offerings / Products"]))

# Diversity for Large Org (TC_014_019, TC_014_020)
def test_large_org_diversity():
    # Large company (10000) marking diversity as N/A
    data_fail = { "Employee Size": "10000", "Diversity Metrics": "N/A" }
    assert not (is_large_company(data_fail["Employee Size"]) and is_null_like(data_fail["Diversity Metrics"]))
