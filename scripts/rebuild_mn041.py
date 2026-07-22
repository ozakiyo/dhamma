#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn041.json (薩羅村婆羅門経／サーラー村の婆羅門たちへの経).

実経: サーラー（薩羅）村の婆羅門·在家者が死後の行き先を問う。
世尊は非法·険しき行により地獄等へ、法·正しき行により天上·善趣へ至ると説く。
十不善業道（身3·語4·意3）と十善業道を詳説し、在俗の未来を開く業の地図を示す。
對照: 中阿含非収録。SC類縁は雑阿含1042·1043（十不善／十善業跡）。
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0272c18"
SAT_1043 = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0273a28"
MAP_URL = "https://dhammarain.github.io/canon/sutta/M-vs-M-dhammarain.pdf"

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

QUOTES = {
    "MN41-P01": (
        "サーラー村の婆羅門·在家者が問う——"
        "『何の因·縁で、衆生は身壊命終して地獄に生まれ、何の因で天上に生まれるか』と。"
        "世尊は答える——非法·険しき行のゆえに悪趣へ、法·正しき行のゆえに善趣へ、と。"
        "（朝、今日の行いが「未来を作る業」だと一度確認する。）"
    ),
    "MN41-P02": (
        "法行·正行——離殺生乃至正見、十善業跡の因縁により、"
        "身壊命終して天上に生まれ、また望む善い家·諸天にも往生し得る。"
        "（今日、身語意の一つを「正しい行い」に結びつける。）"
    ),
    "MN41-P03": (
        "身の三不善——殺生、不与取、欲邪行。"
        "殺生する者は、血に手を染め、無慈悲にして生き物を害する——"
        "これ、身において非法·険しき行である。"
        "（今日、他者の生命·所有·関係を害さないよう一つ意識する。）"
    ),
    "MN41-P04": (
        "不与取——与えられていないものを、盗み心をもって取る。"
        "在俗の戒の根本の一つである。"
        "（今日、得たものの出所を一度問い、不正を避ける。）"
    ),
    "MN41-P05": (
        "欲邪行——母·父·兄弟·姉妹·法によって護られた者など、"
        "守られるべき者のもとへ行く。——他者を守る縁を破る。"
        "（今日、誘惑の前に「守られた関係」を思い出す。）"
    ),
    "MN41-P06": (
        "語の四不善——虚妄語、両舌、粗悪語、綺語。"
        "見ていないのに見たと言い、知らないのに知ったと言う——"
        "虚妄は語における非法である。"
        "（今日、事実でないこと·仲を裂く言葉を一度止める。）"
    ),
    "MN41-P07": (
        "両舌——ここまで聞いてあちらで分裂させ、あちらまで聞いてここで分裂させる。"
        "和合している者を離れさせ、離れている者を喜ぶ。"
        "（今日、噂·伝言で人を分断しない。）"
    ),
    "MN41-P08": (
        "粗悪語——あらあらしく、耳に逆らい、怒りを伴い、"
        "他者の心を傷つける言葉。——恨みを他者に向ける。"
        "（強い言葉の前に、一度呼吸を置く。）"
    ),
    "MN41-P09": (
        "綺語——時機に合わず、実義·法·律にかなわず、"
        "無益·無根の雑談。——涅槃へ導かないむだな語。"
        "（今日、無益な雑談·煽りの言葉を一つ減らす。）"
    ),
    "MN41-P10": (
        "意の三不善——貪欲、瞋恚、邪見。"
        "他者の財を欲し「あれが私のものであれば」と思う——"
        "貪欲は意における非法である。"
        "（今日、他者の所有を「私のもの」と欲する心を一度見る。）"
    ),
    "MN41-P11": (
        "瞋恚·害意——『この者を打ち殺せ、滅ぼせ』と、"
        "他者の幸せを損ないたい思い。"
        "（怒りの中で、他者の幸せを願う思いを一つ置く。）"
    ),
    "MN41-P12": (
        "邪見——『施しに果なし、大施に果なし、善悪業に果なし』と見る。"
        "正見は、業に果あり、善行に未来の縁ありと知ること。"
        "（今日、善い行いに未来の縁があると一度認める。）"
    ),
    "MN41-P13": (
        "十善業跡を行ずる者は、善趣·天上へ至り、"
        "また戒清浄·離欲により禅·果まで願い得る——"
        "在俗の未来を開く業の地図である。"
        "（就寝前、今日の身語意を「法に沿った行い・正しい行い」として一つ振り返る。）"
    ),
}

OBSERVE = {
    "MN41-P01": (
        "薩羅村——死後の行き先を問う。業が未来を作る。"
        "朝、今日の行いが「未来を作る業」だと一度確認する。"
    ),
    "MN41-P02": (
        "法行·正行——十善により善趣·天上へ。"
        "今日、身語意の一つを「正しい行い」に結びつける。"
    ),
    "MN41-P03": (
        "身の三不善——殺生を離れ、生命を害さない。"
        "今日、他者の生命・所有・関係を害さないよう一つ意識する。"
    ),
    "MN41-P04": (
        "不与取——出所を問い、不正を避ける。"
        "今日、得たものの出所を一度問い、不正を避ける。"
    ),
    "MN41-P05": (
        "欲邪行——守られた関係を破らない。"
        "今日、誘惑の前に「守られた関係」を思い出す。"
    ),
    "MN41-P06": (
        "虚妄語——事実でないことを一度止める。"
        "今日、事実でないこと・仲を裂く言葉を一度止める。"
    ),
    "MN41-P07": (
        "両舌——噂·伝言で分断しない。"
        "今日、噂・伝言で人を分断しない。"
    ),
    "MN41-P08": (
        "粗悪語——強い言葉の前に呼吸を置く。"
        "強い言葉の前に、一度呼吸を置く。"
    ),
    "MN41-P09": (
        "綺語——無益な雑談·煽りを一つ減らす。"
        "今日、無益な雑談・煽りの言葉を一つ減らす。"
    ),
    "MN41-P10": (
        "貪欲——「私のもの」と欲する心を一度見る。"
        "今日、他者の所有を「私のもの」と欲する心を一度見る。"
    ),
    "MN41-P11": (
        "瞋恚——怒りの中で他者の幸せを願う。"
        "怒りの中で、他者の幸せを願う思いを一つ置く。"
    ),
    "MN41-P12": (
        "邪見を離れ——善行に未来の縁があると認める。"
        "今日、善い行いに未来の縁があると一度認める。"
    ),
    "MN41-P13": (
        "総括——身語意を法行·正行として振り返る。"
        "就寝前、今日の身語意を「法に沿った行い・正しい行い」として一つ振り返る。"
    ),
}

PRACTICE = {
    "MN41-P01": {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "朝、業が未来を作る教えに触れる", "section": "業の問い", "category": "view"},
    "MN41-P02": {"nidanaId": "release", "pathFactors": ["正業", "正見"], "reason": "身語意の一つを正しい行いに結びつける", "section": "法行·正行", "category": "action"},
    "MN41-P03": {"nidanaId": "clinging", "pathFactors": ["正業", "正念"], "reason": "生命·所有·関係を害する掴みを意識する", "section": "離殺生", "category": "action"},
    "MN41-P04": {"nidanaId": "clinging", "pathFactors": ["正命", "正念"], "reason": "不正な取得への掴みを問い避ける", "section": "離不与取", "category": "livelihood"},
    "MN41-P05": {"nidanaId": "craving", "pathFactors": ["正業", "正念"], "reason": "誘惑の前に守られた関係を思い出す", "section": "離欲邪行", "category": "action"},
    "MN41-P06": {"nidanaId": "clinging", "pathFactors": ["正語", "正念"], "reason": "虚妄·分断の言葉への掴みを止める", "section": "離虚妄語", "category": "speech"},
    "MN41-P07": {"nidanaId": "speech", "pathFactors": ["正語", "正思惟"], "reason": "噂·伝言で分断しない", "section": "離両舌", "category": "speech"},
    "MN41-P08": {"nidanaId": "feeling", "pathFactors": ["正念", "正語"], "reason": "強い言葉の前に呼吸を置き受を整える", "section": "離粗悪語", "category": "mindfulness"},
    "MN41-P09": {"nidanaId": "craving", "pathFactors": ["正語", "正念"], "reason": "無益な雑談·煽りへの欲しがりを減らす", "section": "離綺語", "category": "speech"},
    "MN41-P10": {"nidanaId": "craving", "pathFactors": ["正思惟", "正念"], "reason": "「私のもの」と欲する心を一度見る", "section": "離貪欲", "category": "intention"},
    "MN41-P11": {"nidanaId": "suffering", "pathFactors": ["正思惟", "正念"], "reason": "怒りの苦の中で他者の幸せを願う", "section": "離瞋恚", "category": "intention"},
    "MN41-P12": {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "邪見を離れ、善行に縁ありと認める", "section": "離邪見", "category": "view"},
    "MN41-P13": {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "夜、身語意を法行·正行として振り返る", "section": "業の地図", "category": "mindfulness"},
}

CHINESE = {
    "MN41-P01": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-ask",
        "text": "白佛言：「世尊！何因、何緣有眾生身壞命終，生地獄中？」佛告……：「行非法行、行危嶮行因緣故……」……「何因緣……得生天上？」……「行法行、行正行……」",
        "satLocus": "大正蔵 T2.272c 鞞聞摩", "note": "死後の行き先を問う。對照表は中阿含非収録。", "satUrl": SAT_URL,
    },
    "MN41-P02": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）", "t26": "SA1042-kusala",
        "text": "謂離殺生，乃至正見，十善業跡因緣故，身壞命終，得生天上。……欲求剎利大性家……乃至他化自在天，悉得往生。",
        "satLocus": "大正蔵 T2.273a 鞞聞摩", "note": "十善業跡により天上·善家へ。", "satUrl": SAT_URL,
    },
    "MN41-P03": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-kill",
        "text": "殺生，乃至邪見，具足十不善業因緣故。……是非法行、危嶮行……",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "漢は十不善を略説。殺生は身不善の筆頭。", "satUrl": SAT_URL,
    },
    "MN41-P04": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-steal",
        "text": "（十不善業跡——不与取を含む。漢は「殺生乃至邪見」と略す。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "不与取はパーリ詳説。漢は十不善の略。", "satUrl": SAT_URL,
    },
    "MN41-P05": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-misconduct",
        "text": "（十不善業跡——欲邪行を含む。漢は略説。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "欲邪行はパーリ詳説。", "satUrl": SAT_URL,
    },
    "MN41-P06": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-false",
        "text": "（十不善——妄語を含む。漢は「乃至」略説。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "虚妄語はパーリ詳説。", "satUrl": SAT_URL,
    },
    "MN41-P07": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-divisive",
        "text": "（十不善——両舌を含む。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "両舌はパーリ詳説。", "satUrl": SAT_URL,
    },
    "MN41-P08": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-harsh",
        "text": "（十不善——悪口を含む。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "粗悪語はパーリ詳説。", "satUrl": SAT_URL,
    },
    "MN41-P09": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-idle",
        "text": "（十不善——綺語を含む。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "綺語はパーリ詳説。", "satUrl": SAT_URL,
    },
    "MN41-P10": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-greed",
        "text": "（十不善——貪欲を含む。漢は乃至邪見。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "貪欲はパーリ詳説。", "satUrl": SAT_URL,
    },
    "MN41-P11": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）／類縁", "t26": "SA1042-hate",
        "text": "（十不善——瞋恚を含む。）",
        "satLocus": "大正蔵 T2.272c 鞞聞摩（類縁）", "note": "瞋恚はパーリ詳説。", "satUrl": SAT_URL,
    },
    "MN41-P12": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）", "t26": "SA1042-view",
        "text": "殺生，乃至邪見，具足十不善業因緣故……謂離殺生，乃至正見，十善業跡因緣故……",
        "satLocus": "大正蔵 T2.272c–273a 鞞聞摩", "note": "邪見／正見が十業の端。", "satUrl": SAT_URL,
    },
    "MN41-P13": {
        "status": "mapped", "pin": "雑阿含1042・鞞聞摩（T99）", "t26": "SA1042-map",
        "text": "若有行此法行、行此正行者，欲求……悉得往生。……欲求斷三結，得須陀洹……漏盡智皆悉得。……以法行、正行故，持戒、離欲，所願必得。",
        "satLocus": "大正蔵 T2.273a 鞞聞摩", "note": "法行·正行の願い——善趣から漏尽まで。", "satUrl": SAT_URL,
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c.setdefault("satUrl", SAT_URL)
    c["mapTableUrl"] = MAP_URL
    c.setdefault(
        "note",
        "パーリ中部41経は中阿含非収録。SC類縁は雑阿含1042·1043（十不善／十善業跡）。漢は略説、パーリは十業を詳説。",
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
    PRACTICE["MN41-P07"]["nidanaId"] = "clinging"  # speech invalid as nidana

    old_path = DATA / "majjhima" / "mn041.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 14):
        pid = f"MN41-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid, "category": pr["category"], "ref": "MN 41", "section": pr["section"],
            "observe": OBSERVE[pid], "action": actions[pid], "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"], "pathFactors": pr["pathFactors"], "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・サーラー村の婆羅門たちへの経／パーリMN41）",
                    "locus": f"中部・サーラー村の婆羅門たちへの経（MN41）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 薩羅村婆羅門経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第41経・薩羅村婆羅門経（サーラー村の婆羅門たちへの経）"
    SHORT = "薩羅村婆羅門経（サーラー村の婆羅門たちへの経）"
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
            "pathLabel": "業が未来を作る教えに触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の業の一歩を変える",
            "toNext": "触のあと、語·怒りの受が見える",
            "todayObserve": OBSERVE["MN41-P01"], "todayAction": actions["MN41-P01"],
            "when": ["業を確認した"], "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN41-P01"][:40] + "…", "secondaryObserve": "死後の行き先は業による",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正語"], "pathFactorIds": ["mindfulness", "speech"],
            "pathLabel": "強い言葉の前に呼吸を置く",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、怒りの受が立つ",
            "toNext": "受に乗ると貪欲·綺語へ",
            "todayObserve": OBSERVE["MN41-P08"], "todayAction": actions["MN41-P08"],
            "when": ["呼吸を置いた"], "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN41-P08"][:40] + "…", "secondaryObserve": "粗悪語の手前で止まる",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "貪欲·邪行·綺語の欲しがりを見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、欲しがりが立つ",
            "toNext": "止めないと身語への掴みへ",
            "todayObserve": OBSERVE["MN41-P10"], "todayAction": actions["MN41-P10"],
            "when": ["貪欲を見た", "関係を思い出した", "雑談を減らした"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN41-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN41-P05"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "action", "nidanaLabel": "掴む",
            "pathFactors": ["正業", "正語"], "pathFactorIds": ["action", "speech"],
            "pathLabel": "身·語の不善への掴みを止める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、不善業の掴みが手前",
            "toNext": "掴むと瞋·苦が見える",
            "todayObserve": OBSERVE["MN41-P03"], "todayAction": actions["MN41-P03"],
            "when": ["害さないと意識した", "虚妄を止めた", "分断しなかった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN41-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN41-P06"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "intention", "nidanaLabel": "苦が太る",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "瞋恚の苦の中で他者の幸せを願う",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、怒りの苦が見える",
            "toNext": "見れば、正行·正見へ離す",
            "todayObserve": OBSERVE["MN41-P11"], "todayAction": actions["MN41-P11"],
            "when": ["慈を置いた"], "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN41-P11"][:40] + "…", "secondaryObserve": "害意は苦を太らせる",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正業"], "pathFactorIds": ["view", "action"],
            "pathLabel": "邪見を離れ、正しい行いに結びつける",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、不善·邪見を離す",
            "toNext": "離せば、夜の業の振り返りへ",
            "todayObserve": OBSERVE["MN41-P02"], "todayAction": actions["MN41-P02"],
            "when": ["正しい行いに結びつけた", "縁を認めた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN41-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN41-P12"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "身語意を法行·正行として振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの業の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN41-P13"], "todayAction": actions["MN41-P13"],
            "when": ["一日を閉じるとき"], "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN41-P13"][:40] + "…", "secondaryObserve": "在俗の業の地図を振り返る",
        },
    ]

    out = {
        "chapter": 41, "sutta": 41, "title": TITLE, "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双小品（アラナ：サーラー村の婆羅門たちへの経）",
        "suttas": ["MN 41 薩羅村婆羅門経（サーラー村の婆羅門たちへの経）"],
        "source": {
            "primary": "パーリ・中部第41経（薩羅村婆羅門経／サーラー村の婆羅門たちへの経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN41（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝中阿含非収録；SC類縁は雑阿含1042·1043（十不善／十善業跡）。"
                "在家者への十不善·十善業道と善趣·悪趣の業の地図が主題。"
            ),
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（中部・サーラー村の婆羅門たちへの経）", "url": ARANA_URL,
                         "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（南伝大蔵経・第9巻中部経典一）", "url": TB_URL,
                           "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 雑阿含・鞞聞摩（T2.272c）／類縁", "url": SAT_URL,
                            "note": "對照表: 中阿含非収録。SC類縁SA1042·1043"},
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
            "focusNodeId": "clinging",
            "focusReason": "薩羅村婆羅門経は十不善業への掴みを離れ十善へ向かうのが主題。既定の焦点は掴む。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn041.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 41:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(41, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 13
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    missing = valid - set(by_nidana)
    assert not missing, missing
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    print(f"OK chinese mapped {mapped}/13; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
