#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn029.json (心材喩大経／心材の喩えの大経) to match MN1–28 source alignment.

注: 旧スタブは皮＝衣食·木＝神通·枝＝天界·葉＝名声と誤対応。
実経: 枝葉＝利得·恭敬·名声／嫩芽＝戒／皮＝定／膚材＝智見／心材＝不動心解脱。
actions は保持し、quote·observe で実文へ合わせる。
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0125_%2C02%2C0759a29"
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
    "MN29-P01": (
        "比丘たちよ、この梵行は、利得·恭敬·名声のためでも、戒具足のためでも、"
        "定具足のためでも、智見のためでもない。"
        "この不動の心の解脱——これこそが梵行の目的であり、心材であり、終極である。"
    ),
    "MN29-P02": (
        "出家して利得·恭敬·名声が生じる。……それに酔い、放逸に堕ち、苦を生きる。"
        "心材を求める者が、枝葉を切り『心材』と思い持ち帰る——"
        "これは、梵行の枝葉を掴んだ比丘である。"
        "（衣食等の利養は、この枝葉の一環。）"
    ),
    "MN29-P03": (
        "不放逸にして定具足に達する。……定具足をもって自らを讃え他を軽蔑し、"
        "放逸に堕ち、苦を生きる。"
        "皮を切り『心材』と思い持ち帰る——これは、梵行の皮を掴んだ比丘である。"
        "（定·神通の快さで止まれば、心材に至らない。）"
    ),
    "MN29-P04": (
        "不放逸にして戒具足に達する。……戒具足をもって自らを讃え他を軽蔑し、"
        "放逸に堕ち、苦を生きる。"
        "嫩芽を切り『心材』と思い持ち帰る——これは、梵行の嫩芽を掴んだ比丘である。"
        "（途中段階や別の願いで『足りた』と思えば、心材を逃す。）"
    ),
    "MN29-P05": (
        "利得·恭敬·名声が生じ、自らを讃え他を軽蔑する——"
        "『わたしは利得·恭敬·名声ある者。他の比丘たちは卑小である』と。"
        "……枝葉を心材と誤る。これは、梵行の枝葉を掴んだ比丘である。"
    ),
    "MN29-P06": (
        "……智見についても放逸せず、不放逸にして非一時の解脱に達する。"
        "その比丘が、その非一時の解脱から退転することはありえない。"
        "心材のみを切り、『心材』と知って持ち帰る——"
        "不動の心の解脱が、梵行の心材である。"
    ),
    "MN29-P07": (
        "……それに酔い放逸に堕ち、苦を生きる。"
        "心材で作るべきことを、彼は成就できない。"
        "外の段階（枝葉·嫩芽·皮·膚材）で止まれば、心材に至らず、苦が続く。"
    ),
    "MN29-P08": (
        "利得·恭敬·名声をもって自らを讃えず、他を軽蔑しない。"
        "……戒·定·智見についても同様に、自らを讃えず放逸に堕ちない。"
        "（評価の競争より、心材＝解脱へ。）"
    ),
    "MN29-P09": (
        "この梵行は、利得·恭敬·名声·戒具足·定具足·智見のためではない。"
        "不動の心の解脱——これこそが目的であり、心材であり、終極である。"
    ),
    "MN29-P10": (
        "比丘たちよ、この梵行は、利得·恭敬·名声のためでも、"
        "戒具足のためでも、定具足のためでも、智見のためでもない。"
        "この不動の心の解脱——これこそが梵行の目的であり、心材であり、終極である。"
    ),
    "MN29-P11": (
        "提婆達多が去った後、ほどなくして……世尊は、提婆達多について比丘たちに語った。"
        "……心材を求める者が、心材·膚材·皮·嫩芽·枝葉を知り分け、"
        "心材のみを切り持ち帰る——彼は目的を成就する。"
    ),
}

OBSERVE = {
    "MN29-P01": (
        "梵行の終極は不動の心の解脱＝心材。利得·戒·定·智見は途中段階。"
        "朝、今日「心材（解脱）」を求める一歩を一つ決める。"
    ),
    "MN29-P02": (
        "枝葉＝利得·恭敬·名声。衣食等の利養への過度な追いは枝葉で止まること。"
        "（旧実践語の「皮」は本経では定具足の譬喩——衣食の問いは枝葉側で用いる。）"
        "今日、衣食の追求が「皮の如き外求」でないか問う。"
    ),
    "MN29-P03": (
        "皮＝定具足。定·神通の快さで自らを讃え放逸すれば心材を逃す。"
        "今日、修行が「神通のため」で「解脱のため」でないか問う。"
    ),
    "MN29-P04": (
        "嫩芽＝戒具足。戒や別の願い（天界等）で『足りた』と思えば心材を逃す。"
        "今日、願いが「天界·梵天」で「解脱」でないか問う。"
    ),
    "MN29-P05": (
        "葉·枝＝名声·利養·恭敬。自らを讃え他を軽蔑すれば枝葉を掴む。"
        "今日、名声·利养·尊重を求めていないか問う。"
    ),
    "MN29-P06": (
        "心材＝非一時の解脱／不動の心の解脱。途中段階を一つ手放し心材へ。"
        "今日、外求（皮·木·枝·葉）を一つ手放し、心材（解脱）に向ける。"
    ),
    "MN29-P07": (
        "段階で止まって放逸すれば苦を生き、心材の業は成就しない。"
        "今日の苦を「外求の結果」と一度見る。"
    ),
    "MN29-P08": (
        "自らを讃えず他を軽蔑しない——評価より解脱を優先する善比丘の道。"
        "今日、他者の評価（名声·利养）より自分の解脱を優先する。"
    ),
    "MN29-P09": (
        "夜、利得·戒·定·智見で止まらなかったか振り返り、心材を思い出す。"
        "就寝前、今日「外求を求めた」瞬間を一つ認め、明日心材を求める。"
    ),
    "MN29-P10": (
        "語るなら解脱·心材。利得·戒·定·智見を終極として語らない。"
        "今日、解脱·心材について語る機会があれば、外求を語らない。"
    ),
    "MN29-P11": (
        "提婆達多の後に説かれた心材喩——"
        "枝葉＝利得／嫩芽＝戒／皮＝定／膚材＝智見／心材＝不動解脱。"
        "今日、心材喩を一つ（皮·木·枝·葉·心材）思い出す。"
    ),
}

PRACTICE = {
    "MN29-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "朝、心材＝解脱への一歩に触れて決める",
        "section": "心材＝不動の解脱",
        "category": "view",
    },
    "MN29-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正命", "正念"],
        "reason": "衣食·利養の受が枝葉で止まっていないか見る",
        "section": "枝葉·利養",
        "category": "livelihood",
    },
    "MN29-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正定", "正見"],
        "reason": "定·神通への欲しがりで皮に止まらないか問う",
        "section": "皮·定具足",
        "category": "concentration",
    },
    "MN29-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正見"],
        "reason": "戒や天界の願いで嫩芽に止まらないか問う",
        "section": "嫩芽·戒具足",
        "category": "intention",
    },
    "MN29-P05": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "名声·利養·恭敬への欲しがりを問う",
        "section": "枝葉·名声",
        "category": "intention",
    },
    "MN29-P06": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正見"],
        "reason": "外求を一つ手放し、心材＝解脱へ向ける",
        "section": "心材へ向ける",
        "category": "effort",
    },
    "MN29-P07": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "外求で止まった苦を、外求の結果と見る",
        "section": "放逸·苦",
        "category": "view",
    },
    "MN29-P08": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正念"],
        "reason": "他者評価への掴みより解脱を優先する",
        "section": "自讃·他毀を離れる",
        "category": "intention",
    },
    "MN29-P09": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "夜、外求の瞬間を認め、明日心材へ向ける",
        "section": "夜の心材",
        "category": "view",
    },
    "MN29-P10": {
        "nidanaId": "review",
        "pathFactors": ["正語", "正見"],
        "reason": "語るなら心材＝解脱、外求を終極と語らない",
        "section": "心材を語る",
        "category": "speech",
    },
    "MN29-P11": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "心材喩の段階対応に触れ、一つ思い出す",
        "section": "導·提婆達多の後",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN29-P01": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-goal",
        "text": "夫智慧者，於此法中最為第一。……智慧成就者，此是第一之義。",
        "satLocus": "大正蔵 T2.759c 提婆達",
        "note": "中阿含に相当経なし（對照表）。漢は智慧第一、パーリは不動心解脱が心材。",
    },
    "MN29-P02": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-leaves",
        "text": "往詣大樹……持枝葉而還。今此比丘亦復如是，貪著利養，由此利養，向他自譽，毀呰他人……。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "枝葉＝利養·自譽毀他。",
    },
    "MN29-P03": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-samadhi",
        "text": "好修三昧。彼以此三昧心向他自譽：『我今得定，餘人無定。』比丘所應行法亦不果獲。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "定で自譽＝パーリの皮（定具足）で止まる譬喩に近い。",
    },
    "MN29-P04": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-sila",
        "text": "或時復向他人自稱說：『我是持戒之人，彼是犯戒之士。』比丘所願者而不果獲，如人捨根，持枝還家……。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "持戒で自譽＝パーリの嫩芽（戒）で止まる譬喩に近い。",
    },
    "MN29-P05": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-fame",
        "text": "貪著利養，由此利養，向他自譽，毀呰他人，比丘所行宜，則不果其願。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "利養·自譽毀他＝枝葉。",
    },
    "MN29-P06": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-heartwood",
        "text": (
            "猶如有人……望其實，捨其枝葉，取其根持還。智者見已……：『此人別其根。』"
            "……漸行智慧。夫智慧者，於此法中最為第一。"
        ),
        "satLocus": "大正蔵 T2.759b–c 提婆達",
        "note": "漢は根·智慧第一。パーリは非一時解脱／不動心解脱が心材（段差あり）。",
    },
    "MN29-P07": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-fail",
        "text": "比丘所行宜，則不果其願。……如彼人求寶不得，為智者所棄。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "願不果＝心材の業を成就できない。",
    },
    "MN29-P08": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-no-boast",
        "text": "設有比丘得利養已，亦不自譽，復不毀他人……興起利養，奉持戒律，亦不自譽，復非毀他人……。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "不自譽·不毀他。",
    },
    "MN29-P09": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-review",
        "text": "戒律之法者，世俗常數；三昧成就者，亦是世俗常數；神足飛行者，亦是世俗常數；智慧成就者，此是第一之義。",
        "satLocus": "大正蔵 T2.759c 提婆達",
        "note": "途中を世俗常数とし第一義へ——夜の見直しの根拠。",
    },
    "MN29-P10": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-speak",
        "text": "智慧成就者，此是第一之義。……「智慧最為上，無憂無所慮，久畢獲等見，斷於生死有。」",
        "satLocus": "大正蔵 T2.759c 提婆達",
        "note": "第一義を語る。パーリ結は不動心解脱。",
    },
    "MN29-P11": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）",
        "t26": "EA43.4-nidana",
        "text": "眾多比丘白佛言：「提婆達兜者極大威力……。」爾時，世尊告諸比丘：「……貪提婆達兜比丘利養；彼愚人由此利養自當滅亡。」",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "提婆達多の利養を機縁に心材喩（求樹）を説く。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部29経の対応は増壹阿含43.4（中阿含に相当なし）。對照表: 法雨道場。",
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
    old_path = DATA / "majjhima" / "mn029.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN29-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 29",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・心材の喩えの大経／パーリMN29）",
                    "locus": f"中部・心材の喩えの大経（MN29）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 心材喩大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第29経・心材喩大経（心材の喩えの大経）"
    SHORT = "心材喩大経（心材の喩えの大経）"
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
            "pathLabel": "心材＝解脱への一歩と喩えの段階に触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の心材の一歩を変える",
            "toNext": "触のあと、利養·衣食の受が見える",
            "todayObserve": OBSERVE["MN29-P01"],
            "todayAction": actions["MN29-P01"],
            "when": ["心材の一歩を決めた", "喩えを一つ思い出した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN29-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN29-P11"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "livelihood", "nidanaLabel": "受ける",
            "pathFactors": ["正命", "正念"], "pathFactorIds": ["livelihood", "mindfulness"],
            "pathLabel": "衣食·利養の受が枝葉で止まっていないか見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、利養の受が立つ",
            "toNext": "受に乗ると名声·定·願への欲しがりへ",
            "todayObserve": OBSERVE["MN29-P02"],
            "todayAction": actions["MN29-P02"],
            "when": ["衣食の外求を問うた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN29-P02"][:40] + "…",
            "secondaryObserve": "枝葉＝利養",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "名声·定·願いへの欲しがりで途中段階に止まらない",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、名声·定·天界の欲しがりが立つ",
            "toNext": "止めないと評価の掴みへ",
            "todayObserve": OBSERVE["MN29-P05"],
            "todayAction": actions["MN29-P05"],
            "when": ["名声を問うた", "神通·願いを問うた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN29-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN29-P03"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "他者評価への掴みより解脱を優先する",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、自讃·他毀の掴みが手前",
            "toNext": "掴むと放逸の苦が見える",
            "todayObserve": OBSERVE["MN29-P08"],
            "todayAction": actions["MN29-P08"],
            "when": ["評価より解脱を優先した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN29-P08"][:40] + "…",
            "secondaryObserve": "不自譽·不毀他",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "外求で止まった苦を、外求の結果と見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、放逸の苦が見える",
            "toNext": "見れば、外求を手放し心材へ",
            "todayObserve": OBSERVE["MN29-P07"],
            "todayAction": actions["MN29-P07"],
            "when": ["外求の結果と見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN29-P07"][:40] + "…",
            "secondaryObserve": "放逸すれば苦を生きる",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "外求を一つ手放し、心材＝解脱へ向ける",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、枝葉·皮を手放す",
            "toNext": "離せば、夜の心材の見直しへ",
            "todayObserve": OBSERVE["MN29-P06"],
            "todayAction": actions["MN29-P06"],
            "when": ["外求を一つ手放した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN29-P06"][:40] + "…",
            "secondaryObserve": "不動の心の解脱",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正語"], "pathFactorIds": ["view", "speech"],
            "pathLabel": "外求の瞬間を認め、心材として語り直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの心材の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN29-P09"],
            "todayAction": actions["MN29-P09"],
            "when": ["一日を閉じるとき", "心材を語った夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN29-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN29-P10"],
        },
    ]

    out = {
        "chapter": 29,
        "sutta": 29,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：心材の喩えの大経）",
        "suttas": ["MN 29 心材喩大経（心材の喩えの大経）"],
        "source": {
            "primary": "パーリ・中部第29経（心材喩大経／心材の喩えの大経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN29（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT増壹阿含43.4提婆達（T125；中阿含に相当なし）。"
                "枝葉＝利得·恭敬·名声、嫩芽＝戒、皮＝定、膚材＝智見、心材＝不動の心の解脱。"
                "提婆達多離反の後に説かれ、途中段階で止まらぬよう誡める。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・心材の喩えの大経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 増壹阿含・提婆達（T2.759a）",
                    "url": SAT_URL,
                    "note": "利養·持戒·三昧·智慧。對照表: 法雨道場（EA43.4；中阿含無相当）",
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
            "focusReason": "心材喩大経は途中段階（利得·戒·定·智見）で止まらず、不動の心の解脱＝心材へ離すのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn029.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 29:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(29, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN29-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
