#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch8.json (千品) to match ch1–ch7 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-08"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0565"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap08/"
)

QUOTES = {
    100: "たとえ、もし、千の言葉あるも、義（意味）なき句の呪文集であるなら、それを聞いて〔心が〕静まる、一つの義（意味）ある句のほうが、より勝っている。",
    101: "たとえ、もし、千の詩偈あるも、義（意味）なき句の呪文集であるなら、それを聞いて〔心が〕静まる、一つの詩偈の句のほうが、より勝っている。",
    102: "そして、彼が、百の詩偈を語るとして、義（意味）なき句の呪文集であるなら、それを聞いて〔心が〕静まる、一つの法（教え）の句のほうが、より勝っている。",
    103: "彼が、戦場において、百万の人間たちに勝利するとして、しかしながら、一つの自己に勝利するなら、彼は、まさに、最上の戦勝者である。",
    104: "〔相手が〕自己であるなら、まさに、〔その〕勝利は、より勝っている──そして、すなわち、この、他の人々に〔勝利するとして、それよりも〕。〔その〕人の自己が調御され、常に自制された歩みあるなら──",
    105: "そのような形態の人の勝利を、勝利ならざるものと為すのは、まさしく、天〔の神〕にあらず、音楽神にあらず、梵〔天〕（ブラフマー神）を含む、悪魔にあらず（誰もできない）。",
    106: "彼が、百年のあいだ、月ごとに千〔回〕、祭祀をするとして、しかしながら、自己を修めた者たちの一者を、寸時でさえも供養するなら、まさしく、その供養は、より勝っている──それが、もし、百年の供犠であるとして、〔それよりも〕。",
    107: "そして、その人が、百年のあいだ、林のなかで祭火（アグニ神）を世話するとして、しかしながら、自己を修めた者たちの一者を、寸時でさえも供養するなら、まさしく、その供養は、より勝っている──それが、もし、百年の供犠であるとして、〔それよりも〕。",
    108: "あるいは、供えられたものが、あるいは、捧げられたものが、それが何であれ、世において、功徳を期す者が、まる一年のあいだ、祭祀をするとして、その全てでさえも、〔正しい供養の〕四分の一に至らない。〔心が〕真っすぐに赴いた者たちにたいする表敬のほうが、より勝っている。",
    109: "〔心が真っすぐに赴いた者たちにたいする〕表敬を戒として、常に年長者を敬う者には、四つの法（性質）が増え行く──寿命、色艶、安楽、活力が。",
    110: "〔心が〕定められていない劣戒の者であるなら、そして、彼が、百年のあいだ、生きるとして、戒ある瞑想者の一日の生のほうが、より勝っている。",
    111: "〔心が〕定められていない智慧浅き者であるなら、そして、彼が、百年のあいだ、生きるとして、智慧ある瞑想者の一日の生のほうが、より勝っている。",
    112: "怠惰で精進に劣る者であるなら、そして、彼が、百年のあいだ、生きるとして、断固として精進に励んでいる者の一日の生のほうが、より勝っている。",
    113: "〔事物の〕生成と衰失（無常）を見ずにいる者であるなら、そして、彼が、百年のあいだ、生きるとして、〔事物の〕生成と衰失を〔常に〕見ている者の一日の生のほうが、より勝っている。",
    114: "不死の境処（涅槃）を見ずにいる者であるなら、そして、彼が、百年のあいだ、生きるとして、不死の境処を〔常に〕見ている者の一日の生のほうが、より勝っている。",
    115: "最上の法（真理）を見ずにいる者であるなら、そして、彼が、百年のあいだ、生きるとして、最上の法（真理）を〔常に〕見ている者の一日の生のほうが、より勝っている。",
}

OBSERVE = {
    100: "たとい無益の語を集めて一千言を成すとも、聞きて寂静を得べき、有益の一語これに勝る。",
    101: "たとい無益の句を集めて一千偈を成すとも、聞きて寂静を得べき、一偈の一語これに勝る。",
    102: "無益の句よりなる百偈を誦すとも、聞きて寂静を得べき、一偈の一語これに勝る。",
    103: "戦場に於て百万人に勝つとも、一の自己に克つ者こそ実に最上の戦勝者なれ。",
    104: "克服せられたる自己は、実に他の衆人に勝る。 自己を制御し、常に節制して行う人の〔勝利を〕、",
    105: "天神も、乾闥婆（けんだつば）も、魔王もまた梵天も、かかる人の勝利を〔転じて〕敗北となすことあたわず。",
    106: "月に月に千金を投じて供犠すること百年、しかも一人のよく修養せる人に供養すること瞬時なれば、この供養はかの百年の祭祀に勝る。",
    107: "林中に於て祭火に奉仕すること百年、しかも一人のよく修養せる人に供養すること瞬時なれば、この供養はかの百年の祭祀に勝る。",
    108: "この世に於て、福を求めて一年の間、或いは供犠し或いは祭祀に従事するも、そのすべては、直行の人（阿羅漢）を敬礼する四分の一に値せず。",
    109: "敬礼を守り、常に長上を尊ぶ人には、四種の法増長す、すなわち寿と美と楽と力と。",
    110: "百歳の寿を全うするも、戒を破り三昧に住せざれば、戒を持し禅定に住する者の一日の生、これに勝る。",
    111: "百歳の寿を全うするも、無知にして三昧に住せざれば、智慧を具し禅定に住する者の一日の生、これに勝る。",
    112: "百歳の寿を全うするも、怠惰にして精進せざれば、堅固なる精進を行ずる者の一日の生、これに勝る。",
    113: "百歳の寿を全うするも、生滅の〔理〕を見ざれば、生滅の〔理〕を見る者の一日の生、これに勝る。",
    114: "百歳の寿を全うするも、不死の道（涅槃）を見ざれば、不死の道を見る者の一日の生、これに勝る。",
    115: "百歳の寿を全うするも、最上の法を見ざれば、最上の法を見る者の一日の生、これに勝る。",
}

CHINESE = {
    100: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-001",
          "text": "雖誦千言，句義不正，不如一要，聞可滅意。", "satLocus": "大正蔵 T4.565b 述千品第1頌"},
    101: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-002",
          "text": "雖誦千章，不義何益？不如一義，聞行可度。", "satLocus": "大正蔵 T4.565b 述千品第2頌"},
    102: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-003",
          "text": "雖多誦經，不解何益？解一法句，行可得道。", "satLocus": "大正蔵 T4.565b 述千品第3頌"},
    103: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-004",
          "text": "千千為敵，一夫勝之，未若自勝，為戰中上。", "satLocus": "大正蔵 T4.565b 述千品第4頌"},
    104: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-005",
          "text": "自勝最賢，故曰人雄，護意調身，自損至終。", "satLocus": "大正蔵 T4.565b 述千品第5頌"},
    105: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-006",
          "text": "雖曰尊天，神魔梵釋，皆莫能勝，自勝之人。", "satLocus": "大正蔵 T4.565b 述千品第6頌"},
    106: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-007",
          "text": "月千反祠，終身不輟，不如須臾，一心念法，一念道福，勝彼終身。", "satLocus": "大正蔵 T4.565b 述千品第7頌"},
    107: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-008",
          "text": "雖終百歲，奉事火祠，不如須臾，供養三尊，一供養福，勝彼百年。", "satLocus": "大正蔵 T4.565b 述千品第8頌"},
    108: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-009",
          "text": "祭神以求福，從後觀其報，四分未望一，不如禮賢者。", "satLocus": "大正蔵 T4.565b 述千品第9頌"},
    109: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-010",
          "text": "能善行禮節，常敬長老者，四福自然增，色力壽而安。", "satLocus": "大正蔵 T4.565b 述千品第10頌"},
    110: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-011",
          "text": "若人壽百歲，遠正不持戒，不如生一日，守戒正意禪。", "satLocus": "大正蔵 T4.565b 述千品第11頌"},
    111: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-012",
          "text": "若人壽百歲，邪偽無有智，不如生一日，一心學正智。", "satLocus": "大正蔵 T4.565c 述千品第12頌"},
    112: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-013",
          "text": "若人壽百歲，懈怠不精進，不如生一日，勉力行精進。", "satLocus": "大正蔵 T4.565c 述千品第13頌"},
    113: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-014",
          "text": "若人壽百歲，不知成敗事，不如生一日，見微知所忌。", "satLocus": "大正蔵 T4.565c 述千品第14頌"},
    114: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-015",
          "text": "若人壽百歲，不見甘露道，不如生一日，服行甘露味。", "satLocus": "大正蔵 T4.565c 述千品第15頌"},
    115: {"status": "mapped", "pin": "述千品（T210 第16品）", "t210": "T210-16-016",
          "text": "若人壽百歲，不知大道義，不如生一日，學惟佛法要。", "satLocus": "大正蔵 T4.565c 述千品第16頌"},
}

VERSE_PRACTICE = {
    100: {"nidanaId": "contact", "pathFactors": ["正語", "正念"], "reason": "千言より、聞いて心が静まる一語が勝る"},
    101: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "千偈より、聞いて心が静まる一句が勝る"},
    102: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "百偈より、聞いて心が静まる法句が勝る"},
    103: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "百万人に勝つより、自己に克つ者が最上"},
    104: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "自己を調御し節制する勝利は他に勝る"},
    105: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "自己に勝った者の勝利は天魔も覆せない"},
    106: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "百年の祭祀より、修養者への瞬時の供養が勝る"},
    107: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "百年の祭火より、修養者への瞬時の供養が勝る"},
    108: {"nidanaId": "craving", "pathFactors": ["正見", "正念"], "reason": "一年の祭祀も、直行者への敬礼の四分の一に値せず"},
    109: {"nidanaId": "contact", "pathFactors": ["正業", "正念"], "reason": "長上を敬えば寿・美・楽・力が増す"},
    110: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "戒と禅定の一日は、劣戒の百年に勝る"},
    111: {"nidanaId": "review", "pathFactors": ["正見", "正定"], "reason": "智慧と禅定の一日は、無知の百年に勝る"},
    112: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "堅固な精進の一日は、怠惰の百年に勝る"},
    113: {"nidanaId": "feeling", "pathFactors": ["正見", "正念"], "reason": "生滅を見る一日は、見ぬ百年に勝る"},
    114: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "不死の道を見る一日は、見ぬ百年に勝る"},
    115: {"nidanaId": "review", "pathFactors": ["正見", "正念"], "reason": "最上の法を見る一日は、見ぬ百年に勝る"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP8-P01", 100), ("DP8-P02", 100),
    ("DP8-P03", 101), ("DP8-P04", 101),  # 101–102 combined (both pairs)
    ("DP8-P05", 103), ("DP8-P06", 103),
    ("DP8-P07", 104), ("DP8-P08", 104),  # 104–105 combined
    ("DP8-P09", 106), ("DP8-P10", 106),  # 106–107 combined
    ("DP8-P11", 108),
    ("DP8-P12", 109),
    ("DP8-P13", 110), ("DP8-P14", 110),
    ("DP8-P15", 111),
    ("DP8-P16", 112), ("DP8-P17", 112),
    ("DP8-P18", 113), ("DP8-P19", 113),
    ("DP8-P20", 114), ("DP8-P21", 114),
    ("DP8-P22", 115), ("DP8-P23", 115),
]

COMBINED = {
    101: (101, 102),
    104: (104, 105),
    106: (106, 107),
}


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
    old = json.loads((DATA / "ch8.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        if verse in COMBINED:
            a, b = COMBINED[verse]
            observe = OBSERVE[a] + " " + OBSERVE[b]
            quote = QUOTES[a] + " " + QUOTES[b]
            pali_locus = f"小部・ダンマパダ 千の章 第{a}-{b}偈"
            modern_locus = f"第８章・千品 第{a}-{b}偈（#ch02-08）"
            zh = chinese_block(a)
            verse_out = a
            reason = vp["reason"]
            nidana = vp["nidanaId"]
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 千の章 第{verse}偈"
            modern_locus = f"第８章・千品 第{verse}偈（#ch02-08）"
            zh = chinese_block(verse)
            verse_out = verse
            reason = vp["reason"]
            nidana = vp["nidanaId"]

        pairs.append({
            "id": pid,
            "category": LABEL_TO_ID[factors[0]],
            "verse": verse_out,
            "observe": observe,
            "action": actions[pid],
            "quote": quote,
            "nidanaId": nidana,
            "pathFactors": factors,
            "pathReason": reason,
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

    TITLE = "ダンマパダ 第8章・千品（千の章）"
    SHORT = "千品（千の章）"
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
            "id": "contact", "weekday": 1, "categoryId": "speech", "nidanaLabel": "接触",
            "pathFactors": ["正語", "正念"], "pathFactorIds": ["speech", "mindfulness"],
            "pathLabel": "触れた場で、千より勝る一語を選ぶ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見方が、今朝の接触の土台になる",
            "toNext": "意味ある一語は、心を静める入口になる",
            "todayObserve": OBSERVE[100],
            "todayAction": actions["DP8-P01"],
            "when": ["返答が急がれた", "情報が多い"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[100][:40] + "…",
            "secondaryObserve": "長上への敬礼は、寿・美・楽・力を増す",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "生滅する受を、一日の生の質として見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、快・不快の受が立ち上がる",
            "toNext": "生滅を見れば欲しがりに落ちにくい",
            "todayObserve": OBSERVE[113],
            "todayAction": actions["DP8-P18"],
            "when": ["つらい状況", "始まりと終わりが見えた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[113][:40] + "…",
            "secondaryObserve": "生滅を見る一日は、見ぬ百年に勝る",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "福を求める祭祀より、敬礼の心を選ぶ",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、福徳・儀式への欲しがりへ落ちる",
            "toNext": "止めないと形だけの掴みへ進む",
            "todayObserve": OBSERVE[108],
            "todayAction": actions["DP8-P11"],
            "when": ["形だけの習慣", "見返りを求めた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[108][:40] + "…",
            "secondaryObserve": "直行者への敬礼は、一年の祭祀に勝る",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "effort", "nidanaLabel": "掴む",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "外の勝利への掴みを手放し、自己に克つ",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、外の成果と承認に乗る手前",
            "toNext": "掴むと内なる節制の勝利を見失う",
            "todayObserve": OBSERVE[103],
            "todayAction": actions["DP8-P06"],
            "when": ["誰かに勝ちたい", "外の結果に執着した"],
            "sources": by_nidana.get("clinging", []) or by_nidana.get("release", [])[:3],
            "leadQuote": QUOTES[103][:40] + "…",
            "secondaryObserve": "自己に克つ者こそ、最上の戦勝者",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "mindfulness", "nidanaLabel": "苦が太る",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "外に負けても、内なる勝利は奪えないと見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、外の勝敗に心が重くなる",
            "toNext": "見れば、内なる節制へ戻れる",
            "todayObserve": OBSERVE[105],
            "todayAction": actions["DP8-P08"],
            "when": ["苦境にある", "誰かに負けた気がする"],
            "sources": by_nidana.get("suffering", []) or ["DP8-P08"],
            "leadQuote": QUOTES[105][:40] + "…",
            "secondaryObserve": "自己に勝った者の勝利は、天魔も覆せない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "怠惰を離れ、自己調御と精進へ戻る",
            "chapterHint": SHORT,
            "fromPrev": "外への執着と怠惰が流れを加速させる",
            "toNext": "精進の一日は、怠惰の百年に勝る",
            "todayObserve": OBSERVE[112],
            "todayAction": actions["DP8-P16"],
            "when": ["怠けたい", "誘惑が強い"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[112][:40] + "…",
            "secondaryObserve": "不死の道を見る一日は、見ぬ百年に勝る",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "一日の生の質を、量ではなく質で振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の語り・行いは朝からの心の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE[110],
            "todayAction": actions["DP8-P04"],
            "when": ["一日を閉じるとき", "長く生きた実感がない日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[110][:40] + "…",
            "secondaryObserve": "戒・慧・精進・法を見た一日が勝る",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 8,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第8章（千品／千の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210述千品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・千の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第８章・千品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・述千品（T4.565b）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "contact",
            "focusReason": "千品は「千より一」の質を、言葉・自己・供養・一日の生で示す。既定の焦点は接触。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch8.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch8.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 9):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch8", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])
    for k, v in entries.items():
        print(k, [(e["chapterId"], e["pairCount"]) for e in v])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 23
    assert all(p["id"] == f"DP8-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(100, 116))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    print("OK")


if __name__ == "__main__":
    main()
