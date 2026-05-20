import importlib
import logging

logger = logging.getLogger(__name__)

def test_automated_excel_validation(test_data, rules_config):
    """
    Main test loop that iterates through Excel records and executes mapped rules.
    """
    for case in test_data:
        test_id = case.get("Test ID")
        rule_id = str(case.get("rule_id"))
        input_data = case.get("parsed_input")
        expected = str(case.get("Expected Result")).upper()
        
        # Determine rule category (e.g. "14")
        category = rule_id.split('.')[0] if '.' in rule_id else rule_id
        
        config = rules_config.get(category)
        if not config:
            continue
            
        module_path = config["module"]
        function_names = config["functions"]
        
        # Dynamically import the rules module
        module = importlib.import_module(module_path)
        
        all_errors = []
        all_warnings = []
        
        for func_name in function_names:
            func = getattr(module, func_name, None)
            if func:
                errs, warns = func(input_data)
                all_errors.extend(errs)
                all_warnings.extend(warns)
        
        # Assertion Logic
        if "FAIL" in expected:
            assert len(all_errors) > 0, f"{test_id} failed: Expected FAIL but found no errors"
        elif "PASS" in expected:
            assert len(all_errors) == 0, f"{test_id} failed: Expected PASS but found errors: {all_errors}"
        
        logger.info(f"Test {test_id} ({rule_id}): PASSED")
