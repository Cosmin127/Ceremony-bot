import re
from config import (
    REGIMENT_MAP,
    MEDAL_HEADER_MAP
)


LINE_RE = re.compile(
    r"\[(.*?)\]\s*-?\s*([A-Za-z0-9_]+)\s*[-,]?\s*(.*)"
)


def parse_document(text):

    rows = []

    skipped = []

    current_medal = None

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        upper = line.upper()

        if upper in MEDAL_HEADER_MAP:

            current_medal = MEDAL_HEADER_MAP[upper]

            print(f"\n=== {current_medal} ===")

            continue

        if current_medal is None:
            continue

        m = LINE_RE.match(line)

        if not m:
            continue

        regiment_tag = m.group(1).strip()
        username = m.group(2).strip()
        clasp = m.group(3).strip()

        if not clasp:
            clasp = "No Clasp"

        clasp = clasp.replace(".", "")
        clasp = clasp.replace("  ", " ")
        clasp = clasp.title()

        if clasp not in (
            "Bronze",
            "Silver",
            "Silber",
            "Gold",
            "Großmeister",
            "Kommandeur",
            "Ritter",
            "Hochmeister",
            "Knappe",
            "No Clasp",
        ):
            skipped.append(
                {
                    "user": username,
                    "medal": current_medal,
                    "clasp": clasp,
                }
            )

            print(
                f"Skipping {username} ({current_medal}, {clasp})"
            )

            continue

        regiment = REGIMENT_MAP.get(
            regiment_tag,
            ""
        )

        rows.append(
            {
                "username": username,
                "regiment": regiment,
                "medal": current_medal,
                "clasp": clasp,
            }
        )

        print(
            f"Accepted: {username} | {current_medal} | {clasp}"
        )

    print("\n========== SUMMARY ==========")
    print(f"Accepted : {len(rows)}")
    print(f"Skipped  : {len(skipped)}")

    return rows, skipped
