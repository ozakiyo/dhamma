#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn009.json (正見経／正しい見解の経) to match MN1–8 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0461"
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
    "MN9-P01": (
        "友よ、『正しい見解（正見）』『正しい見解』と説かれます。"
        "友よ、いったい、まさに、どのようなことから、聖なる弟子は、正しい見解ある者と成り、"
        "彼の見解が真っすぐに赴いたものと〔成り〕、法（教え）にたいする確固たる浄信を具備した者と〔成り〕、"
        "この正なる法（教え）に精通した者と〔成るのですか〕。"
    ),
    "MN9-P02": (
        "友よ、すなわち、まさに、聖なる弟子が、そして、善ならざるものを覚知し、さらに、善ならざるものの根元を覚知することから、"
        "そして、善なるものを覚知し、さらに、善なるものの根元を覚知することから、"
        "……聖なる弟子は、正しい見解ある者と成ります。"
        "……貪欲（貪）は、善ならざるものの根元です。憤怒（瞋）は……迷妄（痴）は……。"
        "……貪欲なき〔あり方〕（無貪）は、善なるものの根元です。憤怒なき〔あり方〕（無瞋）は……迷妄なき〔あり方〕（無痴）は……。"
    ),
    "MN9-P03": (
        "生もまた、苦しみです。老もまた、苦しみです。死もまた、苦しみです。"
        "諸々の憂いと嘆きと苦痛と失意と葛藤もまた、苦しみです。"
        "……簡略〔の観点〕によって〔説くなら〕、五つの〔心身を構成する〕執取の範疇（五取蘊）は、苦しみです。"
    ),
    "MN9-P04": (
        "友よ、では、どのようなものが、苦しみの集起なのですか。"
        "すなわち、この、さらなる生存あるものであり、愉悦と貪欲を共具したものであり、そこかしこに愉悦〔の思い〕ある、渇愛です。"
        "それは、すなわち、この、欲望の渇愛（欲愛）であり、生存の渇愛（有愛）であり、非生存の渇愛（非有愛）です。"
        "……まさしく、この、聖なる八つの支分ある道は、苦しみの止滅に至る〔実践の〕道です。"
    ),
    "MN9-P05": (
        "彼は、全てにわたり、貪り〔の思い〕の悪習を捨棄して、敵対〔の思い〕の悪習を除去して、"
        "『〔わたしは〕存在する』という見解と思量の悪習を完破して、無明を捨棄して、明知を生起させて、"
        "所見の法（現世）において、苦しみの終極を為す者と成ります。"
    ),
    "MN9-P06": (
        "友よ、これらの四つの執取があります。"
        "欲望〔の対象〕への執取であり、見解への執取であり、戒と掟への執取であり、自己の論への執取です。"
        "渇愛（愛）の集起あることから、執取の集起があります。"
        "……まさしく、この、聖なる八つの支分ある道は、執取の止滅に至る〔実践の〕道です。"
    ),
    "MN9-P07": (
        "友よ、すなわち、まさに、苦しみについての無知、苦しみの集起についての無知、"
        "苦しみの止滅についての無知、苦しみの止滅に至る〔実践の〕道についての無知は、友よ、これは、無明と説かれます。"
        "……煩悩の止滅あることから、無明の止滅があります。"
        "……無明を捨棄して、明知を生起させて、所見の法（現世）において、苦しみの終極を為す者と成ります。"
    ),
    "MN9-P08": (
        "友よ、これらの六つの感受の体系があります。……眼の接触から生じる感受であり……意の接触から生じる感受です。"
        "接触（触）の集起あることから、感受の集起があります。"
        "感受の集起あることから、渇愛の集起があります。"
        "……まさしく、この、聖なる八つの支分ある道は、渇愛の止滅に至る〔実践の〕道です。"
    ),
    "MN9-P09": (
        "友よ、これらの六つの接触の体系があります。眼の接触であり……意の接触です。"
        "六つの〔認識の〕場所（六処）の集起あることから、接触の集起があります。"
        "……まさしく、この、聖なる八つの支分ある道は、接触の止滅に至る〔実践の〕道です。"
    ),
    "MN9-P10": (
        "まさしく、この、聖なる八つの支分ある道（八正道・八聖道）は、〔その支の〕止滅に至る〔実践の〕道です。"
        "それは、すなわち、この、正しい見解（正見）であり、正しい思惟（正思惟）であり、正しい言葉（正語）であり、"
        "正しい行業（正業）であり、正しい生き方（正命）であり、正しい努力（正精進）であり、"
        "正しい気づき（正念）であり、正しい禅定（正定）です。"
    ),
    "MN9-P11": (
        "友よ、『正しい見解（正見）』『正しい見解』と説かれます。"
        "友よ、いったい、まさに、どのようなことから、聖なる弟子は、正しい見解ある者と成るのですか。"
        "……友よ、たとえ、遠くからでも、まさに、わたしたちは、尊者サーリプッタの現前において、"
        "この語られたことの義（意味）を了知するためにやってくるでしょう。"
    ),
    "MN9-P12": (
        "友よ、すなわち、まさに、聖なる弟子が、そして、煩悩（漏）を覚知し、かつまた、煩悩の集起を覚知し、"
        "かつまた、煩悩の止滅を覚知し、さらに、煩悩の止滅に至る〔実践の〕道を覚知することから、"
        "……無明を捨棄して、明知を生起させて、所見の法（現世）において、苦しみの終極を為す者と成ります。"
    ),
}

OBSERVE = {
    "MN9-P01": (
        "正見とは——聖なる弟子が、見解を真っすぐにし、法への浄信を具備し、正法に精通すること。"
        "その入口は、苦を苦として知ること。"
    ),
    "MN9-P02": (
        "不善・不善の根（貪・瞋・痴）と、善・善の根（無貪・無瞋・無痴）を覚知するとき、正見がある。"
    ),
    "MN9-P03": (
        "生・老・死・愁悲苦憂悩・怨憎会・愛別離・求不得、要約すれば五取蘊は苦。"
    ),
    "MN9-P04": (
        "苦の集は渇愛——欲愛・有愛・非有愛。"
        "苦の滅への道は、聖なる八支道。"
    ),
    "MN9-P05": (
        "四諦を知る者は、貪瞋の随眠を捨て、有見慢を破り、無明を捨て明知を生じ、現法で苦の終極を為す。"
    ),
    "MN9-P06": (
        "四取——欲取・見取・戒禁取・我語取。"
        "渇愛から執取が集起する。執着が来たら縁起の流れを辿る。"
    ),
    "MN9-P07": (
        "四諦への無知が無明。"
        "無明の滅により行が滅し、明知が生じ、現法で苦が終る。"
    ),
    "MN9-P08": (
        "六受は接触から生じ、感受の集起から渇愛の集起がある。"
        "快・不快のあと、愛が乗っていないかを見る。"
    ),
    "MN9-P09": (
        "六触は六処から生じる。"
        "縁起の一支——触・受・愛・取——を一つ意識する。"
    ),
    "MN9-P10": (
        "各支の滅道は、正見から正定までの八支。"
        "因果を単純化せず、縁起と八正道として語る。"
    ),
    "MN9-P11": (
        "舎利弗が比丘たちに正見を問われ答える。"
        "正見の一節を、静かに分かち合う。"
    ),
    "MN9-P12": (
        "漏（欲漏・有漏・無明漏）の集・滅・道を知ることも正見。"
        "無明を捨て明知を生じ、現法で苦の終極を為す——夜に一つ認める。"
    ),
}

PRACTICE = {
    "MN9-P01": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦を苦諦として名づけ、正見の入口に立つ",
        "section": "正見·問",
        "category": "view",
    },
    "MN9-P02": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正思惟"],
        "reason": "善・不善とその根を覚知して正見を確かめる",
        "section": "善不善·根",
        "category": "view",
    },
    "MN9-P03": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "五取蘊の苦を如実に認める",
        "section": "苦諦",
        "category": "view",
    },
    "MN9-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "苦の集＝渇愛、滅道＝八正道と見る",
        "section": "集·道",
        "category": "view",
    },
    "MN9-P05": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正念"],
        "reason": "無明を捨て明知を生じ、現法で苦の終極へ",
        "section": "明知·苦終",
        "category": "mindfulness",
    },
    "MN9-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正精進"],
        "reason": "四取を知り、執着の流れを縁起で辿る",
        "section": "執取",
        "category": "view",
    },
    "MN9-P07": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "無明の滅により逆観で苦を弱める",
        "section": "無明·逆観",
        "category": "view",
    },
    "MN9-P08": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "受のあと渇愛が乗っていないかを見る",
        "section": "受·渇愛",
        "category": "mindfulness",
    },
    "MN9-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正定"],
        "reason": "六触を縁起の一支として意識する",
        "section": "接触",
        "category": "mindfulness",
    },
    "MN9-P10": {
        "nidanaId": "review",
        "pathFactors": ["正語", "正見"],
        "reason": "滅道を八支として語り、単純化しない",
        "section": "八支道",
        "category": "speech",
    },
    "MN9-P11": {
        "nidanaId": "review",
        "pathFactors": ["正思惟", "正語"],
        "reason": "正見の問いを分かち合い、義を了知する",
        "section": "問答",
        "category": "intention",
    },
    "MN9-P12": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "漏の滅・明知を夜に一つ振り返る",
        "section": "漏·結",
        "category": "view",
    },
}

CHINESE = {
    "MN9-P01": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-rightview-q",
        "text": "頗有事因此事。比丘成就見得正見於法得不壞淨入正法耶。答曰。有也。",
        "satLocus": "大正蔵 T1.461c 大拘絺羅経",
        "note": "問答の役割はパーリと異なるが、正見成就の問いが対応。",
    },
    "MN9-P02": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-kusala-mula",
        "text": "謂有比丘知不善知不善根。……貪不善根恚癡不善根。……知善知善根。……無貪善根。無恚無癡善根。……成就見得正見。",
        "satLocus": "大正蔵 T1.461c 大拘絺羅経",
        "note": "不善／善とその根＝パーリの善不善根。",
    },
    "MN9-P03": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-dukkha",
        "text": "謂生苦老苦病苦死苦。怨憎會苦。愛別離苦。所求不得苦。略五盛陰苦。是謂知苦如眞。",
        "satLocus": "大正蔵 T1.462a 大拘絺羅経",
        "note": "五盛陰苦＝五取蘊苦。",
    },
    "MN9-P04": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-tanha-magga",
        "text": "謂因愛便有食……愛滅食便滅……八支聖道。正見乃至正定爲八。……謂有三愛。欲愛色愛無色愛……因覺便有愛。",
        "satLocus": "大正蔵 T1.461c–462b 大拘絺羅経",
        "note": "漢訳の苦習は老死経由の異文あり。愛と八支聖道はパーリの集・道に対応。",
    },
    "MN9-P05": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-vijja",
        "text": "若有比丘無明已盡明已生。復作何等。……若有比丘無明已盡明已生。無所復作。",
        "satLocus": "大正蔵 T1.464a 大拘絺羅経",
        "note": "無明尽・明生＝パーリの無明捨・明知生起に近接。",
    },
    "MN9-P06": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-upadana",
        "text": "云何知受如眞。謂有四受欲受。戒受見受我受。是謂知受如眞。云何知受習如眞。謂因愛便有受。",
        "satLocus": "大正蔵 T1.462b 大拘絺羅経",
        "note": "漢訳「四受」＝パーリ四取（欲・戒禁・見・我語）。",
    },
    "MN9-P07": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-avijja",
        "text": "云何知行習如眞。謂因無明便有行。……謂無明滅行便滅。……無明已盡明已生。無所復作。",
        "satLocus": "大正蔵 T1.463c–464a 大拘絺羅経",
        "note": "無明→行の集滅＝逆観の核。",
    },
    "MN9-P08": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-vedana-tanha",
        "text": "云何知愛習如眞。謂因覺便有愛。是謂知愛習如眞。云何知愛滅如眞。謂覺滅愛便滅。",
        "satLocus": "大正蔵 T1.462c 大拘絺羅経",
        "note": "漢訳「覺」≒受。覺→愛＝受→渇愛。",
    },
    "MN9-P09": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-phassa",
        "text": "謂有四食。一者摶食麤細。二者更樂食。三者意思食。四者識食。……因愛便有食。……知六處如眞。謂眼處耳鼻舌身意處。",
        "satLocus": "大正蔵 T1.461c–463a 大拘絺羅経",
        "note": "更樂食＝触食。六処は接触の集起に近接。",
    },
    "MN9-P10": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-atthangika",
        "text": "謂八支聖道。正見乃至正定爲八。是謂知食滅道如眞。",
        "satLocus": "大正蔵 T1.461c 大拘絺羅経",
        "note": "各支の滅道として反復される八支聖道。",
    },
    "MN9-P11": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-dialogue",
        "text": "尊者舍梨子語尊者大拘絺羅。我欲有所問。……頗有事因此事。比丘成就見得正見於法得不壞淨入正法耶。",
        "satLocus": "大正蔵 T1.461c 大拘絺羅経",
        "note": "正見の問い——対話者はパーリと入れ替わるが主題は同型。",
    },
    "MN9-P12": {
        "status": "mapped",
        "pin": "中阿含29・大拘絺羅経（T26）",
        "t26": "T26-029-asava",
        "text": "謂有三漏。欲漏有漏無明漏。……因無明便有漏。……無明滅漏便滅。……八支聖道。正見乃至正定爲八。",
        "satLocus": "大正蔵 T1.462a 大拘絺羅経",
        "note": "三漏の集滅道＝パーリの煩悩（漏）教相。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部9経と中阿含29大拘絺羅経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn009.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 13):
        pid = f"MN9-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 9",
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
                    "locus": f"中部・正しい見解の経（MN9）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 正見経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第9経・正見経（正しい見解の経）"
    SHORT = "正見経（正しい見解の経）"
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
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "六触を縁起の一支として見る",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の接触の見方を変える",
            "toNext": "触のあと、受が立ち上がる",
            "todayObserve": OBSERVE["MN9-P09"],
            "todayAction": actions["MN9-P09"],
            "when": ["感覚が触れた", "六処が動いた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN9-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN9-P08"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "受のあと渇愛が乗っていないかを見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、六受が立つ",
            "toNext": "受に乗ると渇愛へ",
            "todayObserve": OBSERVE["MN9-P08"],
            "todayAction": actions["MN9-P08"],
            "when": ["快・不快を感じた", "受のあと動きたくなった"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN9-P08"][:40] + "…",
            "secondaryObserve": "感受の集起→渇愛の集起",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "苦の集＝渇愛（欲愛・有愛・非有愛）と見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、渇愛が集起する",
            "toNext": "止めないと執取へ",
            "todayObserve": OBSERVE["MN9-P04"],
            "todayAction": actions["MN9-P04"],
            "when": ["欲しがった", "拒んだ", "有を求めた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN9-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN9-P08"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "四取を知り、執着の流れを縁起で辿る",
            "chapterHint": SHORT,
            "fromPrev": "渇愛のあと、四取が掴む手前",
            "toNext": "掴むと苦が太る",
            "todayObserve": OBSERVE["MN9-P06"],
            "todayAction": actions["MN9-P06"],
            "when": ["見解に固まった", "戒や自己論に掴まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN9-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN9-P07"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "五取蘊の苦を苦諦として認める",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、苦が見える",
            "toNext": "見れば、明知と離すへ向き直る",
            "todayObserve": OBSERVE["MN9-P03"],
            "todayAction": actions["MN9-P03"],
            "when": ["生老病死が迫った", "五取蘊が重くなった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN9-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN9-P01"],
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "無明を捨て明知を生じ、現法で苦の終極へ",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、正見の実践へ戻る",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN9-P05"],
            "todayAction": actions["MN9-P05"],
            "when": ["無明を一つの知で破った", "随眠を捨てた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN9-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN9-P07"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "善不善の根・漏の滅を振り返り、正見を確かめる",
            "chapterHint": SHORT,
            "fromPrev": "一日の知は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN9-P12"],
            "todayAction": actions["MN9-P12"],
            "when": ["一日を閉じるとき", "正見が揺れた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN9-P12"][:40] + "…",
            "secondaryObserve": OBSERVE["MN9-P02"],
        },
    ]

    out = {
        "chapter": 9,
        "sutta": 9,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：正しい見解の経）",
        "suttas": ["MN 9 正見経（正しい見解の経）"],
        "source": {
            "primary": "パーリ・中部第9経（正見経／正しい見解の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含29大拘絺羅経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・正しい見解の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・大拘絺羅経（T1.461c）",
                    "url": SAT_URL,
                    "note": "漢訳は舎梨子・大拘絺羅の問答。對照表: 法雨道場",
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
            "focusReason": "正見経は各支の集・滅・道を知り、無明を捨て明知を生じ現法で苦の終極を為すことが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn009.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 9:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(9, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 12
    assert all(p["id"] == f"MN9-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/12; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
