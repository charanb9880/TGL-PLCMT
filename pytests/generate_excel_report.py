import pandas as pd
import json
import os
import importlib

base_dir = "/Users/charanb/Desktop/TGL_Customised/final_ui/pytests"

def generate_excel_report():
    xl = pd.ExcelFile("/Users/charanb/Desktop/TGL_Customised/TGl.xlsx")
    sheets = [s for s in xl.sheet_names if 'Consolidated' in s]
    
    with open(os.path.join(base_dir, "rules", "rules.json"), "r") as f:
        rules_config = json.load(f)
        
    detailed_results = []
    
    for sheet in sheets:
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
                    try:
                        errs, warns = func(record)
                        
                        if not errs and not warns:
                            detailed_results.append({
                                "Company": sheet.replace("_Consolidated", "").replace(" Consolidated", ""),
                                "Rule Category ID": rule_id,
                                "Function": func_name,
                                "Status": "PASS",
                                "Message": ""
                            })
                        
                        for e in errs:
                            detailed_results.append({
                                "Company": sheet.replace("_Consolidated", "").replace(" Consolidated", ""),
                                "Rule Category ID": rule_id,
                                "Function": func_name,
                                "Status": "FAIL",
                                "Message": e
                            })
                            
                        for w in warns:
                            detailed_results.append({
                                "Company": sheet.replace("_Consolidated", "").replace(" Consolidated", ""),
                                "Rule Category ID": rule_id,
                                "Function": func_name,
                                "Status": "WARNING",
                                "Message": w
                            })
                            
                    except: pass

    df_details = pd.DataFrame(detailed_results)
    
    # Calculate Summary
    summary = df_details.groupby(['Company', 'Status']).size().unstack(fill_value=0)
    # Ensure PASS, FAIL, WARNING columns exist
    for col in ['PASS', 'FAIL', 'WARNING']:
        if col not in summary.columns:
            summary[col] = 0
            
    summary = summary[['PASS', 'FAIL', 'WARNING']].reset_index()
    summary['Total Tests'] = summary['PASS'] + summary['FAIL'] + summary['WARNING']
    
    # Save to Excel
    out_path = "/Users/charanb/Desktop/TGL_Customised/Validation_Results_Report.xlsx"
    with pd.ExcelWriter(out_path) as writer:
        summary.to_excel(writer, sheet_name='Summary', index=False)
        df_details.to_excel(writer, sheet_name='Detailed Results', index=False)
        
    print(f"Report successfully generated at: {out_path}")

generate_excel_report()
