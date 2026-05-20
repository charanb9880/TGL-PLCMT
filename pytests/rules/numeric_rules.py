from datetime import datetime, timedelta
from validators.common import is_null_like

def validate_confidence(record):
    errors = []
    warnings = []
    
    # 15.1 Confidence levels
    source = str(record.get("Source", "")).lower()
    confidence = record.get("confidence_level") or record.get("Confidence Level")
    is_ai = record.get("AI Generated") or record.get("ai_generated")
    
    # Check if critical data exists but confidence is missing
    critical_metric_fields = ["Annual Revenues", "Employee Size", "Company Valuation"]
    has_metrics = any(not is_null_like(record.get(f)) for f in critical_metric_fields)
    
    if has_metrics and is_null_like(confidence) and "confidence_level" in record:
        warnings.append("Estimated data is missing confidence tagging")

    if is_null_like(confidence):
        return errors, warnings

    conf_str = str(confidence).lower()
    
    # Logic from Excel
    if "sec filing" in source and conf_str == "high":
        pass # PASS -> Tier-1 source justifies high confidence level
    elif ("blog" in source or "social" in source) and conf_str == "high":
        warnings.append("Blog/Social media is a low-trust source; high confidence might be exaggerated")
    elif is_ai and conf_str == "high":
        errors.append("AI/inferred data cannot be marked high confidence without human verification")
        
    return errors, warnings


def validate_source_quality(record):
    errors = []
    warnings = []
    
    # 15.2 Source Quality Tiers
    source = record.get("Source")
    if is_null_like(source):
        if "Source" in record:
            warnings.append("Missing data provenance; violates traceability requirement")
        return errors, warnings

    source_str = str(source).lower()
    tier_1 = ["sec", "official", "filing", "company website", "government"]
    tier_2 = ["linkedin", "crunchbase", "reuters", "bloomberg", "news"]
    tier_3 = ["blog", "article", "social media", "twitter", "reddit"]
    
    # Handle list of sources
    sources = source_str.split(",") if isinstance(source, str) else [source_str]
    
    has_tier_1 = any(any(kw in s for kw in tier_1) for s in sources)
    has_tier_3 = any(any(kw in s for kw in tier_3) for s in sources)
    
    if len(sources) > 1 and has_tier_1 and has_tier_3:
        warnings.append("Conflicting reliability levels in sources; needs reconciliation")
    
    if not has_tier_1 and not any(any(kw in s for kw in tier_2) for s in sources):
        if has_tier_3:
            warnings.append(f"Low credibility source detected: {source}")
        else:
            warnings.append(f"Source quality is unverified/Tier 3: {source}")
            
    return errors, warnings

def validate_recency(record):
    errors = []
    warnings = []
    
    # 15.3 Recency Scoring
    last_updated = record.get("date") or record.get("Last Updated")
    if is_null_like(last_updated):
        if "Last Updated" in record or "date" in record:
            warnings.append("Cannot evaluate recency without timestamp")
        return errors, warnings
        
    try:
        if isinstance(last_updated, datetime):
            update_date = last_updated
        else:
            update_date = datetime.strptime(str(last_updated), "%Y-%m-%d")
            
        diff = datetime.now() - update_date
        if diff > timedelta(days=365):
            errors.append(f"Data is stale (>12 months): last updated {last_updated}")
        elif diff > timedelta(days=180):
            warnings.append(f"Data is aging (>6 months): last updated {last_updated}")
    except:
        warnings.append(f"Could not parse date format: {last_updated}")
        
    return errors, warnings

def validate_data_alignment(record):
    errors = []
    warnings = []
    
    # 15.4 Accuracy Alignment (Accuracy)
    revenue = record.get("Annual Revenues")
    emp_size = record.get("Employee Size")
    nature = str(record.get("Nature of Company", "")).lower()
    
    # Cross-check: High revenue for a startup
    if nature == "startup" and revenue and isinstance(revenue, (int, float)) and revenue > 1000000000:
        warnings.append(f"Revenue outlier for Startup: ${revenue:,}")
        
    # Cross-check: Large employee size for private/LLC
    if "private" in nature and emp_size and isinstance(emp_size, (int, float)) and emp_size > 50000:
        warnings.append(f"Employee size outlier for Private entity: {emp_size:,}")
        
    return errors, warnings

def calculate_overall_quality(record):
    errors = []
    warnings = []
    
    # 15.5 Overall Quality Score
    score = 0
    
    # Confidence (40 pts)
    conf = str(record.get("confidence_level") or record.get("Confidence Level", "")).lower()
    if conf == "high": score += 40
    elif conf == "medium": score += 25
    elif conf == "low": score += 10
    
    # Source (30 pts)
    source = str(record.get("Source", "")).lower()
    tier_1 = ["sec", "official", "filing", "company website"]
    if any(kw in source for kw in tier_1): score += 30
    elif any(kw in source for kw in ["linkedin", "crunchbase", "news"]): score += 20
    else: score += 10
    
    # Recency (30 pts)
    last_updated = record.get("date") or record.get("Last Updated")
    if not is_null_like(last_updated):
        try:
            update_date = datetime.strptime(str(last_updated), "%Y-%m-%d")
            diff = datetime.now() - update_date
            if diff < timedelta(days=180): score += 30
            elif diff < timedelta(days=365): score += 15
        except:
             pass

    if is_null_like(record.get("confidence_level")) and is_null_like(record.get("Source")) and is_null_like(last_updated):
        return errors, warnings # Skip quality scoring if dataset has no metadata

    if score < 50:
        warnings.append(f"Overall quality score ({score}) is failing (F)")
    elif score < 70:
        warnings.append(f"Overall quality score ({score}) is marginal (C/D)")
    elif score >= 90:
        # High quality - no warnings
        pass
        
    return errors, warnings



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
