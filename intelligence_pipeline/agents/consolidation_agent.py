def consolidate_records(llm_outputs: list) -> dict:
    """Consolidates multiple outputs into a golden record resolving conflicts."""
    if not llm_outputs:
        return {}
        
    golden_record = {}
    all_keys = set()
    
    # Filter out errored outputs
    valid_outputs = [out for out in llm_outputs if "_error" not in out]
    if not valid_outputs:
        return {}

    for output in valid_outputs:
        all_keys.update([k for k in output.keys() if not k.startswith("_")])
        
    for key in all_keys:
        values = [out.get(key) for out in valid_outputs if out.get(key) is not None]
        if not values:
            continue
            
        # Frequency count for majority vote
        val_counts = {}
        for v in values:
            str_v = str(v)
            val_counts[str_v] = val_counts.get(str_v, 0) + 1
            
        best_val_str = max(val_counts, key=val_counts.get)
        
        # Restore original type
        best_val = next((v for v in values if str(v) == best_val_str), None)
        golden_record[key] = best_val
        
    return golden_record
