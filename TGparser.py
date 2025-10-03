import re
from typing import Optional

def find_solana_contract(message: str) -> Optional[str]:
    strict = re.search(r'^\s*([1-9A-HJ-NP-Za-km-z]{32,44})\s*$', message, re.MULTILINE)
    if strict:
        return strict.group(1).strip()

    pump = re.search(r'([1-9A-HJ-NP-Za-km-z]{32,44}pump)', message)
    if pump:
        return pump.group(1)

    general = re.search(r'([1-9A-HJ-NP-Za-km-z]{32,44})', message)
    if general:
        txt = general.group(0)
        s, e = general.start(), general.end()
        if (s == 0 or not message[s-1].isalnum()) and (e == len(message) or not message[e].isalnum()):
            return txt
    return None
