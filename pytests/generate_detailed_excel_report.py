import pandas as pd
import json
import os
import importlib

base_dir = "/Users/charanb/Desktop/TGL_Customised/final_ui/pytests"

# Map function names back to test descriptions for the report
function_meta = {
    "validate_input_standard": {"ID": "1.1", "Category": "INPUT VALIDATION", "Description": "Test with standard, well-formatted company names"},
    "validate_input_empty": {"ID": "1.2", "Category": "INPUT VALIDATION", "Description": "Test with null, empty, or whitespace-only inputs"},
    "validate_mandatory_fields": {"ID": "2.4", "Category": "DATA COMPLETENESS", "Description": "Critical fields present, optional fields missing"},
    "validate_field_dependency": {"ID": "2.5", "Category": "DATA COMPLETENESS", "Description": "Related fields populated together or empty together"},
    "validate_cross_field_consistency": {"ID": "3.4", "Category": "DATA ACCURACY", "Description": "Values align across related fields"},
    "validate_plausible_but_false": {"ID": "4.2", "Category": "HALLUCINATION DETECTION", "Description": "Reasonable-sounding incorrect information"},
    "validate_logical_consistency": {"ID": "5.2", "Category": "INTERNAL CONSISTENCY", "Description": "Fields logically align with each other"},
    "validate_very_large_companies": {"ID": "6.2", "Category": "EDGE CASES", "Description": "Conglomerates with complex structures"},
    "validate_negative_values": {"ID": "7.3", "Category": "BOUNDARY VALUES", "Description": "Fields that can be negative"},
    "validate_percentage_bounds": {"ID": "7.4", "Category": "BOUNDARY VALUES", "Description": "Values constrained to 0-100%"},
    "validate_url_validity": {"ID": "8.2", "Category": "FORMAT & STRUCTURE", "Description": "Working vs broken links"},
    "validate_text_length": {"ID": "8.6", "Category": "FORMAT & STRUCTURE", "Description": "Fields within reasonable character limits"},
    "validate_context_confusion": {"ID": "9.3", "Category": "ADVERSARIAL TESTS", "Description": "Similar names in sequence"},
    "validate_knowledge_cutoff": {"ID": "10.1", "Category": "TEMPORAL VALIDITY", "Description": "Events after LLM training data cutoff"},
    "validate_multiple_entities": {"ID": "11.1", "Category": "AMBIGUITY RESOLUTION", "Description": "Disambiguation of identical names"},
    "validate_company_category": {"ID": "12.1", "Category": "CLASSIFICATION & CATEGORIZATION", "Description": "Startup/MSME/SMB/Investor/VC classification"},
    "validate_response_time": {"ID": "13.2", "Category": "SCALE & PERFORMANCE", "Description": "Generation time for different company types"},
    "validate_missing_values": {"ID": "14.1", "Category": "NULL/NA HANDLING", "Description": "Unavailable Data"},
    "validate_not_applicable": {"ID": "14.2", "Category": "NULL/NA HANDLING", "Description": "Not Applicable Fields"},
    "validate_ambiguity": {"ID": "14.3", "Category": "NULL/NA HANDLING", "Description": "Ambiguous Availability"},
    "validate_defaults": {"ID": "14.4", "Category": "NULL/NA HANDLING", "Description": "Default Value Handling"},
    "validate_null_propagation": {"ID": "14.5", "Category": "NULL/NA HANDLING", "Description": "Null Propagation"},
    "validate_confidence": {"ID": "15.1", "Category": "QUALITY THRESHOLDS", "Description": "Confidence Levels"},
    "validate_source_quality": {"ID": "15.2", "Category": "QUALITY THRESHOLDS", "Description": "Source Quality Tiers"},
    "validate_recency": {"ID": "15.3", "Category": "QUALITY THRESHOLDS", "Description": "Recency Scoring"},
    "validate_data_alignment": {"ID": "15.4", "Category": "QUALITY THRESHOLDS", "Description": "Accuracy Alignment"},
    "calculate_overall_quality": {"ID": "15.5", "Category": "QUALITY THRESHOLDS", "Description": "Overall Quality Score"}
}

def generate_excel_report():
    xl = pd.ExcelFile("/Users/charanb/Desktop/TGL_Customised/TGl.xlsx")
    sheets = [s for s in xl.sheet_names if 'Consolidated' in s]
    
    with open(os.path.join(base_dir, "rules", "rules.json"), "r") as f:
        rules_config = json.load(f)
        
    detailed_results = []
    
    for sheet in sheets:
        company_name_clean = sheet.replace("_Consolidated", "").replace(" Consolidated", "")
        df = xl.parse(sheet)
        param_col = next((c for c in df.columns if 'Parameter' in str(c)), None)
        data_col = next((c for c in df.columns if 'Research Output' in str(c) or 'Data' in str(c)), None)
        if not param_col or not data_col: continue
        
        df = df.dropna(subset=[param_col])
        record = dict(zip(df[param_col].astype(str).str.strip(), df[data_col]))
        
        for rule_id, config in rules_config.items():
            module_path = config["module"]
            try:
                module = importlib.import_module(module_path)
            except: continue
            
            for func_name in config["functions"]:
                func = getattr(module, func_name, None)
                if func:
                    meta = function_meta.get(func_name, {"ID": f"Category {rule_id}", "Category": f"Rule {rule_id}", "Description": "Validation Check"})
                    
                    try:
                        errs, warns = func(record)
                        
                        if not errs and not warns:
                            detailed_results.append({
                                "Company Tested": company_name_clean,
                                "Test ID": meta["ID"],
                                "Test Category": meta["Category"],
                                "Description": meta["Description"],
                                "Validation Rule": func_name,
                                "Status": "✅ PASS",
                                "Failure / Warning Details": "None - Data met all criteria"
                            })
                        
                        for e in errs:
                            detailed_results.append({
                                "Company Tested": company_name_clean,
                                "Test ID": meta["ID"],
                                "Test Category": meta["Category"],
                                "Description": meta["Description"],
                                "Validation Rule": func_name,
                                "Status": "❌ FAIL",
                                "Failure / Warning Details": e
                            })
                            
                        for w in warns:
                            detailed_results.append({
                                "Company Tested": company_name_clean,
                                "Test ID": meta["ID"],
                                "Test Category": meta["Category"],
                                "Description": meta["Description"],
                                "Validation Rule": func_name,
                                "Status": "⚠️ WARNING",
                                "Failure / Warning Details": w
                            })
                            
                    except Exception as e:
                        detailed_results.append({
                            "Company Tested": company_name_clean,
                            "Test ID": meta["ID"],
                            "Test Category": meta["Category"],
                            "Description": meta["Description"],
                            "Validation Rule": func_name,
                            "Status": "⚠️ EXECUTION ERROR",
                            "Failure / Warning Details": str(e)
                        })

    df_details = pd.DataFrame(detailed_results)
    
    # Calculate Summary
    status_col = df_details['Status'].apply(lambda x: x.split(" ")[1]) # Extract just PASS/FAIL/WARNING
    df_details['RawStatus'] = status_col
    summary = df_details.groupby(['Company Tested', 'RawStatus']).size().unstack(fill_value=0)
    for col in ['PASS', 'FAIL', 'WARNING']:
        if col not in summary.columns:
            summary[col] = 0
            
    summary = summary[['PASS', 'FAIL', 'WARNING']].reset_index()
    summary['Total Executed Tests'] = summary['PASS'] + summary['FAIL'] + summary['WARNING']
    
    df_details = df_details.drop(columns=['RawStatus'])
    
    # Save to Excel with nice formatting
    out_path = "/Users/charanb/Desktop/TGL_Customised/Detailed_Validation_Report.xlsx"
    with pd.ExcelWriter(out_path) as writer:
        summary.to_excel(writer, sheet_name='High-Level Summary', index=False)
        df_details.to_excel(writer, sheet_name='Detailed Test Cases', index=False)
        
    print(f"Report successfully generated at: {out_path}")

if __name__ == "__main__":
    generate_excel_report()
