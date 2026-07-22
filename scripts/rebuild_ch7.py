#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch7.json (阿羅漢品) to match ch1–ch6 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-07"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0565"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap07/"
)

QUOTES = {
    90: "旅を終え憂いを離れる者に、一切所に解脱した者に、一切の拘束（繋）を捨棄した者に、苦悶は見出されない。",
    91: "気づき（念）ある者たちは、〔家を〕出る。彼らは、家において喜ばない。湖を捨棄して〔去り行く〕白鳥たちのように、彼らは、家々を捨棄する。",
    92: "彼らに、蓄積が存在せず、彼らが、食のことを遍知しているなら──彼らの、解脱の境涯が、空にして、かつまた、相なきものであるなら──彼らの境遇（趣：死後に赴く所）は、虚空における鳥たちの〔行方〕のように、捉えどころがない。",
    93: "彼の、諸々の煩悩が完全に滅尽し、そして、〔彼が〕食に依存なき者であるなら──彼の、解脱の境涯が、空にして、かつまた、相なきものであるなら──彼の境処（境地・歩み）は、虚空における鳥たちの〔足跡〕のように、捉えどころがない。",
    94: "彼の、諸々の〔感官の〕機能（根）が、馭者によって善く調御された馬たちのように、〔心の〕止寂（奢摩他・止）に至ったなら、〔我想の〕思量（慢）を捨棄した煩悩なき者を、そのような者である彼を、天〔の神々〕たちもまた羨む。",
    95: "地に等しく、〔何ものにも〕遮られない者──インダの杭（城門に立てられた標柱）の如く、そのように善き掟の者──泥土を離去した〔澄んだ〕湖のような者──そのような者に、諸々の輪廻は有ることなくある。",
    96: "彼の意は、寂静と成る──そして、言葉も、さらに、行為も、寂静と〔成る〕──正しい了知による解脱者にして寂静なる者、そのような者であるなら。",
    97: "〔特定のものについて〕信なく、かつまた、作られざるもの（涅槃）について知あり、そして、〔輪廻の〕鎖を断ち切る、その人──〔造悪の〕機会を打ち砕き、〔自利の〕願望を吐き捨てた者──彼は、まさに、最上の人士である。",
    98: "もしくは、村であろうが、林であろうが、もしくは、低地であろうが、高地であろうが、そこにおいて、阿羅漢（人格完成者）たちが住むなら、その地は、喜ぶべきものとなる。",
    99: "すなわち、〔世俗の〕人が喜ばないところである、〔人里離れた〕諸々の林は、〔阿羅漢たちにとっては〕喜ぶべきものとなる。貪欲を離れた者たちは、〔そこにおいて〕喜ぶであろう。彼らは、欲望〔の対象〕を探し求める者たちにあらず。",
}

OBSERVE = {
    90: "〔有為の〕路を終えて憂患を離れ、一切に於て解脱し、一切の繋縛（けばく）を断ちたる人には苦悩なし。",
    91: "正念ある人は出家し、彼らは在家を喜ばず。 池を捨て去る鵞鳥の如く、彼らはいずれの家をも捨つ。",
    92: "蓄積することなく、正念食をなし、空にして無相の解脱を境とする人の道は、虚空に於ける鳥の〔道〕の如く、追随し難し。",
    93: "煩悩を滅尽し、飲食に捉われず、空にして無相の解脱を境とする人の跡は、虚空に於ける鳥の〔跡〕の如く、追随し難し。",
    94: "諸根寂静に帰して、御者によく調御（ちょうご）せられし馬の如く、慢を断ち、煩悩を滅尽せる人、天神といえどもこの如き人を羨む。",
    95: "敬虔なる聖者は、忍辱（にんにく）なること大地の如く、また門閾に似たり。 〔浄きこと〕泥土なき池〔水〕の如し。 この如き人には輪廻あることなし。",
    96: "正智によりて解脱し、安穏を得たる聖者の意は寂静なり。 語もまた業も寂静なり。",
    97: "妄信なく、無為（涅槃）を悟り、〔輪廻の〕繋縛（けばく）を断ち、〔善悪の〕契機を退け、欲望を捨てたる人こそ実に最上の人士なれ。",
    98: "村落に於ても、また森林に於ても、低地に於ても、また丘陵に於ても、阿羅漢の住する処、その地は楽し。",
    99: "森林は楽しむべし。 衆人の楽しまざる処に於て、離欲の人は楽しまん。 彼らは欲楽を求めざればなり。",
}

CHINESE = {
    90: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-001",
         "text": "去離憂患，脫於一切，縛結已解，冷而無煖。", "satLocus": "大正蔵 T4.565a 羅漢品第1頌"},
    91: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-002",
         "text": "心淨得念，無所貪樂，已度癡淵，如鴈棄池。", "satLocus": "大正蔵 T4.565a 羅漢品第2頌"},
    92: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-003",
         "text": "量腹而食，無所藏積，心空無想，度眾行地，如空中鳥，遠逝無礙。", "satLocus": "大正蔵 T4.565a 羅漢品第3頌"},
    93: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-004",
         "text": "世間習盡，不復仰食，虛心無患，已到脫處，譬如飛鳥，暫下輒逝。", "satLocus": "大正蔵 T4.565a 羅漢品第4頌"},
    94: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-005",
         "text": "制根從正，如馬調御，捨憍慢習，為天所敬。", "satLocus": "大正蔵 T4.565a 羅漢品第5頌"},
    95: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-006",
         "text": "不怒如地，不動如山，真人無垢，生死世絕。", "satLocus": "大正蔵 T4.565a 羅漢品第6頌"},
    96: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-007",
         "text": "心已休息，言行亦止，從正解脫，寂然歸滅。", "satLocus": "大正蔵 T4.565a 羅漢品第7頌"},
    97: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-008",
         "text": "棄欲無着，缺三界障，望意已絕，是謂上人。", "satLocus": "大正蔵 T4.565b 羅漢品第8頌"},
    98: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-009",
         "text": "在聚在野，平地高岸，應真所過，莫不蒙祐。", "satLocus": "大正蔵 T4.565b 羅漢品第9頌"},
    99: {"status": "mapped", "pin": "羅漢品（T210 第15品）", "t210": "T210-15-010",
         "text": "彼樂空閑，眾人不能，快哉無婬，無所欲求。", "satLocus": "大正蔵 T4.565b 羅漢品第10頌"},
}

VERSE_PRACTICE = {
    90: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "繋縛を断ちた者には苦悩がない"},
    91: {"nidanaId": "craving", "pathFactors": ["正念", "正精進"], "reason": "正念ある者は家に喜ばず、鵞鳥の如く離れる"},
    92: {"nidanaId": "clinging", "pathFactors": ["正念", "正命"], "reason": "蓄積なく正念食し、空・無相の道は捉え難い"},
    93: {"nidanaId": "craving", "pathFactors": ["正念", "正定"], "reason": "漏尽し飲食に捉われぬ足跡は鳥の如し"},
    94: {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "諸根を調御し慢を断った者を天も羨む"},
    95: {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "大地の如く忍辱し、泥土なき池の如く浄い"},
    96: {"nidanaId": "release", "pathFactors": ["正語", "正業"], "reason": "正智の解脱者は意・語・業が寂静である"},
    97: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "妄信なく涅槃を知り、望みを捨てた者が最上"},
    98: {"nidanaId": "contact", "pathFactors": ["正念", "正定"], "reason": "阿羅漢の住む処は、どこでも楽し"},
    99: {"nidanaId": "craving", "pathFactors": ["正念", "正定"], "reason": "離欲の人は欲を求めず、空閑を楽しむ"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP7-P01", 90), ("DP7-P02", 90),
    ("DP7-P03", 91),
    ("DP7-P04", 92),
    ("DP7-P05", 93),
    ("DP7-P06", 94),
    ("DP7-P07", 95), ("DP7-P08", 95),
    ("DP7-P09", 96),
    ("DP7-P10", 97),
    ("DP7-P11", 98), ("DP7-P12", 98),
    ("DP7-P13", 99), ("DP7-P14", 99),
]


def chinese_block(verse: int) -> dict:
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    c.setdefault(
        "note",
        "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号はパーリとずれる場合あり。",
    )
    return c


def main() -> None:
    old = json.loads((DATA / "ch7.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        pairs.append({
            "id": pid,
            "category": LABEL_TO_ID[factors[0]],
            "verse": verse,
            "observe": OBSERVE[verse],
            "action": actions[pid],
            "quote": QUOTES[verse],
            "nidanaId": vp["nidanaId"],
            "pathFactors": factors,
            "pathReason": vp["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー",
                    "locus": f"小部・ダンマパダ 阿羅漢の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第７章・阿羅漢品 第{verse}偈（#ch02-07）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第7章・阿羅漢品（阿羅漢の章）"
    SHORT = "阿羅漢品（阿羅漢の章）"
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
            "pathLabel": "どこに触れても、その場を清らかに住む",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見方が、今朝の接触の土台になる",
            "toNext": "阿羅漢の住む処は、どこでも楽しとなる",
            "todayObserve": OBSERVE[98],
            "todayAction": actions["DP7-P11"],
            "when": ["場所が変わった", "環境が整わない"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[98][:40] + "…",
            "secondaryObserve": "場ではなく、住む心が地を楽しにする",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "不快を大地の如く受け、諸根を調御する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、快・不快の受が立ち上がる",
            "toNext": "受け流せれば欲しがりに落ちにくい",
            "todayObserve": OBSERVE[95],
            "todayAction": actions["DP7-P07"],
            "when": ["不快が来た", "慢心が立ち上がった"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[95][:40] + "…",
            "secondaryObserve": "諸根を調御し慢を断った者を、天も羨む",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "家・食・欲への欲しがりを離す",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、居場所と快楽への欲しがりへ落ちる",
            "toNext": "止めないと蓄積と執着の掴みへ進む",
            "todayObserve": OBSERVE[91],
            "todayAction": actions["DP7-P03"],
            "when": ["居続けたい", "もっと欲しい"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[91][:40] + "…",
            "secondaryObserve": "離欲の人は欲を求めず、空閑を楽しむ",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正命"], "pathFactorIds": ["mindfulness", "livelihood"],
            "pathLabel": "蓄積と依存の掴みを手放す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、地位・承認・蓄積に乗る手前",
            "toNext": "掴むと跡が残り、鳥の道のようには離れられない",
            "todayObserve": OBSERVE[92],
            "todayAction": actions["DP7-P04"],
            "when": ["貯め込みたくなった", "承認に掴まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[92][:40] + "…",
            "secondaryObserve": "空にして無相の道は、追随し難い",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "繋縛が苦悶を生むと見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、心が重く苦悶する",
            "toNext": "見れば、断ち離す道が開く",
            "todayObserve": OBSERVE[90],
            "todayAction": actions["DP7-P02"],
            "when": ["こうでなければと苦しむ", "束縛を感じる"],
            "sources": by_nidana.get("suffering", []) or by_nidana.get("release", [])[:2],
            "leadQuote": QUOTES[90][:40] + "…",
            "secondaryObserve": "繋縛を断ちた者には苦悩がない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "繋縛・妄信・願望を断ちて離す",
            "chapterHint": SHORT,
            "fromPrev": "執着と慢心が流れを加速させる",
            "toNext": "意・語・業が寂静になれば、安穏に近づく",
            "todayObserve": OBSERVE[97],
            "todayAction": actions["DP7-P10"],
            "when": ["信じ込みが強い", "望みにしがみついた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[97][:40] + "…",
            "secondaryObserve": "正智の解脱者は、意・語・業が寂静である",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "欲を求めず静けさを味わったかを振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の語り・行いは朝からの心の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE[99],
            "todayAction": actions["DP7-P14"],
            "when": ["一日を閉じるとき", "賑やかさに疲れた日"],
            "sources": by_nidana.get("review", []) or [p["id"] for p in pairs if p["verse"] == 99],
            "leadQuote": QUOTES[99][:40] + "…",
            "secondaryObserve": "スマホを置き、ただ静かに座る",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 7,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第7章（阿羅漢品／阿羅漢の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210羅漢品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・阿羅漢の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第７章・阿羅漢品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・羅漢品（T4.565a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "阿羅漢品は繋縛の断尽・離欲・寂静が中心。既定の焦点は離す。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch7.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch7.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 8):
        d = json.loads((DATA / f"ch{ch_id}.json").read_text(encoding="utf-8"))
        by_path = defaultdict(list)
        for p in d["pairs"]:
            labels = set(p.get("pathFactors") or [])
            cat = p.get("category")
            for lab, pid in LABEL_TO_ID.items():
                if lab in labels or cat == pid:
                    by_path[pid].append(p["id"])
        for pid in PATH_ORDER:
            ids = sorted(set(by_path[pid]), key=lambda x: int(x.split("-P")[1]))
            if not ids:
                continue
            entries[pid].append({
                "collectionId": "dhammapada",
                "collectionName": "ダンマパダ",
                "chapterId": ch_id,
                "shortTitle": d["shortTitle"],
                "title": d["title"],
                "pairCount": len(ids),
                "pairIds": ids,
            })

    psi = {"version": 1, "scope": "dhammapada-ch1-ch7", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])
    for k, v in entries.items():
        print(k, [(e["chapterId"], e["pairCount"]) for e in v])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 14
    assert all(p["id"] == f"DP7-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(90, 100))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    print("OK")


if __name__ == "__main__":
    main()
