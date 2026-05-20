import os
import json

base_dir = "/Users/charanb/Desktop/TGL_Customised/final_ui/pytests/rules"

text_additions = """

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
    if not is_null_like(ceo) and is_null_like(ceo_linkedin):
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
def validate_multiple_entities(record):
    errors, warnings = [], []
    # 11.1 Multiple Entities Same Name
    desc = str(record.get("Company Description", "")).lower()
    if "did you mean" in desc or "multiple entities" in desc:
        warnings.append("Ambiguity detected in output description")
    return errors, warnings

# ==========================================
# CATEGORY 12: CLASSIFICATION & CATEGORIZATION
# ==========================================
def validate_company_category(record):
    errors, warnings = [], []
    # 12.1 Company Category
    category = str(record.get("Category", "")).lower()
    valid_categories = ["startup", "msme", "smb", "investor", "vc", "enterprise", "public"]
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
"""

numeric_additions = """

# ==========================================
# CATEGORY 3: DATA ACCURACY
# ==========================================
def validate_cross_field_consistency(record):
    errors, warnings = [], []
    # 3.4 Cross-Field Consistency
    inc_year = record.get("Year of Incorporation")
    ceo_start = record.get("CEO Tenure Start")
    if not is_null_like(inc_year) and not is_null_like(ceo_start):
        try:
            if int(inc_year) > int(ceo_start):
                errors.append("Year of Incorporation cannot be after CEO tenure start")
        except ValueError:
            pass
    return errors, warnings

# ==========================================
# CATEGORY 5: INTERNAL CONSISTENCY
# ==========================================
def validate_logical_consistency(record):
    errors, warnings = [], []
    # 5.2 Logical Consistency
    profits = record.get("Profits")
    is_profitable = record.get("Profitable")
    if not is_null_like(profits) and not is_null_like(is_profitable):
        if is_profitable in [True, "Yes", "true", "Y"] and isinstance(profits, (int, float)) and profits <= 0:
            errors.append("Profitable company cannot have profits <= 0")
            
    revenue = record.get("Annual Revenues")
    nature = record.get("Nature of Company")
    if str(nature).lower() == "pre-revenue" and isinstance(revenue, (int, float)) and revenue > 0:
        errors.append("Pre-revenue company cannot have > 0 revenue")
    return errors, warnings

# ==========================================
# CATEGORY 6: EDGE CASES
# ==========================================
def validate_very_large_companies(record):
    errors, warnings = [], []
    # 6.2 Very Large Companies
    emp_size = record.get("Employee Size")
    if isinstance(emp_size, (int, float)) and emp_size > 1000000:
        warnings.append("Very large conglomerate detected, generic fields might lack nuance")
    return errors, warnings

# ==========================================
# CATEGORY 7: BOUNDARY VALUES
# ==========================================
def validate_negative_values(record):
    errors, warnings = [], []
    # 7.3 Negative Values
    emp_size = record.get("Employee Size")
    if isinstance(emp_size, (int, float)) and emp_size < 0:
        errors.append("Employee size cannot be negative")
    return errors, warnings

def validate_percentage_bounds(record):
    errors, warnings = [], []
    # 7.4 Percentage Bounds
    market_share = record.get("Market Share (%)")
    if isinstance(market_share, (int, float)) and (market_share < 0 or market_share > 100):
        errors.append("Market share must be between 0 and 100")
    return errors, warnings

# ==========================================
# CATEGORY 10: TEMPORAL VALIDITY
# ==========================================
def validate_knowledge_cutoff(record):
    errors, warnings = [], []
    # 10.1 Knowledge Cutoff Events
    last_updated = record.get("Last Updated")
    if not is_null_like(last_updated):
        try:
            update_date = datetime.strptime(str(last_updated), "%Y-%m-%d")
            if update_date > datetime.now():
                errors.append("Last Updated date cannot be in the future")
        except ValueError:
            pass
    return errors, warnings
"""

# Read original files, remove previous additions if any (by checking if "CATEGORY 1" is there)
with open(os.path.join(base_dir, "text_rules.py"), "r") as f:
    text_content = f.read()

if "CATEGORY 1: INPUT VALIDATION" not in text_content:
    with open(os.path.join(base_dir, "text_rules.py"), "a") as f:
        f.write(text_additions)

with open(os.path.join(base_dir, "numeric_rules.py"), "r") as f:
    numeric_content = f.read()

if "CATEGORY 3: DATA ACCURACY" not in numeric_content:
    with open(os.path.join(base_dir, "numeric_rules.py"), "a") as f:
        f.write(numeric_additions)

# Update rules.json
rules_mapping = {
    "1": {
        "module": "rules.text_rules",
        "functions": ["validate_input_standard", "validate_input_empty"]
    },
    "2": {
        "module": "rules.text_rules",
        "functions": ["validate_mandatory_fields", "validate_field_dependency"]
    },
    "3": {
        "module": "rules.numeric_rules",
        "functions": ["validate_cross_field_consistency"]
    },
    "4": {
        "module": "rules.text_rules",
        "functions": ["validate_plausible_but_false"]
    },
    "5": {
        "module": "rules.numeric_rules",
        "functions": ["validate_logical_consistency"]
    },
    "6": {
        "module": "rules.numeric_rules",
        "functions": ["validate_very_large_companies"]
    },
    "7": {
        "module": "rules.numeric_rules",
        "functions": ["validate_negative_values", "validate_percentage_bounds"]
    },
    "8": {
        "module": "rules.text_rules",
        "functions": ["validate_url_validity", "validate_text_length"]
    },
    "9": {
        "module": "rules.text_rules",
        "functions": ["validate_context_confusion"]
    },
    "10": {
        "module": "rules.numeric_rules",
        "functions": ["validate_knowledge_cutoff"]
    },
    "11": {
        "module": "rules.text_rules",
        "functions": ["validate_multiple_entities"]
    },
    "12": {
        "module": "rules.text_rules",
        "functions": ["validate_company_category"]
    },
    "13": {
        "module": "rules.text_rules",
        "functions": ["validate_response_time"]
    },
    "14": {
        "module": "rules.text_rules",
        "functions": ["validate_missing_values", "validate_not_applicable", "validate_ambiguity", "validate_defaults", "validate_null_propagation"]
    },
    "15": {
        "module": "rules.numeric_rules",
        "functions": ["validate_confidence", "validate_source_quality", "validate_recency", "validate_data_alignment", "calculate_overall_quality"]
    }
}

with open(os.path.join(base_dir, "rules.json"), "w") as f:
    json.dump(rules_mapping, f, indent=4)

# Delete the separate files
files_to_delete = [
    "input_validation_rules.py", "completeness_rules.py", "accuracy_rules.py",
    "hallucination_rules.py", "consistency_rules.py", "edge_cases_rules.py",
    "boundary_rules.py", "format_structure_rules.py", "adversarial_rules.py",
    "temporal_rules.py", "ambiguity_rules.py", "classification_rules.py",
    "performance_rules.py"
]
for file in files_to_delete:
    p = os.path.join(base_dir, file)
    if os.path.exists(p):
        os.remove(p)

print("Rules reorganized successfully.")
