#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch14.json (仏陀品) to match ch1–ch13 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-14"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0567"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap14/"
)

QUOTES = {
    179: "彼の勝利は、失われることがない。彼の勝利に、世において、誰であれ、行き着くことはない。彼を、覚者（ブッダ）を、終極なき境涯の者を、〔特定の〕境処なき者を、どのような境処をもってして、〔あなたたちは〕導くというのだろう。",
    180: "彼に、執着の網が〔存在せず〕、どこにであれ、誘い導くための渇愛が存在しないなら、彼を、覚者を、終極なき境涯の者を、〔特定の〕境処なき者を、どのような境処をもってして、〔あなたたちは〕導くというのだろう。",
    181: "彼ら、瞑想（禅・静慮：禅定の境地）を追求する慧者たち、離欲と寂止に喜びある者たち──彼らを、正覚者たちを、気づき（念）ある者たちを、天〔の神々〕たちもまた羨む。",
    182: "むずかしきは、人間〔の生〕の獲得あること。むずかしきは、死すべき者たちに生命あること。むずかしきは、正なる法（教え）の聴聞あること。むずかしきは、覚者たちの生起あること。",
    183: "一切の悪を為さないこと、善を成就すること、自らの心を遍く清めること──これは、覚者たちの教えである。",
    184: "「忍耐と忍受は、最高の苦行である。涅槃は、最高〔の安楽〕である」〔と〕、覚者たちは説く。他者を害する者は、まさに、出家者にあらず。他者を悩ましている者が、沙門と成ることはない。",
    185: "〔他者を〕批判しないこと、害さないこと、そして、戒条（波羅提木叉：戒律条項）において統御すること、かつまた、食について量を知ること、かつまた、辺境に臥坐すること、さらに、卓越の心（瞑想）に専念すること──これは、覚者たちの教えである。",
    186: "諸々の欲望〔の対象〕にたいし、貨幣の雨をもってしても、満足〔の思い〕は見出されない。「諸々の欲望〔の対象〕は、悦楽少なく、苦しみである」〔と〕、かくのごとく識知して、賢者は──",
    187: "彼は、天の諸々の欲望〔の対象〕にたいしてさえも、喜びには到達しない。渇愛の滅尽に喜びある者が、正等覚者（ブッダ）の弟子と成る。",
    188: "恐怖に怯えた人間たちは、まさに、帰依所として、多くのものに行き着く──諸々の山に、さらに、諸々の林に、諸々の林園や樹木や塔廟に。",
    189: "まさに、この帰依所は、平安にあらず。この帰依所は、最上にあらず。この帰依所を頼りにしても、一切の苦しみからは解放されない。",
    190: "しかしながら、彼が、帰依所として、そして、覚者（仏：ブッダ）のもとに、かつまた、法（法：ダンマ）のもとに、さらに、僧団（僧：サンガ）のもとに、赴いたなら、〔彼は〕四つの聖なる真理（四聖諦）を、正しい智慧によって見る。",
    191: "苦しみを、苦しみの生起を、そして、苦しみの超越を、さらに、苦しみの寂止に至る、聖なる八つの支分ある道（八正道・八聖道）を、〔これらの四つの聖なる真理を見る〕。",
    192: "まさに、この帰依所は、平安である。この帰依所は、最上である。この帰依所を頼りにして、一切の苦しみから解放される。",
    193: "得難きは、善き生まれの人士である。彼は、一切所において生まれず、そこにおいて、その慧者が生まれるなら、その家は、安楽に満ち栄える。",
    194: "安楽なるは、覚者たちの生起あること。安楽なるは、正なる法（教え）の説示あること。安楽なるは、僧団の和合あること。和合者たちの苦行は、安楽である。",
    195: "覚者たちを、もしくは、弟子たちであろうが、供養に値する者たちを供養しているなら──戯論（分別妄想）を超え行き、憂いと嘆きを超え渡った者たちを〔供養しているなら〕──",
    196: "涅槃に到達し、何も恐れない、そのような者たちである、彼らを供養しているなら──この功徳〔の量〕を、これなるものと計測するのは、たとえ、何をもってしても、できないであろう（その功徳の量は計り知れない）。",
}

OBSERVE = {
    179: "その勝利は決して凌駕せられず、その勝利にはこの世に於て何人も及ぶあたわざる、かの〔智見〕無辺にして〔流転の〕道跡なき仏陀を、いかなる道によりて導き来らんとするや。",
    180: "羅網を具して纏綿（てんめん）たる愛欲すら、そを何処にも導き得ざる、かの〔智見〕無辺にして〔流転の〕道跡なき仏陀を、いかなる道によりて導き来らんとするや。",
    181: "禅定に専念し、賢明にして出家の寂静を喜び、正覚を得て憶念に富む賢者は、諸天すらこれを羨む。",
    182: "人と生まるるは難く、人間の生存は難し。 妙法を聞くことは難く、諸仏の出世は難し。",
    183: "一切の悪をなさず、善を行い、自己の心を浄む。 これ諸仏の教えなり。",
    184: "忍辱（にんにく）・忍受は最上の苦行にして、涅槃は最勝なりと諸仏は説く。 実に他を害する出家なく、他を悩ます沙門なし。",
    185: "謗らず害（そこな）わず、戒律を厳守し、食するに量を知り、孤独に坐臥し、高尚なる思慮に専念す。 これ諸仏の教えなり。",
    186: "金貨の雨によりても欲心の満足あることなし。 欲は甘味少なく苦なりと知りて賢者は、",
    187: "天上の欲楽に於ても喜悦せず。 正等覚者の弟子は愛欲を滅尽するを喜ぶ。",
    188: "恐怖に駆られて人は、山岳に、森林に、園苑に、聖樹に、種々なる依所を求む。",
    189: "然れどもこは安全なる依所にあらず。 最上の依所にあらず。 かかる依所に赴くとも、一切の苦より脱することなし。",
    190: "仏と法と僧とに帰依する者は、正智によりて四種の聖諦を見る。",
    191: "苦と、苦の因と、苦の滅と、苦の滅尽に至る八支の聖道、〔すなわちこれなり〕。",
    192: "こは安全なる依所なり。 最上の依所なり。 かかる依所に赴きて、一切の苦より脱す。",
    193: "聖者は得難し。 彼は随所に生まるるものにあらず。 かかる賢者の生まるる所、その氏族は繁栄す。",
    194: "諸仏の現わるるは快く、正法を説くは快し。 僧衆の和合するは快く、和合せる人々の修行は快し。",
    195: "まさに供養を受くべき、虚妄を逸脱し憂患を超越せる仏陀、或いは仏弟子を供養する者、",
    196: "この如き寂静にして畏怖なき人を供養する者の、その大功徳は、何人によりても計量せられ難し。",
}

CHINESE = {
    179: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-001",
          "text": "己勝不受惡，一切勝世間，叡智廓無疆，開蒙令入道。", "satLocus": "大正蔵 T4.567b 述佛品第1頌"},
    180: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-002",
          "text": "決網無罣礙，愛盡無所積，佛意深無極，未踐迹令踐。", "satLocus": "大正蔵 T4.567b 述佛品第2頌"},
    181: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-003",
          "text": "勇健立一心，出家日夜滅，根斷無欲意，學正念清明。", "satLocus": "大正蔵 T4.567b 述佛品第3頌"},
    182: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-005",
          "text": "得生人道難，生壽亦難得，世間有佛難，佛法難得聞。", "satLocus": "大正蔵 T4.567b 述佛品第5頌"},
    183: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-011",
          "text": "諸惡莫作，諸善奉行，自淨其意，是諸佛教。", "satLocus": "大正蔵 T4.567b 述佛品第11頌"},
    184: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-009",
          "text": "觀行忍第一，佛說泥洹最，捨罪作沙門，無嬈害於彼。", "satLocus": "大正蔵 T4.567b 述佛品第9頌"},
    185: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-010",
          "text": "不嬈亦不惱，如戒一切持，少食捨身貪，有行幽隱處，意諦以有黠，是能奉佛教。", "satLocus": "大正蔵 T4.567b 述佛品第10頌"},
    186: {"status": "mapped", "pin": "利養品（T210 第33品）", "t210": "T210-33-003",
          "text": "天雨七寶，欲猶無厭，樂少苦多，覺者為賢。", "satLocus": "大正蔵 T4.569c 利養品第3頌",
          "note": "パーリ覚者の章186はT210述佛品ではなく利養品に対応（蘇錦坤對照表）。"},
    187: {"status": "mapped", "pin": "利養品（T210 第33品）", "t210": "T210-33-004",
          "text": "雖有天欲，慧捨無貪，樂離恩愛，為佛弟子。", "satLocus": "大正蔵 T4.569c 利養品第4頌",
          "note": "パーリ覚者の章187はT210述佛品ではなく利養品に対応（蘇錦坤對照表）。"},
    188: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-014",
          "text": "或多自歸，山川樹神，廟立圖像，祭祀求福。", "satLocus": "大正蔵 T4.567b 述佛品第14頌"},
    189: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-015",
          "text": "自歸如是，非吉非上，彼不能來，度我眾苦。", "satLocus": "大正蔵 T4.567b 述佛品第15頌"},
    190: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-016",
          "text": "如有自歸，佛法聖眾，道德四諦，必見正慧。", "satLocus": "大正蔵 T4.567b 述佛品第16頌"},
    191: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-017",
          "text": "生死極苦，從諦得度，度世八道，斯除眾苦。", "satLocus": "大正蔵 T4.567b 述佛品第17頌"},
    192: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-018",
          "text": "自歸三尊，最吉最上，唯獨有是，度一切苦。", "satLocus": "大正蔵 T4.567c 述佛品第18頌"},
    193: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-020",
          "text": "明人難值，亦不比有，其所生處，族親蒙慶。", "satLocus": "大正蔵 T4.567c 述佛品第20頌"},
    194: {"status": "mapped", "pin": "述佛品（T210 第22品）", "t210": "T210-22-021",
          "text": "諸佛興快，說經道快，眾聚和快，和則常安。", "satLocus": "大正蔵 T4.567c 述佛品第21頌"},
    195: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ覚者の章195はT210に対応なし（蘇錦坤對照表）。"},
    196: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ覚者の章196はT210に対応なし（蘇錦坤對照表）。"},
}

VERSE_PRACTICE = {
    179: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "覚者の勝利は失われず、誰も導けない"},
    180: {"nidanaId": "clinging", "pathFactors": ["正念", "正見"], "reason": "渇愛の網すら覚者を導けない"},
    181: {"nidanaId": "release", "pathFactors": ["正定", "正念"], "reason": "禅定と寂静を喜ぶ覚者を、天も羨む"},
    182: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "人の生・法の聴聞・覚者の生起は難し"},
    183: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "悪をなさず、善を行い、心を浄める"},
    184: {"nidanaId": "feeling", "pathFactors": ["正念", "正業"], "reason": "忍辱は最上、他を害する者は出家にあらず"},
    185: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "謗らず害わず、戒・少食・独坐・禅定"},
    186: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "欲は甘味少なく苦、満足はない"},
    187: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "天上の欲楽にも喜悦せず、渇愛を滅す"},
    188: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "恐怖で外の依所を求めても、苦から解放されない"},
    189: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "外の依所では一切の苦から解放されない"},
    190: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "三宝に帰依し、四聖諦を見る"},
    191: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "苦・集・滅・道を正智で見る"},
    192: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "三宝の帰依は最上の依所"},
    193: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "聖者は得難く、生まれる所は安楽に栄える"},
    194: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "仏出世・正法・僧和合・修行は安楽"},
    195: {"nidanaId": "review", "pathFactors": ["正念", "正業"], "reason": "虚妄を超えた者への供養"},
    196: {"nidanaId": "review", "pathFactors": ["正念", "正業"], "reason": "その功徳は計り知れない"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP14-P01", 179), ("DP14-P02", 179),
    ("DP14-P03", 180),
    ("DP14-P04", 181), ("DP14-P05", 181),
    ("DP14-P06", 182), ("DP14-P07", 182),
    ("DP14-P08", 183), ("DP14-P09", 183),
    ("DP14-P10", 184), ("DP14-P11", 184),
    ("DP14-P12", 185), ("DP14-P13", 185), ("DP14-P14", 185),
    ("DP14-P15", 186),
    ("DP14-P16", 187),
    ("DP14-P17", 188),  # 188–189
    ("DP14-P18", 190), ("DP14-P19", 190),  # 190–192
    ("DP14-P20", 193),
    ("DP14-P21", 194), ("DP14-P22", 194),
    ("DP14-P23", 195), ("DP14-P24", 195),  # 195–196
]

COMBINED = {
    188: (188, 189),
    190: (190, 191, 192),
    195: (195, 196),
}


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


def main():
    old = json.loads((DATA / "ch14.json").read_text(encoding="utf-8"))
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
            pali_locus = f"小部・ダンマパダ 覚者の章 第{a}-{b}偈"
            modern_locus = f"第１４章・仏陀品 第{a}-{b}偈（#ch02-14）"
            zh = chinese_for_pair(verse, parts)
            verse_out = a
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 覚者の章 第{verse}偈"
            modern_locus = f"第１４章・仏陀品 第{verse}偈（#ch02-14）"
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

    TITLE = "ダンマパダ 第14章・仏陀品（覚者の章）"
    SHORT = "仏陀品（覚者の章）"
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
            "pathLabel": "稀有な人の生と法に触れ、覚者の境地を仰ぐ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の感謝が、今朝の稀有な機会への気づきになる",
            "toNext": "教えへの接触のあと、忍辱の受が試される",
            "todayObserve": OBSERVE[182],
            "todayAction": actions["DP14-P06"],
            "when": ["朝の始まり", "教えに触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[182][:40] + "…",
            "secondaryObserve": "覚者の勝利は失われず、誰も導けない",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "不快の受を忍辱として受け、他を害さない",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、理不尽・不快の受が来る",
            "toNext": "受けた痛みを、欲への欲しがりへ落とさない",
            "todayObserve": OBSERVE[184],
            "todayAction": actions["DP14-P10"],
            "when": ["理不尽を感じた", "耐え難いと感じた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[184][:40] + "…",
            "secondaryObserve": "忍辱は最上、他を害する者は出家にあらず",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "欲は甘味少なく苦と知り、渇愛を緩める",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、満たされない欲への欲しがりへ",
            "toNext": "止めないと外の依所への掴みへ進む",
            "todayObserve": OBSERVE[186],
            "todayAction": actions["DP14-P15"],
            "when": ["もっと欲しいと感じた", "快楽に引かれた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[186][:40] + "…",
            "secondaryObserve": "渇愛の網すら覚者を導けない",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "渇愛の網を掴まず、覚者の境地を仰ぐ",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、纏綿たる愛欲の網として掴む手前",
            "toNext": "掴むと外の依所へ逃げ、苦が太る",
            "todayObserve": OBSERVE[180],
            "todayAction": actions["DP14-P03"],
            "when": ["欲に導かれそう", "網にかかったと感じた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[180][:40] + "…",
            "secondaryObserve": "渇愛の網すら覚者を導けない",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "外の依所では苦から脱せず、四聖諦へ立ち返る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、依所なき苦が熟す",
            "toNext": "見れば、三宝と諸仏の教えへ向き直る",
            "todayObserve": OBSERVE[188] + " " + OBSERVE[189],
            "todayAction": actions["DP14-P17"],
            "when": ["安心を外に求め過ぎた", "苦から逃れられない"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[188][:40] + "…",
            "secondaryObserve": "かかる依所に赴くとも、一切の苦より脱することなし",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "action", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "諸仏の教えどおりに行い、三宝に帰依して離す",
            "chapterHint": SHORT,
            "fromPrev": "外への執着が流れを加速させる",
            "toNext": "離すと、供養と和合の見直しへつながる",
            "todayObserve": OBSERVE[183],
            "todayAction": actions["DP14-P08"],
            "when": ["教えどおりに生きたい", "三宝に立ち返りたい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[183][:40] + "…",
            "secondaryObserve": "三宝に帰依し、四聖諦を見る",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "仏法僧の安楽と供養の功徳を見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、和合と敬意の跡",
            "toNext": "見直しが、翌朝の稀有な機会への気づきになる",
            "todayObserve": OBSERVE[194],
            "todayAction": actions["DP14-P21"],
            "when": ["一日を閉じるとき", "教えへの感謝を確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[194][:40] + "…",
            "secondaryObserve": "虚妄を超えた者への供養の功徳は計り知れない",
        },
    ]

    # suffering node: no dedicated verse; use clinging pairs as bridge (already set)
    # Better: assign a concentration node that uses 181 - we have concentration nidana
    # Add concentration into feeling secondary or leave as is. Check if UI needs all nidanas in pairs.
    # We have concentration on 181 but no practicePath node for concentration - that's fine like other chapters.

    out = {
        "title": TITLE,
        "chapter": 14,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第14章（仏陀品／覚者の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210述佛品、一部利養品・未対応あり）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・覚者の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１４章・仏陀品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・述佛品（T4.567b）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "仏陀品は諸仏の教えと三宝帰依による離しが中心。既定の焦点は離す。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch14.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch14.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 15):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch14", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid_nidana = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid_nidana]
    assert not bad, bad
    assert len(pairs) == 24
    assert all(p["id"] == f"DP14-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(179, 197))
    p23 = next(p for p in pairs if p["id"] == "DP14-P23")
    assert p23["alignment"]["chinese"]["status"] == "unmapped"
    print("OK")


if __name__ == "__main__":
    main()
