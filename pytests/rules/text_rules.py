from validators.common import is_null_like

def validate_missing_values(record):
    errors = []
    warnings = []
    
    # 14.1 Missing values: CEO must exist for Public companies
    nature = record.get("Nature of Company")
    ceo = record.get("CEO Name")
    revenue = record.get("Annual Revenues")
    valuation = record.get("Company Valuation")
    
    if nature == "Public" and is_null_like(ceo):
        errors.append("CEO Name is missing for a Public company")
        
    # Implied data dependencies (Section 14.1)
    if not is_null_like(record.get("Market Share (%)")) and is_null_like(revenue):
        errors.append("Market share implies Annual Revenues should exist")
        
    if not is_null_like(valuation) and is_null_like(revenue):
        errors.append("Annual Revenues expected when Company Valuation exists")
        
    if not is_null_like(valuation) and is_null_like(record.get("Recent Funding Rounds")):
        errors.append("Funding rounds expected when Company Valuation exists")

    if not is_null_like(record.get("Total Capital Raised")) and is_null_like(record.get("Key Investors / Backers")):
        errors.append("Key Investors expected when Total Capital Raised exists")
        
    if not is_null_like(record.get("Customer Lifetime Value (CLV)")) and is_null_like(record.get("Customer Acquisition Cost (CAC)")):
        errors.append("CAC required if CLV exists")

    # TC_014_005 & TC_014_015: Social Media vs Sentiment
    if not is_null_like(record.get("Social Media Followers – Combined")) and is_null_like(record.get("Brand Sentiment Score")):
        errors.append("Brand Sentiment Score should be derivable when Social Media Followers are present")

    # TC_014_014: Employee Turnover vs Average Retention Tenure
    if not is_null_like(record.get("Employee Turnover")) and is_null_like(record.get("Average Retention Tenure")):
        errors.append("Average Retention Tenure is required when Employee Turnover is present")

    # TC_014_007: CEO must exist even after resignation event
    recent_news = str(record.get("Recent News", "")).lower()
    if "ceo resigned" in recent_news and is_null_like(ceo):
        errors.append("CEO Name must still exist/be updated even if news mentions a resignation")
        
    return errors, warnings

def validate_not_applicable(record):
    errors = []
    warnings = []
    
    # 14.2 Not Applicable: VC should not have products
    if record.get("Category") == "VC" and not is_null_like(record.get("Services / Offerings / Products")):
        errors.append("Products should not exist for a VC entity")
        
    return errors, warnings

import re
def validate_ambiguity(record):
    errors = []
    warnings = []
    
    # 14.3 Ambiguity: Flag "TBD", "TBC", "Pending", "To be updated"
    # Use regex to avoid matching inside other words, or known acceptable phrases like "TBD (Open Source Bitcoin)"
    ambiguous_pattern = re.compile(r'\b(TBD|TBC|PENDING|UNKNOWN|DATA NOT FOUND)\b', re.IGNORECASE)
    acceptable_phrases = ["tbd (open source bitcoin)", "pending 2026", "decentralized id (tbd)"]
    
    for field, value in record.items():
        if isinstance(value, str):
            if any(p in value.lower() for p in acceptable_phrases): continue
            if ambiguous_pattern.search(value):
                warnings.append(f"Ambiguous data in '{field}': {value}")
            
    return errors, warnings

def validate_defaults(record):
    errors = []
    warnings = []
    
    # 14.4 Default Value Handling: Reject $0/0 for critical fields
    critical_numeric_fields = ["Annual Revenues", "Employee Size", "Company Valuation"]
    for field in critical_numeric_fields:
        val = record.get(field)
        if val in [0, "0", "$0", "None"]:
            errors.append(f"Inappropriate default value '{val}' for critical field '{field}'")
            
    return errors, warnings

def validate_null_propagation(record):
    errors = []
    warnings = []
    
    # 14.5 Null Propagation: If Parent is Null, Child must be Null
    if record.get("Annual Revenues") is None and record.get("YoY Growth") is not None:
        errors.append("YoY Growth exists while Annual Revenues is Null (Propagation Error)")
        
    return errors, warnings


# ==========================================
# CATEGORY 1: INPUT VALIDATION
# ==========================================
def validate_input_standard(record):
    errors, warnings = [], []
    # 1.1 Valid Standard Input
    company_name = record.get("Company Name", "")
    if is_null_like(company_name):
        errors.append("Company Name cannot be empty or null")
    return errors, warnings

def validate_input_empty(record):
    errors, warnings = [], []
    # 1.2 Invalid/Empty Input
    company_name = record.get("Company Name", "")
    if not str(company_name).strip():
        errors.append("Company Name cannot be whitespace only")
    return errors, warnings

# ==========================================
# CATEGORY 2: DATA COMPLETENESS
# ==========================================
def validate_mandatory_fields(record):
    errors, warnings = [], []
    # 2.4 Mandatory Fields Only
    mandatory_fields = ["Company Name", "Category"]
    for field in mandatory_fields:
        if is_null_like(record.get(field)):
            errors.append(f"Mandatory field {field} is missing")
    return errors, warnings

def validate_field_dependency(record):
    errors, warnings = [], []
    # 2.5 Field Dependency
    ceo = record.get("CEO Name")
    ceo_linkedin = record.get("CEO LinkedIn Profile")
    if not is_null_like(ceo) and is_null_like(ceo_linkedin) and "CEO LinkedIn Profile" in record:
        warnings.append("CEO exists but CEO LinkedIn is missing")
        
    funding = record.get("Total Capital Raised")
    investors = record.get("Key Investors / Backers")
    if not is_null_like(funding) and is_null_like(investors):
        warnings.append("Funding exists but investors are missing")
    return errors, warnings

# ==========================================
# CATEGORY 4: HALLUCINATION DETECTION
# ==========================================
def validate_plausible_but_false(record):
    errors, warnings = [], []
    # 4.2 Plausible but False
    funding_amt = record.get("Total Capital Raised")
    if isinstance(funding_amt, (int, float)) and funding_amt > 1e12:
        warnings.append("Suspiciously high funding amount, potential hallucination")
    return errors, warnings

# ==========================================
# CATEGORY 8: FORMAT & STRUCTURE
# ==========================================
def validate_url_validity(record):
    errors, warnings = [], []
    # 8.2 URL Validity
    website = str(record.get("Website", ""))
    if website and not is_null_like(website) and not website.startswith("http"):
        warnings.append("Website URL should start with http or https")
    return errors, warnings

def validate_text_length(record):
    errors, warnings = [], []
    # 8.6 Text Length Validation
    short_name = str(record.get("Short Name", ""))
    if not is_null_like(short_name) and len(short_name) > 100:
        warnings.append("Short name is suspiciously long (>100 chars)")
    return errors, warnings

# ==========================================
# CATEGORY 9: ADVERSARIAL TESTS
# ==========================================
def validate_context_confusion(record):
    errors, warnings = [], []
    # 9.3 Context Confusion (Placeholder)
    return errors, warnings

# ==========================================
# CATEGORY 11: AMBIGUITY RESOLUTION
# ==========================================
import re
def validate_multiple_entities(record):
    errors, warnings = [], []
    # 11.1 Multiple Entities Same Name
    desc = str(record.get("Company Description", ""))
    if re.search(r'\b(did you mean|multiple entities)\b', desc, re.IGNORECASE):
        warnings.append("Ambiguity detected in output description")
    return errors, warnings

# ==========================================
# CATEGORY 12: CLASSIFICATION & CATEGORIZATION
# ==========================================
def validate_company_category(record):
    errors, warnings = [], []
    # 12.1 Company Category
    category = str(record.get("Category", "")).lower()
    valid_categories = ["startup", "msme", "smb", "investor", "vc", "enterprise", "public", "private", "nonprofit", "charitable", "technology company"]
    if category and not is_null_like(category) and not any(v in category for v in valid_categories):
        warnings.append(f"Unusual category detected: {category}")
    return errors, warnings

# ==========================================
# CATEGORY 13: SCALE & PERFORMANCE
# ==========================================
def validate_response_time(record):
    errors, warnings = [], []
    # 13.2 Response Time
    return errors, warnings
