#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch16.json (愛好品) to match ch1–ch15 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-16"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0568"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap16/"
)

QUOTES = {
    209: "道理なきことに自己を結び付け、かつまた、道理あることに〔自己を〕結び付けずにいる者──義（道理）を捨棄して、愛しいものを収め取る者は、自己〔の道〕に専念する者たちを羨む。",
    210: "愛しい者たち（愛着の対象）と集いあつまってはならない。いついかなる時も、愛しくない者たち（憎悪の対象）と〔集いあつまってはならない〕。愛しい者たちと会見なくあることは、苦しみである。かつまた、愛しくない者たちと会見あることも、〔苦しみである〕。",
    211: "それゆえに、愛しい者を作らないように。まさに、愛しい者を失うことは、悪しきこと（苦しみ）である。彼らに、愛しい者と愛しくない者（愛憎の対象）が存在しないなら、彼らに、諸々の拘束は見出されない。",
    212: "愛しいものから、憂いが生まれ、愛しいものから、恐れが生まれる。愛しいもの〔の拘束〕から解放された者に、憂いは存在しない。どうして、恐れがあろう。",
    213: "愛情から、憂いが生まれ、愛情から、恐れが生まれる。愛情〔の拘束〕から解放された者に、憂いは存在しない。どうして、恐れがあろう。",
    214: "歓楽から、憂いが生まれ、歓楽から、恐れが生まれる。歓楽〔の拘束〕から解放された者に、憂いは存在しない。どうして、恐れがあろう。",
    215: "欲望から、憂いが生まれ、欲望から、恐れが生まれる。欲望〔の拘束〕から解放された者に、憂いは存在しない。どうして、恐れがあろう。",
    216: "渇愛から、憂いが生まれ、渇愛から、恐れが生まれる。渇愛〔の拘束〕から解放された者に、憂いは存在しない。どうして、恐れがあろう。",
    217: "戒と見を成就し、法（正義）に依って立ち、真理（諦）を説く者を──自己の〔為すべき〕行為（業）を〔常に〕為している者を──人は、彼を、愛しき者と為す（彼は、誰からも愛される）。",
    218: "告げ知らされることなきもの（涅槃）にたいする欲〔の思い〕が生じた者（涅槃への意欲を起こした者）として、かつまた、〔その〕意に満たされた者として、〔世に〕存するように。そして、諸々の欲望〔の対象〕にたいし、心が縛られない者は、「上流にある者（欲界を離れた者）」と説かれる。",
    219: "長き不在の人が、遠方から〔無事〕安穏に帰ってきたなら、親族や朋友たちは、そして、知人たちも、〔彼の〕帰還を喜ぶ。",
    220: "まさしく、そのように、善き〔行為〕を為した者（功徳を作った者）もまた、この世から他〔の世〕へと赴いたなら、諸々の善きこと（功徳）が迎え取る──親族たちが、愛しき者の帰還を〔喜ぶ〕ように。",
}

OBSERVE = {
    209: "瞑想なき〔行作〕に専注して、瞑想に専注せず、道義を捨てて愛好する所を取る者は、〔かえって〕瞑想に専注する者を羨む。",
    210: "愛好するものと会するなかれ、愛好せざるものと決して〔会するなかれ〕。 愛好するものを見ざるは苦なり。 愛好せざるものを見るもまた〔苦なり〕。",
    211: "故に愛好するものを造るなかれ。 愛好するものを失うは災いなればなり。 愛憎なき人には桎梏（しっこく）（煩悩）なし。",
    212: "愛好より憂患生じ、愛好より畏怖生ず。 愛好を離脱せる人には憂患なし。 何処にか畏怖あらん。",
    213: "親愛より憂患生じ、親愛より畏怖生ず。 親愛を離脱せる人には憂患なし。 何処にか畏怖あらん。",
    214: "淫欲より憂患生じ、淫欲より畏怖生ず。 淫欲を離脱せる人には憂患なし。 何処にか畏怖あらん。",
    215: "欲楽より憂患生じ、欲楽より畏怖生ず。 欲楽を離脱せる人には憂患なし。 何処にか畏怖あらん。",
    216: "愛欲より憂患生じ、愛欲より畏怖生ず。 愛欲を離脱せる人には憂患なし。 何処にか畏怖あらん。",
    217: "戒行と正見とを備え、正法に住し、真実を知り、自ら自己の業務を行う者、世人はかかる人を愛好す。",
    218: "不可説法（涅槃）に望みを起こして思慮に富み、しかも諸欲に心を束縛せられざる者は上流者（涅槃に近づける者）と称せらる。",
    219: "久しく異郷にあり、遠隔の地より無事に戻れる帰来者を、親族・朋友・知己は歓び迎う。",
    220: "これと等しく、福業をなしてこの世よりかの世に赴ける人を、福業は迎う、あたかも愛好する帰来者を親族の〔迎うる〕如く。",
}

CHINESE = {
    209: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-001",
          "text": "違道則自順，順道則自違，捨義取所好，是為順愛欲。", "satLocus": "大正蔵 T4.568a 好喜品第1頌"},
    210: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-002",
          "text": "不當趣所愛，亦莫有不愛，愛之不見憂，不愛見亦憂。", "satLocus": "大正蔵 T4.568a 好喜品第2頌"},
    211: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-003",
          "text": "是以莫造愛，愛憎惡所由，已除縛結者，無愛無所憎。", "satLocus": "大正蔵 T4.568a 好喜品第3頌"},
    212: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-004",
          "text": "愛喜生憂，愛喜生畏，無所愛喜，何憂何畏？", "satLocus": "大正蔵 T4.568a 好喜品第4頌"},
    213: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ愛しいものの章213はT210に対応なし（蘇錦坤對照表）。"},
    214: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-005",
          "text": "好樂生憂，好樂生畏，無所好樂，何憂何畏？", "satLocus": "大正蔵 T4.568a 好喜品第5頌"},
    215: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-006",
          "text": "貪欲生憂，貪欲生畏；解無貪欲，何憂何畏？", "satLocus": "大正蔵 T4.568a 好喜品第6頌"},
    216: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ愛しいものの章216はT210に対応なし（蘇錦坤對照表）。"},
    217: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-007",
          "text": "貪法戒成，至誠知慚，行身近道，為眾所愛。", "satLocus": "大正蔵 T4.568a 好喜品第7頌"},
    218: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-008",
          "text": "欲態不出，思正乃語，心無貪愛，必截流渡。", "satLocus": "大正蔵 T4.568a 好喜品第8頌"},
    219: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-009",
          "text": "譬人久行，從遠吉還，親厚普安，歸來喜歡。", "satLocus": "大正蔵 T4.568a 好喜品第9頌"},
    220: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-010",
          "text": "好行福者，從此到彼，自受福祚，如親來喜。", "satLocus": "大正蔵 T4.568a 好喜品第10頌"},
}

VERSE_PRACTICE = {
    209: {"nidanaId": "contact", "pathFactors": ["正念", "正精進"], "reason": "道理あることに自己を結び、愛しいものに流されない"},
    210: {"nidanaId": "feeling", "pathFactors": ["正念", "正見"], "reason": "愛しい者・愛しくない者との会離はともに苦"},
    211: {"nidanaId": "suffering", "pathFactors": ["正念", "正見"], "reason": "愛しい者を失うは災い、愛憎なき人には桎梏なし"},
    212: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "愛好から憂患・畏怖が生まれる"},
    213: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "親愛から憂患・畏怖が生まれる"},
    214: {"nidanaId": "craving", "pathFactors": ["正念", "正定"], "reason": "歓楽から憂患・畏怖が生まれる"},
    215: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "欲望から憂患・畏怖が生まれる"},
    216: {"nidanaId": "clinging", "pathFactors": ["正念", "正見"], "reason": "渇愛を掴まず、離脱すれば憂患・畏怖なし"},
    217: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "戒と正見を備え、自己の業務を為す者は愛される"},
    218: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "涅槃への望みを起こし、諸欲に心を縛られない"},
    219: {"nidanaId": "contact", "pathFactors": ["正念", "正思惟"], "reason": "帰来者を親族が喜ぶ如く、再会を喜ぶ"},
    220: {"nidanaId": "review", "pathFactors": ["正業", "正念"], "reason": "福業が、帰来者を迎える親族のように迎える"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP16-P01", 209),
    ("DP16-P02", 210), ("DP16-P03", 210),
    ("DP16-P04", 211), ("DP16-P05", 211),
    ("DP16-P06", 212),
    ("DP16-P07", 213),
    ("DP16-P08", 214),
    ("DP16-P09", 215),
    ("DP16-P10", 216),
    ("DP16-P11", 217), ("DP16-P12", 217),
    ("DP16-P13", 218),
    ("DP16-P14", 219),
    ("DP16-P15", 220), ("DP16-P16", 220),
    ("DP16-P17", 217),
]


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
        )
    return c


def main():
    old = json.loads((DATA / "ch16.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 愛しいものの章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第１６章・愛好品 第{verse}偈（#ch02-16）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第16章・愛好品（愛しいものの章）"
    SHORT = "愛好品（愛しいものの章）"
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
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "愛しいものに触れても、道理ある道に自己を結ぶ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の福業の見直しが、今朝の正しい結びつきになる",
            "toNext": "接触のあと、会いたい・会いたくないの受が来る",
            "todayObserve": OBSERVE[209],
            "todayAction": actions["DP16-P01"],
            "when": ["誘惑に流されそう", "朝の始まり"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[209][:40] + "…",
            "secondaryObserve": "帰来者を親族が喜ぶ如く、再会を喜ぶ",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "好き・嫌いの会離の受を、ともに苦として受け取る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、愛好・非愛の受が立ち上がる",
            "toNext": "受けた受を、もっと掴みたい欲しがりへ落とさない",
            "todayObserve": OBSERVE[210],
            "todayAction": actions["DP16-P02"],
            "when": ["好きなものに会えなかった", "嫌いなものに会った"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[210][:40] + "…",
            "secondaryObserve": "愛好・非愛との会離はともに苦",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "愛好・親愛・渇愛から憂患が生まれると知る",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、愛好への欲しがりへ落ちる",
            "toNext": "止めないと愛憎の掴みへ進む",
            "todayObserve": OBSERVE[212],
            "todayAction": actions["DP16-P06"],
            "when": ["心配・恐怖が起きた", "もっと欲しいと感じた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[212][:40] + "…",
            "secondaryObserve": "渇愛から憂患・畏怖が生まれる",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "渇愛を掴まず、離脱すれば憂患・畏怖なし",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、渇愛として掴む手前",
            "toNext": "掴むと失う災いと憂患の苦が太る",
            "todayObserve": OBSERVE[216],
            "todayAction": actions["DP16-P10"],
            "when": ["もっと手に入れたい", "失うのが怖い"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[216][:40] + "…",
            "secondaryObserve": "渇愛を離脱せる人には憂患なし",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "愛好を失う災いと、会離の苦を知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、失う憂患が熟す",
            "toNext": "見れば、戒行と涅槃への望みへ向き直る",
            "todayObserve": OBSERVE[211],
            "todayAction": actions["DP16-P04"],
            "when": ["失って苦しんでいる", "会えない苦しさ"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[211][:40] + "…",
            "secondaryObserve": "愛好するものを失うは災い",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "action", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "戒と正見で行い、諸欲への縛りから離す",
            "chapterHint": SHORT,
            "fromPrev": "愛好への掴みが憂患を加速させる",
            "toNext": "離すと、福業が迎える見直しへつながる",
            "todayObserve": OBSERVE[217],
            "todayAction": actions["DP16-P11"],
            "when": ["誠実に業務をしたい", "欲に縛られたくない"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[217][:40] + "…",
            "secondaryObserve": "涅槃への望みを起こし、諸欲に心を縛られない",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "action", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "今日の福業が、将来の自分を迎えるか見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、将来を迎える福業の跡",
            "toNext": "見直しが、翌朝の正しい結びつきになる",
            "todayObserve": OBSERVE[220],
            "todayAction": actions["DP16-P15"],
            "when": ["一日を閉じるとき", "善業を確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[220][:40] + "…",
            "secondaryObserve": "福業は、帰来者を迎える親族のように迎える",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 16,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第16章（愛好品／愛しいものの章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210好喜品、213・216は対応なし）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・愛しいものの章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１６章・愛好品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・好喜品（T4.568a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "craving",
            "focusReason": "愛好品は愛好・親愛・渇愛から憂患が生まれる構造が中心。既定の焦点は欲しがる。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch16.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch16.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 17):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch16", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 17
    assert all(p["id"] == f"DP16-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(209, 221))
    p07 = next(p for p in pairs if p["id"] == "DP16-P07")
    p10 = next(p for p in pairs if p["id"] == "DP16-P10")
    assert p07["alignment"]["chinese"]["status"] == "unmapped"
    assert p10["alignment"]["chinese"]["status"] == "unmapped"
    print("OK")


if __name__ == "__main__":
    main()
