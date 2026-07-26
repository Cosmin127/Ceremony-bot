# in regiment map, you put the shortened tags of the regiments you're going to log medals for, then put their full name from the sheet. Example:

REGIMENT_MAP = {
    "MO": "Esercito Ducale di Modena",
    "Nr.16": 'NR.16 "Lusignan"',
    "NR.16": 'NR.16 "Lusignan"',
    "Nr.9": 'Nr.9 "Fürst Czartoryski"',
    "UH": "Kavallerie",
    "TFA": "Artillery",
    "V": "",
    "AG": "Alte Grenadiere",
    "JG": "Junge Grenadiere",
    "MG": "Alte Grenadière",
    "GS": "",
    "GR": "Grenz Infanterie",
    "UH": "Kaiserliche Husaren",
    "RH": "Kaiserliche Ulanen",
    "LG": "Kaiserliche Leibgarde",
    "NR.4": 'NR.4 "Deutschmeister"',
    "NR.1": 'NR.1 "Kaiser Franz"',
    "WUR": "Kurfürstentum Württemberg",
    "ARTY": "Artillery",
    "NR.59": 'NR.59 "Jordis"',
    "LEK": "Legion Erzherzog Karl",
    "NR.25": 'NR.25 "Graf Sporck"',
    "TR": "Trieste Freikorps",
    "NR.38": 'NR.38 "Freiherr von Prohaska"',
    "NR.49": 'NR.49 "von Kerpen"',
    "IF": "Artillery",
    
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
    "AWARDED ORDER OF THE GOLDEN FLEECE": "Ordn des Goldenen Vlies",
}

# When medals with higher clasps are given, you just manually change the clasp in the google sheet, so with this the algorithm will ignore people who got medals with clasps higher than bronze, except social medals which only have silver.

IGNORE_CLASPS = {
    "Gold",
    "Silver"
}

# Self explanatory no?

LOGGED_BY = "Cosmin_dEste"
