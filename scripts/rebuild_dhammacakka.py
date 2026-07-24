#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build data/dhammacakka/ — 初転法輪 as a standalone collection (like Dhammapada).

Spine: 四諦通し（二辺·中道 → 苦·集·滅·道 → 三転十二行相 → 法輪転起）
Origin track (初転のみ): 苦諦→集諦→滅諦→道諦（汎用7支縁起ではない）
Path track: 八正道（道諦の中身）
Source: SN 56.11 / アラナ · true-buddhism · 雑阿含379（SAT）
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dhammacakka"

ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E7%9B%B8%E5%BF%9C%E9%83%A8%E7%B5%8C%E5%85%B8"
)
TB_URL = "https://true-buddhism.com/sutra/palisanzo/"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0103c13"
MAP_URL = "https://dhammarain.github.io/canon/sutta/S-vs-SA-dhammarain.pdf"

CATEGORIES = [
    {"id": "dukkha", "name": "苦諦", "short": "苦", "weekday": 1, "order": 1},
    {"id": "samudaya", "name": "集諦", "short": "集", "weekday": 2, "order": 2},
    {"id": "nirodha", "name": "滅諦", "short": "滅", "weekday": 3, "order": 3},
    {"id": "magga", "name": "道諦", "short": "道", "weekday": 4, "order": 4},
]

# 初転法輪専用：縁起トラック＝四聖諦の流れ（触→受→欲…ではない）
ORIGIN_NODES = [
    {"id": "dukkha", "label": "苦諦"},
    {"id": "samudaya", "label": "集諦"},
    {"id": "nirodha", "label": "滅諦"},
    {"id": "magga", "label": "道諦"},
]

PATH_FACTORS_META = [
    {"id": "view", "label": "正見"}, {"id": "intention", "label": "正思惟"},
    {"id": "speech", "label": "正語"}, {"id": "action", "label": "正業"},
    {"id": "livelihood", "label": "正命"}, {"id": "effort", "label": "正精進"},
    {"id": "mindfulness", "label": "正念"}, {"id": "concentration", "label": "正定"},
]

LABEL_TO_ID = {m["label"]: m["id"] for m in PATH_FACTORS_META}
ALL_EIGHT = [m["label"] for m in PATH_FACTORS_META]

# chapters: id, file, title, shortTitle, focusNodeId, focusReason, pairs
CHAPTERS = [
    {
        "id": 1,
        "file": "ch1.json",
        "title": "初転法輪・二辺と中道",
        "shortTitle": "二辺と中道",
        "mapNote": "SN 56.11 · 鹿野苑 · 二辺を離れた中道",
        "focusNodeId": "magga",
        "focusReason": "二辺（欲楽·苦行）を離れ、中道＝八正道へ向かうのが主題。",
        "pairs": [
            {
                "id": "FT-P01",
                "category": "magga",
                "section": "二辺",
                "nidanaId": "samudaya",
                "pathFactors": ["正見", "正思惟"],
                "pathReason": "欲楽·苦行への傾きを、苦を増やす集（掴み）として見る",
                "observe": (
                    "二つの辺——欲における欲楽の実践と、自己を苦しめる実践。"
                    "どちらも出家者の道ではなく、利益を伴わない。"
                ),
                "action": "朝、今日の行いが「欲しがり」か「無理な苦行」に寄っていないか一度見る",
                "quote": (
                    "比丘たちよ、出家者によって従うべきでない二つの辺がある。"
                    "諸々の欲における欲楽の実践——これは下劣であり、粗野であり、凡夫のものであり、"
                    "聖ならざるものであり、利益を伴わないものである。"
                    "および自己を苦しめる実践——これは苦であり、聖ならざるものであり、"
                    "利益を伴わないものである。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）／類縁",
                    "text": "（二辺を離れて中道を説く——パーリ詳説。漢訳SA379は四諦三転が中心。）",
                    "satLocus": "大正蔵 T2.103c 転法輪（類縁）",
                    "note": "二辺の明示はパーリが詳しい。漢は四諦三転が主。",
                },
            },
            {
                "id": "FT-P02",
                "category": "magga",
                "section": "中道",
                "nidanaId": "magga",
                "pathFactors": ["正見", "正念"],
                "pathReason": "二辺を離れ、中道（道諦）に触れる",
                "observe": (
                    "中道——如来が現正覚した道。"
                    "眼を生じ、智を生じ、寂静·勝智·正覚·涅槃へ導く。"
                ),
                "action": "今日、「中道」を一言思い出し、極端に寄らない一歩を一つ取る",
                "quote": (
                    "比丘たちよ、これらの二つの辺に近づかず、中道が如来によって現正覚された。"
                    "それは眼を生じ、智を生じ、寂静へ、勝智へ、正覚へ、涅槃へ転起するものである。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）／類縁",
                    "text": "（中道＝八支聖道。SA379は道跡聖諦として八正道を含む。）",
                    "satLocus": "大正蔵 T2.103c 転法輪（類縁）",
                    "note": "中道の核は道諦と一体。",
                },
            },
            {
                "id": "FT-P03",
                "category": "magga",
                "section": "八正道",
                "nidanaId": "magga",
                "pathFactors": ALL_EIGHT,
                "pathReason": "中道の中身として八支聖道を一度通しで見る",
                "observe": (
                    "その中道とは、まさにこの八支の聖道である——"
                    "正見·正思惟·正語·正業·正命·正精進·正念·正定。"
                ),
                "action": "今日、八正道のうち一支を選び、一つの行為に結びつける",
                "quote": (
                    "比丘たちよ、では、その中道とは何か。"
                    "まさにこの八支の聖道である——"
                    "すなわち正見、正思惟、正語、正業、正命、正精進、正念、正定である。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "此苦滅道跡聖諦……正見、正志、正語、正業、正命、正方便、正念、正定。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪",
                    "note": "道跡聖諦として八正道。",
                },
            },
        ],
    },
    {
        "id": 2,
        "file": "ch2.json",
        "title": "初転法輪・苦諦",
        "shortTitle": "苦諦",
        "mapNote": "SN 56.11 · 苦聖諦",
        "focusNodeId": "dukkha",
        "focusReason": "苦諦——生老病死·五取蘊を苦として見るのが主題。",
        "pairs": [
            {
                "id": "FT-P04",
                "category": "dukkha",
                "section": "苦聖諦",
                "nidanaId": "dukkha",
                "pathFactors": ["正見", "正念"],
                "pathReason": "今日の苦を、苦聖諦の一側面として見る",
                "observe": (
                    "苦聖諦——生は苦、老は苦、病は苦、死は苦。"
                    "愁·悲·苦·憂·悩は苦。怨憎会·愛別離·求不得は苦。"
                    "要約すれば、五つの執取の集まりは苦である。"
                ),
                "action": "今日生じた苦しみを一つ特定し、「これが苦諦の一側面」と静かに観る",
                "quote": (
                    "比丘たちよ、これが苦聖諦である。"
                    "生は苦であり、老もまた苦であり、病もまた苦であり、死もまた苦である。"
                    "愁·悲·苦·憂·悩は苦である。"
                    "怨憎の者と会うことは苦、愛する者と別れることは苦、求めて得られないことは苦である。"
                    "要約すれば、五つの執取の集まりは苦である。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "此苦聖諦……生苦、老苦、病苦、死苦、恩愛別離苦、怨憎會苦、所求不得苦。略說五受陰苦。",
                    "satLocus": "大正蔵 T2.103c 転法輪",
                    "note": "苦聖諦の列挙。",
                },
            },
            {
                "id": "FT-P05",
                "category": "dukkha",
                "section": "五取蘊",
                "nidanaId": "dukkha",
                "pathFactors": ["正見", "正念"],
                "pathReason": "掴んでいる集まりを、苦の要約として一度見る",
                "observe": (
                    "五取蘊——色·受·想·行·識への執取の集まりが、苦の要約である。"
                    "「これは私のもの」と掴むところに、苦がまとまる。"
                ),
                "action": "今日「これは私のもの」と掴んだ一つを、五取蘊の苦として一度見る",
                "quote": (
                    "要約すれば、五つの執取の集まりは苦である。"
                    "（色·受·想·行·識に対する執取——それが苦の要約である。）"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "略說五受陰苦。",
                    "satLocus": "大正蔵 T2.103c 転法輪",
                    "note": "五受陰（五取蘊）苦。",
                },
            },
        ],
    },
    {
        "id": 3,
        "file": "ch3.json",
        "title": "初転法輪・集諦",
        "shortTitle": "集諦",
        "mapNote": "SN 56.11 · 苦集聖諦",
        "focusNodeId": "samudaya",
        "focusReason": "集諦——渇愛が苦の集起であるのが主題。",
        "pairs": [
            {
                "id": "FT-P06",
                "category": "samudaya",
                "section": "苦集聖諦",
                "nidanaId": "samudaya",
                "pathFactors": ["正思惟", "正念"],
                "pathReason": "渇愛を、苦の集として名づける",
                "observe": (
                    "苦集聖諦——まさにこの渇愛である。"
                    "再有を伴い、喜びと貪を伴い、そこかしこに歓喜するもの——"
                    "欲渇愛·有渇愛·無有渇愛。"
                ),
                "action": "今日生じた渇愛を一つ特定し、「これが苦の集である」と名づけて観る",
                "quote": (
                    "比丘たちよ、これが苦集聖諦である。"
                    "まさにこの渇愛である——再有を伴い、喜びと貪を伴い、そこかしこに歓喜するもの——"
                    "すなわち欲渇愛·有渇愛·無有渇愛である。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "此苦集聖諦……當知是愛喜、倶行、愛樂、彼彼喜樂……謂欲愛、有愛、無有愛。",
                    "satLocus": "大正蔵 T2.103c 転法輪",
                    "note": "集＝愛（渇愛）。",
                },
            },
            {
                "id": "FT-P07",
                "category": "samudaya",
                "section": "三種の渇愛",
                "nidanaId": "samudaya",
                "pathFactors": ["正念", "正精進"],
                "pathReason": "欲·有·無有のどれに近いか一度見る",
                "observe": (
                    "三種の渇愛——"
                    "欲しがる（欲渇愛）、あり続けたい（有渇愛）、無くしたい（無有渇愛）。"
                    "いずれも再有を招き、そこかしこに歓喜する。"
                ),
                "action": "今日の欲しがりが「欲·有·無有」のどれに近いか、一度だけ名づける",
                "quote": (
                    "欲渇愛·有渇愛·無有渇愛——"
                    "再有を伴い、喜びと貪を伴い、そこかしこに歓喜する渇愛である。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "謂欲愛、有愛、無有愛。",
                    "satLocus": "大正蔵 T2.103c 転法輪",
                    "note": "三愛。",
                },
            },
        ],
    },
    {
        "id": 4,
        "file": "ch4.json",
        "title": "初転法輪・滅諦",
        "shortTitle": "滅諦",
        "mapNote": "SN 56.11 · 苦滅聖諦",
        "focusNodeId": "nirodha",
        "focusReason": "滅諦——渇愛の残りなき離欲·滅が主題。",
        "pairs": [
            {
                "id": "FT-P08",
                "category": "nirodha",
                "section": "苦滅聖諦",
                "nidanaId": "nirodha",
                "pathFactors": ["正見", "正念"],
                "pathReason": "渇愛を離欲する方向へ意図を戻す",
                "observe": (
                    "苦滅聖諦——その渇愛の残りなき離欲·消滅·放棄·捨離·解脱·無執着。"
                    "集が滅するとき、苦も滅する。"
                ),
                "action": "渇愛が来たら「この渇愛を離欲する」と意図し、呼吸三回に意識を戻す",
                "quote": (
                    "比丘たちよ、これが苦滅聖諦である。"
                    "まさにその渇愛の残りなき離欲·消滅·放棄·捨離·解脱·無執着である。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "此苦滅聖諦……彼彼愛喜無餘斷吐盡無欲滅沒息沒。",
                    "satLocus": "大正蔵 T2.103c 転法輪",
                    "note": "滅＝愛の無余断。",
                },
            },
            {
                "id": "FT-P09",
                "category": "nirodha",
                "section": "離欲",
                "nidanaId": "nirodha",
                "pathFactors": ["正精進", "正念"],
                "pathReason": "一つ手放すことで滅の方向を味わう",
                "observe": (
                    "離欲——掴みを一つ手放すとき、滅の方向が少し見える。"
                    "残りなく断つことが滅諦の核心である。"
                ),
                "action": "今日、小さな欲しがりを一つだけ手放し、「離欲の方向」と静かに認める",
                "quote": (
                    "その渇愛の残りなき離欲·消滅·放棄·捨離·解脱·無執着——"
                    "これが苦の滅である。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）／類縁",
                    "text": "彼彼愛喜無餘斷吐盡無欲滅沒息沒。",
                    "satLocus": "大正蔵 T2.103c 転法輪（類縁）",
                    "note": "無欲·滅。",
                },
            },
        ],
    },
    {
        "id": 5,
        "file": "ch5.json",
        "title": "初転法輪・道諦",
        "shortTitle": "道諦",
        "mapNote": "SN 56.11 · 苦滅道跡聖諦 · 八正道",
        "focusNodeId": "magga",
        "focusReason": "道諦——八正道が苦滅への道跡であるのが主題。",
        "pairs": [
            {
                "id": "FT-P10",
                "category": "magga",
                "section": "苦滅道跡聖諦",
                "nidanaId": "magga",
                "pathFactors": ALL_EIGHT,
                "pathReason": "道諦として八支聖道を通しで見る",
                "observe": (
                    "苦滅道跡聖諦——苦の滅へ至る道は、まさにこの八支の聖道である。"
                    "中道としてすでに示された道が、ここに道諦として再び立てられる。"
                ),
                "action": "今日の修行を八正道のうち一支に意識的に結びつける",
                "quote": (
                    "比丘たちよ、これが苦滅へ至る道の聖諦である。"
                    "まさにこの八支の聖道である——"
                    "すなわち正見、正思惟、正語、正業、正命、正精進、正念、正定である。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "此苦滅道跡聖諦……正見、正志、正語、正業、正命、正方便、正念、正定。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪",
                    "note": "道跡＝八正道。",
                },
            },
            {
                "id": "FT-P11",
                "category": "magga",
                "section": "正見・正思惟",
                "nidanaId": "magga",
                "pathFactors": ["正見", "正思惟"],
                "pathReason": "四諦を見る正見と、離欲へ向かう正思惟から入る",
                "observe": (
                    "正見——苦·集·滅·道をあるがままに見る入口。"
                    "正思惟——出離·無恚·無害へ心を向ける。"
                    "（経は八支を列挙する。繰り返し読むために、まず慧の二支を味わう。）"
                ),
                "action": "朝、四諦を一言ずつ（苦·集·滅·道）確認し、今日の観察の入口とする",
                "quote": (
                    "八支の聖道——正見、正思惟……。"
                    "正見があって道は苦の滅へ転起し、正思惟は出離の意図として道を支える。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）／類縁",
                    "text": "正見、正志……（道跡聖諦の冒頭二支）。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪（類縁）",
                    "note": "正見·正志（正思惟）。繰り返し用の分割。",
                },
            },
            {
                "id": "FT-P12",
                "category": "magga",
                "section": "正語・正業・正命",
                "nidanaId": "magga",
                "pathFactors": ["正語", "正業", "正命"],
                "pathReason": "身口意の行いを、道の支えとして整える",
                "observe": (
                    "正語·正業·正命——言葉·行為·生計が、苦を増やさない方向へ整う。"
                    "（経は八支を一列に示す。繰り返し読むために、戒の三支を味わう。）"
                ),
                "action": "今日、言葉か行為か生計のうち一つを選び、「道の支え」として一度整える",
                "quote": (
                    "八支の聖道——……正語、正業、正命……。"
                    "道は見と意図だけでは足りず、行いの場でも修される。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）／類縁",
                    "text": "正語、正業、正命……（道跡聖諦の中間三支）。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪（類縁）",
                    "note": "正語·正業·正命。繰り返し用の分割。",
                },
            },
            {
                "id": "FT-P13",
                "category": "magga",
                "section": "正精進・正念・正定",
                "nidanaId": "magga",
                "pathFactors": ["正精進", "正念", "正定"],
                "pathReason": "断つ・守る・集める心の働きを道として修する",
                "observe": (
                    "正精進·正念·正定——"
                    "不善を防ぎ断ち、善を生じ満たす精進。"
                    "身·受·心·法をあるがままに憶念する正念。"
                    "一心に安定する正定。"
                    "（経は八支を一列に示す。繰り返し読むために、定の三支を味わう。）"
                ),
                "action": "今日、精進·念·定のうち一支を選び、一つの行為に結びつける",
                "quote": (
                    "八支の聖道——……正精進、正念、正定である。"
                    "道は修されるべきものであり、修されたときに法輪は清浄となる。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）／類縁",
                    "text": "正方便、正念、正定……（道跡聖諦の後三支）。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪（類縁）",
                    "note": "正方便·正念·正定。繰り返し用の分割。",
                },
            },
        ],
    },
    {
        "id": 6,
        "file": "ch6.json",
        "title": "初転法輪・三転十二行相",
        "shortTitle": "三転十二行相",
        "mapNote": "SN 56.11 · 示·勧·証の三転",
        "focusNodeId": "dukkha",
        "focusReason": "三転——知る／なすべき／すでに、の十二行相が主題。",
        "pairs": [
            {
                "id": "FT-P14",
                "category": "dukkha",
                "section": "示転",
                "nidanaId": "dukkha",
                "pathFactors": ["正見", "正念"],
                "pathReason": "四諦を「これである」と示す知に触れる",
                "observe": (
                    "示転——「これは苦である」「これは集である」「これは滅である」「これは道である」。"
                    "かつて聞かなかった法について、眼·智·明·覚が生じる。"
                ),
                "action": "朝、「苦を知ること·集を断つこと·滅を証すること·道を修すること」と四諦の課題を一言確認する",
                "quote": (
                    "比丘たちよ、この苦聖諦は、かつて聞かなかった諸法について——"
                    "眼が生じた、智が生じた、慧が生じた、明が生じた、光が生じた。"
                    "（集·滅·道についても、同じく眼·智·明·光が生じた。）"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "此苦聖諦本所未曾聞法，當正思惟時，生眼、智、明、覺；此苦集、此苦滅、此苦滅道跡聖諦……生眼、智、明、覺。",
                    "satLocus": "大正蔵 T2.103c 転法輪",
                    "note": "示転——本未曾聞に眼智明覚。",
                },
            },
            {
                "id": "FT-P15",
                "category": "samudaya",
                "section": "勧転",
                "nidanaId": "samudaya",
                "pathFactors": ["正精進", "正念"],
                "pathReason": "集は断つべき、と勧める方向へ精進する",
                "observe": (
                    "勧転——苦は遍知すべき、集は断つべき、滅は証すべき、道は修すべき。"
                    "「これである」から「なすべき」へ転ずる。"
                ),
                "action": "今日、「集は断つべき」と一度意図し、小さな欲しがりを一つ弱める",
                "quote": (
                    "この苦聖諦は遍知されるべきである……"
                    "この苦集聖諦は断たれるべきである……"
                    "この苦滅聖諦は証されるべきである……"
                    "この苦滅道跡聖諦は修されるべきである——"
                    "眼が生じた、智が生じた……。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "苦聖諦智當復知……苦集聖諦已知當斷……苦滅聖諦已知當作證……苦滅道跡聖諦已知當修……生眼、智、明、覺。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪",
                    "note": "勧転——当知·当断·当証·当修。",
                },
            },
            {
                "id": "FT-P16",
                "category": "nirodha",
                "section": "証転",
                "nidanaId": "nirodha",
                "pathFactors": ["正見", "正念"],
                "pathReason": "すでに知った·断った方向を振り返る",
                "observe": (
                    "証転——苦は遍知された、集は断たれた、滅は証された、道は修された。"
                    "「なすべき」から「すでに」へ転ずる。"
                ),
                "action": "就寝前、今日「知った·断とうとした·離れた·修した」を一つずつ認める",
                "quote": (
                    "この苦聖諦は遍知された……"
                    "この苦集聖諦は断たれた……"
                    "この苦滅聖諦は証された……"
                    "この苦滅道跡聖諦は修された——"
                    "眼が生じた、智が生じた……。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "苦聖諦智已知……苦集聖諦已知已斷……苦滅聖諦已知已作證……苦滅道跡聖諦已知已修……生眼、智、明、覺。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪",
                    "note": "証転——已知·已断·已証·已修。",
                },
            },
        ],
    },
    {
        "id": 7,
        "file": "ch7.json",
        "title": "初転法輪・法輪転起",
        "shortTitle": "法輪転起",
        "mapNote": "SN 56.11 · 正覚の宣言 · 憍陳如",
        "focusNodeId": "magga",
        "focusReason": "三転十二行相が清浄となって法輪が転起し、正覚が宣言される。",
        "pairs": [
            {
                "id": "FT-P17",
                "category": "magga",
                "section": "正覚の宣言",
                "nidanaId": "magga",
                "pathFactors": ["正見", "正念"],
                "pathReason": "知見が清浄になるまで覚を宣言しない、という基準を見る",
                "observe": (
                    "四諦の三転十二行相について如実の知見が清浄となるまで——"
                    "正覚を宣言しなかった。"
                    "清浄となったとき、無上の正等覚を現正覚したと宣言した。"
                ),
                "action": "今日の学びを「まだ途中」と認め、一つの行相（知る／断つ／証する／修する）に戻る",
                "quote": (
                    "比丘たちよ、私のこの四聖諦における三転十二行の如実の知見が、"
                    "清浄とならなかったあいだは——"
                    "天·魔·梵の世、沙門·婆羅門·神々と人間たちからなる衆において、"
                    "無上の正等覚を現正覚したとは宣言しなかった。"
                    "しかし、如実の知見が清浄となったとき、宣言した。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "我於此四聖諦三轉十二行……生眼智明覺故……自證得成阿耨多羅三藐三菩提。",
                    "satLocus": "大正蔵 T2.104 転法輪",
                    "note": "三転十二行が清浄→正覚の宣言。",
                },
            },
            {
                "id": "FT-P18",
                "category": "dukkha",
                "section": "憍陳如の法眼",
                "nidanaId": "dukkha",
                "pathFactors": ["正見", "正念"],
                "pathReason": "生滅の法眼に触れる",
                "observe": (
                    "憍陳如に塵なく汚れなき法の眼が生じた——"
                    "「生起する性質のものは、滅尽する性質のものである」。"
                ),
                "action": "今日見た一つの出来事に「生じたものは滅する」と一度当てはめる",
                "quote": (
                    "そして、この説示が説かれているとき、尊者コンダンニャに、"
                    "塵なく汚れなき法の眼が生じた——"
                    "『生起する性質のものは、すべて滅尽する性質のものである』と。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "尊者憍陳如……遠塵離垢得法眼淨……「一切集法皆是滅法」。",
                    "satLocus": "大正蔵 T2.104 転法輪",
                    "note": "憍陳如の法眼。",
                },
            },
            {
                "id": "FT-P19",
                "category": "magga",
                "section": "転法輪",
                "nidanaId": "magga",
                "pathFactors": ["正見", "正念"],
                "pathReason": "法輪が転起した一日を振り返る",
                "observe": (
                    "無上の法輪が転起された——"
                    "沙門·婆羅門·天·魔·梵によって転じ戻され得ない。"
                    "「コンダンニャは悟った」と、諸天が声を上げた。"
                ),
                "action": "就寝前、今日の苦·集·滅·道の体験を一つずつ思い返し、清らかな修行を続けた一日を静かに認める",
                "quote": (
                    "こうして、比丘たちよ、バーラーナシーのイスパティアナの鹿の園において、"
                    "無上の法輪が転起された——"
                    "それは沙門によっても、婆羅門によっても、天によっても、魔によっても、"
                    "梵によっても、世の誰によっても転じ戻され得ないものである。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "世尊於波羅㮈國仙人住處鹿野苑中轉法輪……沙門婆羅門若天魔梵……所不能轉。",
                    "satLocus": "大正蔵 T2.104 転法輪",
                    "note": "法輪転起。",
                },
            },
        ],
    },
]


def source_block():
    return {
        "primary": "パーリ・相応部 SN 56.11（転法輪経／法輪転起経）観察ペア単位対応",
        "note": (
            "経典の言葉＝パーリSN56.11（アラナ精舎系和訳表記）、"
            "現代語訳＝南伝大蔵経系の読みやすい現代語表記（true-buddhismが南伝大蔵経を公開）、"
            "対応漢訳＝雑阿含379転法輪（T99）。"
            "初転法輪——二辺·中道·四諦·三転十二行相。"
            "縁起トラックは四聖諦（苦→集→滅→道）。八正道は道諦の中身。"
        ),
        "verifyLinks": {
            "pali": {
                "label": "アラナ精舎（相応部・転法輪／法輪転起）",
                "url": ARANA_URL,
                "note": "パーリ和訳出典",
            },
            "modern": {
                "label": "true-buddhism（南伝大蔵経・相応部）",
                "url": TB_URL,
                "note": "南伝大蔵経系の現代語表記",
            },
            "chinese": {
                "label": "SAT 雑阿含・転法輪（T2.103c）",
                "url": SAT_URL,
                "note": "對照: 雑阿含379（類縁T109等）",
            },
        },
        "chineseMapTable": MAP_URL,
    }


def alignment_for(pair):
    c = dict(pair["chinese"])
    c.setdefault("satUrl", SAT_URL)
    c["mapTableUrl"] = MAP_URL
    c.setdefault("t26", "")
    return {
        "pali": {
            "source": "アラナ精舎 経典ライブラリー（相応部・転法輪経／パーリSN56.11）",
            "locus": f"相応部・転法輪経（SN56.11）·{pair['section']}",
            "url": ARANA_URL,
        },
        "modern": {
            "source": "true-buddhism（南伝大蔵経系・現代語表記）",
            "locus": "相応部 · 諦相応 · 転法輪経（南伝公開目次）",
            "url": TB_URL,
        },
        "chinese": c,
    }


def pf_ids(labels):
    return [LABEL_TO_ID[l] for l in labels if l in LABEL_TO_ID]


def _first_for(pairs, nidana, field, default=""):
    for p in pairs:
        if p["nidanaId"] == nidana:
            return p[field]
    return default


def practice_nodes(pairs, short):
    """四諦ノード。pair.nidanaId と一致させる。"""
    by_nidana = {}
    for p in pairs:
        by_nidana.setdefault(p["nidanaId"], []).append(p["id"])
    lead = pairs[0]

    specs = [
        {
            "id": "dukkha",
            "weekday": 1,
            "categoryId": "dukkha",
            "nidanaLabel": "苦聖諦",
            "pathFactors": ["正見", "正念"],
            "pathLabel": "苦を苦として見る",
            "pathReason": "今日の苦を、苦聖諦の一側面として認める",
            "fromPrev": "道を修したあと、再び苦が見える",
            "toNext": "苦が見えれば、集（渇愛）へ問う",
            "when": ["苦を認めた"],
            "fallbackObserve": "苦を苦として一度認める",
            "fallbackAction": "今日の苦を一つ特定して観る",
        },
        {
            "id": "samudaya",
            "weekday": 2,
            "categoryId": "samudaya",
            "nidanaLabel": "苦集聖諦",
            "pathFactors": ["正思惟", "正念"],
            "pathLabel": "渇愛を集として名づける",
            "pathReason": "欲しがりを、苦の集起として見る",
            "fromPrev": "苦のあと、集（渇愛）が手前に立つ",
            "toNext": "集を見れば、滅（離欲）へ向かう",
            "when": ["渇愛を名づけた"],
            "fallbackObserve": "渇愛を集と見る",
            "fallbackAction": "今日の欲しがりを一つ名づける",
        },
        {
            "id": "nirodha",
            "weekday": 3,
            "categoryId": "nirodha",
            "nidanaLabel": "苦滅聖諦",
            "pathFactors": ["正見", "正念"],
            "pathLabel": "渇愛を離欲し、滅へ向かう",
            "pathReason": "掴みを手放す方向へ意図を戻す",
            "fromPrev": "集が見えれば、離欲へ戻る",
            "toNext": "離せば、道（八正道）を修する",
            "when": ["離欲した"],
            "fallbackObserve": "渇愛を離欲する",
            "fallbackAction": "小さな欲しがりを一つ手放す",
        },
        {
            "id": "magga",
            "weekday": 4,
            "categoryId": "magga",
            "nidanaLabel": "苦滅道跡聖諦",
            "pathFactors": ["正見", "正念"],
            "pathLabel": "八正道を道として修する",
            "pathReason": "中道＝八支聖道を、苦滅への道跡として歩む",
            "fromPrev": "滅の方向が見えれば、道を修する",
            "toNext": "道を修したあと、再び苦を見直す",
            "when": ["道を修した"],
            "fallbackObserve": "八正道の一支に触れる",
            "fallbackAction": "一支を今日の行為に結びつける",
        },
    ]

    nodes = []
    for spec in specs:
        nid = spec["id"]
        factors = spec["pathFactors"]
        # Prefer factors from a pair on this node when present
        pair_factors = _first_for(pairs, nid, "pathFactors", factors)
        if pair_factors:
            factors = pair_factors[:3] if len(pair_factors) > 3 and nid != "magga" else (
                pair_factors if len(pair_factors) <= 3 else ["正見", "正念"]
            )
            # For magga with all eight, keep 正見·正念 as node highlight default
            if len(pair_factors) > 3:
                factors = ["正見", "正念"]
        observe = _first_for(pairs, nid, "observe", spec["fallbackObserve"])
        action = _first_for(pairs, nid, "action", spec["fallbackAction"] or lead["action"])
        quote = _first_for(pairs, nid, "quote", lead["quote"])
        nodes.append({
            "id": nid,
            "weekday": spec["weekday"],
            "categoryId": spec["categoryId"],
            "nidanaLabel": spec["nidanaLabel"],
            "pathFactors": factors,
            "pathFactorIds": pf_ids(factors),
            "pathLabel": spec["pathLabel"],
            "pathReason": spec["pathReason"],
            "chapterHint": short,
            "fromPrev": spec["fromPrev"],
            "toNext": spec["toNext"],
            "todayObserve": observe,
            "todayAction": action,
            "when": spec["when"],
            "sources": by_nidana.get(nid, [lead["id"]] if nid == lead["nidanaId"] else []),
            "leadQuote": (quote[:48] + "…") if quote else "",
            "secondaryObserve": "",
        })
    return nodes


def write_chapter(ch):
    pairs_out = []
    for p in ch["pairs"]:
        pairs_out.append({
            "id": p["id"],
            "category": p["category"],
            "ref": "SN 56.11",
            "section": p["section"],
            "observe": p["observe"],
            "action": p["action"],
            "quote": p["quote"],
            "nidanaId": p["nidanaId"],
            "pathFactors": p["pathFactors"],
            "pathReason": p["pathReason"],
            "alignment": alignment_for(p),
        })

    out = {
        "chapter": ch["id"],
        "sutta": 11,
        "title": ch["title"],
        "shortTitle": ch["shortTitle"],
        "mapNote": ch["mapNote"],
        "suttas": ["SN 56.11 転法輪経（法輪転起経）"],
        "source": source_block(),
        "categories": CATEGORIES,
        "practicePath": {
            "model": "four-noble-truths",
            "chapterTitle": ch["title"],
            "shortTitle": ch["shortTitle"],
            "spineOrigin": "苦諦を見た→集諦（渇愛）を見た→滅諦へ離した→道諦を修した",
            "spinePath": "四諦を通しで見る。八正道は道諦（中道）の中身",
            "originNodes": ORIGIN_NODES,
            "pathFactors": PATH_FACTORS_META,
            "nodes": practice_nodes(ch["pairs"], ch["shortTitle"]),
            "focusNodeId": ch["focusNodeId"],
            "focusReason": ch["focusReason"],
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs_out,
    }
    path = DATA / ch["file"]
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(pairs_out)


def update_path_scene(all_pairs_by_chapter):
    """Register 道諦 pairs under eightfold scene index where pathFactors apply."""
    psi_path = ROOT / "data" / "path-scene-index.json"
    psi = json.loads(psi_path.read_text(encoding="utf-8"))
    # remove old dhammacakka entries
    for pid, entries in list(psi.get("entries", {}).items()):
        psi["entries"][pid] = [
            e for e in entries if e.get("collectionId") != "dhammacakka"
        ]

    from collections import defaultdict
    by_path = defaultdict(list)
    titles = {}
    for ch_id, (short, title, pairs) in all_pairs_by_chapter.items():
        titles[ch_id] = (short, title)
        for p in pairs:
            for lab in p["pathFactors"]:
                by_path[(LABEL_TO_ID[lab], ch_id)].append(p["id"])

    for (path_id, ch_id), ids in by_path.items():
        short, title = titles[ch_id]
        ids = sorted(set(ids), key=lambda x: int(x.split("-P")[1]))
        psi["entries"].setdefault(path_id, []).append({
            "collectionId": "dhammacakka",
            "collectionName": "初転法輪",
            "chapterId": ch_id,
            "shortTitle": short,
            "title": title,
            "pairCount": len(ids),
            "pairIds": ids,
        })

    scope = psi.get("scope", "")
    if "dhammacakka" not in scope:
        psi["scope"] = scope + "+dhammacakka-ch1-ch7" if scope else "dhammacakka-ch1-ch7"
    psi_path.write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    index_chapters = []
    total = 0
    all_pairs = {}
    for ch in CHAPTERS:
        n = write_chapter(ch)
        total += n
        index_chapters.append({
            "id": ch["id"],
            "file": ch["file"],
            "title": ch["title"],
            "shortTitle": ch["shortTitle"],
            "pairCount": n,
            "mapNote": ch["mapNote"],
        })
        all_pairs[ch["id"]] = (ch["shortTitle"], ch["title"], ch["pairs"])
        print("wrote", ch["file"], n)

    index = {
        "title": "初転法輪（SN 56.11・転法輪経）",
        "source": "パーリ相応部 SN 56.11／雑阿含379",
        "totalPairs": total,
        "chapters": index_chapters,
    }
    (DATA / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote index.json", total, "pairs", len(index_chapters), "chapters")
    update_path_scene(all_pairs)
    print("updated path-scene-index.json")


if __name__ == "__main__":
    main()
