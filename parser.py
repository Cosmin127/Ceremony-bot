import re
from config import (
    KORPS_MAP,
    REGIMENT_MAP_BY_KORPS,
    REGIMENT_MAP_FALLBACK,
    MEDAL_HEADER_MAP,
    VALID_CLASPS
)

EU_PATTERN = re.compile(r"(?:\[(.*?)\]\s*-*\s*)?([A-Za-z0-9_]+)\s*(?:,|-)\s*(.+)")
ASIA_MEDAL_PATTERN = re.compile(r"^\*\s*([A-Za-z0-9_]+)\s*(?:-|\s+)?\s*(.*)$")
ASIA_ORDER_REGIMENT = re.compile(r"^Regiment:\s*(.+)$", re.IGNORECASE)
ASIA_ORDER_USERNAME = re.compile(r"^Username:\s*(.+)$", re.IGNORECASE)
ASIA_ORDER_CLASS = re.compile(r"^Class:\s*(.+)$", re.IGNORECASE)

def clean_clasp(clasp):
    if not clasp:
        return "No Clasp"
    clasp = clasp.lower().strip()
    clasp = re.sub(r'\s+clasp\b', '', clasp)
    clasp = re.sub(r'\s+class\b', '', clasp)
    clasp = re.sub(r'\s+medal\b', '', clasp)
    clasp = re.sub(r'[.,;:]+$', '', clasp)
    clasp = re.sub(r'\s+', ' ', clasp).strip()
    if "no" in clasp or clasp == "":
        return "No Clasp"
    if "silver" in clasp:
        return "Silber"
    if "bronze" in clasp:
        return "Bronze"
    if "gold" in clasp:
        return "Gold"
    if "knappe" in clasp:
        return "Knappe"
    if "ritter" in clasp:
        return "Ritter"
    if "kommandeur" in clasp:
        return "Kommandeur"
    if "großmeister" in clasp or "grossmeister" in clasp:
        return "Großmeister"
    if "hochmeister" in clasp:
        return "Hochmeister"
    return clasp.title()

def get_regiment_name(regiment_tag, korps):
    if not regiment_tag:
        return ""
    if korps and korps in REGIMENT_MAP_BY_KORPS:
        return REGIMENT_MAP_BY_KORPS[korps].get(regiment_tag, REGIMENT_MAP_FALLBACK.get(regiment_tag, ""))
    return REGIMENT_MAP_FALLBACK.get(regiment_tag, "")

def get_korps_from_regiment_with_context(regiment_tag, context_korps=None):
    """Get korps from regiment tag, using context if provided"""
    if not regiment_tag:
        return ""
    
    if context_korps:
        if context_korps in REGIMENT_MAP_BY_KORPS:
            if regiment_tag in REGIMENT_MAP_BY_KORPS[context_korps]:
                return context_korps
    
    found_korps = []
    for korps, regiments in REGIMENT_MAP_BY_KORPS.items():
        if regiment_tag in regiments:
            found_korps.append(korps)
    
    if len(found_korps) == 1:
        return found_korps[0]
    
    if found_korps:
        return found_korps[0]
    
    return ""

def detect_format(text):
    lines = text.splitlines()
    asia_score = sum(1 for i in ["ASIAN KORPS CEREMONY", "ASIA KORPS-MEDAILLEN", "ÖSTERREICHISCHER ADELSHOF", "REGIMENTALE PROMOTIONEN", "GRENADIER-ENTWÜRFE"] if i in text)
    eu_score = sum(1 for i in ["KAISERLICHE ZEREMONIE", "GENERALSTAB", "KÖNIGLICHE UNGARN", "ERSTE KORPS", "ZWEITE KORPS", "DRITTE KORPS", "FÜNFTES KORPS"] if i in text)
    asia_score += sum(1 for line in lines[:30] if line.strip().startswith("*") and " - " in line) * 0.5
    eu_score += sum(1 for line in lines[:30] if "[" in line and "]" in line and (" - " in line or ", " in line)) * 0.5
    return 'asia' if asia_score > eu_score else 'eu_na'

def parse_document(text, exclude_clasps=None):
    if exclude_clasps is None:
        exclude_clasps = {}
    
    rows, skipped = [], []
    current_item, current_korps = None, None
    format_type = detect_format(text)
    asia_order_buffer = {}
    in_asia_order = False

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        upper = line.upper()

        if upper in KORPS_MAP:
            current_korps = KORPS_MAP[upper]
            current_item = None
            in_asia_order = False
            continue

        if upper in MEDAL_HEADER_MAP:
            current_item = MEDAL_HEADER_MAP[upper]
            in_asia_order = "ORDER" in upper
            continue

        if current_item is None:
            continue

        if format_type == 'eu_na':
            match = EU_PATTERN.match(line)
            if not match:
                continue

            regiment_tag, username, clasp = (match.group(1) or "").strip(), match.group(2).strip(), clean_clasp(match.group(3).strip())

            if clasp not in VALID_CLASPS:
                skipped.append({"user": username, "medal": current_item, "clasp": clasp})
                continue

            if exclude_clasps.get(clasp, False) or (clasp == "Silber" and "no" in line.lower() and exclude_clasps.get("No Clasp", False)):
                continue

            if clasp == "No Clasp" or "SOCIAL" in upper or "SOCIAL" in current_item.upper():
                clasp = "Silber"

            korps_name = current_korps
            
            if not korps_name and regiment_tag:
                korps_name = get_korps_from_regiment_with_context(regiment_tag, None)
            
            if korps_name and regiment_tag:
                if korps_name in REGIMENT_MAP_BY_KORPS:
                    if regiment_tag not in REGIMENT_MAP_BY_KORPS[korps_name]:
                        found = get_korps_from_regiment_with_context(regiment_tag, None)
                        if found:
                            korps_name = found
            
            regiment_name = get_regiment_name(regiment_tag, korps_name)
            if not regiment_name and regiment_tag:
                regiment_name = REGIMENT_MAP_FALLBACK.get(regiment_tag, "")

            rows.append({
                "username": username, 
                "korps": korps_name, 
                "regiment": regiment_name, 
                "medal": current_item, 
                "clasp": clasp
            })

        else:
            if in_asia_order:
                regiment_match = ASIA_ORDER_REGIMENT.match(line)
                username_match = ASIA_ORDER_USERNAME.match(line)
                class_match = ASIA_ORDER_CLASS.match(line)

                if regiment_match:
                    asia_order_buffer["regiment"] = regiment_match.group(1).strip()
                    continue
                if username_match:
                    asia_order_buffer["username"] = username_match.group(1).strip()
                    continue
                if class_match:
                    asia_order_buffer["clasp"] = clean_clasp(class_match.group(1).strip())
                    continue

                if "regiment" in asia_order_buffer and "username" in asia_order_buffer and "clasp" in asia_order_buffer:
                    regiment_tag, username, clasp = asia_order_buffer["regiment"], asia_order_buffer["username"], asia_order_buffer["clasp"]
                    korps_name, regiment_name = "", ""
                    
                    korps_name = get_korps_from_regiment_with_context(regiment_tag, current_korps)
                    
                    for korps, regs in REGIMENT_MAP_BY_KORPS.items():
                        for tag, name in regs.items():
                            if name and name.lower() in regiment_tag.lower():
                                regiment_name = name
                                break
                        if regiment_name:
                            break
                    
                    if not regiment_name:
                        for tag, name in REGIMENT_MAP_FALLBACK.items():
                            if name and name.lower() in regiment_tag.lower():
                                regiment_name = name
                                break
                    
                    if not regiment_name:
                        regiment_name = regiment_tag
                    
                    if clasp == "No Clasp":
                        clasp = "Silber"
                    
                    if clasp in VALID_CLASPS:
                        rows.append({"username": username, "korps": korps_name, "regiment": regiment_name, "medal": current_item, "clasp": clasp})
                    else:
                        skipped.append({"user": username, "medal": current_item, "clasp": clasp})
                    
                    asia_order_buffer = {}
                continue

            if "SOCIAL" in upper or "SOCIAL" in current_item.upper():
                match = ASIA_MEDAL_PATTERN.match(line)
                if match:
                    rows.append({"username": match.group(1).strip(), "korps": "", "regiment": "", "medal": current_item, "clasp": "Silber"})
                continue

            match = ASIA_MEDAL_PATTERN.match(line)
            if not match:
                continue

            username, clasp = match.group(1).strip(), clean_clasp(match.group(2).strip())

            if "Social" in current_item or "SOCIAL" in upper:
                rows.append({"username": username, "korps": "", "regiment": "", "medal": current_item, "clasp": "Silber"})
                continue

            if clasp not in VALID_CLASPS:
                skipped.append({"user": username, "medal": current_item, "clasp": clasp})
                continue

            if exclude_clasps.get(clasp, False):
                continue

            if clasp == "No Clasp":
                clasp = "Silber"

            rows.append({"username": username, "korps": "", "regiment": "", "medal": current_item, "clasp": clasp})

    return rows, skipped
