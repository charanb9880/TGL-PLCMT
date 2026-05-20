import pandas as pd
import json
import os
import importlib
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

def generate_report():
    xl_path = "/Users/charanb/Desktop/TGL_Customised/TGl.xlsx"
    if not os.path.exists(xl_path):
        print(f"Excel file not found at {xl_path}")
        return

    xl = pd.ExcelFile(xl_path)
    sheets = [s for s in xl.sheet_names if 'Consolidated' in s]
    
    with open(os.path.join(base_dir, "rules", "rules.json"), "r") as f:
        rules_config = json.load(f)
        
    report_md = "# TGI Data Validation Report\n\n"
    total_errors = 0
    total_warnings = 0
    
    for sheet in sheets:
        df = xl.parse(sheet)
        param_col = next((c for c in df.columns if 'Parameter' in str(c)), None)
        data_col = next((c for c in df.columns if 'Research Output' in str(c) or 'Data' in str(c)), None)
        if not param_col or not data_col: continue
        
        df = df.dropna(subset=[param_col])
        record = dict(zip(df[param_col].astype(str).str.strip(), df[data_col]))
        
        company_errors = []
        company_warnings = []
        
        for rule_id, config in rules_config.items():
            module_path = config["module"]
            try:
                module = importlib.import_module(module_path)
            except: continue
            
            for func_name in config["functions"]:
                func = getattr(module, func_name, None)
                if func:
                    try:
                        errs, warns = func(record)
                        company_errors.extend([(rule_id, e) for e in errs])
                        company_warnings.extend([(rule_id, w) for w in warns])
                    except: pass
                    
        if company_errors or company_warnings:
            report_md += f"## {sheet}\n"
            if company_errors:
                report_md += "### ❌ Failures\n"
                for r_id, err in company_errors:
                    report_md += f"- **[Rule {r_id}]** {err}\n"
                total_errors += len(company_errors)
            if company_warnings:
                report_md += "### ⚠️ Warnings\n"
                for r_id, warn in company_warnings:
                    report_md += f"- **[Rule {r_id}]** {warn}\n"
                total_warnings += len(company_warnings)
            report_md += "\n"
            
    report_md = f"**Summary:** Found {total_errors} errors and {total_warnings} warnings.\n\n" + report_md
    with open(os.path.join(base_dir, "validation_report.md"), "w") as f:
        f.write(report_md)
    print(f"✅ Validation Report generated at: {os.path.join(base_dir, 'validation_report.md')}")

if __name__ == "__main__":
    generate_report()
