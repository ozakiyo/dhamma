#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build data/dhammacakka/ — 初転法輪 as a standalone collection (like Dhammapada).

Spine: 四諦通し（二辺·中道 → 苦·集·滅·道 → 三転十二行相 → 法輪転起）
Source: SN 56.11 / アラナ · true-buddhism · 雑阿含379（SAT）
UI: same app; categories = 四諦（八正道は道諦の中身として提示）
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

ORIGIN_NODES = [
    {"id": "contact", "label": "接触"},
    {"id": "feeling", "label": "受ける"},
    {"id": "craving", "label": "欲しがる"},
    {"id": "clinging", "label": "掴む"},
    {"id": "suffering", "label": "苦"},
    {"id": "release", "label": "離す"},
    {"id": "review", "label": "見直す"},
]

PATH_FACTORS_META = [
    {"id": "view", "label": "正見"}, {"id": "intention", "label": "正思惟"},
    {"id": "speech", "label": "正語"}, {"id": "action", "label": "正業"},
    {"id": "livelihood", "label": "正命"}, {"id": "effort", "label": "正精進"},
    {"id": "mindfulness", "label": "正念"}, {"id": "concentration", "label": "正定"},
]

# chapters: id, file, title, shortTitle, focusNodeId, focusReason, pairs
CHAPTERS = [
    {
        "id": 1,
        "file": "ch1.json",
        "title": "初転法輪・二辺と中道",
        "shortTitle": "二辺と中道",
        "mapNote": "SN 56.11 · 鹿野苑 · 二辺を離れた中道",
        "focusNodeId": "release",
        "focusReason": "二辺（欲楽·苦行）を離れ、中道へ向かうのが主題。",
        "pairs": [
            {
                "id": "FT-P01",
                "category": "magga",
                "section": "二辺",
                "nidanaId": "clinging",
                "pathFactors": ["正見", "正思惟"],
                "pathReason": "欲楽·苦行への掴みを離れる見を立てる",
                "observe": "二つの辺——欲楽への耽溺と、苦行への耽溺。どちらも出家の道ではない。",
                "action": "朝、今日の行いが「欲しがり」か「無理な苦行」に寄っていないか一度見る",
                "quote": (
                    "比丘たちよ、出家者によって従うべきでない二つの辺がある。"
                    "諸々の欲における欲楽の実践——下劣·粗野·凡夫のもの、聖ならざるもの、利益を伴わないもの。"
                    "および自己を苦しめる実践——苦であり、聖ならざるもの、利益を伴わないもの。"
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
                "nidanaId": "release",
                "pathFactors": ["正見", "正念"],
                "pathReason": "二辺を離れ、八正道の中道に触れる",
                "observe": "中道——如来が現正覚した道。眼を生じ、智を生じ、寂静·勝智·正覚·涅槃へ導く。",
                "action": "今日、「中道」を一言思い出し、極端に寄らない一歩を一つ取る",
                "quote": (
                    "比丘たちよ、これらの二つの辺に近づかず、中道が如来によって現正覚された。"
                    "それは眼を生じ、智を生じ、寂静·勝智·正覚·涅槃へ転起する。"
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
                "nidanaId": "contact",
                "pathFactors": ["正見", "正念", "正定"],
                "pathReason": "中道の中身として八支に触れる",
                "observe": "その中道とは八支の聖道——正見·正思惟·正語·正業·正命·正精進·正念·正定。",
                "action": "今日、八正道のうち一支を選び、一つの行為に結びつける",
                "quote": (
                    "比丘たちよ、では、その中道とは何か。"
                    "まさにこの八支の聖道である——"
                    "すなわち正見·正思惟·正語·正業·正命·正精進·正念·正定である。"
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
        "focusNodeId": "suffering",
        "focusReason": "苦諦——生老病死·五取蘊を苦として見るのが主題。",
        "pairs": [
            {
                "id": "FT-P04",
                "category": "dukkha",
                "section": "苦聖諦",
                "nidanaId": "suffering",
                "pathFactors": ["正見", "正念"],
                "pathReason": "今日の苦を苦諦の一側面として見る",
                "observe": "苦聖諦——生は苦、老は苦、病は苦、死は苦。要約すれば五取蘊は苦。",
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
                "nidanaId": "clinging",
                "pathFactors": ["正見", "正念"],
                "pathReason": "掴んでいる集まりを苦として一度見る",
                "observe": "五取蘊——色·受·想·行·識への執取の集まりが、苦の要約である。",
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
        "focusNodeId": "craving",
        "focusReason": "集諦——渇愛が苦の集起であるのが主題。",
        "pairs": [
            {
                "id": "FT-P06",
                "category": "samudaya",
                "section": "苦集聖諦",
                "nidanaId": "craving",
                "pathFactors": ["正思惟", "正念"],
                "pathReason": "渇愛を苦の集として名づける",
                "observe": "苦集聖諦——再有を招く渇愛。欲渇愛·有渇愛·無有渇愛。",
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
                "nidanaId": "craving",
                "pathFactors": ["正念", "正精進"],
                "pathReason": "欲·有·無有のどれに近いか一度見る",
                "observe": "三種の渇愛——欲しがる（欲）、あり続けたい（有）、無くしたい（無有）。",
                "action": "今日の欲しがりが「欲·有·無有」のどれに近いか、一度だけ名づける",
                "quote": (
                    "欲渇愛·有渇愛·無有渇愛——"
                    "そこかしこに歓喜し、再有を招く渇愛である。"
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
        "focusNodeId": "release",
        "focusReason": "滅諦——渇愛の残りなき離欲·滅が主題。",
        "pairs": [
            {
                "id": "FT-P08",
                "category": "nirodha",
                "section": "苦滅聖諦",
                "nidanaId": "release",
                "pathFactors": ["正見", "正念"],
                "pathReason": "渇愛を離欲する方向へ意図を戻す",
                "observe": "苦滅聖諦——その渇愛の残りなき離欲·滅·放棄·捨離·解脱·無執着。",
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
                "nidanaId": "release",
                "pathFactors": ["正精進", "正念"],
                "pathReason": "一つ手放すことで滅の方向を味わう",
                "observe": "離欲——掴みを一つ手放すとき、滅の方向が少し見える。",
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
        "focusNodeId": "contact",
        "focusReason": "道諦——八正道が苦滅への道跡であるのが主題。",
        "pairs": [
            {
                "id": "FT-P10",
                "category": "magga",
                "section": "苦滅道跡聖諦",
                "nidanaId": "contact",
                "pathFactors": ["正見", "正念"],
                "pathReason": "道諦として八正道に触れる",
                "observe": "苦滅道跡聖諦——八支の聖道が、苦の滅への道である。",
                "action": "今日の修行を八正道のうち一支に意識的に結びつける",
                "quote": (
                    "比丘たちよ、これが苦滅へ至る道の聖諦である。"
                    "まさにこの八支の聖道である——"
                    "正見·正思惟·正語·正業·正命·正精進·正念·正定である。"
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
                "section": "正見を入口に",
                "nidanaId": "feeling",
                "pathFactors": ["正見", "正念"],
                "pathReason": "苦·集·滅·道を見る正見から入る",
                "observe": "正見——苦を苦と見、集を集と見、滅を滅と見、道を道と見る入口。",
                "action": "朝、四諦を一言ずつ（苦·集·滅·道）確認し、今日の観察の入口とする",
                "quote": (
                    "八支の聖道——正見を始めとする。"
                    "正見があって、道は苦の滅へ転起する。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）／類縁",
                    "text": "正見、正志、正語、正業、正命、正方便、正念、正定。",
                    "satLocus": "大正蔵 T2.103c–104 転法輪（類縁）",
                    "note": "正見が道の入口。",
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
        "focusNodeId": "review",
        "focusReason": "三転——知る／なすべき／すでに、の十二行相が主題。",
        "pairs": [
            {
                "id": "FT-P12",
                "category": "dukkha",
                "section": "示転",
                "nidanaId": "contact",
                "pathFactors": ["正見", "正念"],
                "pathReason": "四諦を「これである」と示す知に触れる",
                "observe": "示転——「これは苦である」「これは集である」……未聞の法に眼·智·明·覚が生じる。",
                "action": "朝、「苦を知ること·集を断つこと·滅を証すること·道を修すること」と四諦の課題を一言確認する",
                "quote": (
                    "比丘たちよ、この苦聖諦は、かつて聞かなかった諸法について——"
                    "眼が生じた、智が生じた、慧が生じた、明が生じた、光が生じた。"
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
                "id": "FT-P13",
                "category": "samudaya",
                "section": "勧転",
                "nidanaId": "craving",
                "pathFactors": ["正精進", "正念"],
                "pathReason": "集は断つべき、と勧める方向へ精進する",
                "observe": "勧転——苦は遍知すべき、集は断つべき、滅は証すべき、道は修すべき。",
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
                "id": "FT-P14",
                "category": "nirodha",
                "section": "証転",
                "nidanaId": "review",
                "pathFactors": ["正見", "正念"],
                "pathReason": "すでに知った·断った方向を振り返る",
                "observe": "証転——苦は遍知された、集は断たれた、滅は証された、道は修された。",
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
                    "text": "（已知·已断·已証·已修——三転の第三。パーリ·漢ともに十二行相。）",
                    "satLocus": "大正蔵 T2.103c–104 転法輪",
                    "note": "証転——已知見。",
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
        "focusNodeId": "review",
        "focusReason": "三転十二行相が清浄となって法輪が転起し、正覚が宣言される。",
        "pairs": [
            {
                "id": "FT-P15",
                "category": "magga",
                "section": "正覚の宣言",
                "nidanaId": "release",
                "pathFactors": ["正見", "正念"],
                "pathReason": "知見が清浄になるまで覚を宣言しない、という基準を見る",
                "observe": "四諦の三転十二行相について如実の知見が清浄となるまで——正覚を宣言しなかった。",
                "action": "今日の学びを「まだ途中」と認め、一つの行相（知る／断つ／証する／修する）に戻る",
                "quote": (
                    "比丘たちよ、私のこの四聖諦における三転十二行の如実の知見が、"
                    "清浄とならなかったあいだは——"
                    "天·魔·梵の世、沙門·婆羅門·神々と人間たちからなる衆において、"
                    "無上の正等覚を現正覚したとは宣言しなかった。"
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
                "id": "FT-P16",
                "category": "dukkha",
                "section": "憍陳如の法眼",
                "nidanaId": "contact",
                "pathFactors": ["正見", "正念"],
                "pathReason": "生滅の法眼に触れる",
                "observe": "憍陳如に塵なく汚れなき法の眼が生じた——「生起する性質のものは、滅尽する性質のものである」。",
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
                "id": "FT-P17",
                "category": "magga",
                "section": "転法輪",
                "nidanaId": "review",
                "pathFactors": ["正見", "正念"],
                "pathReason": "法輪が転起した一日を振り返る",
                "observe": "無上の法輪が転起された——沙門·婆羅門·天·魔·梵によって転じ戻され得ない。",
                "action": "就寝前、今日の苦·集·滅·道の体験を一つずつ思い返し、清らかな修行を続けた一日を静かに認める",
                "quote": (
                    "尊師によって、バーラーナシーの仙人堕処・鹿野苑において、"
                    "無上の法輪が転起された——"
                    "それは沙門によっても、婆羅門によっても、神によっても、マーラによっても、"
                    "梵天によっても、誰によっても、世において転じ戻され得ない、と。"
                ),
                "chinese": {
                    "status": "mapped",
                    "pin": "雑阿含379・転法輪（T99）",
                    "text": "世尊於波羅捺國仙人住處鹿野苑中，三轉十二行法輪……是故此經名轉法輪經。",
                    "satLocus": "大正蔵 T2.104 転法輪",
                    "note": "法輪転起·経名。",
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


def practice_nodes(pairs, short, actions_by_id):
    by_nidana = {}
    for p in pairs:
        by_nidana.setdefault(p["nidanaId"], []).append(p["id"])
    # minimal nodes for UI compatibility
    lead = pairs[0]
    return [
        {
            "id": "contact", "weekday": 1, "categoryId": "magga", "nidanaLabel": "接触",
            "pathFactors": lead["pathFactors"][:2],
            "pathFactorIds": [],
            "pathLabel": "四諦·中道の教えに触れる",
            "chapterHint": short,
            "fromPrev": "見直しが、今朝の一歩を変える",
            "toNext": "触のあと、受·渇愛が見える",
            "todayObserve": lead["observe"],
            "todayAction": lead["action"],
            "when": ["教えに触れた"],
            "sources": by_nidana.get("contact", [lead["id"]]),
            "leadQuote": lead["quote"][:40] + "…",
            "secondaryObserve": "",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "dukkha", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "苦·受をあるがままに見る",
            "chapterHint": short,
            "fromPrev": "接触のあと、受が立つ",
            "toNext": "受に乗ると渇愛へ",
            "todayObserve": next((p["observe"] for p in pairs if p["nidanaId"] == "feeling"), lead["observe"]),
            "todayAction": next((p["action"] for p in pairs if p["nidanaId"] == "feeling"), lead["action"]),
            "when": ["受を見た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": "",
            "secondaryObserve": "",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "samudaya", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "渇愛を集として名づける",
            "chapterHint": short,
            "fromPrev": "受のあと、欲しがりが立つ",
            "toNext": "止めないと掴みへ",
            "todayObserve": next((p["observe"] for p in pairs if p["nidanaId"] == "craving"), "渇愛を集と見る"),
            "todayAction": next((p["action"] for p in pairs if p["nidanaId"] == "craving"), lead["action"]),
            "when": ["渇愛を名づけた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": "",
            "secondaryObserve": "",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "dukkha", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "二辺·五取蘊への掴みを見る",
            "chapterHint": short,
            "fromPrev": "欲しがりのあと、掴みが手前",
            "toNext": "掴むと苦が見える",
            "todayObserve": next((p["observe"] for p in pairs if p["nidanaId"] == "clinging"), "掴みを見る"),
            "todayAction": next((p["action"] for p in pairs if p["nidanaId"] == "clinging"), lead["action"]),
            "when": ["掴みを見た"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": "",
            "secondaryObserve": "",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "dukkha", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "苦諦として苦を認める",
            "chapterHint": short,
            "fromPrev": "掴んだ結果として苦が見える",
            "toNext": "見れば、滅·道へ離す",
            "todayObserve": next((p["observe"] for p in pairs if p["nidanaId"] == "suffering"), "苦を認める"),
            "todayAction": next((p["action"] for p in pairs if p["nidanaId"] == "suffering"), lead["action"]),
            "when": ["苦を認めた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": "",
            "secondaryObserve": "",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "nirodha", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "渇愛を離欲し、中道へ戻る",
            "chapterHint": short,
            "fromPrev": "苦が見えれば、渇愛·二辺を離す",
            "toNext": "離せば、夜の見直しへ",
            "todayObserve": next((p["observe"] for p in pairs if p["nidanaId"] == "release"), "離欲する"),
            "todayAction": next((p["action"] for p in pairs if p["nidanaId"] == "release"), lead["action"]),
            "when": ["離欲した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": "",
            "secondaryObserve": "",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "magga", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "四諦·三転を振り返る",
            "chapterHint": short,
            "fromPrev": "一日の離しは、朝からの道の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": next((p["observe"] for p in pairs if p["nidanaId"] == "review"), "四諦を振り返る"),
            "todayAction": next((p["action"] for p in pairs if p["nidanaId"] == "review"), lead["action"]),
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": "",
            "secondaryObserve": "",
        },
    ]


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
            "spineOrigin": "苦を見た→集（渇愛）を見た→滅へ離した→道を修した",
            "spinePath": "四諦を通しで見る。八正道は道諦の中身",
            "originNodes": ORIGIN_NODES,
            "pathFactors": PATH_FACTORS_META,
            "nodes": practice_nodes(ch["pairs"], ch["shortTitle"], {}),
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
    label_to_id = {
        "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
        "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
    }
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
                by_path[(label_to_id[lab], ch_id)].append(p["id"])

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

    # keep scope string informative
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
