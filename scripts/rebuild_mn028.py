#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn028.json (象跡喩大経／象跡の喩えの大経) to match MN1–27 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0464b01"
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
    "MN28-P01": (
        "諸賢よ、歩行する一切の生き物の足跡は、象の足跡に含むされる。"
        "ゆえに、象の足跡は、その中で最勝と称される。"
        "このように、一切の善い法は、四聖諦に含むされる。"
        "……苦の聖諦、苦の集の聖諦、苦の滅の聖諦、苦の滅へ至る道の聖諦である。"
    ),
    "MN28-P02": (
        "何が、苦の聖諦であるか。"
        "生は苦、老は苦、死は苦、愁·悲·苦·憂·悩は苦、求めて得ざるは苦である。"
        "要約すれば、五取蘊は苦である。"
    ),
    "MN28-P03": (
        "この五取蘊に対する欲·愛著·随貪·執着が、苦の集である。"
    ),
    "MN28-P04": (
        "「これは、わたしのものではない。これは、わたしではない。これは、わたしの我ではない」——"
        "このように、あるがままに正慧をもって見るべし。"
        "（内·外の地界は、ただ地界である。——水·火·風界も同様。）"
    ),
    "MN28-P05": (
        "この五取蘊に対する欲と貪欲を捨て、捨て去ることが、苦の滅である。"
    ),
    "MN28-P06": (
        "……苦の滅へ至る道の聖諦——"
        "一切の善い法は四聖諦に含むされるがゆえに、道諦もまた象跡の中に収まる。"
        "（本経は道支の列挙より、四大·五取蘊·縁起の観を展開する。）"
    ),
    "MN28-P07": (
        "舎利弗は、比丘たちに告げた——"
        "「諸賢よ、……一切の善い法は、四聖諦に含むされる」と。"
        "……略して五取蘊は苦である。"
    ),
    "MN28-P08": (
        "「縁起を見る者は、法を見る。法を見る者は、縁起を見る。」"
        "そして、この五取蘊は、まことに縁起して生じたものである。"
    ),
    "MN28-P09": (
        "このようにして、これら五取蘊への含む·集合·結合がある——"
        "眼が内に健全で、外の色が範囲に入り、相応の作意があるとき、"
        "相応の識が現れる。……色·受·想·行·識は、各々の取蘊に属する。"
    ),
    "MN28-P10": (
        "一切の善い法は、四聖諦に含むされる——"
        "象の足跡が一切の足跡を含むように。"
        "縁起を見る者は法を見る。……五取蘊は縁起して生じたものである。"
    ),
}

OBSERVE = {
    "MN28-P01": (
        "歩行する生き物の足跡は象跡に収まり、象跡が最勝——"
        "同様に、一切の善い法は四聖諦に含むされる。"
        "今日の判断を、苦·集·滅·道のどれに当たるか照らす。"
    ),
    "MN28-P02": (
        "苦の聖諦——生·老·死·愁悲苦憂悩·求不得、要約すれば五取蘊は苦。"
        "一つの苦について「これが苦」と静かに認める。"
    ),
    "MN28-P03": (
        "苦の集——五取蘊への欲·愛著·随貪·執着。"
        "一つの苦について、原因（集）を一つ考える。"
    ),
    "MN28-P04": (
        "地·水·火·風——内外ともにただその界。「私のものではない·私ではない·私の我ではない」と正慧に見る。"
        "身体への執着が来たら、地界一つに「私にではない」と見る。"
    ),
    "MN28-P05": (
        "苦の滅——五取蘊への欲と貪欲を捨て去る。"
        "快楽·不快の後に、執着（愛·取）が生じていないか観察する。"
    ),
    "MN28-P06": (
        "苦の滅へ至る道の聖諦も四諦に含むされる——"
        "今日、正しい見から正しい定まで、八正道の一つを意識する。"
    ),
    "MN28-P07": (
        "舎利弗が比丘たちに象跡の喩えを説く——四諦の総括。"
        "今日学んだ一節を、誰かと静かに分かち合う。"
    ),
    "MN28-P08": (
        "縁起を見る者は法を見る——五取蘊は縁起して生じたもの。"
        "執着が来たら「縁起の一環」と一つ名づける。"
    ),
    "MN28-P09": (
        "根·境·作意が揃うとき識が現れ、色·受·想·行·識が五取蘊へ含む·集合·結合される。"
        "今日触れた対象一つを「含む·集合·結合された蘊」と見る。"
    ),
    "MN28-P10": (
        "四諦を正しく語れば、一切の有用な法を語る——象跡のように。"
        "今日、因果を単純化せず、四諦·縁起として語る。"
    ),
}

PRACTICE = {
    "MN28-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "判断に触れ、四諦のどれに当たるか照らす",
        "section": "象跡·四聖諦",
        "category": "view",
    },
    "MN28-P02": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "一つの苦を「これが苦」と認める",
        "section": "苦諦·五取蘊",
        "category": "view",
    },
    "MN28-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "苦の集として、五取蘊への欲しがりを一つ考える",
        "section": "集諦",
        "category": "intention",
    },
    "MN28-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "身体への掴みを、地界に「私にではない」と見る",
        "section": "四大·無我",
        "category": "view",
    },
    "MN28-P05": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "快楽·不快の後の愛·取を見て、欲しがりを離す",
        "section": "滅諦",
        "category": "effort",
    },
    "MN28-P06": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "道諦として八正道の一つを意識し、離す方向へ進む",
        "section": "道諦",
        "category": "view",
    },
    "MN28-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正念"],
        "reason": "学んだ一節を分かち合い、法に触れる",
        "section": "舎利弗の説示",
        "category": "speech",
    },
    "MN28-P08": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "執着の受を「縁起の一環」と名づける",
        "section": "縁起を見る",
        "category": "view",
    },
    "MN28-P09": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "触れた対象を五取蘊への含む·集合として見る",
        "section": "五取蘊の合会",
        "category": "view",
    },
    "MN28-P10": {
        "nidanaId": "review",
        "pathFactors": ["正語", "正見"],
        "reason": "一日の因果を四諦·縁起として語り直す",
        "section": "四諦·縁起として語る",
        "category": "speech",
    },
}

CHINESE = {
    "MN28-P01": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-footprint",
        "text": (
            "無量善法，彼一切法皆四聖諦所攝，來入四聖諦中……。"
            "猶如諸畜之跡，象跡為第一……。云何為四？謂苦聖諦，苦習、苦滅、苦滅道聖諦。"
        ),
        "satLocus": "大正蔵 T1.464b 象跡喻経",
        "note": "象跡第一＝四聖諦が一切善法を摂する。",
    },
    "MN28-P02": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-dukkha",
        "text": "云何苦聖諦？謂生苦、老苦、病苦、死苦、怨憎會苦、愛別離苦、所求不得苦、略五盛陰苦。",
        "satLocus": "大正蔵 T1.464b–c 象跡喻経",
        "note": "略五盛陰苦＝要約すれば五取蘊は苦。",
    },
    "MN28-P03": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-samudaya",
        "text": (
            "（パーリは五取蘊への欲·愛著·随貪·執着を苦の集とする。"
            "漢訳は結で五盛陰を厭し無欲へ至る流れで対応。）"
        ),
        "satLocus": "大正蔵 T1.467a 象跡喻経",
        "note": "集諦の明示はパーリが詳しい。漢は厭·無欲の側で対応。",
    },
    "MN28-P04": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-not-mine",
        "text": (
            "云何四大？謂地界，水、火、風界。……"
            "多聞聖弟子不作此念：『是我，是我所，我是彼所。』"
        ),
        "satLocus": "大正蔵 T1.464c 象跡喻経",
        "note": "不作是我·我所＝パーリの「私のものではない」観に対応。",
    },
    "MN28-P05": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-nirodha",
        "text": "彼厭此過去、未來、現在五盛陰，厭已便無欲，無欲已便解脫……。",
        "satLocus": "大正蔵 T1.467a 象跡喻経",
        "note": "厭·無欲＝パーリの欲·貪欲を捨て去る滅諦に近い。",
    },
    "MN28-P06": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-magga",
        "text": "云何為四？謂苦聖諦，苦習、苦滅、苦滅道聖諦。",
        "satLocus": "大正蔵 T1.464b 象跡喻経",
        "note": "道諦は四諦列挙で明示。八支の詳細列挙は本経の主展開ではない。",
    },
    "MN28-P07": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-sariputta",
        "text": "尊者舍梨子……告諸比丘：「諸賢！……無量善法，彼一切法皆四聖諦所攝……。」",
        "satLocus": "大正蔵 T1.464b 象跡喻経",
        "note": "舍梨子が比丘に説く。",
    },
    "MN28-P08": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-do",
        "text": "世尊亦如是說：『若見緣起便見法，若見法便見緣起。』……世尊說五盛陰從因緣生。",
        "satLocus": "大正蔵 T1.467a 象跡喻経",
        "note": "見緣起便見法——パーリと同文脈。",
    },
    "MN28-P09": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-aggregates",
        "text": (
            "內意處及法，意識知外色法，是屬色陰。"
            "若有覺是覺陰……如是觀陰合會。"
        ),
        "satLocus": "大正蔵 T1.467a 象跡喻経",
        "note": "陰合会＝五取蘊への含む·集合。",
    },
    "MN28-P10": {
        "status": "mapped",
        "pin": "中阿含30・象跡喻経（T26）",
        "t26": "T26-30-speak",
        "text": (
            "無量善法……皆四聖諦所攝……象跡為第一。"
            "若見緣起便見法，若見法便見緣起。"
        ),
        "satLocus": "大正蔵 T1.464b·467a 象跡喻経",
        "note": "四諦·縁起として語る根拠。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部28経と中阿含30象跡喻経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn028.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 11):
        pid = f"MN28-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 28",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・象跡の喩えの大経／パーリMN28）",
                    "locus": f"中部・象跡の喩えの大経（MN28）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 象跡喩大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第28経・象跡喩大経（象跡の喩えの大経）"
    SHORT = "象跡喩大経（象跡の喩えの大経）"
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
            "id": "contact", "weekday": 1, "categoryId": "view", "nidanaLabel": "接触",
            "pathFactors": ["正見", "正語"], "pathFactorIds": ["view", "speech"],
            "pathLabel": "判断·法に触れ、四諦で照らす·分かち合う",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の四諦の当て方を変える",
            "toNext": "触のあと、縁起の受が見える",
            "todayObserve": OBSERVE["MN28-P01"],
            "todayAction": actions["MN28-P01"],
            "when": ["判断を四諦に照らした", "一節を分かち合った"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN28-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN28-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "執着の受を縁起の一環と名づける",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、掴みそうな受が立つ",
            "toNext": "受に乗ると五取蘊への欲しがりへ",
            "todayObserve": OBSERVE["MN28-P08"],
            "todayAction": actions["MN28-P08"],
            "when": ["縁起の一環と名づけた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN28-P08"][:40] + "…",
            "secondaryObserve": "見緣起者見法",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "苦の集として、五取蘊への欲しがりを考える",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、欲·愛著が立つ",
            "toNext": "止めないと身体·蘊の掴みへ",
            "todayObserve": OBSERVE["MN28-P03"],
            "todayAction": actions["MN28-P03"],
            "when": ["集を一つ考えた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN28-P03"][:40] + "…",
            "secondaryObserve": "五取蘊への欲·愛著",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "地界に「私にではない」と見、対象を蘊の合会と見る",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、身体·対象の掴みが手前",
            "toNext": "掴むと五取蘊の苦が見える",
            "todayObserve": OBSERVE["MN28-P04"],
            "todayAction": actions["MN28-P04"],
            "when": ["地界に非我所と見た", "対象を蘊と見た"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN28-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN28-P09"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "要約すれば五取蘊は苦——これが苦と認める",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、五取蘊の苦が見える",
            "toNext": "見れば、滅·道へ離す",
            "todayObserve": OBSERVE["MN28-P02"],
            "todayAction": actions["MN28-P02"],
            "when": ["これが苦と認めた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN28-P02"][:40] + "…",
            "secondaryObserve": "略五盛陰苦",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "欲·貪欲を捨て、道諦の一支を意識して離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、愛·取を見て離す",
            "toNext": "離せば、四諦·縁起としての見直しへ",
            "todayObserve": OBSERVE["MN28-P05"],
            "todayAction": actions["MN28-P05"],
            "when": ["愛·取を観察した", "八正道の一つを意識した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN28-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN28-P06"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "speech", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正語", "正見"], "pathFactorIds": ["speech", "view"],
            "pathLabel": "一日の因果を四諦·縁起として語り直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの四諦の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN28-P10"],
            "todayAction": actions["MN28-P10"],
            "when": ["一日を閉じるとき", "四諦·縁起として語った夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN28-P10"][:40] + "…",
            "secondaryObserve": "象跡·四聖諦",
        },
    ]

    out = {
        "chapter": 28,
        "sutta": 28,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：象跡の喩えの大経）",
        "suttas": ["MN 28 象跡喩大経（象跡の喩えの大経）"],
        "source": {
            "primary": "パーリ・中部第28経（象跡喩大経／象跡の喩えの大経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN28（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含30象跡喻経（T26）。"
                "一切の善い法は四聖諦に含むされ、五取蘊·四大·縁起が象跡として展開される。"
                "（MN27の漸次道·漏尽結論とは別系統の舎利弗説示。）"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・象跡の喩えの大経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・象跡喻経（T1.464b）",
                    "url": SAT_URL,
                    "note": "四聖諦·五盛陰·四大·見緣起。對照表: 法雨道場（中阿含30）",
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
            "focusNodeId": "suffering",
            "focusReason": "象跡喩大経は一切の善い法が四聖諦に含むされ、要約すれば五取蘊は苦と説くのが主題。既定の焦点は苦。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn028.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 28:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(28, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 10
    assert all(p["id"] == f"MN28-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/10; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
