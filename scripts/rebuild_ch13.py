#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch13.json (世品) to match ch1–ch12 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-13"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0567"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap13/"
)

QUOTES = {
    167: "下劣な法（教え）に慣れ親しまないように。怠り（放逸）と共に住まないように。誤った見解（邪見）に慣れ親しまないように。世〔俗〕の繁栄ある者として存さないように。",
    168: "奮起するように。〔気づきを〕怠らないように。善き行ないの法（教え）を行なうように。〔善き行ないの〕法（教え）を行なう者は、安楽のうちに臥す──この世において、さらに、他〔の世〕において。",
    169: "善き行ないの法（教え）を行なうように。〔まさに〕その、悪しき行ないを行なわないように。〔善き行ないの〕法（教え）を行なう者は、安楽のうちに臥す──この世において、さらに、他〔の世〕において。",
    170: "泡粒を見るかのように、陽炎（かげろう）を見るかのように、このように、世〔のあり様〕を注視している者を、死魔の王は見ない。",
    171: "来たれ、見よ──彩りあざやかな王車の如き、この世〔のあり様〕を。そこにおいて、愚者たちは沈むが、〔あるがままに〕識知している者たちに、執着〔の思い〕は存在しない。",
    172: "そして、彼が、過去において〔気づきを〕怠っていても、彼が、のちに怠らないなら、彼は、雲から解き放たれた月のように、この世を照らす。",
    173: "彼の為した悪しき行為（悪業）が、善によって塞がれるなら、彼は、雲から解き放たれた月のように、この世を照らす。",
    174: "暗愚と成ったのが、この世〔の人々〕である。ここにおいて、数少ない者が、〔真実をあるがままに〕観察する──網から解き放たれた僅かな鳥が、天上に赴くように。",
    175: "白鳥たちは、太陽の道（大空）を行き、神通によって、〔聖賢たちは〕虚空を行く。慧者たちは、軍勢を有する悪魔に勝利して、〔この〕世から〔彼岸へと〕導かれる（涅槃に到達する）。",
    176: "一なる法（真理）を超え行った、虚偽を説く人にとって、他の世（来世）を否認する者にとって、為さずにいられる悪は存在しない。",
    177: "吝嗇の者たちは、まさに、天の世に行かない。愚者たちは、まさに、布施を賞賛しない。そして、慧者は、布施に随喜しながら、まさしく、それによって、彼は、他所（来世）において、安楽の者と成る。",
    178: "地における一なる王となることよりも、あるいは、天上に赴くことよりも、一切の世の君主となることよりも、預流果（覚りの第一階梯）のほうが、優れている。",
}

OBSERVE = {
    167: "下劣の法に従うべからず、放逸に住すべからず、邪見に従うべからず、世俗の徒となるべからず。",
    168: "奮起すべし、放逸なるべからず。 善行の法を行うべし。 法に従って行なう人は、この世に於てもかの世に於ても安楽に臥す。",
    169: "善行の法を行うべし。 悪行の〔法〕を行うべからず。 法に従って行なう人は、この世に於てもかの世に於ても安楽に臥す。",
    170: "泡沫を見る如く、陽炎（蜃気楼）を見る如く、かく世間を観ずる者を、死王は見ず。",
    171: "来たれ粉飾せられて王車に譬うべきこの世を見よ。愚者はこの中に沈湎す、智者は〔これに〕執着することなし。",
    172: "前に放逸なるも、後に放逸ならざる人は、あたかも雲間を出でし月の如くに、この世を照らす。",
    173: "そのなしたる悪業を、善を以て覆う人は、あたかも雲間を出でし月の如くに、この世を照らす。",
    174: "この世は暗黒なり。 この中に於てよく洞察する者は稀なり。 網を脱れし鳥の如く、天に昇る者は少なし。",
    175: "鵞鳥は太陽の道を行き、通力を以て虚空を行く。 賢者は魔王とその眷属とを破りて、世間より離脱す。",
    176: "唯一法を犯し、妄語を吐き、来世を信ぜざる人は悪としてなさざるなし。",
    177: "貪欲の人は天界に赴かず。 愚者は決して施与を称揚せず。 賢者は施与を随喜し、これにより来世に於て安楽なり。",
    178: "地上に於ける王権よりも、或いは天界に赴くよりも、一切世界の主権よりも、預流果（よるか）（涅槃に至る第一階梯）は勝れたり。",
}

CHINESE = {
    167: {"status": "mapped", "pin": "教學品（T210 第2品）", "t210": "T210-02-005",
          "text": "莫學小道，以信邪見，莫習放蕩，令增欲意。", "satLocus": "大正蔵 T4.562a 教學品第5頌",
          "note": "パーリ世の章167はT210世俗品ではなく教學品に対応（蘇錦坤對照表）。"},
    168: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ世の章168はT210に対応なし（蘇錦坤對照表）。併記169の漢訳を参照。"},
    169: {"status": "mapped", "pin": "世俗品（T210 第21品）", "t210": "T210-21-003",
          "text": "順行正道，勿隨邪業，行法臥安，世世無患。", "satLocus": "大正蔵 T4.567a 世俗品第3頌"},
    170: {"status": "mapped", "pin": "世俗品（T210 第21品）", "t210": "T210-21-004",
          "text": "萬物如泡，意如野馬，居世若幻，奈何樂此？", "satLocus": "大正蔵 T4.567a 世俗品第4頌"},
    171: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ世の章171はT210に対応なし（蘇錦坤對照表）。出曜経・法集要頌経側に近い文言あり。"},
    172: {"status": "mapped", "pin": "放逸品（T210 第10品）", "t210": "T210-10-015",
          "text": "若前放逸，後能自禁，是炤世間，念定其宜。", "satLocus": "大正蔵 T4.564a 放逸品第15頌",
          "note": "パーリ世の章172はT210世俗品ではなく放逸品に対応（蘇錦坤對照表）。"},
    173: {"status": "mapped", "pin": "放逸品（T210 第10品）", "t210": "T210-10-016",
          "text": "過失為惡，追覆以善，是炤世間，念善其宜。", "satLocus": "大正蔵 T4.564a 放逸品第16頌",
          "note": "パーリ世の章173はT210世俗品ではなく放逸品に対応（蘇錦坤對照表）。"},
    174: {"status": "mapped", "pin": "世俗品（T210 第21品）", "t210": "T210-21-007",
          "text": "世俗無眼，莫見道真，如少見明，當養善意。", "satLocus": "大正蔵 T4.567a 世俗品第7頌"},
    175: {"status": "mapped", "pin": "世俗品（T210 第21品）", "t210": "T210-21-008",
          "text": "如鴈將群，避羅高翔，明人導世，度脫邪眾。", "satLocus": "大正蔵 T4.567a 世俗品第8頌"},
    176: {"status": "mapped", "pin": "世俗品（T210 第21品）", "t210": "T210-21-012",
          "text": "一法脫過，謂妄語人，不免後世，靡惡不更。", "satLocus": "大正蔵 T4.567a 世俗品第12頌"},
    177: {"status": "mapped", "pin": "篤信品（T210 第4品）", "t210": "T210-04-002",
          "text": "愚不修天行，亦不喜布施，信施助善者，從是到彼安。", "satLocus": "大正蔵 T4.562c 篤信品第2頌",
          "note": "パーリ世の章177はT210世俗品ではなく篤信品に対応（蘇錦坤對照表）。"},
    178: {"status": "mapped", "pin": "世俗品（T210 第21品）", "t210": "T210-21-013",
          "text": "雖多積珍寶，崇高至于天，如是滿世間，不如見道迹。", "satLocus": "大正蔵 T4.567a 世俗品第13頌"},
}

VERSE_PRACTICE = {
    167: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "下劣・放逸・邪見・世俗に従わない"},
    168: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "奮起し、善行の法を行う"},
    169: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "善行を行い、悪行を行わない"},
    170: {"nidanaId": "feeling", "pathFactors": ["正念", "正見"], "reason": "世を泡沫・陽炎と観る者を、死王は見ない"},
    171: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "粉飾の世に沈まず、執着しない"},
    172: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "後に不放逸なら、雲間の月のように輝く"},
    173: {"nidanaId": "review", "pathFactors": ["正業", "正念"], "reason": "悪業を善で覆えば、雲間の月のように輝く"},
    174: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "世は暗黒、洞察する者は稀"},
    175: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "魔王を破り、世間より離脱する"},
    176: {"nidanaId": "clinging", "pathFactors": ["正語", "正念"], "reason": "妄語は一切の悪の入り口"},
    177: {"nidanaId": "craving", "pathFactors": ["正命", "正念"], "reason": "貪欲せず、施与を随喜する"},
    178: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "王権より預流果（覚りの第一階梯）が勝る"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP13-P01", 167), ("DP13-P02", 167),
    ("DP13-P03", 168), ("DP13-P04", 168),  # 168–169
    ("DP13-P05", 170), ("DP13-P06", 170),
    ("DP13-P07", 171),
    ("DP13-P08", 172), ("DP13-P09", 172),
    ("DP13-P10", 173), ("DP13-P11", 173),
    ("DP13-P12", 174), ("DP13-P13", 174),
    ("DP13-P14", 175), ("DP13-P15", 175),
    ("DP13-P16", 176), ("DP13-P17", 176),
    ("DP13-P18", 177), ("DP13-P19", 177),
    ("DP13-P20", 178), ("DP13-P21", 178),
]

COMBINED = {
    168: (168, 169),
}


def chinese_block(verse: int) -> dict:
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
        )
    return c


def chinese_for_pair(verse, parts=None):
    if parts:
        for v in parts:
            if CHINESE[v]["status"] == "mapped":
                zh = chinese_block(v)
                if v != verse:
                    zh["note"] = (
                        f"併記偈のうち第{v}偈の漢訳対応を表示。"
                        + (CHINESE[verse].get("note") or "")
                    ).strip()
                return zh
    return chinese_block(verse)


def main() -> None:
    old = json.loads((DATA / "ch13.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        if verse in COMBINED:
            parts = COMBINED[verse]
            observe = " ".join(OBSERVE[v] for v in parts)
            quote = " ".join(QUOTES[v] for v in parts)
            a, b = parts[0], parts[-1]
            pali_locus = f"小部・ダンマパダ 世の章 第{a}-{b}偈"
            modern_locus = f"第１３章・世品 第{a}-{b}偈（#ch02-13）"
            zh = chinese_for_pair(verse, parts)
            verse_out = a
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 世の章 第{verse}偈"
            modern_locus = f"第１３章・世品 第{verse}偈（#ch02-13）"
            zh = chinese_block(verse)
            verse_out = verse

        pairs.append({
            "id": pid,
            "category": LABEL_TO_ID[factors[0]],
            "verse": verse_out,
            "observe": observe,
            "action": actions[pid],
            "quote": quote,
            "nidanaId": vp["nidanaId"],
            "pathFactors": factors,
            "pathReason": vp["reason"],
            "alignment": {
                "pali": {"source": "アラナ精舎 経典ライブラリー", "locus": pali_locus, "url": ARANA_URL},
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": modern_locus,
                    "url": TB_URL,
                },
                "chinese": zh,
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第13章・世品（世の章）"
    SHORT = "世品（世の章）"
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
            "pathLabel": "世俗の流れに触れても、下劣・放逸・邪見に従わない",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の世俗への戒めになる",
            "toNext": "世への接触のあと、粉飾への受が立ち上がる",
            "todayObserve": OBSERVE[167],
            "todayAction": actions["DP13-P01"],
            "when": ["流されそう", "朝の始まり"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[167][:40] + "…",
            "secondaryObserve": "世は暗黒、洞察する者は稀",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "世の受を泡沫・陽炎として受け取る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、世間の魅力・不安の受が来る",
            "toNext": "受けた魅力を、沈湎の欲しがりへ落とさない",
            "todayObserve": OBSERVE[170],
            "todayAction": actions["DP13-P05"],
            "when": ["こだわりが強まった", "欲しいものが目についた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[170][:40] + "…",
            "secondaryObserve": "泡沫のように観る者を、死王は見ない",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "粉飾の世への欲しがりを緩め、施与へ向ける",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、王車のような世への欲しがりへ",
            "toNext": "止めないと妄語・世俗の掴みへ進む",
            "todayObserve": OBSERVE[171],
            "todayAction": actions["DP13-P07"],
            "when": ["華やかなものに引かれた", "もっと欲しいと感じた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[171][:40] + "…",
            "secondaryObserve": "貪欲せず、施与を随喜する",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正念"], "pathFactorIds": ["speech", "mindfulness"],
            "pathLabel": "妄語を掴まず、真実の語を守る",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、嘘・否認として掴む手前",
            "toNext": "掴むと悪の入り口が開き、苦が太る",
            "todayObserve": OBSERVE[176],
            "todayAction": actions["DP13-P16"],
            "when": ["嘘をつきそう", "来世を軽んじそう"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[176][:40] + "…",
            "secondaryObserve": "妄語は一切の悪の入り口",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "世俗の成功より預流果が勝ると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、世俗の苦が熟す",
            "toNext": "見れば、不放逸と善行へ向き直る",
            "todayObserve": OBSERVE[178],
            "todayAction": actions["DP13-P20"],
            "when": ["成功を追い過ぎた", "修行の一歩を思い出したい"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[178][:40] + "…",
            "secondaryObserve": "王権より預流果が勝る",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "奮起し、不放逸と善で世の流れから離す",
            "chapterHint": SHORT,
            "fromPrev": "世俗への沈湎が流れを加速させる",
            "toNext": "離すと、雲間の月のように見直しへつながる",
            "todayObserve": OBSERVE[172],
            "todayAction": actions["DP13-P08"],
            "when": ["過去の放逸を悔いている", "今から変えたい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[172][:40] + "…",
            "secondaryObserve": "悪業を善で覆えば、雲間の月のように輝く",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "action", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "今日の悪業を善で覆えたか、雲間の月として見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、善で覆える悪の跡",
            "toNext": "見直しが、翌朝の世俗への戒めになる",
            "todayObserve": OBSERVE[173],
            "todayAction": actions["DP13-P11"],
            "when": ["一日を閉じるとき", "過ちを善で覆いたい"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[173][:40] + "…",
            "secondaryObserve": "法に従って行なう人は、両世で安楽に臥す",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 13,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第13章（世品／世の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210世俗品、一部他品・未対応あり）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・世の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１３章・世品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・世俗品（T4.567a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "feeling",
            "focusReason": "世品は泡沫・陽炎として世を観る受が中心。既定の焦点は受ける。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch13.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch13.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 14):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch13", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 21
    assert all(p["id"] == f"DP13-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(167, 179))
    p07 = next(p for p in pairs if p["id"] == "DP13-P07")
    assert p07["alignment"]["chinese"]["status"] == "unmapped"
    p03 = next(p for p in pairs if p["id"] == "DP13-P03")
    assert p03["alignment"]["chinese"]["status"] == "mapped"  # via 169
    print("OK")


if __name__ == "__main__":
    main()
