#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch17.json (忿怒品) to match ch1–ch16 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-17"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0568"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap17/"
)

QUOTES = {
    221: "忿激〔の思い〕（忿）を捨棄するように。〔我想の〕思量（慢）を捨棄し去るように。束縛するもの（結）の一切を超越するように。無一物の者に、名前と色形（名色：心的作用と肉体）について執着せずにいる者に、彼に、諸々の苦しみが従い行くことはない。",
    222: "迷走する車を阻止するように、彼が、まさに、沸き起こった忿激〔の思い〕を〔調御するなら〕、わたしは、彼を「馭者」と説く。他の人々は、手綱を掴むが、〔それだけのこと〕。",
    223: "忿激なき〔心〕によって、忿激に勝つのだ。善によって、不善に勝つのだ。布施によって、吝嗇に勝つのだ。真理（諦：真実）によって、偽りを説く者に〔勝つのだ〕。",
    224: "真理を話すように。忿激しないように。乞われた者は、たとえ、少なくとも施すように。これらの三つの境位によって、天〔の神々〕たちの現前に至るであろう。",
    225: "彼ら、牟尼たちは、〔生類を〕害さず、常に身体によって統御された者たちである。彼らは、死滅なき境位へと行く──すなわち、赴いて〔そののち〕、憂い悲しまないところ（涅槃）へと。",
    226: "常に〔眠らずに〕起きていて、昼夜に学び、涅槃を志す者たちの、諸々の煩悩（漏）は〔自ずと〕滅却に至る。",
    227: "アトゥラよ、これは、過去からのことである。これは、今日一日のようなことにあらず。〔人々は〕沈黙して坐っている者を非難し、多く話す者を非難し、節度をもって話す者さえも非難する。世において、非難されずにいた者は、〔どこにも〕存在しない。",
    228: "そして、〔これまでに〕有ったことはなく、さらに、〔これからも〕有ることはなく、かつまた、今現在も見出されない──〔すなわち〕一方的に非難された人も、あるいは、一方的に賞賛された〔人〕も。",
    229: "生活に瑕疵なく思慮ある者を、智慧と戒によって〔心が〕定められた者を、もし、識者たちが、日々に随知して、彼を賞賛するなら──",
    230: "まさしく、ジャンブー川の金貨（高品質の砂金で鋳造した金貨）たる彼を非難することが、誰ができるというのだろう。天〔の神々〕たちもまた、彼を賞賛し、梵〔天〕（ブラフマー神）からもまた、賞賛される者となる。",
    231: "身体（身）の動乱を守り押さえるがよい。身体によって統御された者として存するがよい。身体による悪しき行ないを捨棄して、身体による善き行ないを行なうがよい。",
    232: "言葉（口・語）の動乱を守り押さえるがよい。言葉によって統御された者として存するがよい。言葉による悪しき行ないを捨棄して、言葉による善き行ないを行なうがよい。",
    233: "意（意）の動乱を守り押さえるがよい。意によって統御された者として存するがよい。意による悪しき行ないを捨棄して、意による善き行ないを行なうがよい。",
    234: "慧者たちは、身体によって統御された者たちであり、さらに、言葉によって統御された者たちである。慧者たちは、意によって統御された者たちであり、彼らは、まさに、完全無欠の統御者たちである。",
}

OBSERVE = {
    221: "忿怒を去るべし、慢心を捨つべし、一切の繋縛（けばく）を脱すべし。 かく名色（精神・物質）に執着せざる無一物の人には苦の随うことなし。",
    222: "勃発したる忿怒を、動揺する馬車の如くに抑止する人、我はこれを〔真の〕御者と呼ぶ。 他はただ手綱を執れるのみ。",
    223: "忍辱（にんにく）によりて忿怒を克服すべし。 善によりて不善を克服すべし。 施与によりて吝嗇者（りんしょくしゃ）を克服すべし。 真実によりて妄語者を〔克服すべし〕。",
    224: "真実を語るべし。 怒るべからず。 〔自己の所有〕少しといえども乞わるれば与うべし。 この三事により諸天の元に至り得るべし。",
    225: "殺生することなく、常に身を制御する賢者は、そこに至りて憂患なき不死の境（涅槃）に達す。",
    226: "常に覚醒し、昼夜に勉学し、涅槃に志す者の煩悩は終息す。",
    227: "アトゥラ（優婆塞の名）よ、こは古来より然り、今始まれるにあらず。 〔すなわち〕人は黙して坐するを謗り、多言を謗り、寡言をもまた謗る。 世に謗られざる者なし。",
    228: "ただ謗らるるのみの人、またはただ褒めらるるのみの人は、〔過去にも〕なかりき、〔将来にも〕なかるべし、現在にもまたなし。",
    229: "智者よく判別して日々に称讃し、所行失なく、賢明にして、慧戒兼ね備わるとなす者あらば、",
    230: "あたかも閻浮檀金（えんぶだごん）にて造りし貨幣の如く、誰か彼を謗り得んや。 諸天も彼を称讃し、彼は梵天によりてもまた称讃せらる。",
    231: "身の忿怒を摂護し、身を制御すべし。 身の悪行を捨て、身によりて善行を修すべし。",
    232: "語の忿怒を摂護し、語を制御すべし。 語の悪行を捨て、語によりて善行を修すべし。",
    233: "意の忿怒を摂護し、意を制御すべし。 意の悪行を捨て、意によりて善行を修すべし。",
    234: "身を制御し、また語を制御し、意を制御する賢者は実によく制御せるものなり。",
}

CHINESE = {
    221: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-016",
          "text": "捨恚離慢，避諸愛貪，不著名色，無為滅苦。", "satLocus": "大正蔵 T4.568b 忿怒品第16頌"},
    222: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-003",
          "text": "恚能自制，如止奔車，是為善御，棄冥入明。", "satLocus": "大正蔵 T4.568a 忿怒品第3頌"},
    223: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-004",
          "text": "忍辱勝恚，善勝不善，勝者能施，至誠勝欺。", "satLocus": "大正蔵 T4.568a 忿怒品第4頌"},
    224: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-005",
          "text": "不欺不怒，意不多求，如是三事，死則上天。", "satLocus": "大正蔵 T4.568a 忿怒品第5頌"},
    225: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-006",
          "text": "常自攝身，慈心不殺，是生天上，到彼無憂。", "satLocus": "大正蔵 T4.568a 忿怒品第6頌"},
    226: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-007",
          "text": "意常覺悟，明暮勤學，漏盡意解，可致泥洹。", "satLocus": "大正蔵 T4.568a 忿怒品第7頌"},
    227: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-008",
          "text": "人相謗毀，自古至今，既毀多言，又毀訥訒，亦毀中和，世無不毀。", "satLocus": "大正蔵 T4.568a 忿怒品第8頌"},
    228: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-009",
          "text": "欲意非聖，不能制中，一毀一譽，但為利名。", "satLocus": "大正蔵 T4.568a 忿怒品第9頌"},
    229: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-010",
          "text": "明智所譽，唯稱是賢，慧人守戒，無所譏謗。", "satLocus": "大正蔵 T4.568b 忿怒品第10頌"},
    230: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-011",
          "text": "如羅漢淨，莫而誣謗，諸天咨嗟，梵釋所稱。", "satLocus": "大正蔵 T4.568b 忿怒品第11頌"},
    231: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-012",
          "text": "常守慎身，以護瞋恚，除身惡行，進修德行。", "satLocus": "大正蔵 T4.568b 忿怒品第12頌"},
    232: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-013",
          "text": "常守慎言，以護瞋恚，除口惡言，誦習法言。", "satLocus": "大正蔵 T4.568b 忿怒品第13頌"},
    233: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-014",
          "text": "常守慎心，以護瞋恚，除意惡念，思惟念道。", "satLocus": "大正蔵 T4.568b 忿怒品第14頌"},
    234: {"status": "mapped", "pin": "忿怒品（T210 第25品）", "t210": "T210-25-015",
          "text": "節身慎言，守攝其心，捨恚行道，忍辱最強。", "satLocus": "大正蔵 T4.568b 忿怒品第15頌"},
}

VERSE_PRACTICE = {
    221: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "忿激と慢を捨て、名色への執着を離す"},
    222: {"nidanaId": "feeling", "pathFactors": ["正念", "正精進"], "reason": "勃発した忿激を、馬車の如く抑止する"},
    223: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "忍辱・善・施与・真実で忿激に勝つ"},
    224: {"nidanaId": "release", "pathFactors": ["正語", "正念"], "reason": "真実を語り、怒らず、乞われれば与える"},
    225: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "害さず身を制御し、憂いなき境へ"},
    226: {"nidanaId": "review", "pathFactors": ["正念", "正精進"], "reason": "常に覚醒し、昼夜に学び、涅槃に志す"},
    227: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "世に謗られざる者なし、古来より然り"},
    228: {"nidanaId": "suffering", "pathFactors": ["正念", "正見"], "reason": "ただ謗るのみ・褒めるのみの人はいない"},
    229: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "慧戒兼ね備えた者を、智者が称讃する"},
    230: {"nidanaId": "release", "pathFactors": ["正念", "正見"], "reason": "諸天も梵天も、彼を称讃する"},
    231: {"nidanaId": "clinging", "pathFactors": ["正念", "正業"], "reason": "身の忿怒を摂護し、身の善行を修す"},
    232: {"nidanaId": "clinging", "pathFactors": ["正語", "正念"], "reason": "語の忿怒を摂護し、語の善行を修す"},
    233: {"nidanaId": "craving", "pathFactors": ["正念", "正定"], "reason": "意の忿怒を摂護し、意の善行を修す"},
    234: {"nidanaId": "review", "pathFactors": ["正念", "正業"], "reason": "身・語・意を制御する賢者はよく制御せる者"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP17-P01", 221), ("DP17-P02", 221),
    ("DP17-P03", 222), ("DP17-P04", 222),
    ("DP17-P05", 223), ("DP17-P06", 223),
    ("DP17-P07", 224), ("DP17-P08", 224),
    ("DP17-P09", 225),
    ("DP17-P10", 226),
    ("DP17-P11", 227),
    ("DP17-P12", 228),
    ("DP17-P13", 229),  # 229–230
    ("DP17-P14", 231),
    ("DP17-P15", 232),
    ("DP17-P16", 233),
    ("DP17-P17", 234), ("DP17-P18", 234),
    ("DP17-P19", 221),
]

COMBINED = {
    229: (229, 230),
}


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    c.setdefault(
        "note",
        "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
    )
    return c


def main():
    old = json.loads((DATA / "ch17.json").read_text(encoding="utf-8"))
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
            pali_locus = f"小部・ダンマパダ 忿激の章 第{a}-{b}偈"
            modern_locus = f"第１７章・忿怒品 第{a}-{b}偈（#ch02-17）"
            zh = chinese_block(a)
            verse_out = a
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 忿激の章 第{verse}偈"
            modern_locus = f"第１７章・忿怒品 第{verse}偈（#ch02-17）"
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

    TITLE = "ダンマパダ 第17章・忿怒品（忿激の章）"
    SHORT = "忿怒品（忿激の章）"
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
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "謗りに触れても、世に謗られざる者なしと知る",
            "chapterHint": SHORT,
            "fromPrev": "前夜の制御の見直しが、今朝の謗りへの不動になる",
            "toNext": "接触のあと、忿激の受が勃発しやすい",
            "todayObserve": OBSERVE[227],
            "todayAction": actions["DP17-P11"],
            "when": ["批判された", "朝の始まり"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[227][:40] + "…",
            "secondaryObserve": "世に謗られざる者なし、古来より然り",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "勃発した忿激の受を、真の御者として抑止する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、忿激の受が沸き起こる",
            "toNext": "受けた怒りを、仕返しの欲しがりへ落とさない",
            "todayObserve": OBSERVE[222],
            "todayAction": actions["DP17-P03"],
            "when": ["怒りが勃発した", "言い返したくなった"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[222][:40] + "…",
            "secondaryObserve": "忿激を抑止する人が真の御者",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "意の忿怒を欲しがらず、意の善行へ向ける",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、意の怒りへの欲しがりへ落ちる",
            "toNext": "止めないと身・語の掴みへ進む",
            "todayObserve": OBSERVE[233],
            "todayAction": actions["DP17-P16"],
            "when": ["心の中で怒りが燃えた", "意地を張りそう"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[233][:40] + "…",
            "secondaryObserve": "意の忿怒を摂護し、意の善行を修す",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "忿激・慢・身語の怒りを掴まず、繋縛を脱す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、忿激・慢として掴む手前",
            "toNext": "掴むと苦が随い、離すと忍辱へ向かう",
            "todayObserve": OBSERVE[221],
            "todayAction": actions["DP17-P01"],
            "when": ["怒りを手放せない", "慢心が湧いた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[221][:40] + "…",
            "secondaryObserve": "身・語の忿怒を摂護し、善行を修す",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "一方的な謗り・褒めへの執着が苦になると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、評価への苦が熟す",
            "toNext": "見れば、忍辱と真実の語へ向き直る",
            "todayObserve": OBSERVE[228],
            "todayAction": actions["DP17-P12"],
            "when": ["批判に落ち込んだ", "褒めに有頂天になった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[228][:40] + "…",
            "secondaryObserve": "ただ謗るのみ・褒めるのみの人はいない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "action", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "忍辱・真実・施与で忿激から離す",
            "chapterHint": SHORT,
            "fromPrev": "忿激への掴みが流れを加速させる",
            "toNext": "離すと、身語意の制御の見直しへつながる",
            "todayObserve": OBSERVE[223],
            "todayAction": actions["DP17-P05"],
            "when": ["怒りを克服したい", "真実で応じたい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[223][:40] + "…",
            "secondaryObserve": "真実を語り、怒らず、乞われれば与える",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "身・語・意を制御できたか、覚醒して見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、忿激か制御かの跡",
            "toNext": "見直しが、翌朝の謗りへの不動になる",
            "todayObserve": OBSERVE[234],
            "todayAction": actions["DP17-P17"],
            "when": ["一日を閉じるとき", "制御を確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[234][:40] + "…",
            "secondaryObserve": "常に覚醒し、昼夜に学び、涅槃に志す",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 17,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第17章（忿怒品／忿激の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210忿怒品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・忿激の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１７章・忿怒品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・忿怒品（T4.568a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "clinging",
            "focusReason": "忿怒品は忿激・慢・身語意の怒りを掴まず脱することが中心。既定の焦点は掴む。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch17.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch17.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 18):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch17", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 19
    assert all(p["id"] == f"DP17-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(221, 235))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    print("OK")


if __name__ == "__main__":
    main()
