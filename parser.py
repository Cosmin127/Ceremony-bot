# Benjamin netanyahu please help me.
# please let this parser parse correctly

import re
from config import (
    KORPS_MAP,
    REGIMENT_MAP_BY_KORPS,
    REGIMENT_MAP_FALLBACK,
    MEDAL_HEADER_MAP,
)

LINE_RE = re.compile(
    r"(?:\[(.*?)\]\s*-*\s*)?([A-Za-z0-9_]+)\s*(?:,|-)\s*(.+)"
)


def parse_document(text, exclude_clasps=None):
    if exclude_clasps is None:
        exclude_clasps = {}

    rows = []
    skipped = []
    current_medal = None
    current_korps = "Generalstab" 

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        upper = line.upper()

        if upper in KORPS_MAP:
            current_korps = KORPS_MAP[upper]
            print(f"\n--- {current_korps} ---")
            continue

        if upper in MEDAL_HEADER_MAP:
            current_medal = MEDAL_HEADER_MAP[upper]
            print(f"\n=== {current_medal} ===")
            continue

        if current_medal is not None and not LINE_RE.match(line):
            if line.startswith("_") or line.startswith("-") or line.isupper():
                current_medal = None
            continue

        if current_medal is None:
            continue

        m = LINE_RE.match(line)
        if not m:
            continue

        regiment_tag = (m.group(1) or "GS").strip()
        username = m.group(2).strip()
        clasp = m.group(3).strip()

        if not clasp:
            clasp = "No Clasp"

        clasp = re.sub(r"\s+clasp\b", "", clasp, flags=re.IGNORECASE)
        clasp = re.sub(r"\s+class\b", "", clasp, flags=re.IGNORECASE)
        clasp = re.sub(r"\s+medal\b", "", clasp, flags=re.IGNORECASE)
        clasp = re.sub(r"[.,;:]+$", "", clasp)
        clasp = re.sub(r"\s+", " ", clasp).strip()
        clasp = clasp.title()

        if clasp in ("No", "no", "No Clasp"):
            clasp = "Silber"
        elif clasp == "Silver":
            clasp = "Silber"

        valid_clasps = (
            "Bronze",
            "Silber",
            "Gold",
            "Großmeister",
            "Kommandeur",
            "Ritter",
            "Hochmeister",
            "Knappe",
        )

        if clasp not in valid_clasps:
            skipped.append({
                "user": username,
                "medal": current_medal,
                "clasp": clasp,
            })
            print(f"Skipping {username} ({current_medal}, {clasp})")
            continue

        original_clasp = clasp

        if clasp == "Silber":
            if re.search(r"\bno\b", m.group(3), flags=re.IGNORECASE):
                if exclude_clasps.get("No Clasp", False):
                    print(f"Excluded {username} (No Clasp)")
                    continue
            elif exclude_clasps.get("Silver", False):
                print(f"Excluded {username} (Silver)")
                continue
        elif exclude_clasps.get(clasp, False):
            print(f"Excluded {username} ({clasp})")
            continue

        korps_regiments = REGIMENT_MAP_BY_KORPS.get(current_korps, {})
        regiment = korps_regiments.get(regiment_tag)

        if regiment is None:
            regiment = REGIMENT_MAP_FALLBACK.get(regiment_tag, "")

        rows.append({
            "username": username,
            "korps": current_korps,
            "regiment": regiment,
            "medal": current_medal,
            "clasp": clasp,
        })

        print(f"Accepted: {username} | {current_korps} | {regiment} | {current_medal} | {clasp}")

    print("\n========== SUMMARY ==========")
    print(f"Accepted : {len(rows)}")
    print(f"Skipped  : {len(skipped)}")

    return rows, skipped
