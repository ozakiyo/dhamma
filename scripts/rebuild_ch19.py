#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch19.json (法住品) to match ch1–ch18 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-19"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0569"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap19/"
)

QUOTES = {
    256: "すなわち、無理やり義（道理）を導くことで、それによって、法（正義）に依って立つ者と成るのではない。しかしながら、彼が、賢者として、義（道理）を、さらに、義（道理）ならざることを、両者ともに〔正しく〕判別できるなら──",
    257: "無理やりではなく、正しい法（正義）によって他者たちを導くなら、法（正義）の保護ある者であり、思慮ある者として、「法（正義）に依って立つ者」と呼ばれる。",
    258: "すなわち、多く語るだけで、それによって、賢者と成るのではない。〔心が〕平安で、怨みなく、恐れなき者が、「賢者」と呼ばれる。",
    259: "すなわち、多く語るだけで、それだけで、法（教え）を保つ者と〔成るのでは〕ない。しかしながら、彼が、たとえ、僅かでも、聞いて〔そののち〕、身体によって法（教え）を見るなら、彼が、法（教え）を怠らないなら、彼は、まさに、法（教え）を保つ者と成る。",
    260: "すなわち、彼に、白髪の頭があることで、それによって、彼が、長老（上座）と成るのではない。彼には、年齢の積み重ねがある〔だけのこと〕。〔彼は〕「無駄なる老いぼれ」と説かれる。",
    261: "彼において、かつまた、真理があり、かつまた、法（教え）があるなら、不害があり、自制があり、調御があるなら、彼は、まさに、垢（汚れ）を吐き捨てた慧者であり、「長老」と呼ばれる。",
    262: "言葉遣いのみで、あるいは、蓮華の色艶あることで、嫉妬と物惜〔の思い〕ある狡猾の者が、形姿善き人と成るのではない。",
    263: "しかしながら、彼の、この〔汚点〕が断絶され、根元から殲滅され、完破されたなら、彼は、〔心の〕汚点（憎しみや怒りなどの悪意）を吐き捨てた思慮ある者であり、「形姿善き者」と説かれる。",
    264: "掟なく、偽りを話している者が、剃髪によって、沙門（修行者）と〔成るのでは〕ない。〔悪しき〕欲求と貪欲〔の思い〕に関与している者が、どうして、沙門と成るのだろう。",
    265: "しかしながら、彼が、諸々の悪を、微細なるものも、諸々の粗大なるものも、全てにわたり静めるなら、まさに、諸々の悪が静められたことから、〔彼は〕「沙門」と呼ばれる。",
    266: "すなわち、他者たちに〔食を〕乞うだけで、それによって、彼は、比丘（行乞者）と成るのではない。腐臭の法（性質）を受持して〔世に有るなら〕、それだけでは、比丘と成らない。",
    267: "彼が、この〔世において〕、そして、善を、さらに、悪を、〔両者ともに〕拒否して、梵行ある者（禁欲清浄行の実践者）となり、〔法を〕究めて、世を歩むなら、彼は、まさに、「比丘」と説かれる。",
    268: "迷乱した形態の無知なる者が、〔ただの〕沈黙によって、牟尼（沈黙の聖者）と成るのではない。しかしながら、彼が、〔あたかも〕秤（はかり）を掴んでいるかのように、賢者としてあり、優れているものを〔正しく〕取って──",
    269: "諸々の悪を遍く避けるなら、彼は、牟尼であり、それによって、彼は、牟尼と〔成る〕。彼が、世において、〔善と悪の〕両者を〔あるがままに〕思い考えるなら、それによって、〔彼は〕「牟尼」〔と〕呼ばれる。",
    270: "すなわち、〔祭祀において〕命あるものたちを害することで、それによって、聖者と成るのではない。全ての命あるものたちを害さないことで、〔彼は〕「聖者」と呼ばれる。",
    271: "さにあらず──戒や掟のみによっても、かつまた、あるいは、多聞によっても、さらに、あるいは、禅定（定・三昧）を得ることによっても、あるいは、遠離の臥所によっても──",
    272: "「凡夫の慣れ親しむところならざる離欲の安楽を、〔わたしは〕体得する」〔と〕、比丘よ、信頼〔の思い〕を起こしては〔ならない〕──煩悩の滅尽に至り得ていないあいだは（過信は禁物である）。",
}

OBSERVE = {
    256: "躁急に事を処するの故を以て、法住者たるにあらず。 正と邪とを二つながらよく弁別し、学識あり、",
    257: "躁急ならず如法・平等に他を導き、正法を護り、賢慮ある者は、法住者と称せらる。",
    258: "多言の故を以て賢者たるにあらず。 平静にして怨憎なく、畏怖なき者は、賢者と称せらる。",
    259: "多言の故を以て持法者たるにあらず。 聞くこと少なきも身を以て法を見、法を軽んぜざる者は、実に持法者なり。",
    260: "頭髪白きの故を以て長老たるにあらず。 彼の齢は〔徒に〕熟せるのみ。 彼は空しく老いたる者と称せらる。",
    261: "真実と法と不殺生と節制と調御（ちょうご）とを持し、〔心の〕垢穢を捨棄したる賢者は、長老と称せらる。",
    262: "嫉妬・慳貪（けんどん）・虚偽ある者は、弁舌の故のみを以て、或いは容色の美の故を以て、端正の人たるにあらず。",
    263: "かかる〔悪徳を〕断ち、根元より絶滅し、罪過を捨棄し、賢慮ある者は、端正の人と称せらる。",
    264: "剃髪すといえども、戒を破り、妄語を語る者は沙門にあらず。 欲望と貪欲とを有する者、いかで沙門たるべき。",
    265: "大小すべての悪を鎮めたる者は諸悪を鎮めたるの故を以て、沙門と称せらる。",
    266: "他人に行乞（ぎょうこつ）するの故を以て、比丘たるにあらず。 一切の法を服膺（ふくよう）せる者のみ比丘なり。 〔行乞の故に〕然るにあらず。",
    267: "この世に於て善と悪とを捨て、梵行（ぼんぎょう）を修し、慎重に世を行く者は、実に比丘と称せらる。",
    268: "愚昧にして無知ならば、〔唯〕寂黙（じゃくもく）の故を以て、牟尼（むに）（寂黙者・賢人）たるを得ず。 賢者もし権衡を執るが如くに善を取り、",
    269: "悪を退くれば、彼は牟尼なり。 彼はこれによりて牟尼なり。 この世に於て、〔善悪〕二つながら知る者は、これによりて牟尼と称せらる。",
    270: "生類を害するの故を以て、聖者たるにあらず。 一切の生類を害せざるの故を以て、聖者と称せらる。",
    271: "戒律・戒行のみによりても、或いはまた多聞によりても、或いは禅定の達成によりても、或いは独臥によりても、",
    272: "我は凡夫の受け得ざる出家の楽に触るることなし。 比丘よ、煩悩の滅尽に達せざれば、決して意を安んずることなかれ。",
}

CHINESE = {
    256: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-001",
          "text": "好經道者，不競於利，有利無利，無欲不惑。", "satLocus": "大正蔵 T4.569a 奉持品第1頌"},
    257: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-002",
          "text": "常愍好學，正心以行，懽懷寶慧，是謂為道。", "satLocus": "大正蔵 T4.569a 奉持品第2頌"},
    258: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-003",
          "text": "所謂智者，不必辯言，無恐無懼，守善為智。", "satLocus": "大正蔵 T4.569a 奉持品第3頌"},
    259: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-004",
          "text": "奉持法者，不以多言，雖素少聞，身依法行，守道不忘，可謂奉法。", "satLocus": "大正蔵 T4.569a 奉持品第4頌"},
    260: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-005",
          "text": "所謂長老，不必年耆，形熟髮白，惷愚而已。", "satLocus": "大正蔵 T4.569a 奉持品第5頌"},
    261: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-006",
          "text": "謂懷諦法，順調慈仁，明達清潔，是為長老。", "satLocus": "大正蔵 T4.569a 奉持品第6頌"},
    262: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-007",
          "text": "所謂端正，非色如花，慳嫉虛飾，言行有違。", "satLocus": "大正蔵 T4.569a 奉持品第7頌"},
    263: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-008",
          "text": "謂能捨惡，根原已斷，慧而無恚，是謂端政。", "satLocus": "大正蔵 T4.569a 奉持品第8頌"},
    264: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-009",
          "text": "所謂沙門，非必除髮，妄語貪取，有欲如凡。", "satLocus": "大正蔵 T4.569a 奉持品第9頌"},
    265: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-010",
          "text": "謂能止惡，恢廓弘道，息心滅意，是為沙門。", "satLocus": "大正蔵 T4.569a 奉持品第10頌"},
    266: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-011",
          "text": "所謂比丘，非時乞食，邪行望彼，稱名而已。", "satLocus": "大正蔵 T4.569a 奉持品第11頌"},
    267: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-012",
          "text": "謂捨罪福，淨修梵行，慧能破惡，是為比丘。", "satLocus": "大正蔵 T4.569a 奉持品第12頌"},
    268: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-013",
          "text": "所謂仁明，非口不言，用心不淨，外順而已。", "satLocus": "大正蔵 T4.569a 奉持品第13頌"},
    269: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-014",
          "text": "謂心無為，內行清虛，此彼寂滅，是為仁明。", "satLocus": "大正蔵 T4.569a 奉持品第14頌"},
    270: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-015",
          "text": "所謂有道，非救一物，普濟天下，無害為道。", "satLocus": "大正蔵 T4.569a 奉持品第15頌"},
    271: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-016",
          "text": "戒眾不言，我行多誠，得定意者，要由閉損。", "satLocus": "大正蔵 T4.569a 奉持品第16頌"},
    272: {"status": "mapped", "pin": "奉持品（T210 第27品）", "t210": "T210-27-017",
          "text": "意解求安，莫習凡人，使結未盡，莫能得脫。", "satLocus": "大正蔵 T4.569a 奉持品第17頌"},
}

VERSE_PRACTICE = {
    256: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "躁急ではなく、正邪を弁別する者が法住者"},
    257: {"nidanaId": "contact", "pathFactors": ["正念", "正業"], "reason": "如法・平等に導き、正法を護る者が法住者"},
    258: {"nidanaId": "feeling", "pathFactors": ["正念", "正思惟"], "reason": "平静・怨憎なく畏怖なき者が賢者"},
    259: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "身を以て法を見、法を軽んぜざる者が持法者"},
    260: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "白髪だけでは長老にならない"},
    261: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "真実・法・不殺・節制・調御を持つ者が長老"},
    262: {"nidanaId": "suffering", "pathFactors": ["正念", "正見"], "reason": "嫉妬・慳貪・虚偽ある者は端正にあらず"},
    263: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "悪徳を断ち、罪過を捨棄した者が端正"},
    264: {"nidanaId": "clinging", "pathFactors": ["正念", "正語"], "reason": "戒を破り妄語を語れば沙門にあらず"},
    265: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "大小すべての悪を鎮めた者が沙門"},
    266: {"nidanaId": "contact", "pathFactors": ["正念", "正命"], "reason": "行乞だけでは比丘にあらず"},
    267: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "善悪を捨て梵行を修し、慎重に世を行く者が比丘"},
    268: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "唯寂黙だけでは牟尼にあらず、善を取れ"},
    269: {"nidanaId": "release", "pathFactors": ["正念", "正思惟"], "reason": "善を取り悪を退く者が牟尼"},
    270: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "一切の生類を害せざる者が聖者"},
    271: {"nidanaId": "review", "pathFactors": ["正見", "正念"], "reason": "戒律・多聞・禅定だけでは足りず、滅尽まで意を安んずるな"},
    272: {"nidanaId": "review", "pathFactors": ["正念", "正精進"], "reason": "煩悩の滅尽に達せざれば、意を安んずるな"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP19-P01", 256), ("DP19-P02", 256),  # 256–257
    ("DP19-P03", 258), ("DP19-P04", 258),
    ("DP19-P05", 259), ("DP19-P06", 259),
    ("DP19-P07", 260), ("DP19-P08", 260),  # 260–261
    ("DP19-P09", 262), ("DP19-P10", 262),  # 262–263
    ("DP19-P11", 264), ("DP19-P12", 264),  # 264–265
    ("DP19-P13", 266), ("DP19-P14", 266),  # 266–267
    ("DP19-P15", 268), ("DP19-P16", 268),  # 268–269
    ("DP19-P17", 270),
    ("DP19-P18", 271), ("DP19-P19", 271),  # 271–272
    ("DP19-P20", 264),  # 264–265 again
    ("DP19-P21", 271),  # 271–272 again
]

COMBINED = {
    256: (256, 257),
    260: (260, 261),
    262: (262, 263),
    264: (264, 265),
    266: (266, 267),
    268: (268, 269),
    271: (271, 272),
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


def chinese_for_pair(verse, parts=None):
    if parts:
        for v in parts:
            if CHINESE[v]["status"] == "mapped":
                return chinese_block(v)
    return chinese_block(verse)


def main():
    old = json.loads((DATA / "ch19.json").read_text(encoding="utf-8"))
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
            pali_locus = f"小部・ダンマパダ 法に依って立つ者の章 第{a}-{b}偈"
            modern_locus = f"第１９章・法住品 第{a}-{b}偈（#ch02-19）"
            zh = chinese_for_pair(verse, parts)
            verse_out = a
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 法に依って立つ者の章 第{verse}偈"
            modern_locus = f"第１９章・法住品 第{verse}偈（#ch02-19）"
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

    TITLE = "ダンマパダ 第19章・法住品（法に依って立つ者の章）"
    SHORT = "法住品（法に依って立つ者の章）"
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
            "pathLabel": "外形に触れず、正邪を弁別して法に依って立つ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の精進の見直しが、今朝の法住になる",
            "toNext": "接触のあと、怨憎・畏怖の受が立ち上がる",
            "todayObserve": OBSERVE[256] + " " + OBSERVE[257],
            "todayAction": actions["DP19-P01"],
            "when": ["焦って判断しそう", "朝の始まり"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[256][:40] + "…",
            "secondaryObserve": "如法・平等に導き、正法を護る者が法住者",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "怨憎・畏怖の受を平静に受け、賢者として住む",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、怨憎・畏怖の受が来る",
            "toNext": "受けた不安を、外形への欲しがりへ落とさない",
            "todayObserve": OBSERVE[258],
            "todayAction": actions["DP19-P03"],
            "when": ["恐れを感じた", "恨みと憎しみが湧いた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[258][:40] + "…",
            "secondaryObserve": "平静・怨憎なく畏怖なき者が賢者",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "唯黙・外形への欲しがりを緩め、善を取る",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、外形だけの黙・見せかけへの欲しがりへ",
            "toNext": "止めないと嫉妬・妄語の掴みへ進む",
            "todayObserve": OBSERVE[268] + " " + OBSERVE[269],
            "todayAction": actions["DP19-P15"],
            "when": ["形だけの修行に安住しそう", "善悪を選ばない"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[268][:40] + "…",
            "secondaryObserve": "善を取り悪を退く者が牟尼",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正語"], "pathFactorIds": ["mindfulness", "speech"],
            "pathLabel": "妄語・貪欲を掴まず、内実の戒を守る",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、妄語・欲求として掴む手前",
            "toNext": "掴むと外形だけの苦が太る",
            "todayObserve": OBSERVE[264] + " " + OBSERVE[265],
            "todayAction": actions["DP19-P11"],
            "when": ["外見で取り繕おうとした", "欲が修行を阻んだ"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[264][:40] + "…",
            "secondaryObserve": "戒を破り妄語を語れば沙門にあらず",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "嫉妬・虚偽の掴みが、端正ならざる苦になると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、外形の安易さの苦が熟す",
            "toNext": "見れば、身で法を見る実践へ向き直る",
            "todayObserve": OBSERVE[262] + " " + OBSERVE[263],
            "todayAction": actions["DP19-P09"],
            "when": ["嫉妬が苦になった", "虚偽が露呈した"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[262][:40] + "…",
            "secondaryObserve": "嫉妬・慳貪・虚偽ある者は端正にあらず",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "action", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "身で法を見、悪を鎮め、害さずに離す",
            "chapterHint": SHORT,
            "fromPrev": "外形への掴みが流れを加速させる",
            "toNext": "離すと、滅尽への見直しへつながる",
            "todayObserve": OBSERVE[259],
            "todayAction": actions["DP19-P05"],
            "when": ["法を実践したい", "悪を鎮めたい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[259][:40] + "…",
            "secondaryObserve": "一切の生類を害せざる者が聖者",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "effort", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "形式に満足せず、滅尽まで意を安んじず見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、外形か内実かの跡",
            "toNext": "見直しが、翌朝の法住になる",
            "todayObserve": OBSERVE[271] + " " + OBSERVE[272],
            "todayAction": actions["DP19-P19"],
            "when": ["一日を閉じるとき", "満足し過ぎた"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[272][:40] + "…",
            "secondaryObserve": "煩悩の滅尽に達せざれば、決して意を安んずることなかれ",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 19,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第19章（法住品／法に依って立つ者の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210奉持品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・法に依って立つ者の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１９章・法住品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・奉持品（T4.569a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "法住品は外形ではなく正邪の弁別で法に依って立つ接触が中心。既定の焦点は接触。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch19.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch19.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 20):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch19", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 21
    assert all(p["id"] == f"DP19-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(256, 273))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    print("OK")


if __name__ == "__main__":
    main()
