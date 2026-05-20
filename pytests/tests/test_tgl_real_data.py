import pytest
import pandas as pd
import json
import os
import importlib
import logging

logger = logging.getLogger(__name__)

def load_tgl_data():
    file_path = "/Users/charanb/Desktop/TGL_Customised/TGl.xlsx"
    if not os.path.exists(file_path):
        return []
    
    xl = pd.ExcelFile(file_path)
    sheets = [s for s in xl.sheet_names if 'Consolidated' in s]
    
    combined_data = []
    for sheet in sheets:
        try:
            df = xl.parse(sheet)
            # Find the parameter and output columns regardless of exact spacing
            param_col = next((c for c in df.columns if 'Parameter' in str(c)), None)
            data_col = next((c for c in df.columns if 'Research Output' in str(c) or 'Data' in str(c)), None)
            
            if param_col and data_col:
                # Drop rows where Parameter is NaN
                df = df.dropna(subset=[param_col])
                record = dict(zip(df[param_col].astype(str).str.strip(), df[data_col]))
                combined_data.append({
                    "company_sheet": sheet,
                    "record": record
                })
        except Exception as e:
            logger.error(f"Failed to parse sheet {sheet}: {e}")
            
    return combined_data

@pytest.fixture(scope="session")
def tgl_data():
    return load_tgl_data()

def test_tgl_real_data(tgl_data, rules_config):
    """
    Validates actual company data from TGl.xlsx against all configured rules.
    """
    if not tgl_data:
        pytest.skip("TGl.xlsx not found or empty.")
        
    total_errors = 0
    all_reports = []
    
    for case in tgl_data:
        company_name = case["company_sheet"]
        record = case["record"]
        
        company_errors = []
        company_warnings = []
        
        # Run all rules defined in rules_config
        for rule_id, config in rules_config.items():
            module_path = config["module"]
            function_names = config["functions"]
            
            try:
                module = importlib.import_module(module_path)
            except Exception as e:
                continue
                
            for func_name in function_names:
                func = getattr(module, func_name, None)
                if func:
                    try:
                        errs, warns = func(record)
                        company_errors.extend([(rule_id, e) for e in errs])
                        company_warnings.extend([(rule_id, w) for w in warns])
                    except Exception as e:
                        logger.error(f"Error running {func_name} on {company_name}: {e}")
                        
        if company_errors:
            report = f"\n--- {company_name} FAILURES ---"
            for r_id, err in company_errors:
                report += f"\n[Rule {r_id}] {err}"
            all_reports.append(report)
            total_errors += len(company_errors)
            
        if company_warnings:
            logger.warning(f"\n--- {company_name} WARNINGS ---")
            for r_id, warn in company_warnings:
                logger.warning(f"[Rule {r_id}] {warn}")
                
    if total_errors > 0:
        for report in all_reports:
            print(report)
        assert False, f"Found {total_errors} total validation errors across companies in TGl.xlsx. See stdout for details."
