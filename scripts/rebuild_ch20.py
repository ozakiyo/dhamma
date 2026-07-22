#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch20.json (道品) to match ch1–ch19 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-20"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0569"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap20/"
)

QUOTES = {
    273: "諸々の道のなかでは、〔聖なる〕八つの支分ある〔道〕（八正道）が最勝である。諸々の真理のなかでは、四つの〔聖なる〕境処（四聖諦）が〔最勝である〕。諸々の法（教え）のなかでは、離貪〔の法〕が最勝である。そして、二足の者（人間）たちのなかでは、眼ある者が〔最勝である〕。",
    274: "これこそは、道である。見の清浄のための、他〔の道〕は存在しない。まさに、この〔道〕を、あなたたちは実践しなさい──悪魔を迷妄ならしむ、この〔道〕を。",
    275: "まさに、この〔道〕を実践したなら、あなたたちは、苦しみの終極を為すであろう。矢を折ることを了知して、わたしによって、あなたたちに、道は告げ知らされた。",
    276: "熱く為すべきは、あなたたちである。如来たちは、〔道を〕告げ知らせる者たちである。〔この道を〕実践した瞑想者たちは、悪魔の結縛から解き放たれるであろう。",
    277: "すなわち、「諸々の形成〔作用〕（形成されたもの・現象世界）は、全てが常住ならざるものである（諸行無常）」と、智慧によって見るとき、そこで、苦しみについて厭離する──これは、清浄への道である。",
    278: "すなわち、「諸々の形成〔作用〕（形成されたもの・現象世界）は、全てが苦しみである（一切皆苦）」と、智慧によって見るとき、そこで、苦しみについて厭離する──これは、清浄への道である。",
    279: "すなわち、「諸々の法（事象）は、全てが自己ならざるものである（諸法無我）」と、智慧によって見るとき、そこで、苦しみについて厭離する──これは、清浄への道である。",
    280: "奮起する時に奮起せずにいる者、若く力があるのに怠け癖を具した者、思惟と意〔の働き〕が沈滞した怠惰の者──怠け者は、智慧によって道を見出すことがない。",
    281: "言葉（口・語）を守り、意（意）によって善く統御され、そして、身体（身）によって善ならざることを為さないなら、これらの三つの行為の道を清め、聖賢によって知らされた道に達するであろう。",
    282: "〔心の〕制止（瑜伽）あるがゆえに、まさに、英知は生まれる。〔心の〕制止なきがゆえに、英知の消滅がある。実体（有：存在）への〔道を〕、さらに、虚無（非有：無）への〔道を〕──この二種の道を〔あるがままに〕知って、すなわち、英知が増え行くままに、そのように、自己を確たるものとするがよい。",
    283: "〔欲の〕林を断て──木を〔断つの〕ではなく。〔欲の〕林からは、恐怖が生まれる。かつまた、林を、かつまた、林の下生えを、〔両者ともに〕断って、比丘たちよ、〔欲の〕林なき者たちと成れ。",
    284: "まさに、女たちにたいする男の〔欲の〕林の下生えが、微塵ばかりでさえも断たれずにある、そのかぎりは、そのあいだ、彼は、まさしく、意が縛られた者となる──乳を飲む子牛が、母〔牛〕にたいするように。",
    285: "自己への愛執〔の思い〕を断て──秋の蓮を、手で〔断ち切る〕ように。善き至達者（善逝：ブッダの尊称）によって説示された涅槃〔の境処〕を、寂静の道こそを、育てよ。",
    286: "「雨期のあいだ、〔わたしは〕ここに住するであろう。冬と夏には、ここに〔住するであろう〕」〔と〕、かくのごとく、愚者は熟慮するが、〔すぐ目の前の〕障り（危険）を覚らない。",
    287: "彼を、子供や家畜に夢中になり執着の意図ある人を、死魔は取って去り行く──眠りについた村を、大激流が〔流し去ってしまう〕ように。",
    288: "子供たちは、〔わが身の〕救いのために存在するのではない。父親も、さにあらず。眷属たちもまた、さにあらず。死神に囚われた者の救い手は、親族たちのなかには存在しない。",
    289: "この義（利益）たる所以を知って、戒において統御された賢者は、涅槃に至る道を、まさしく、すみやかに清めるであろう。",
}

OBSERVE = {
    273: "諸道の中、八支（八支聖道）最も勝れ、諸諦の中、四句（四聖諦）最も勝れ、諸法の中、離欲最も勝れ、二足（人間）の中、具眼者〔最も勝る〕。",
    274: "唯この道あるのみ、知見を浄むるに他の〔道〕あることなし。 汝らこの〔道〕を行くべし。 これ魔王を幻惑するものなり。",
    275: "汝らこの〔道〕を行かば、苦を終息せしむべし。 〔欲〕矢を除去することを悟りて、我実にこの道を説けり。",
    276: "汝らまさに努力すべし。 如来は説者なり。 禅定に住して〔この道を〕行く者は、魔王の繋縛を脱すべし。",
    277: "一切の事象は無常なりと、智によりて観る時、苦を厭離す。 これ浄に至る道なり。",
    278: "一切の事象は苦なりと、智によりて観る時、苦を厭離す。 これ浄に至る道なり。",
    279: "一切の法は無我なりと、智によりて観る時、苦を厭離す。 これ浄に至る道なり。",
    280: "起つべき時に起たず、若く強くして怠惰に陥り、意気消沈して惰弱・懶惰なる者は、智によりて道を得ることなし。",
    281: "語を慎しみ、意をよく制御し、身を以て不善をなすべからず。 この三業道を浄むべし。 〔然らば〕聖仙所説の道を得ん。",
    282: "実に智は瑜伽（瞑想）より生じ、瑜伽を行ぜざれば智は滅ぶ。 この得と失との両道を知り、自ら努めて、以て智を増大せしむべし。",
    283: "欲林を伐れ、樹木を〔伐るに止まる〕なかれ。 欲林より畏怖生ず。 欲林と欲叢とを伐りて、比丘らよ、欲林より脱せよ。",
    284: "男子の女子に対する欲情、いささかなりとも断たれざる間は、彼の心は繋縛せらる、あたかも乳を飲む子牛の母牛に於けるが如く。",
    285: "自己に対する愛を断つこと、秋の蓮を手にて〔折るが〕如くせよ。 寂静の道のみを固守せよ。 涅槃は善逝（仏陀）により説かれたり。",
    286: "「我雨期にはここに住せん、冬と夏とはここに〔住せん〕」と、愚者は思惟して、死の〔至る〕を覚らず。",
    287: "子と家畜とに惑溺し、その心これに執着せる人を、死は捉え去る、あたかも眠れる村落を、瀑流の〔漂蕩し去る〕が如く。",
    288: "子も救うあたわず、父も親戚もまた〔救うあたわず〕。 死に捉えられし者を救うは、親族もなすあたわざる所なり。",
    289: "この義を知りて、賢者は戒により制御し、涅槃に至る道を速やかに浄むべし。",
}

PIN28 = "道行品（T210 第28品）"
PIN13 = "愚闇品（T210 第13品）"
PIN01 = "無常品（T210 第1品）"

CHINESE = {
    273: {"status": "mapped", "pin": PIN28, "t210": "T210-28-001",
          "text": "八直最上道，四諦為法迹，不婬行之尊，施燈必得眼。", "satLocus": "大正蔵 T4.569a 道行品第1頌"},
    274: {"status": "mapped", "pin": PIN28, "t210": "T210-28-002",
          "text": "是道無復畏，見淨乃度世，此能壞魔兵，力行滅邪苦。", "satLocus": "大正蔵 T4.569a 道行品第2頌"},
    275: {"status": "mapped", "pin": PIN28, "t210": "T210-28-003",
          "text": "我已開正道，為大現異明，已聞當自行，行乃解邪縛。", "satLocus": "大正蔵 T4.569a 道行品第3頌"},
    276: {"status": "mapped", "pin": PIN28, "t210": "T210-28-022",
          "text": "吾語汝法，愛箭為射，宜以自勗，受如來言。", "satLocus": "大正蔵 T4.569c 道行品第22頌",
          "note": "パーリ道の章276はT210道行品第22頌に対応（蘇錦坤對照表）。"},
    277: {"status": "mapped", "pin": PIN28, "t210": "T210-28-004",
          "text": "生死非常苦，能觀見為慧，欲離一切苦，行道一切除。", "satLocus": "大正蔵 T4.569a 道行品第4頌"},
    278: {"status": "mapped", "pin": PIN28, "t210": "T210-28-020",
          "text": "知眾行苦，是為慧見，罷厭世苦，從是道除。", "satLocus": "大正蔵 T4.569c 道行品第20頌"},
    279: {"status": "mapped", "pin": PIN28, "t210": "T210-28-021",
          "text": "眾行非身，是為慧見，罷厭世苦，從是道除。", "satLocus": "大正蔵 T4.569c 道行品第21頌"},
    280: {"status": "mapped", "pin": PIN28, "t210": "T210-28-006",
          "text": "起時當即起，莫如愚覆淵，與墮無瞻聚，計罷不進道。", "satLocus": "大正蔵 T4.569a–b 道行品第6頌"},
    281: {"status": "mapped", "pin": PIN28, "t210": "T210-28-008",
          "text": "慎言守意正，身不善不行，如是三行除，佛說是得道。", "satLocus": "大正蔵 T4.569b 道行品第8頌"},
    282: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ道の章282はT210に対応なし（蘇錦坤對照表）。"},
    283: {"status": "mapped", "pin": PIN28, "t210": "T210-28-009",
          "text": "斷樹無伐本，根在猶復生，除根乃無樹，比丘得泥洹。", "satLocus": "大正蔵 T4.569b 道行品第9頌"},
    284: {"status": "mapped", "pin": PIN28, "t210": "T210-28-010",
          "text": "不能斷樹，親戚相戀，貪意自縛，如犢慕乳。", "satLocus": "大正蔵 T4.569b 道行品第10頌"},
    285: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ道の章285はT210に対応なし（蘇錦坤對照表）。"},
    286: {"status": "mapped", "pin": PIN13, "t210": "T210-13-005",
          "text": "暑當止此，寒當止此，愚多預慮，莫知來變。", "satLocus": "大正蔵 T4.563b 愚闇品第5頌",
          "note": "パーリ道の章286はT210道行品ではなく愚闇品に対応（蘇錦坤對照表）。"},
    287: {"status": "mapped", "pin": PIN28, "t210": "T210-28-014",
          "text": "人營妻子，不觀病法，死命卒至，如水湍驟。", "satLocus": "大正蔵 T4.569b 道行品第14頌"},
    288: {"status": "mapped", "pin": PIN01, "t210": "T210-01-017",
          "text": "非有子恃，亦非父兄，為死所迫，無親可怙。", "satLocus": "大正蔵 T4.559a 無常品第17頌",
          "note": "パーリ道の章288はT210道行品ではなく無常品に対応（蘇錦坤對照表）。"},
    289: {"status": "mapped", "pin": PIN28, "t210": "T210-28-016",
          "text": "慧解是意，可修經戒，勤行度世，一切除苦。", "satLocus": "大正蔵 T4.569b 道行品第16頌"},
}

VERSE_PRACTICE = {
    273: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "八正道・四諦・離欲・具眼者が最勝と知る接触"},
    274: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "知見を浄める道はこの道のみ"},
    275: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "この道を行けば苦を終息せしめ得る"},
    276: {"nidanaId": "release", "pathFactors": ["正精進", "正定"], "reason": "如来は説者、自ら努力し禅定に住して魔の繋縛を脱す"},
    277: {"nidanaId": "feeling", "pathFactors": ["正見", "正念"], "reason": "諸行無常と観るとき苦を厭離す"},
    278: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "諸行皆苦と観るとき苦を厭離す"},
    279: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "諸法無我と観るとき苦を厭離し離す"},
    280: {"nidanaId": "craving", "pathFactors": ["正精進", "正念"], "reason": "起つべき時に怠惰すれば道を得ず"},
    281: {"nidanaId": "clinging", "pathFactors": ["正語", "正業"], "reason": "語・意・身の不善を掴まず三業道を浄む"},
    282: {"nidanaId": "release", "pathFactors": ["正定", "正念"], "reason": "瑜伽より智が生じ、自ら努めて智を増大す"},
    283: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "欲林を根ごと伐り、畏怖の源を断つ"},
    284: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "わずかな欲情も断たれぬ間は心が繋縛される"},
    285: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "自己への愛を断ち、寂静の道を固守する"},
    286: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "住処を思い巡らす愚は死の至るを覚らない"},
    287: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "子と家畜への執着を死が捉え去る"},
    288: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "死に捉えられた者を親族も救えない"},
    289: {"nidanaId": "review", "pathFactors": ["正精進", "正念"], "reason": "戒により制御し、涅槃への道を速やかに浄む"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP20-P01", 273), ("DP20-P02", 273),
    ("DP20-P03", 274),
    ("DP20-P04", 275),
    ("DP20-P05", 276),
    ("DP20-P06", 277),
    ("DP20-P07", 278),
    ("DP20-P08", 279),
    ("DP20-P09", 280),
    ("DP20-P10", 281), ("DP20-P11", 281),
    ("DP20-P12", 282),
    ("DP20-P13", 283),
    ("DP20-P14", 284),
    ("DP20-P15", 285),
    ("DP20-P16", 287),
    ("DP20-P17", 288),
    ("DP20-P18", 286),
    ("DP20-P19", 289), ("DP20-P20", 289),
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
    old = json.loads((DATA / "ch20.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 道の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第２０章・道品 第{verse}偈（#ch02-20）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第20章・道品（道の章）"
    SHORT = "道品（道の章）"
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
            "pathLabel": "八正道に触れ、この道のみと見定める",
            "chapterHint": SHORT,
            "fromPrev": "前夜の戒の見直しが、今朝の道への接触になる",
            "toNext": "接触のあと、無常の受が立ち上がる",
            "todayObserve": OBSERVE[273],
            "todayAction": actions["DP20-P01"],
            "when": ["朝の始まり", "道を選び直すとき"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[273][:40] + "…",
            "secondaryObserve": "唯この道あるのみ、知見を浄むるに他の道なし",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "無常の受を智慧で観て、苦を厭離する",
            "chapterHint": SHORT,
            "fromPrev": "道に触れたあと、移ろう事象の受が来る",
            "toNext": "受けた不安を、怠惰や欲林への欲しがりへ落とさない",
            "todayObserve": OBSERVE[277],
            "todayAction": actions["DP20-P06"],
            "when": ["移ろいを感じた", "執着が揺らいだ"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[277][:40] + "…",
            "secondaryObserve": "一切の事象は無常なりと観る時、苦を厭離す",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "effort", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "怠惰と欲林への欲しがりを緩め、起つ",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、怠けや欲林への欲しがりへ",
            "toNext": "止めないと三業・欲情の掴みへ進む",
            "todayObserve": OBSERVE[280],
            "todayAction": actions["DP20-P09"],
            "when": ["あとでと思った", "欲の森が広がった"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[280][:40] + "…",
            "secondaryObserve": "欲林を伐れ、樹木を伐るに止まるなかれ",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正業"], "pathFactorIds": ["speech", "action"],
            "pathLabel": "不善の三業と欲情・執着を掴まず浄む",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、不善・欲情・子財への掴みになる手前",
            "toNext": "掴むと苦が太り、死の迫りが見える",
            "todayObserve": OBSERVE[281],
            "todayAction": actions["DP20-P10"],
            "when": ["言葉を発する前", "小さな欲が残っている"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[281][:40] + "…",
            "secondaryObserve": "わずかな欲情も断たれぬ間は心が繋縛される",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "欲矢と執着の掴みが、救いなき苦になると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、欲矢・死の苦が熟す",
            "toNext": "見れば、自ら歩き無我を観る実践へ向き直る",
            "todayObserve": OBSERVE[275],
            "todayAction": actions["DP20-P04"],
            "when": ["苦境にいる", "誰かに頼ろうとした"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[275][:40] + "…",
            "secondaryObserve": "死に捉えられし者を、親族も救うあたわず",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正定"], "pathFactorIds": ["effort", "concentration"],
            "pathLabel": "自ら努力し、無我を観て、自己愛を断ち離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、歩む努力と離欲へ向き直る",
            "toNext": "離すと、戒による夜の見直しへつながる",
            "todayObserve": OBSERVE[276],
            "todayAction": actions["DP20-P05"],
            "when": ["教えを行動に落とす", "自己像を手放す"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[276][:40] + "…",
            "secondaryObserve": "自己に対する愛を断ち、寂静の道のみを固守せよ",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "effort", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "死を覚え、戒に照らして道を浄める",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、道を歩んだかの跡",
            "toNext": "見直しが、翌朝の八正道への接触になる",
            "todayObserve": OBSERVE[286] + " " + OBSERVE[289],
            "todayAction": actions["DP20-P20"],
            "when": ["一日を閉じるとき", "先延ばしを反省する"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[289][:40] + "…",
            "secondaryObserve": "賢者は戒により制御し、涅槃に至る道を速やかに浄むべし",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 20,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第20章（道品／道の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210道行品ほか）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・道の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第２０章・道品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・道行品（T4.569a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "道品は自ら歩み魔の繋縛を脱する実践が中心。既定の焦点は離す。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch20.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch20.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 21):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch20", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 20
    assert all(p["id"] == f"DP20-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(273, 290))
    assert all(p["alignment"]["chinese"]["status"] in ("mapped", "unmapped") for p in pairs)
    assert pairs[11]["alignment"]["chinese"]["status"] == "unmapped"  # P12 = 282
    assert pairs[14]["alignment"]["chinese"]["status"] == "unmapped"  # P15 = 285
    assert set(by_nidana) == valid
    print("OK")


if __name__ == "__main__":
    main()
