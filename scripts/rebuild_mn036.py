#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn036.json (薩遮迦大経／薩遮迦との大経) to match MN1–35 source alignment.

実経: 薩遮迦が身の修習·心の修習を問う。世尊は苦楽に圧倒されない身·心の修習を示し、
自らが歩んだ道——幼時の禅、極端な苦行（止息·断食）、二辺を離れた中道、
四禅と三明（宿住·天眼·漏尽）——を語る。苦行だけでは覚れず、欲楽辺でも覚れない。
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
# SC類縁: 増壹阿含31.8 無息禅（苦行·止息）。對照表は中阿含非収録（cf.MA32はMN123相当）。
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0125_%2C02%2C0670c02"
SAT_T757 = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0757_%2C17%2C0598a"
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
    "MN36-P01": (
        "薩遮迦は問う——『身の修習と心の修習とは、何か』と。"
        "世尊は説く——苦受が生じて心を圧倒しないように心を修め、"
        "楽受が生じて身を圧倒しないように身を修める者——"
        "それが身·心の修習である。"
        "（朝、今日「中道·覚道」を一つ思い出す。）"
    ),
    "MN36-P02": (
        "わたしは思い出した——幼少のとき、父釈迦の農耕祭の日、"
        "ジャンブ樹の陰に坐して離欲·離不善法から生じた喜と楽を伴う初禅に入った。"
        "『これが覚への道ではないか』と。"
        "（一呼吸で、離生喜楽の方向に心を向ける。）"
    ),
    "MN36-P03": (
        "わたしは極端な苦行をした——歯を食いしばり、口蓋に舌を押し当て、"
        "息を止め、わずかばかりの食に限った。身は極度に痩せ、毛は抜け落ちた。"
        "しかし、そのような激しい苦行をもってしても、人の法を超えた聖なる知見は得られなかった。"
        "（過度な苦行·無理を一度止める。）"
    ),
    "MN36-P04": (
        "そこでわたしは知った——苦行の辺も、欲楽の辺も、覚への道ではない。"
        "中道があり、それは眼を生じ、智を生じ、寂静·勝智·正覚·涅槃へ導く——"
        "すなわち八支の聖道である。"
        "（苦行·欲楽の二極に寄らず、中道を歩む。）"
    ),
    "MN36-P05": (
        "粗食を取り、力を取り戻して四禅に入り、"
        "夜の初更に宿住隨念智を証し、中更に有情の死生を見る天眼を証し、"
        "後更に漏尽智を証して覚った。"
        "（経験を縁起·無常の一環として見る。）"
    ),
    "MN36-P06": (
        "激しい苦行だけでは、人の法を超えた聖なる知見は現れない。"
        "身を苦しめること自体が覚道ではない。"
        "（無理·苦行を「覚道ではない」と一度見る。）"
    ),
    "MN36-P07": (
        "諸々の欲に耽り、卑しく、凡夫の法である欲楽の辺も、覚への道ではない。"
        "（欲楽に寄りすぎていないか問う。）"
    ),
    "MN36-P08": (
        "比丘たちよ、このように中道を歩み、心を修め身を修め、"
        "三明を成就すれば、覚道に至る。"
        "（就寝前、今日「中道を歩んだ」一歩を振り返る。）"
    ),
    "MN36-P09": (
        "わたしは薩遮迦に、自らが歩んだ覚道の物語——"
        "幼時の禅、苦行の限界、中道、四禅と三明——を説いた。"
        "（覚道の物語を一つ思い出す。）"
    ),
    "MN36-P10": (
        "覚道を語る者は、苦行の辺や欲楽の辺を勧めず、中道を語る。"
        "身の修習·心の修習は、苦楽に圧倒されないことにある。"
        "（修行について語るとき、中道を語る。）"
    ),
    "MN36-P11": (
        "覚道の前に、正念·正知を保てば、中道に至る土台となる。"
        "楽受が来ても身に溺れず、苦受が来ても心に溺れない。"
        "（一つの行為に正念·正知を置く。）"
    ),
}

OBSERVE = {
    "MN36-P01": (
        "身·心の修習——苦楽に圧倒されない。朝、中道·覚道を一つ思い出す。"
        "朝、今日「中道・覚道」を一つ思い出す。"
    ),
    "MN36-P02": (
        "幼時の禅——ジャンブ樹の陰の離生喜楽。一呼吸でその方向へ。"
        "今日、一呼吸で「離生喜楽」の記憶・方向に心を向ける。"
    ),
    "MN36-P03": (
        "極端な苦行では聖なる知見は得られない——無理を一度止める。"
        "今日、過度な苦行・無理を一度止める。"
    ),
    "MN36-P04": (
        "苦行·欲楽の二辺を離れ、八正道の中道を歩む。"
        "今日、苦行・欲楽の二極に寄らず、中道を歩む。"
    ),
    "MN36-P05": (
        "三明——宿住·天眼·漏尽。経験を縁起·無常の一環と見る。"
        "今日、経験を「縁起・無常」の一環として見る。"
    ),
    "MN36-P06": (
        "苦行だけでは覚れない——無理を覚道と誤認しない。"
        "今日、無理・苦行を「覚道ではない」と一度見る。"
    ),
    "MN36-P07": (
        "欲楽の辺も覚道ではない——寄りすぎを問う。"
        "今日、欲楽に寄りすぎていないか問う。"
    ),
    "MN36-P08": (
        "夜、中道を歩んだ一歩を振り返る。"
        "就寝前、今日「中道を歩んだ」一歩を振り返る。"
    ),
    "MN36-P09": (
        "薩遮迦への教え——覚道の物語で二辺を離れる見を示す。"
        "今日、覚道の物語（中道・三明）を一つ思い出す。"
    ),
    "MN36-P10": (
        "覚道を語るときは中道を語り、苦行·欲楽を勧めない。"
        "今日、修行について語るとき、中道を語る。"
    ),
    "MN36-P11": (
        "正念·正知——苦楽に溺れない土台。"
        "今日、一つの行為に「正念・正知」を置く。"
    ),
}

PRACTICE = {
    "MN36-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "朝、中道·覚道の教えに触れて一つ思い出す",
        "section": "身·心の修習",
        "category": "view",
    },
    "MN36-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正定", "正念"],
        "reason": "離生喜楽の方向に心を向け、受を整える",
        "section": "幼時の禅",
        "category": "concentration",
    },
    "MN36-P03": {
        "nidanaId": "clinging",
        "pathFactors": ["正精進", "正見"],
        "reason": "苦行への掴み·無理を一度止める",
        "section": "極端な苦行",
        "category": "effort",
    },
    "MN36-P04": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正思惟"],
        "reason": "二辺を離れ、八正道の中道へ",
        "section": "中道",
        "category": "view",
    },
    "MN36-P05": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "経験を縁起·無常として見直し、三明の方向を見る",
        "section": "三明",
        "category": "view",
    },
    "MN36-P06": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正精進"],
        "reason": "苦行の苦を覚道と誤認しない",
        "section": "苦行の限界",
        "category": "view",
    },
    "MN36-P07": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "欲楽への欲しがり·寄りすぎを問う",
        "section": "欲楽の辺",
        "category": "intention",
    },
    "MN36-P08": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜、中道の一歩を振り返る",
        "section": "夜の中道",
        "category": "mindfulness",
    },
    "MN36-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正語"],
        "reason": "覚道の物語に触れ、二辺を離れる見を思い出す",
        "section": "薩遮迦への説示",
        "category": "view",
    },
    "MN36-P10": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正見"],
        "reason": "苦行·欲楽の勧めを離れ、中道を語る",
        "section": "覚道を語る",
        "category": "speech",
    },
    "MN36-P11": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正精進"],
        "reason": "行為に正念·正知を置き、苦楽の受に溺れない",
        "section": "正念·正知",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN36-P01": {
        "status": "mapped",
        "pin": "増壹阿含31.8・無息禅（T125）／類縁",
        "t26": "EA31.8-body-mind",
        "text": "（身の修習·心の修習——苦楽に圧倒されない。パーリMN36の問答核。漢は苦行·禅の類縁で対応。）",
        "satLocus": "大正蔵 T2.670c 無息禅（類縁）",
        "note": "對照表は中阿含非収録。SC類縁EA31.8。",
        "satUrl": SAT_URL,
    },
    "MN36-P02": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）／類縁",
        "t26": "T757-child-jhana",
        "text": "（菩薩幼時、樹下に坐して初禅——仏伝·身毛喜豎系に類縁の記述。）",
        "satLocus": "大正蔵 T17.598 身毛喜豎（類縁）",
        "note": "ジャンブ樹下の初禅は仏伝・T757.2系に類縁。",
        "satUrl": SAT_T757,
    },
    "MN36-P03": {
        "status": "mapped",
        "pin": "増壹阿含31.8・無息禅（T125）",
        "t26": "EA31.8-austerity",
        "text": "聞如是。一時佛在毘舍離城外林中。……（無息·苦行の精進。身痩せ、知見は得られず——パーリの苦行段と対応。）",
        "satLocus": "大正蔵 T2.670c–671 無息禅",
        "note": "止息·断食の苦行。激しい苦行でも聖知見は得られない。",
        "satUrl": SAT_URL,
    },
    "MN36-P04": {
        "status": "mapped",
        "pin": "増壹阿含31.8・無息禅（T125）／類縁",
        "t26": "EA31.8-middle",
        "text": "（二辺を離れ中道へ——パーリ八正道。漢も苦行辺を離れる流れで類縁。）",
        "satLocus": "大正蔵 T2.670c–671 無息禅（類縁）",
        "note": "苦行辺·欲楽辺を離れる中道。",
        "satUrl": SAT_URL,
    },
    "MN36-P05": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）／類縁",
        "t26": "T757-tevijja",
        "text": "（宿住·天眼·漏尽の三明——覚道の成就。身毛喜豎·仏伝に類縁。）",
        "satLocus": "大正蔵 T17.598–599 身毛喜豎（類縁）",
        "note": "三明の証得。",
        "satUrl": SAT_T757,
    },
    "MN36-P06": {
        "status": "mapped",
        "pin": "増壹阿含31.8・無息禅（T125）",
        "t26": "EA31.8-not-enough",
        "text": "（無息·苦行の精進をもってしても、究極の知見に至らず——苦行だけでは覚れない。）",
        "satLocus": "大正蔵 T2.670c–671 無息禅",
        "note": "苦行≠覚道。",
        "satUrl": SAT_URL,
    },
    "MN36-P07": {
        "status": "unmapped",
        "pin": "（漢訳に直接対応なし）",
        "t26": "",
        "text": "",
        "satLocus": "對照表: 中阿含非収録。欲楽辺の明示はパーリMN36に詳しい。",
        "note": "欲楽の辺も覚道に非ず——パーリ固有の二辺対句の片側。",
    },
    "MN36-P08": {
        "status": "mapped",
        "pin": "増壹阿含31.8・無息禅（T125）／類縁",
        "t26": "EA31.8-review",
        "text": "（中道·身心理を成就する方向——夜の振り返りの実践根拠。）",
        "satLocus": "大正蔵 T2.670c 無息禅（類縁）",
        "note": "中道成就の振り返り。",
        "satUrl": SAT_URL,
    },
    "MN36-P09": {
        "status": "mapped",
        "pin": "増壹阿含31.8・無息禅（T125）／類縁",
        "t26": "EA31.8-teach",
        "text": "一時佛在毘舍離城外林中。……（覚道·苦行の物語を説く場。パーリは薩遮迦への説示。）",
        "satLocus": "大正蔵 T2.670c 無息禅（類縁）",
        "note": "漢は毘舍離での説示。パーリは薩遮迦への覚道物語。",
        "satUrl": SAT_URL,
    },
    "MN36-P10": {
        "status": "unmapped",
        "pin": "（漢訳に直接対応なし）",
        "t26": "",
        "text": "",
        "satLocus": "對照表: 中阿含非収録。『覚道を語る者は中道を語る』は実践要約。",
        "note": "正語としての中道——アプリ用の実践対応。漢に同一句なし。",
    },
    "MN36-P11": {
        "status": "mapped",
        "pin": "増壹阿含31.8・無息禅（T125）／類縁",
        "t26": "EA31.8-sati",
        "text": "（正念·正知を保ち、苦楽に溺れない——身·心の修習の土台。）",
        "satLocus": "大正蔵 T2.670c 無息禅（類縁）",
        "note": "正念·正知。",
        "satUrl": SAT_URL,
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c.setdefault("satUrl", SAT_URL)
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部36経は中阿含非収録。SC類縁は増壹阿含31.8無息禅・身毛喜豎T757.2。對照表: 法雨道場。",
        )
    elif c.get("status") == "unmapped":
        c.setdefault(
            "note",
            "對照表は中阿含非収録。このペアはパーリMN36側の実践要約／固有句。",
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
    old_path = DATA / "majjhima" / "mn036.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN36-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 36",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・薩遮迦との大経／パーリMN36）",
                    "locus": f"中部・薩遮迦との大経（MN36）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 薩遮迦大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第36経・薩遮迦大経（薩遮迦との大経）"
    SHORT = "薩遮迦大経（薩遮迦との大経）"
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
            "pathLabel": "中道·覚道の教えに触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の中道の一歩を変える",
            "toNext": "触のあと、離生喜楽の受が見える",
            "todayObserve": OBSERVE["MN36-P01"],
            "todayAction": actions["MN36-P01"],
            "when": ["中道を思い出した", "教えに触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN36-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN36-P09"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "concentration", "nidanaLabel": "受ける",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "離生喜楽·正念で受を整える",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、喜楽·苦楽の受が立つ",
            "toNext": "受に乗ると欲楽への欲しがりへ",
            "todayObserve": OBSERVE["MN36-P02"],
            "todayAction": actions["MN36-P02"],
            "when": ["一呼吸で心を向けた", "正念を置いた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN36-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN36-P11"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "欲楽への寄りすぎを問う",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、欲楽への欲しがりが立つ",
            "toNext": "止めないと苦行への掴みや偏りへ",
            "todayObserve": OBSERVE["MN36-P07"],
            "todayAction": actions["MN36-P07"],
            "when": ["欲楽に寄りすぎを問うた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN36-P07"][:40] + "…",
            "secondaryObserve": "欲楽辺は覚道に非ず",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "effort", "nidanaLabel": "掴む",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "苦行への掴み·無理を一度止める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりや焦りのあと、苦行への掴みが手前",
            "toNext": "掴むと苦行の苦が見える",
            "todayObserve": OBSERVE["MN36-P03"],
            "todayAction": actions["MN36-P03"],
            "when": ["無理を一度止めた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN36-P03"][:40] + "…",
            "secondaryObserve": "苦行では聖知見は得られない",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "苦行の苦を覚道と誤認しない",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、苦行の限界の苦が見える",
            "toNext": "見れば、二辺を離れて中道へ",
            "todayObserve": OBSERVE["MN36-P06"],
            "todayAction": actions["MN36-P06"],
            "when": ["苦行は覚道でないと見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN36-P06"][:40] + "…",
            "secondaryObserve": "身を苦しめること自体が覚道ではない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "二辺を離れ、中道を歩み語る",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、苦行·欲楽の辺を離す",
            "toNext": "離せば、夜の中道の見直しへ",
            "todayObserve": OBSERVE["MN36-P04"],
            "todayAction": actions["MN36-P04"],
            "when": ["中道を歩んだ", "中道を語った"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN36-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN36-P10"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "中道の一歩と三明の方向を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの中道の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN36-P08"],
            "todayAction": actions["MN36-P08"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN36-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN36-P05"],
        },
    ]

    out = {
        "chapter": 36,
        "sutta": 36,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：薩遮迦との大経）",
        "suttas": ["MN 36 薩遮迦大経（薩遮迦との大経）"],
        "source": {
            "primary": "パーリ・中部第36経（薩遮迦大経／薩遮迦との大経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN36（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝中阿含非収録；SC類縁は増壹阿含31.8無息禅（T125）"
                "および身毛喜豎経（T757.2）。"
                "身·心の修習、幼時の禅、苦行の限界、中道、四禅·三明が主題。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・薩遮迦との大経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 増壹阿含・無息禅（T2.670c）／類縁",
                    "url": SAT_URL,
                    "note": "對照表: 中阿含非収録。SC類縁EA31.8・T757.2",
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
            "focusNodeId": "release",
            "focusReason": "薩遮迦大経は苦行·欲楽の二辺を離れ、中道·身心理·三明へ向かうのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn036.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 36:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(36, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN36-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] != "mapped"]
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; unmapped {unmapped}; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
