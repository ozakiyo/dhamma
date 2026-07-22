#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn042.json (鞞蘭若村婆羅門経／ヴェーランジャー村の婆羅門たちへの経).

実経: ヴェーランジャー（鞞蘭若）の婆羅門·在家者が舎衛城に滞在中、世尊に
死後の行き先を問う。教えの本体はMN41（薩羅村）と同文——十不善／十善業道。
生まれではなく行い（業）が趣を決める、という在俗の地図。
對照: 中阿含非収録。SC類縁は雑阿含1043（上文を「如上修多羅廣説」）。
"""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0273a28"
MAP_URL = "https://dhammarain.github.io/canon/sutta/M-vs-M-dhammarain.pdf"

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

QUOTES = {
    "MN42-P01": (
        "ヴェーランジャーの婆羅門·在家者が舎衛に滞在し、世尊に問う——"
        "『何の因で地獄に、何の因で天上に生まれるか』と。"
        "答えは行いによる——生まれの称号ではなく、非法·法の業が趣を決める。"
        "（朝、人を評価するとき「生まれ」より「行い」を先に見る。）"
    ),
    "MN42-P02": (
        "教えを誤って掴み、極端に走れば、自らを害する。"
        "十不善を離れ十善を修する道は、中道の行いであり、"
        "誤った修行の毒を取るものではない。"
        "（教えを極端に掴んでいないか、一度問う。）"
    ),
    "MN42-P03": (
        "非法·険しき行の核——身·語·意の不善。"
        "貪欲·瞋恚·愚痴、および慢·邪見など、心を汚すものを名づけ手放せ。"
        "（今日、五毒の一つを名づけ、手放す。）"
    ),
    "MN42-P04": (
        "真に尊ばれるのは、戒を守り善業を修する者——"
        "離殺生·離不与取·離欲邪行など、身の法行である。"
        "（今日、戒·約束の一つを確かに守る。）"
    ),
    "MN42-P05": (
        "語の法行——虚妄を離れ、両舌を離れ、粗悪·綺語を離れる。"
        "真実語·和合語を語る者が、語における正しき行者である。"
        "（今日、嘘·仲割れの言葉を止める。）"
    ),
    "MN42-P06": (
        "生まれにより「婆羅門」と呼ばれる者と、"
        "行いにより法行·正行する者とがある。"
        "世尊が尊ぶのは後者——行いが趣を開く。"
        "（人を見るとき、行いを先に評価する。）"
    ),
    "MN42-P07": (
        "邪見——『施しに果なし、業に果なし』と見ることを離れよ。"
        "正見は、布施·供養·善行に結果あり、未来の縁ありと知ること。"
        "（今日、善い行いに未来の縁があると一度認める。）"
    ),
    "MN42-P08": (
        "十不善業跡の因縁により、身壊命終して地獄·悪趣に生ずる。"
        "非法·険しき行は苦報の因である。"
        "（苦を感じたら、身語意の因を一つ辿る。）"
    ),
    "MN42-P09": (
        "法行·正行し戒清浄·心離欲なれば、"
        "五蓋を断じ、禅定·乃至諸果を願い得る——"
        "行いの先に定がある。"
        "（今日、五盖の一つを対治する。）"
    ),
    "MN42-P10": (
        "法行·正行により、漏尽智をも願い得る——"
        "煩悩の滅尽·心解脱·慧解脱への道は、まず不善を離れることにある。"
        "（執着を「漏」と名づけ、一つ手放す。）"
    ),
    "MN42-P11": (
        "ヴェーランジャーの婆羅門たちは教えを聞き、歓喜随喜して去った。"
        "行いの法を受けた者は、帰依の心をもって学びを行いに結ぶ。"
        "（学びを行いに結び、帰依の心を一度確認する。）"
    ),
    "MN42-P12": (
        "鞞蘭若村——行いの法行·正行こそ、真に尊ばれる道。"
        "生まれではなく、今日の身語意の行いを振り返る。"
        "（就寝前、今日の行いを「真の婆羅門の行」として振り返る。）"
    ),
}

OBSERVE = {
    "MN42-P01": (
        "鞞蘭若——生まれより行い。業が趣を決める。"
        "朝、人を評価するとき「生まれ」より「行い」を先に見る。"
    ),
    "MN42-P02": (
        "教えの極端な掴みは自らを害す——十善の中道へ。"
        "教えを極端に掴んでいないか、一度問う。"
    ),
    "MN42-P03": (
        "不善の核——貪·瞋·痴等を名づけ手放す。"
        "今日、五毒の一つを名づけ、手放す。"
    ),
    "MN42-P04": (
        "戒を守り善業を修する——身の法行。"
        "今日、戒・約束の一つを確かに守る。"
    ),
    "MN42-P05": (
        "真実語·和合語——嘘·仲割れを止める。"
        "今日、嘘・仲割れの言葉を止める。"
    ),
    "MN42-P06": (
        "行いの婆羅門を尊ぶ——人を見るとき行いを先に。"
        "人を見るとき、行いを先に評価する。"
    ),
    "MN42-P07": (
        "正見——善行に未来の縁あり。"
        "今日、善い行いに未来の縁があると一度認める。"
    ),
    "MN42-P08": (
        "不善業は悪趣の因——身語意の因を辿る。"
        "苦を感じたら、身語意の因を一つ辿る。"
    ),
    "MN42-P09": (
        "五蓋を対治し、定·果への道を開く。"
        "今日、五盖の一つを対治する。"
    ),
    "MN42-P10": (
        "漏尽への道——執着を漏と名づけ手放す。"
        "執着を「漏」と名づけ、一つ手放す。"
    ),
    "MN42-P11": (
        "歓喜随喜——学びを行いに結び帰依を確認する。"
        "学びを行いに結び、帰依の心を一度確認する。"
    ),
    "MN42-P12": (
        "結——行いの婆羅門として一日を振り返る。"
        "就寝前、今日の行いを「真の婆羅門の行」として振り返る。"
    ),
}

PRACTICE = {
    "MN42-P01": {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "朝、生まれより行いの教えに触れる", "section": "問い·行い", "category": "view"},
    "MN42-P02": {"nidanaId": "clinging", "pathFactors": ["正見", "正念"], "reason": "教えへの極端な掴みを問う", "section": "極端を離れる", "category": "view"},
    "MN42-P03": {"nidanaId": "craving", "pathFactors": ["正念", "正精進"], "reason": "貪瞋痴等の一つを名づけ手放す", "section": "不善の核", "category": "mindfulness"},
    "MN42-P04": {"nidanaId": "action", "pathFactors": ["正業", "正念"], "reason": "戒·約束の一つを確かに守る", "section": "身の戒", "category": "action"},
    "MN42-P05": {"nidanaId": "clinging", "pathFactors": ["正語", "正念"], "reason": "嘘·仲割れの言葉への掴みを止める", "section": "語の戒", "category": "speech"},
    "MN42-P06": {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "人を見るとき行いを先に評価する", "section": "行いを尊ぶ", "category": "view"},
    "MN42-P07": {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "邪見を離れ善行の縁を認める", "section": "正見", "category": "view"},
    "MN42-P08": {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "苦の因を身語意に一つ辿る", "section": "業報", "category": "view"},
    "MN42-P09": {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "五蓋の一つを対治する", "section": "五蓋·定", "category": "mindfulness"},
    "MN42-P10": {"nidanaId": "release", "pathFactors": ["正見", "正精進"], "reason": "執着を漏と名づけ一つ手放す", "section": "漏尽の方向", "category": "view"},
    "MN42-P11": {"nidanaId": "speech", "pathFactors": ["正見", "正念"], "reason": "学びを行いに結び帰依を確認する", "section": "帰依", "category": "view"},
    "MN42-P12": {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "夜、行いを真の婆羅門の行として振り返る", "section": "夜の振り返り", "category": "mindfulness"},
}

CHINESE = {
    "MN42-P01": {
        "status": "mapped", "pin": "雑阿含1043・鞞聞摩（T99）", "t26": "SA1043-ask",
        "text": "時，鞞羅磨聚落中，婆羅門長者……白佛言：「瞿曇！何因、何緣有人命終生地獄中，乃至生天？……」如上修多羅廣說。",
        "satLocus": "大正蔵 T2.273a–b 鞞聞摩", "note": "鞞羅磨（ヴェーランジャー系）の問い。内容は上文（SA1042）に同じ。", "satUrl": SAT_URL,
    },
    "MN42-P02": {
        "status": "unmapped", "pin": "（漢訳に直接対応なし）", "t26": "", "text": "",
        "satLocus": "對照表: 中阿含非収録。極端な掴みへの誡めは実践要約。", "note": "教えの誤掴み——アプリ用の実践対応。",
    },
    "MN42-P03": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-akusala",
        "text": "殺生，乃至邪見，具足十不善業因緣故。……是非法行、危嶮行……",
        "satLocus": "大正蔵 T2.272c（上文·類縁）", "note": "十不善。漢は略説。", "satUrl": "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18",
    },
    "MN42-P04": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-sila",
        "text": "謂離殺生，乃至正見，十善業跡因緣故……以法行、正行故，持戒清淨……",
        "satLocus": "大正蔵 T2.273a（上文·類縁）", "note": "十善·持戒清浄。", "satUrl": "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18",
    },
    "MN42-P05": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-vac",
        "text": "（十善——離妄語等を含む。漢は「離殺生乃至正見」と略す。）",
        "satLocus": "大正蔵 T2.273a（上文·類縁）", "note": "語の善業。パーリMN41/42詳説。", "satUrl": "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18",
    },
    "MN42-P06": {
        "status": "mapped", "pin": "雑阿含1043・鞞聞摩（T99）／類縁", "t26": "SA1043-conduct",
        "text": "（趣は非法行／法行による——生まれの称号ではなく行い。上文の業説を受ける。）",
        "satLocus": "大正蔵 T2.273a–b 鞞聞摩（類縁）", "note": "行いによる趣。", "satUrl": SAT_URL,
    },
    "MN42-P07": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-view",
        "text": "殺生，乃至邪見……謂離殺生，乃至正見，十善業跡……",
        "satLocus": "大正蔵 T2.272c–273a（上文·類縁）", "note": "邪見／正見。", "satUrl": "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18",
    },
    "MN42-P08": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-hell",
        "text": "行非法行、行危嶮行因緣故，身壞命終，生地獄中。",
        "satLocus": "大正蔵 T2.272c（上文·類縁）", "note": "非法行→地獄。", "satUrl": "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18",
    },
    "MN42-P09": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-jhana",
        "text": "欲求離欲、惡不善法……乃至第四禪具足住，悉得成就。……以彼法行、正行故，持戒清淨，心離愛欲……",
        "satLocus": "大正蔵 T2.273a（上文·類縁）", "note": "法行·持戒·離欲→禅。", "satUrl": "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18",
    },
    "MN42-P10": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-asava",
        "text": "欲求斷三結……漏盡智皆悉得。……以法行、正行故，持戒、離欲，所願必得。",
        "satLocus": "大正蔵 T2.273a（上文·類縁）", "note": "漏尽智への願い。", "satUrl": "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18",
    },
    "MN42-P11": {
        "status": "mapped", "pin": "雑阿含1043・鞞聞摩（T99）", "t26": "SA1043-rejoice",
        "text": "時，鞞羅磨婆羅門聞佛所說，歡喜隨喜，從坐起而去。",
        "satLocus": "大正蔵 T2.273b 鞞聞摩", "note": "歓喜随喜して去る。", "satUrl": SAT_URL,
    },
    "MN42-P12": {
        "status": "mapped", "pin": "雑阿含1043・鞞聞摩（T99）／類縁", "t26": "SA1043-close",
        "text": "（法行·正行を聞いて随喜——行いの道として一日を閉じる実践根拠。）",
        "satLocus": "大正蔵 T2.273b 鞞聞摩（類縁）", "note": "行いの振り返り。", "satUrl": SAT_URL,
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c.setdefault("satUrl", SAT_URL)
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部42経は中阿含非収録。SC類縁SA1043（内容はSA1042＝十業道の廣説に同じ）。本体はMN41と同文。",
        )
    else:
        c.setdefault("note", "對照表は中阿含非収録。このペアは実践要約。")
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
                "collectionId": "majjhima", "collectionName": "中部",
                "chapterId": sutta_id, "shortTitle": short, "title": title,
                "pairCount": len(ids), "pairIds": ids,
            })
        psi["entries"][pid] = entries
    mns = {e["chapterId"] for entries in psi["entries"].values() for e in entries if e.get("collectionId") == "majjhima"}
    mns.add(sutta_id)
    psi["scope"] = "dhammapada-ch1-ch26+majjhima-" + "+".join(f"mn{n}" for n in sorted(mns))
    psi_path.write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return psi["scope"]


def main():
    PRACTICE["MN42-P04"]["nidanaId"] = "clinging"
    PRACTICE["MN42-P11"]["nidanaId"] = "contact"

    old_path = DATA / "majjhima" / "mn042.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 13):
        pid = f"MN42-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid, "category": pr["category"], "ref": "MN 42", "section": pr["section"],
            "observe": OBSERVE[pid], "action": actions[pid], "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"], "pathFactors": pr["pathFactors"], "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・ヴェーランジャー村の婆羅門たちへの経／パーリMN42）",
                    "locus": f"中部・ヴェーランジャー村の婆羅門たちへの経（MN42）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 鞞蘭若村婆羅門経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第42経・鞞蘭若村婆羅門経（ヴェーランジャー村の婆羅門たちへの経）"
    SHORT = "鞞蘭若村婆羅門経（ヴェーランジャー村の婆羅門たちへの経）"
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
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "生まれより行いの教えに触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の行いの一歩を変える",
            "toNext": "触のあと、蓋の受が見える",
            "todayObserve": OBSERVE["MN42-P01"], "todayAction": actions["MN42-P01"],
            "when": ["行いを先に見た", "帰依を確認した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN42-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN42-P06"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "五蓋を対治する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、蓋の受が立つ",
            "toNext": "蓋に乗ると不善の欲しがりへ",
            "todayObserve": OBSERVE["MN42-P09"], "todayAction": actions["MN42-P09"],
            "when": ["五蓋を対治した"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN42-P09"][:40] + "…",
            "secondaryObserve": "定への道を開く",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "貪瞋痴等の一つを名づけ手放す",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、不善の欲しがりが立つ",
            "toNext": "止めないと極端·不善への掴みへ",
            "todayObserve": OBSERVE["MN42-P03"], "todayAction": actions["MN42-P03"],
            "when": ["五毒を手放した"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN42-P03"][:40] + "…",
            "secondaryObserve": "不善の核を名づける",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "action", "nidanaLabel": "掴む",
            "pathFactors": ["正業", "正語"], "pathFactorIds": ["action", "speech"],
            "pathLabel": "極端·不善語·戒破への掴みを止める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、掴みが手前",
            "toNext": "掴むと業報の苦が見える",
            "todayObserve": OBSERVE["MN42-P02"], "todayAction": actions["MN42-P02"],
            "when": ["極端を問うた", "戒を守った", "嘘を止めた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN42-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN42-P05"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "不善業の苦報を見て因を辿る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、業報の苦が見える",
            "toNext": "見れば、正見·漏尽へ離す",
            "todayObserve": OBSERVE["MN42-P08"], "todayAction": actions["MN42-P08"],
            "when": ["因を辿った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN42-P08"][:40] + "…",
            "secondaryObserve": "非法行は悪趣の因",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "邪見·漏を離れ、善行の縁を認める",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、邪見·執着を離す",
            "toNext": "離せば、夜の振り返りへ",
            "todayObserve": OBSERVE["MN42-P07"], "todayAction": actions["MN42-P07"],
            "when": ["縁を認めた", "漏を手放した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN42-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN42-P10"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "行いを真の婆羅門の行として振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの行いの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN42-P12"], "todayAction": actions["MN42-P12"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN42-P12"][:40] + "…",
            "secondaryObserve": "生まれではなく行いを振り返る",
        },
    ]

    out = {
        "chapter": 42, "sutta": 42, "title": TITLE, "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双小品（アラナ：ヴェーランジャー村の婆羅門たちへの経）",
        "suttas": ["MN 42 鞞蘭若村婆羅門経（ヴェーランジャー村の婆羅門たちへの経）"],
        "source": {
            "primary": "パーリ・中部第42経（鞞蘭若村婆羅門経／ヴェーランジャー村の婆羅門たちへの経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN42（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝中阿含非収録；SC類縁は雑阿含1043"
                "（内容はSA1042の十業道廣説に同じ。パーリはMN41と同文で聴衆のみ異なる）。"
                "生まれではなく行い（十不善／十善）が趣を決めるのが主題。"
            ),
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（中部・ヴェーランジャー村の婆羅門たちへの経）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（南伝大蔵経・第9巻中部経典一）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 雑阿含・鞞聞摩（T2.273a）／類縁", "url": SAT_URL, "note": "對照表: 中阿含非収録。SC類縁SA1043"},
            },
            "chineseMapTable": MAP_URL,
        },
        "categories": CATEGORIES,
        "practicePath": {
            "model": "dependent-origination-x-eightfold",
            "chapterTitle": TITLE, "shortTitle": SHORT,
            "spineOrigin": "触れた→感じた→欲しがった／拒んだ→掴んだ→苦が太った",
            "spinePath": "そこで気づき、見方・言葉・行い・努力で応える",
            "originNodes": [
                {"id": "contact", "label": "接触"}, {"id": "feeling", "label": "受ける"},
                {"id": "craving", "label": "欲しがる"}, {"id": "clinging", "label": "掴む"},
                {"id": "suffering", "label": "苦"}, {"id": "release", "label": "離す"},
                {"id": "review", "label": "見直す"},
            ],
            "pathFactors": [
                {"id": "view", "label": "正見"}, {"id": "intention", "label": "正思惟"},
                {"id": "speech", "label": "正語"}, {"id": "action", "label": "正業"},
                {"id": "livelihood", "label": "正命"}, {"id": "effort", "label": "正精進"},
                {"id": "mindfulness", "label": "正念"}, {"id": "concentration", "label": "正定"},
            ],
            "nodes": nodes,
            "focusNodeId": "release",
            "focusReason": "鞞蘭若村婆羅門経は生まれを離れ行い（十善）へ向かうのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn042.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 42:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(42, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 12
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    missing = valid - set(by_nidana)
    assert not missing, missing
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] != "mapped"]
    print(f"OK chinese mapped {mapped}/12; unmapped {unmapped}; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
