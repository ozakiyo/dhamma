#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn015.json (思量経／推知の経) to match MN1–14 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E4%B8%AD%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E4%B8%AD%E9%83%A8%E7%B5%8C%E5%85%B8%E6%A0%B9%E6%9C%AC%E4%BA%94%E5%8D%81%E7%B5%8C%E7%AF%87%E4%B8%8A"
)
TB_URL = "https://true-buddhism.com/sutra/palisanzo/"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0571b29"
MAP_URL = "https://dhammarain.github.io/canon/sutta/M-vs-M-dhammarain.pdf"

LABEL_TO_ID = {
    "正見": "view",
    "正思惟": "intention",
    "正語": "speech",
    "正業": "action",
    "正命": "livelihood",
    "正精進": "effort",
    "正念": "mindfulness",
    "正定": "concentration",
}

QUOTES = {
    "MN15-P01": (
        "友よ、そこで、比丘は、まさしく、自己みずから、自己のことを、このように推知するべきです。"
        "『すなわち、まさに、この人物が、悪しき欲求ある者であり……この人物は、わたしにとって、愛しくない者であり、意に適わない者である。"
        "また、まさに……わたしが、悪しき欲求ある者として……存するなら、わたしもまた、他者たちにとって、愛しくない者として……存するであろう』と。"
    ),
    "MN15-P02": (
        "友よ、さらに、また、他に、比丘が、偽装ある者として、加虐ある者として、〔世に〕有ります。"
        "友よ、すなわち、また、比丘が、偽装ある者として、加虐ある者として、〔世に〕有るなら、これもまた、〔人を〕頑固に作り為す法（性質）です。"
    ),
    "MN15-P03": (
        "友よ、さらに、また、他に、比丘が、自己を賞揚し他者を蔑視する者として〔世に〕有ります。"
        "友よ、すなわち、また、比丘が、自己を賞揚し他者を蔑視する者として〔世に〕有るなら、これもまた、〔人を〕頑固に作り為す法（性質）です。"
    ),
    "MN15-P04": (
        "友よ、さらに、また、他に、比丘が、忿激する者として、忿激〔の思い〕に由縁する言葉を放つ者として、〔世に〕有ります。"
        "友よ、すなわち、また、比丘が、忿激する者として、忿激〔の思い〕に由縁する言葉を放つ者として、〔世に〕有るなら、これもまた、〔人を〕頑固に作り為す法（性質）です。"
    ),
    "MN15-P05": (
        "友よ、さらに、また、他に、比丘が、叱責者によって叱責され、叱責者に逆襲します。"
        "友よ、すなわち、また、比丘が、叱責者によって叱責され、叱責者に逆襲するなら、これもまた、〔人を〕頑固に作り為す法（性質）です。"
    ),
    "MN15-P06": (
        "友よ、もし、また、比丘が、『尊者たちは、わたしに説いてください。……』と申し出るとして、かつまた、彼が、素直で、諸々の〔人を〕素直に作り為す法（性質）を具備し、忍耐があり、〔他者の〕教示を上手に把握できる者として〔世に〕有るなら、"
        "……梵行を共にする者たちは……説くべき者と思い考え、かつまた、教示するべき者と思い考え、さらに、その人物にたいし、信頼を惹起するべき者と思い考えます。"
    ),
    "MN15-P07": (
        "友よ、それで、もし、比丘が、綿密に注視しながら、『まさに、〔わたしは〕悪しき欲求ある者として……存している』と、このように知るなら、"
        "友よ、その比丘は、まさしく、それらの悪しき善ならざる法（性質）の捨棄のために努力するべきです。"
    ),
    "MN15-P08": (
        "友よ、ここに、比丘が、悪しき欲求ある者として、諸々の悪しき欲求の支配に赴いた者として、〔世に〕有ります。"
        "……これもまた、〔人を〕頑固に作り為す法（性質）です。"
        "……彼のことを、梵行を共にする者たちは……説くべき者と思い考えず……信頼を惹起するべき者と思い考えません。"
    ),
    "MN15-P09": (
        "友よ、そこで、比丘は、まさしく、自己みずから、自己のことを、このように綿密に注視するべきです。"
        "『いったい、まさに、どうなのだろう、〔わたしは〕悪しき欲求ある者として……存しているのでは』と。"
        "……知るなら……悪しき善ならざる法（性質）の捨棄のために努力するべきです。"
        "……〔存していないと〕知るなら……喜悦と歓喜とともに〔世に〕住むべきです──諸々の善なる法（性質）において、昼夜に随学ある者として。"
    ),
    "MN15-P10": (
        "友よ、もし、また、比丘が……しかしながら、彼が、頑固で……忍耐がなく、〔他者の〕教示を上手に把握できない者として〔世に〕有るなら、"
        "……梵行を共にする者たちは……説くべき者と思い考えず……信頼を惹起するべき者と思い考えません。"
        "……忿激〔の思い〕に由縁する言葉を放つ者として〔世に〕有るなら、これもまた、〔人を〕頑固に作り為す法（性質）です。"
    ),
    "MN15-P11": (
        "友よ、では、どのようなものが、諸々の〔人を〕素直に作り為す法（性質）なのですか。"
        "友よ、ここに、比丘が、悪しき欲求ある者ではなく……自己を賞揚せず他者を蔑視しない者として……偽装なき者として……"
        "自らの見解に偏執せず、保持するものに執持せず、放棄し易き者として、〔世に〕有ります。"
        "……これもまた、〔人を〕素直に作り為す法（性質）です。"
    ),
}

OBSERVE = {
    "MN15-P01": (
        "推知——他者に嫌な性質を、自分が持てば同じように嫌われる。"
        "朝、今日「他者からどう見られるか」を一度意識する。"
    ),
    "MN15-P02": (
        "偽装・加虐は、人を頑固に作り為す法——"
        "ごまかしを一度止める。"
    ),
    "MN15-P03": (
        "自己を賞揚し他者を蔑視するのも、頑固に作り為す法——"
        "見下す衝動で一度止まる。"
    ),
    "MN15-P04": (
        "忿激に由縁する言葉は、頑固に作り為す法——"
        "鋭い言葉を一度和らげる。"
    ),
    "MN15-P05": (
        "叱責への逆襲は、頑固に作り為す法——"
        "反論したくなったとき、一度沈黙する。"
    ),
    "MN15-P06": (
        "素直で忍耐があり教示を把握できる者は、説かれ・信頼される——"
        "他者の良い点を一つ認める。"
    ),
    "MN15-P07": (
        "綿密に注視して悪法を知れば、捨棄のために努力する——"
        "恥ずべき行為を一つ認め、改める。"
    ),
    "MN15-P08": (
        "悪しき欲求の支配は頑固な法となり、梵行者は説かず信頼しない——"
        "他者の前で恥ずかしい行為を一度止める。"
    ),
    "MN15-P09": (
        "夜の綿密注視——悪法があれば捨棄に努め、なければ善法に随学し喜ぶ。"
        "今日の「誑·慢·利口·諍」を一つ認め、明日改める。"
    ),
    "MN15-P10": (
        "頑固で教示を把握できず、忿激の言葉を放つ者は信頼されない——"
        "話す前に「この言葉は信頼されるか」と一度止まる。"
    ),
    "MN15-P11": (
        "素直に作り為す法——悪欲なき・蔑視なき・偽装なき・放棄し易き。"
        "対人で一つの善い性質を意識する。"
    ),
}

PRACTICE = {
    "MN15-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、他者との接触でどう推知されるかを意識する",
        "section": "推知",
        "category": "mindfulness",
    },
    "MN15-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正業"],
        "reason": "偽装の欲しがりを見てごまかしを止める",
        "section": "偽装",
        "category": "intention",
    },
    "MN15-P03": {
        "nidanaId": "feeling",
        "pathFactors": ["正思惟", "正念"],
        "reason": "見下す受を見て蔑視に乗らない",
        "section": "賞揚·蔑視",
        "category": "intention",
    },
    "MN15-P04": {
        "nidanaId": "feeling",
        "pathFactors": ["正語", "正念"],
        "reason": "忿激の受から出る言葉を和らげる",
        "section": "忿激·語",
        "category": "speech",
    },
    "MN15-P05": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正業"],
        "reason": "正しさへの掴みとしての逆襲を沈黙で離す",
        "section": "逆襲",
        "category": "speech",
    },
    "MN15-P06": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "素直・忍耐へ向き、信頼を惹起する側に立つ",
        "section": "素直·信頼",
        "category": "effort",
    },
    "MN15-P07": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正見"],
        "reason": "悪法を認め捨棄のために努力する",
        "section": "捨棄·努力",
        "category": "effort",
    },
    "MN15-P08": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "悪欲の支配が信頼されない苦を招くと見る",
        "section": "悪欲·患",
        "category": "view",
    },
    "MN15-P09": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜に性質を綿密注視し、改めるか喜ぶかを分ける",
        "section": "綿密注視",
        "category": "mindfulness",
    },
    "MN15-P10": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正念"],
        "reason": "語る前に信頼されるかを問い、頑固な語の掴みを止める",
        "section": "語·信頼",
        "category": "speech",
    },
    "MN15-P11": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "素直に作り為す法を一つ選び、対人の鏡とする",
        "section": "素直な法",
        "category": "view",
    },
}

CHINESE = {
    "MN15-P01": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-anumana",
        "text": "諸賢！比丘者，當自思量。諸賢！若有人惡欲、念欲者，我不愛彼；若我惡欲、念欲者，彼亦不愛我。比丘如是觀，不行惡欲、不念欲者，當學如是。",
        "satLocus": "大正蔵 T1.571c 比丘請経",
        "note": "當自思量＝推知。",
    },
    "MN15-P02": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-maya",
        "text": "如是染行染、不語結住，欺誑諛諂，慳貪嫉妬……是謂戾語法。若有成就戾語法者，諸梵行者不語彼，不教、不訶而難彼人。",
        "satLocus": "大正蔵 T1.571c 比丘請経",
        "note": "欺誑諛諂＝偽装。戾語法＝頑固に作り為す法。",
    },
    "MN15-P03": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-avanna",
        "text": "訶比丘訶，訶比丘輕慢，訶比丘發露……是謂戾語法。",
        "satLocus": "大正蔵 T1.571c 比丘請経",
        "note": "訶比丘軽慢≈賞揚・蔑視の対人態度。",
    },
    "MN15-P04": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-kodha-vacana",
        "text": "瞋弊惡意，瞋恚語言……是謂戾語法。",
        "satLocus": "大正蔵 T1.571c 比丘請経",
        "note": "瞋恚語言＝忿激に由縁する言葉。",
    },
    "MN15-P05": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-patippharati",
        "text": "訶比丘訶……更互相避而說外事，不語、瞋恚、憎嫉熾盛……是謂戾語法。",
        "satLocus": "大正蔵 T1.571c 比丘請経",
        "note": "訶への反発・外事への転嫁＝逆襲・はぐらかし。",
    },
    "MN15-P06": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-sovacassa",
        "text": "諸賢！或有一人善語，成就善語法……諸梵行者善語彼，善教、善訶，不難彼人。……不欺誑諛諂……不無恩、不知恩……是謂善語法。",
        "satLocus": "大正蔵 T1.572a 比丘請経",
        "note": "善語法＝素直に作り為す法。",
    },
    "MN15-P07": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-pahana",
        "text": "諸賢！若比丘觀時，則知我是惡欲、念欲者，則不歡悅，便求欲斷。……猶有目人以鏡自照，則見其面淨及不淨。……見面有垢者，則不歡悅，便求欲洗。",
        "satLocus": "大正蔵 T1.572b 比丘請経",
        "note": "觀知→求欲断。鏡喩。",
    },
    "MN15-P08": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-papiccha",
        "text": "諸賢！或有一人惡欲、念欲。……若有人惡欲、念欲者，是謂戾語法。……令諸梵行者不語彼，不教、不訶而難彼人。",
        "satLocus": "大正蔵 T1.571c 比丘請経",
        "note": "悪欲・念欲＝悪しき欲求。",
    },
    "MN15-P09": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-paccavekkhana",
        "text": "諸賢！若比丘如是觀者，必多所饒益，我為惡欲、念欲，為不惡欲、念欲耶？……則知我是惡欲、念欲者，則不歡悅，便求欲斷。……則知我無惡欲、不念欲者，即便歡悅，我自清淨，求學尊法。",
        "satLocus": "大正蔵 T1.572a–b 比丘請経",
        "note": "自觀・断・歡悅＝綿密注視。",
    },
    "MN15-P10": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-vacana-saddha",
        "text": "成就戾語法故，令諸梵行者不語彼，不教、不訶而難彼人。……瞋恚語言……是謂戾語法。",
        "satLocus": "大正蔵 T1.571c 比丘請経",
        "note": "戾語ゆえ教え難く、瞋恚の語が信頼を損ねる。",
    },
    "MN15-P11": {
        "status": "mapped",
        "pin": "中阿含89・比丘請経（T26）",
        "t26": "T26-89-sovacassa-dhamma",
        "text": "諸賢！何者善語法？……不惡欲、不念欲……不欺誑諛諂……不瞋恚語言……不無恩、不知恩。……是謂諸善語法。若有成就善語法者，諸梵行者善語彼，善教、善訶，不難彼人。",
        "satLocus": "大正蔵 T1.572a 比丘請経",
        "note": "善語法の列挙＝素直に作り為す法。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部15経と中阿含89比丘請経の内容対応（對照表: 法雨道場）。",
        )
    return c


def rebuild_path_scene_for_mn(sutta_id, short, title, pairs):
    psi_path = DATA / "path-scene-index.json"
    psi = json.loads(psi_path.read_text(encoding="utf-8"))
    PATH_ORDER = list(LABEL_TO_ID.values())
    by_path = defaultdict(list)
    for p in pairs:
        for lab in p["pathFactors"]:
            by_path[LABEL_TO_ID[lab]].append(p["id"])
        by_path[p["category"]].append(p["id"])

    for pid in PATH_ORDER:
        ids = sorted(set(by_path[pid]), key=lambda x: int(x.split("-P")[1]))
        entries = [
            e for e in psi["entries"].setdefault(pid, [])
            if not (e.get("collectionId") == "majjhima" and e.get("chapterId") == sutta_id)
        ]
        if ids:
            entries.append({
                "collectionId": "majjhima",
                "collectionName": "中部",
                "chapterId": sutta_id,
                "shortTitle": short,
                "title": title,
                "pairCount": len(ids),
                "pairIds": ids,
            })
        psi["entries"][pid] = entries

    mns = set()
    for entries in psi["entries"].values():
        for e in entries:
            if e.get("collectionId") == "majjhima":
                mns.add(e["chapterId"])
    mns.add(sutta_id)
    mn_part = "+".join(f"mn{n}" for n in sorted(mns))
    psi["scope"] = f"dhammapada-ch1-ch26+majjhima-{mn_part}"

    psi_path.write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return psi["scope"]


def main():
    old_path = DATA / "majjhima" / "mn015.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN15-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 15",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー",
                    "locus": f"中部・推知の経（MN15）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 思量経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第15経・思量経（推知の経）"
    SHORT = "思量経（推知の経）"
    CATEGORIES = [
        {"id": "view", "name": "正見", "short": "正見", "weekday": 1, "order": 1},
        {"id": "intention", "name": "正思惟", "short": "思惟", "weekday": 2, "order": 2},
        {"id": "speech", "name": "正語", "short": "正語", "weekday": 3, "order": 3},
        {"id": "action", "name": "正業", "short": "正業", "weekday": 4, "order": 4},
        {"id": "livelihood", "name": "正命", "short": "正命", "weekday": 5, "order": 5},
        {"id": "effort", "name": "正精進", "short": "精進", "weekday": 6, "order": 6},
        {"id": "mindfulness", "name": "正念", "short": "正念", "weekday": 0, "order": 7},
        {"id": "concentration", "name": "正定", "short": "正定", "weekday": 0, "order": 8},
    ]

    nodes = [
        {
            "id": "contact", "weekday": 1, "categoryId": "mindfulness", "nidanaLabel": "接触",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "朝、他者との接触でどう推知されるかを意識する",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の対人の接触を変える",
            "toNext": "触のあと、見下しや忿激の受が見える",
            "todayObserve": OBSERVE["MN15-P01"],
            "todayAction": actions["MN15-P01"],
            "when": ["人と会う朝", "他者の目を思った"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN15-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN15-P08"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "intention", "nidanaLabel": "受ける",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "見下し・忿激の受を見て語と態度に乗らない",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、優劣や怒りの受が立つ",
            "toNext": "受に乗ると偽装や逆襲の欲しがりへ",
            "todayObserve": OBSERVE["MN15-P03"],
            "todayAction": actions["MN15-P03"],
            "when": ["見下したくなった", "忿激の言葉が出そう"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN15-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN15-P04"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正業"], "pathFactorIds": ["intention", "action"],
            "pathLabel": "偽装の欲しがりを見てごまかしを止める",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、隠したい欲しがりが立つ",
            "toNext": "止めないと正しさへの掴みへ",
            "todayObserve": OBSERVE["MN15-P02"],
            "todayAction": actions["MN15-P02"],
            "when": ["ごまかしそうになった", "嘘が浮かんだ"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN15-P02"][:40] + "…",
            "secondaryObserve": "欺誑諛諂",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正業"], "pathFactorIds": ["speech", "action"],
            "pathLabel": "逆襲と鋭い語の掴みを、沈黙と問い直しで離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、言い返す掴みが手前",
            "toNext": "掴むと信頼されない苦が見える",
            "todayObserve": OBSERVE["MN15-P05"],
            "todayAction": actions["MN15-P05"],
            "when": ["反論したくなった", "話す前に止まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN15-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN15-P10"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "悪欲の支配が、説かれず信頼されない苦を招くと見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、梵行者が遠ざかる患が見える",
            "toNext": "見れば、素直・捨棄の離しへ向き直る",
            "todayObserve": OBSERVE["MN15-P08"],
            "todayAction": actions["MN15-P08"],
            "when": ["恥が残った", "信頼を失いそう"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN15-P08"][:40] + "…",
            "secondaryObserve": "諸梵行者不語彼",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "素直・忍耐へ向き、悪法の捨棄に努力する",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、認める・改める・良い点を見る",
            "toNext": "離せば、夜の綿密注視へつながる",
            "todayObserve": OBSERVE["MN15-P06"],
            "todayAction": actions["MN15-P06"],
            "when": ["良い点を認めた", "悪法を改めた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN15-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN15-P07"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "綿密に注視し、素直な法を一つ選んで振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の性質は、朝からの推知の跡",
            "toNext": "見直しが、翌朝の対人接触の土台になる",
            "todayObserve": OBSERVE["MN15-P09"],
            "todayAction": actions["MN15-P09"],
            "when": ["一日を閉じるとき", "性質を鏡で見た日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN15-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN15-P11"],
        },
    ]

    out = {
        "chapter": 15,
        "sutta": 15,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：推知の経）",
        "suttas": ["MN 15 思量経（推知の経）"],
        "source": {
            "primary": "パーリ・中部第15経（思量経／推知の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含89比丘請経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・推知の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・比丘請経（T1.571b）",
                    "url": SAT_URL,
                    "note": "大目揵連説。對照表: 法雨道場（比丘講経表記）",
                },
            },
            "chineseMapTable": MAP_URL,
        },
        "categories": CATEGORIES,
        "practicePath": {
            "model": "dependent-origination-x-eightfold",
            "chapterTitle": TITLE,
            "shortTitle": SHORT,
            "spineOrigin": "触れた→感じた→欲しがった／拒んだ→掴んだ→苦が太った",
            "spinePath": "そこで気づき、見方・言葉・行い・努力で応える",
            "originNodes": [
                {"id": "contact", "label": "接触"},
                {"id": "feeling", "label": "受ける"},
                {"id": "craving", "label": "欲しがる"},
                {"id": "clinging", "label": "掴む"},
                {"id": "suffering", "label": "苦"},
                {"id": "release", "label": "離す"},
                {"id": "review", "label": "見直す"},
            ],
            "pathFactors": [
                {"id": "view", "label": "正見"}, {"id": "intention", "label": "正思惟"},
                {"id": "speech", "label": "正語"}, {"id": "action", "label": "正業"},
                {"id": "livelihood", "label": "正命"}, {"id": "effort", "label": "正精進"},
                {"id": "mindfulness", "label": "正念"}, {"id": "concentration", "label": "正定"},
            ],
            "nodes": nodes,
            "focusNodeId": "review",
            "focusReason": "推知の経は自己を推知し綿密に注視して悪法を捨て善法に随学するのが主題。既定の焦点は見直す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn015.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 15:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(15, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN15-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
