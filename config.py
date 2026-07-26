# in regiment map, you put the shortened tags of the regiments you're going to log medals for, then put their full name from the sheet. Example:

REGIMENT_MAP = {
    "MO": "Esercito Ducale di Modena",
    "Nr.16": 'NR.16 "Lusignan"',
    "NR.16": 'NR.16 "Lusignan"',
    "Nr.9": 'Nr.9 "Fürst Czartoryski"',
    "UH": "Kavallerie",
    "TFA": "Artillery",
    "V": "",
}

# in MEDAL_HEADER_MAP it's mostly the same thing. You go see the exact wording of the medals in the ceremony document, then put the names of the medals inside the google sheet. Example:

MEDAL_HEADER_MAP = {
    "AWARDED MEDAL OF EXCELLENCE":
        "Exzellenz Kampfkruiz",

    "AWARDED MEDAL OF VALOR":
        "Tapferkeit Verdienstmedaille",

    "AWARDED MEDAL OF BRAVERY":
        "Heldenmut Verdienstmedaille",

    "AWARDED CHAPLAIN'S MEDAL":
        "Kaplan Verdienstkruiz",

    "AWARDED FLAG-BEARER CROSS":
        "Fähnrich Kampfkruiz",

    "AWARDED FLAG-GUARD MEDAL":
        "Fahnenfeldweibel Verdienstmedaille",

    "AWARDED SOCIAL MEDAL":
        "Gesellschafts Verdienstmedaille",

    "AWARDED RECRUITER’S MEDAL":
        "Rekrutierungs Verdienstmedaille",

    "AWARDED FÜNFTES KORPS MEDAL":
        "Fünftes Korps Verdienststern",

    "GRENADIER KORP MEDALS":
        "Grenadier Korps Ehrenkruiz",
}

# When medals with higher clasps are given, you just manually change the clasp in the google sheet, so with this the algorithm will ignore people who got medals with clasps higher than bronze, except social medals which only have silver.

IGNORE_CLASPS = {
    "Gold",
    "Silver"
}

# Self explanatory no?

LOGGED_BY = "Cosmin_dEste"
