import re
from config_asia import MEDAL_HEADER_MAP_ASIA

# second regex of doom and despair but for asia. 
# at least asia hicom that makes documents respect formatting way more
MEDAL_LINE_RE = re.compile(
    r"^\*\s*([A-Za-z0-9_]+)\s*(?:-|\s+)?\s*(.*)$"
)


def parse_document(text, exclude_clasps=None):
    if exclude_clasps is None:
        exclude_clasps = {}

    rows = []
    skipped = []
    current_medal = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        upper = line.upper()

        if upper in MEDAL_HEADER_MAP_ASIA:
            current_medal = MEDAL_HEADER_MAP_ASIA[upper]
            print(f"\n=== {current_medal} ===")
            continue

        if "ORDERS OF THE EMPIRE" in upper:
            current_medal = None
            continue
        if "ÖSTERREICHISCHER ADELSHOF" in upper:
            current_medal = None
            continue
        if "REGIMENTALE PROMOTIONEN" in upper:
            current_medal = None
            continue
        if "GRENADIER-ENTWÜRFE" in upper:
            current_medal = None
            continue

        if current_medal is None:
            continue

        if line.startswith("*"):
            medal_match = MEDAL_LINE_RE.match(line)
            if medal_match:
                username = medal_match.group(1).strip()
                clasp = medal_match.group(2).strip()
                
                # Clean up clasp
                if not clasp:
                    clasp = "No Clasp"
                elif "Bronze" in clasp:
                    clasp = "Bronze"
                elif "Silver" in clasp:
                    clasp = "Silber"
                elif "Gold" in clasp:
                    clasp = "Gold"
                else:
                    clasp = "No Clasp"

                valid_clasps = ("Bronze", "Silber", "Gold")
                if clasp not in valid_clasps:
                    skipped.append({
                        "user": username,
                        "medal": current_medal,
                        "clasp": clasp,
                    })
                    print(f"Skipping {username} ({current_medal}, {clasp})")
                    continue

                if exclude_clasps.get(clasp, False):
                    print(f"Excluded {username} ({clasp})")
                    continue

                rows.append({
                    "username": username,
                    "korps": "",     
                    "regiment": "",  
                    "medal": current_medal,
                    "clasp": clasp,
                })
                print(f"Accepted: {username} | {current_medal} | {clasp}")

    print("\n========== SUMMARY ==========")
    print(f"Accepted : {len(rows)}")
    print(f"Skipped  : {len(skipped)}")

    return rows, skipped
