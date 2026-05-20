from validators.url_validator import is_valid_url

def validate_logo_url(record):
    errors = []
    warnings = []
    
    logo_url = record.get("Logo")
    if logo_url and not is_valid_url(logo_url):
        errors.append(f"Invalid Logo URL format: {logo_url}")
        
    return errors, warnings
