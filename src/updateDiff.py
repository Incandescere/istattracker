# pipip install deepdiff
from deepdiff import DeepDiff

def updateDiff(old_update_json, new_update_json):
    result = "<b>Stats gained</b>\n\n"
    changed = DeepDiff(old_update_json, new_update_json).get('values_changed')
    for key, val in changed.items():
        # Clean key name
        clean_key = key.split('[')[1].strip("']").replace("_", " ")
        old = val['old_value']
        new = val['new_value']
        
        # Try to compute numeric delta
        try:
            delta = int(new) - int(old)
            result += f"{clean_key}: {old} -> {new} ({'+' if delta >= 0 else ''}{delta})\n"
        except ValueError:
            # For non-numeric values like date or time
            result += f"{clean_key}: {old} -> {new}\n"
    return result