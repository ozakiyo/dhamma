#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch5.json (愚品) to match ch1–ch4 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-05"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0564"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap05/"
)

QUOTES = {
    60: "〔眠れずに〕起きている者に、夜は長い。〔歩みつづけ〕疲れている者に、〔一〕ヨージャナ（由旬：長さの単位・一ヨージャナは軛牛の一日の移動距離で約７キロメートルもしくは１５キロメートルとされる）は長い。正なる法（教え）を識知せずにいる愚者たちに、輪廻〔の道〕は長い。",
    61: "〔道を〕歩んでいる者が、自己と等しくあるか、より勝っている者に、もし、到達しないなら、断固として、独り歩むこと（独行）を為すように。愚者のうちに、道友たること（真の友情）は存在しない。",
    62: "「わたしには、子たちが存在する。わたしには、財が存在する」〔と〕、かくのごとく、愚者は〔所有の思いに〕打ちのめされる。まさに、自己は、自己のものとして存在しない（思いのままにならない存在である）。どうして、子たちが、どうして、財が、〔自己のものとして存在するというのだろう〕。",
    63: "〔自己の〕愚かさを思い考える、その愚者は──彼は、それによって、まさしく、賢者でさえある。しかしながら、〔自己を〕賢者と思量する愚者は──彼は、まさに、「愚者」と説かれる。",
    64: "もし、愚者が、たとえ、生あるかぎり、賢者に奉侍するとして、彼は、法（真理）を識知しない──すなわち、匙（さじ）が、汁の味を〔識知しない〕ように。",
    65: "もし、識者が、寸時でさえも、賢者に奉侍するなら、すみやかに、法（真理）を識知する──すなわち、舌が、汁の味を〔識知する〕ように。",
    66: "愚者たちは、思慮浅き者たちであり、まさしく、自己を朋友ならざるものとして、〔世を〕歩む──〔まさに〕その、辛き果と成る、悪しき行為（悪業）を為しながら。",
    67: "それを為して悩み苦しむなら、為したその行為は、善きものではない──その〔行為〕の報い（異熟）を、泣き叫びながら、涙顔で受けるなら。",
    68: "しかしながら、それを為して悩み苦しまないなら、為したその行為は、善きものである──その〔行為〕の報いを、悦意の者となり、機嫌よく受けるなら。",
    69: "〔自己の為した〕悪しき〔行為〕が煮られない、それまでのあいだ、愚者は、〔自己の為す悪しき行為を〕蜜のように思いなす。しかしながら、〔自己の為した〕悪しき〔行為〕が煮られる、そのとき、愚者は、苦しみを受ける。",
    70: "月ごとに〔断食苦行の真似をして〕、草の先端で食を受ける愚者──彼は、法（真理）を究めた者たちの、十六分の一にも値しない。",
    71: "まさに、〔愚者が〕為した悪しき行為は、〔搾りたての〕乳のように、今日のうちには固まらない。灰に覆われた火のように、〔徐々に〕焼き尽くしながら、その愚者に従い行く。",
    72: "義（目的）ならざるもののために、愚者に知識が生まれる、まさしく、そのかぎりは、〔その知識が〕愚者の幸運を打ち砕く──彼の頭を打ち落としながら。",
    73: "〔愚者は〕求める──正しからざる者たちの敬愛を、そして、比丘たちのなかでは尊奉を、かつまた、諸々の居住のなかでは権力を、さらに、他者の家々においては諸々の供養を。",
    74: "「在家者たちと出家者たちは、両者ともに、まさしく、わたしの為したことを思い考えよ。諸々の為すべきことと為すべきではないことについては、何であれ、まさしく、わたしの支配するものとして存するのだ」〔と〕、かくのごとく、愚者の、妄想と欲求は、かつまた、〔我想の〕思量（慢：自他を比較し価値づける心・慢心）は、〔自ずと〕増え行く。",
    75: "まさに、他なるものとして、利得を機縁とするものがあり、他なるものとして、涅槃に至るものがある（両者は別個のものである）。このように、このことを証知して、覚者（ブッダ）の弟子たる比丘は、〔自己への〕尊敬に愉悦せず、遠離〔の境地〕を増進するがよい。",
}

OBSERVE = {
    60: "不眠者には夜長く、疲れたる人には一由旬（ゆじゅん）（距離の単位）も長く、正法を知らざる愚者には流転長し。",
    61: "道を歩みて自己に勝る人、自己に等しき人に逢わざれば、敢えて独り行くべし。 愚者は断じて伴侶となすべからず。",
    62: "「我に子あり、我に財あり」とて愚者は悩む。 自己すでに自分のものにあらず。 況んやいかで子をや、いかで財をや。",
    63: "愚者にして〔自ら〕その愚を知るものは、これによりて既に賢なり。 されど愚者にして〔自ら〕賢なりと思うものは、実に〔真の〕愚者と称せらる。",
    64: "たとい終生賢者に侍すとも、愚者は正法を悟らざること、あたかも食匙の香味に於けるが如し。",
    65: "たとい一瞬賢者に侍すとも、智者は直ちに正法を悟ること、あたかも舌の香味に於けるが如し。",
    66: "無知なる愚者は自己に対し仇敵の如く振る舞う、苦果をもたらす悪業を行いつつ。",
    67: "行いて後悔い、顔に涙し、哭泣してその果報をうく、かかる業は善くなされたるものにあらず。",
    68: "されど行いて後悔いず、歓喜愉悦してその果報をうく、かかる業は善くなされたるものなり。",
    69: "悪業の未だ熟せざる間、愚者はそを蜜の如く思惟す。 されど悪業の熟するや、愚者はその時に至りて苦悩す。",
    70: "愚者は〔節食して〕月に月に（数ヶ月間毎日）、クサ草の先端を以て食を取るとも、彼は正法を思量する者の十六分の一にも値せず。",
    71: "犯したる悪業は、牛乳の如く直ちに凝固せず。 灰に覆われたる火の如く、燃えつつ愚者に従う。",
    72: "思慮生じて〔かえって〕愚者の災厄となる、そは彼の頭を砕きつつ、愚者の幸福を滅ぼす。",
    73: "〔愚者をして〕虚名を欲せしめよ、比丘衆の間にありては上位を、僧院に於ては主権を、他人（在家衆）の間に於ては供養を〔欲せしめよ〕。",
    74: "「こは我により為されたりと、在家も出家も共に考うべし、彼らは為すべきこと、為すべからざること、何事に於てもわが意に従うべし」とは、愚者の思惟なり。 〔この故に〕欲心と慢心とは増長す。",
    75: "一は利得に導く〔道〕にして、一は涅槃に至る〔道〕なりと、かく仏弟子たる比丘は悟りて、尊敬を喜ぶべからず、遠離に専心すべし。",
}

# 蘇錦坤對照表（主対応のT210）
CHINESE = {
    60: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-001",
         "text": "不寐夜長，疲惓道長，愚生死長，莫知正法。", "satLocus": "大正蔵 T4.564a 愚闇品第1頌"},
    61: {"status": "mapped", "pin": "教學品（T210 第2品）", "t210": "T210-02-013",
         "text": "學無朋類，不得善友，寧獨守善，不與愚偕。", "satLocus": "大正蔵 T4.562a 教學品第13頌",
         "note": "パーリ愚者の章61はT210愚闇品ではなく教學品に対応（蘇錦坤對照表）。"},
    62: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-004",
         "text": "有子有財，愚惟汲汲，我且非我，何憂子財？", "satLocus": "大正蔵 T4.564a 愚闇品第4頌"},
    63: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-006",
         "text": "愚曚愚極，自謂我智，愚而勝智，是謂極愚。", "satLocus": "大正蔵 T4.564a 愚闇品第6頌"},
    64: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-007",
         "text": "頑闇近智，如瓢斟味，雖久狎習，猶不知法。", "satLocus": "大正蔵 T4.564a 愚闇品第7頌"},
    65: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-008",
         "text": "開達近智，如舌甞味，雖須臾習，即解道要。", "satLocus": "大正蔵 T4.564b 愚闇品第8頌"},
    66: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-009",
         "text": "愚人施行，為身招患，快心作惡，自致重殃。", "satLocus": "大正蔵 T4.564b 愚闇品第9頌"},
    67: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-010",
         "text": "行為不善，退見悔悋，致涕流面，報由宿習。", "satLocus": "大正蔵 T4.564b 愚闇品第10頌"},
    68: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-011",
         "text": "行為德善，進覩歡喜，應來受福，喜笑玩習。", "satLocus": "大正蔵 T4.564b 愚闇品第11頌"},
    69: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-012",
         "text": "過罪未熟，愚以恬惔，至其熟時，自受大罪。", "satLocus": "大正蔵 T4.564b 愚闇品第12頌"},
    70: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-015",
         "text": "愚好美食，月月滋甚，於十六分，未一思法。", "satLocus": "大正蔵 T4.564b 愚闇品第15頌"},
    71: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-013",
         "text": "惡不即時，如搆牛乳，罪在陰伺，如灰覆火。", "satLocus": "大正蔵 T4.565a 惡行品第13頌",
         "note": "パーリ愚者の章71はT210愚闇品ではなく惡行品に対応（蘇錦坤對照表）。"},
    72: {"status": "mapped", "pin": "利養品（T210 第33品）", "t210": "T210-33-002",
         "text": "如是貪無利，當知從癡生，愚為此害賢，首領分于地。", "satLocus": "大正蔵 T4.569c 利養品第2頌",
         "note": "パーリ愚者の章72はT210愚闇品ではなく利養品に対応（蘇錦坤對照表）。"},
    73: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-018",
         "text": "遠道近欲者，為食在學名，貪倚家居故，多取供異姓。", "satLocus": "大正蔵 T4.564b 愚闇品第18頌"},
    74: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-020",
         "text": "此行與愚同，但令欲慢增，利求之願異，求道意亦異。", "satLocus": "大正蔵 T4.564c 愚闇品第20頌"},
    75: {"status": "mapped", "pin": "愚闇品（T210 第13品）", "t210": "T210-13-021",
         "text": "是以有識者，出為佛弟子，棄愛捨世習，終不墮生死。", "satLocus": "大正蔵 T4.564c 愚闇品第21頌"},
}

VERSE_PRACTICE = {
    60: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "正法を知らぬ愚者には輪廻が長い"},
    61: {"nidanaId": "contact", "pathFactors": ["正思惟", "正念"], "reason": "勝る友がいなければ独り行き、愚者と交わらない"},
    62: {"nidanaId": "craving", "pathFactors": ["正見", "正念"], "reason": "子・財への執着は、自己さえ己のものでない"},
    63: {"nidanaId": "review", "pathFactors": ["正見", "正念"], "reason": "己の愚かさを知る者はすでに賢に近い"},
    64: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "愚は賢に侍しても法を知らず、匙が味を知らぬ如し"},
    65: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "智は瞬時の侍従でも法を知り、舌が味を知る如し"},
    66: {"nidanaId": "clinging", "pathFactors": ["正業", "正見"], "reason": "愚は己を敵のように扱い、悪業で苦果を招く"},
    67: {"nidanaId": "review", "pathFactors": ["正業", "正念"], "reason": "為して悔やむ業は善ではない"},
    68: {"nidanaId": "review", "pathFactors": ["正業", "正念"], "reason": "為して悔やまぬ業は善である"},
    69: {"nidanaId": "craving", "pathFactors": ["正見", "正念"], "reason": "熟さぬ間は蜜に見え、熟すれば苦となる"},
    70: {"nidanaId": "review", "pathFactors": ["正見", "正精進"], "reason": "形だけの苦行は、法を究めた者の十六分の一にも値しない"},
    71: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "悪業はすぐ固まらず、灰の下の火のように従う"},
    72: {"nidanaId": "clinging", "pathFactors": ["正見", "正思惟"], "reason": "誤った知識は愚者の頭を砕き幸福を滅ぼす"},
    73: {"nidanaId": "craving", "pathFactors": ["正思惟", "正念"], "reason": "虚名・上位・権力・供養を求める"},
    74: {"nidanaId": "clinging", "pathFactors": ["正思惟", "正念"], "reason": "すべてを己の支配下に置く慢心が増す"},
    75: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "利得の道と涅槃の道は別、尊敬を喜ばず遠離へ"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP5-P01", 60), ("DP5-P02", 60),
    ("DP5-P03", 61), ("DP5-P04", 61),
    ("DP5-P05", 62), ("DP5-P06", 62),
    ("DP5-P07", 63), ("DP5-P08", 63),
    ("DP5-P09", 64),
    ("DP5-P10", 65),
    ("DP5-P11", 66),
    ("DP5-P12", 67),
    ("DP5-P13", 68),
    ("DP5-P14", 69),
    ("DP5-P15", 70),
    ("DP5-P16", 71),
    ("DP5-P17", 72),
    ("DP5-P18", 74),  # 73–74 combined in text; primary 74
    ("DP5-P19", 75),
]


def chinese_block(verse: int) -> dict:
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    c.setdefault(
        "note",
        "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
    )
    return c


def main() -> None:
    old = json.loads((DATA / "ch5.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        if pid == "DP5-P18":
            observe = OBSERVE[73] + " " + OBSERVE[74]
            quote = QUOTES[73] + " " + QUOTES[74]
            pali_locus = "小部・ダンマパダ 愚者の章 第73-74偈"
            modern_locus = "第５章・愚品 第73-74偈（#ch02-05）"
            zh = chinese_block(74)
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 愚者の章 第{verse}偈"
            modern_locus = f"第５章・愚品 第{verse}偈（#ch02-05）"
            zh = chinese_block(verse)

        pairs.append({
            "id": pid,
            "category": LABEL_TO_ID[factors[0]],
            "verse": verse,
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

    TITLE = "ダンマパダ 第5章・愚品（愚者の章）"
    SHORT = "愚品（愚者の章）"
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
            "id": "contact", "weekday": 1, "categoryId": "intention", "nidanaLabel": "接触",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "誰と歩むかを、触れた場で選ぶ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見方が、今朝の接触の土台になる",
            "toNext": "愚と交わる接触は、長い輪廻を伸ばす",
            "todayObserve": OBSERVE[61],
            "todayAction": actions["DP5-P03"],
            "when": ["誘いを受けた", "誰かと歩き始めた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[61][:40] + "…",
            "secondaryObserve": "舌が味を知るように、瞬時でも法を味わう",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念"], "pathFactorIds": ["mindfulness"],
            "pathLabel": "蜜のように甘い感じを疑う",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、快の受が立ち上がる",
            "toNext": "甘さに止まると欲しがりへ進む",
            "todayObserve": OBSERVE[69],
            "todayAction": actions["DP5-P14"],
            "when": ["甘く見えた", "つい続けたくなった"],
            "sources": by_nidana.get("feeling", []) or by_nidana.get("craving", [])[:2],
            "leadQuote": QUOTES[69][:40] + "…",
            "secondaryObserve": "熟せぬ間は蜜に見え、熟すれば苦となる",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "子・財・名声への欲しがりを手放す",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、所有と承認へ落ちる",
            "toNext": "止めないと慢心の掴みへ進む",
            "todayObserve": OBSERVE[62],
            "todayAction": actions["DP5-P05"],
            "when": ["持っていないと不安", "認めてほしい"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[62][:40] + "…",
            "secondaryObserve": "虚名と供養を求める心が、慢を増す",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "「すべて私の意のままに」を離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、支配と慢心に乗る手前",
            "toNext": "掴むと災厄の知識さえ頭を砕く",
            "todayObserve": OBSERVE[74],
            "todayAction": actions["DP5-P18"],
            "when": ["支配したくなった", "自分が正しいと固まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[74][:40] + "…",
            "secondaryObserve": "誤った知識は、愚者の幸福を滅ぼす",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "正法を知らぬ流転の長さを見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、輪廻と業果が重くなる",
            "toNext": "見ないままだと灰の下の火が続く",
            "todayObserve": OBSERVE[60],
            "todayAction": actions["DP5-P01"],
            "when": ["疲れが長い", "同じ悩みが続く"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[60][:40] + "…",
            "secondaryObserve": "悪業はすぐ固まらず、後から焼き尽くす",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "利得の道と涅槃の道を見分けて離す",
            "chapterHint": SHORT,
            "fromPrev": "尊敬と利得への執着が流れを加速させる",
            "toNext": "遠離を増進すれば、生死の堕から離れる",
            "todayObserve": OBSERVE[75],
            "todayAction": actions["DP5-P19"],
            "when": ["評価を求めた", "一人の時間を避けた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[75][:40] + "…",
            "secondaryObserve": "尊敬を喜ばず、遠離に専心する",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "己の愚かさと業の報いを振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の語り・行いは朝からの心の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE[63],
            "todayAction": actions["DP5-P07"],
            "when": ["一日を閉じるとき", "後悔が残った日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[63][:40] + "…",
            "secondaryObserve": "為して悔やまぬ行いを、一つ確認して眠る",
        },
    ]

    # action nidana pairs feed effort-adjacent node; keep action as separate nidana for pairs
    # Map "action" nidana (66) into clinging/suffering sources? Better rename 66 to craving or action→ use valid nidana
    # Fix: verse 66 uses nidanaId "action" which is NOT a valid origin node!
    # Already need to fix VERSE_PRACTICE 66 and 70

    out = {
        "title": TITLE,
        "chapter": 5,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第5章（愚品／愚者の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210愚闇品、一部他品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・愚者の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第５章・愚品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・愚闇品（T4.564a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "愚品は所有・名声・蜜のような悪への欲しがりが中心。既定の焦点は欲しがる。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch5.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch5.json", len(pairs))

    # Rebuild path-scene-index ch1–ch5
    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 6):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch5", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])
    for k, v in entries.items():
        print(k, [(e["chapterId"], e["pairCount"]) for e in v])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 19
    assert all(p["id"] == f"DP5-P{i:02d}" for i, p in enumerate(pairs, 1))
    print("OK")


if __name__ == "__main__":
    main()
