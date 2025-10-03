import re
from typing import Optional

def find_solana_contract(message: str) -> Optional[str]:
    strict_match = re.search(r'^\s*([1-9A-HJ-NP-Za-km-z]{32,44})\s*$', message, re.MULTILINE)
    if strict_match:
        return strict_match.group(1).strip()

    pump_match = re.search(r'([1-9A-HJ-NP-Za-km-z]{32,44}pump)', message)
    if pump_match:
        return pump_match.group(1)

    general_match = re.search(r'([1-9A-HJ-NP-Za-km-z]{32,44})', message)
    if general_match:
        full_match_text = general_match.group(0)
        start_index = general_match.start(0)
        end_index = general_match.end(0)
        prev_char_ok = start_index == 0 or not message[start_index-1].isalnum()
        next_char_ok = end_index == len(message) or not message[end_index].isalnum()
        if prev_char_ok and next_char_ok:
            return full_match_text
    return None