import os
import json

base_dir = "/Users/charanb/Desktop/TGL_Customised/final_ui/pytests/rules"

files_content = {
    "input_validation_rules.py": """from validators.common import is_null_like

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
""",
    "completeness_rules.py": """from validators.common import is_null_like

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
""",
    "accuracy_rules.py": """from validators.common import is_null_like

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
""",
    "hallucination_rules.py": """from validators.common import is_null_like

def validate_plausible_but_false(record):
    errors, warnings = [], []
    # 4.2 Plausible but False
    funding_amt = record.get("Total Capital Raised")
    if isinstance(funding_amt, (int, float)) and funding_amt > 1e12:
        warnings.append("Suspiciously high funding amount, potential hallucination")
    return errors, warnings
""",
    "consistency_rules.py": """from validators.common import is_null_like

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
""",
    "edge_cases_rules.py": """from validators.common import is_null_like

def validate_very_large_companies(record):
    errors, warnings = [], []
    # 6.2 Very Large Companies
    emp_size = record.get("Employee Size")
    if isinstance(emp_size, (int, float)) and emp_size > 1000000:
        warnings.append("Very large conglomerate detected, generic fields might lack nuance")
    return errors, warnings
""",
    "boundary_rules.py": """from validators.common import is_null_like

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
""",
    "format_structure_rules.py": """from validators.common import is_null_like

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
""",
    "adversarial_rules.py": """from validators.common import is_null_like

def validate_context_confusion(record):
    errors, warnings = [], []
    # 9.3 Context Confusion (Placeholder)
    return errors, warnings
""",
    "temporal_rules.py": """from datetime import datetime
from validators.common import is_null_like

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
""",
    "ambiguity_rules.py": """from validators.common import is_null_like

def validate_multiple_entities(record):
    errors, warnings = [], []
    # 11.1 Multiple Entities Same Name
    desc = str(record.get("Company Description", "")).lower()
    if "did you mean" in desc or "multiple entities" in desc:
        warnings.append("Ambiguity detected in output description")
    return errors, warnings
""",
    "classification_rules.py": """from validators.common import is_null_like

def validate_company_category(record):
    errors, warnings = [], []
    # 12.1 Company Category
    category = str(record.get("Category", "")).lower()
    valid_categories = ["startup", "msme", "smb", "investor", "vc", "enterprise", "public"]
    if category and not is_null_like(category) and not any(v in category for v in valid_categories):
        warnings.append(f"Unusual category detected: {category}")
    return errors, warnings
""",
    "performance_rules.py": """from validators.common import is_null_like

def validate_response_time(record):
    errors, warnings = [], []
    # 13.2 Response Time
    return errors, warnings
"""
}

# Write files
for filename, content in files_content.items():
    with open(os.path.join(base_dir, filename), "w") as f:
        f.write(content)

# Update rules.json
rules_mapping = {
    "1": {
        "module": "rules.input_validation_rules",
        "functions": ["validate_input_standard", "validate_input_empty"]
    },
    "2": {
        "module": "rules.completeness_rules",
        "functions": ["validate_mandatory_fields", "validate_field_dependency"]
    },
    "3": {
        "module": "rules.accuracy_rules",
        "functions": ["validate_cross_field_consistency"]
    },
    "4": {
        "module": "rules.hallucination_rules",
        "functions": ["validate_plausible_but_false"]
    },
    "5": {
        "module": "rules.consistency_rules",
        "functions": ["validate_logical_consistency"]
    },
    "6": {
        "module": "rules.edge_cases_rules",
        "functions": ["validate_very_large_companies"]
    },
    "7": {
        "module": "rules.boundary_rules",
        "functions": ["validate_negative_values", "validate_percentage_bounds"]
    },
    "8": {
        "module": "rules.format_structure_rules",
        "functions": ["validate_url_validity", "validate_text_length"]
    },
    "9": {
        "module": "rules.adversarial_rules",
        "functions": ["validate_context_confusion"]
    },
    "10": {
        "module": "rules.temporal_rules",
        "functions": ["validate_knowledge_cutoff"]
    },
    "11": {
        "module": "rules.ambiguity_rules",
        "functions": ["validate_multiple_entities"]
    },
    "12": {
        "module": "rules.classification_rules",
        "functions": ["validate_company_category"]
    },
    "13": {
        "module": "rules.performance_rules",
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

if os.path.exists(os.path.join(base_dir, "extended_rules.py")):
    os.remove(os.path.join(base_dir, "extended_rules.py"))

print("Rule files generated and rules.json updated successfully.")
