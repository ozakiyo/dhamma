#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch6.json (賢品) to match ch1–ch5 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-06"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0564"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap06/"
)

QUOTES = {
    76: "諸々の財宝の〔隠し場所を〕伝授する者のように、〔わが身の〕罪過に見ある者（無自覚の罪過を指摘してくれる者）を、彼を見るなら、そのような賢者と、〔過誤を「過誤である」と正しく〕批判して説く思慮ある者と、親しくするがよい。そのような者と親しくしている者には、より勝ることが有り、より悪しきことは〔有りえ〕ない。",
    77: "〔他者を〕教え諭すように。〔真理を〕教え示すように。そして、不当なることから〔自己を〕防ぎ護るように。まさに、彼は、正しくある者たちにとって愛しき者と成り、正しからざる者たちにとって愛しからざる者と成る。",
    78: "悪しき朋友たちとは、親しくしないように。最低の人士たちとは、親しくしないように。善き朋友たちとは、親しくするように。最上の人士たちとは、親しくするように。",
    79: "法（真理）の喜悦ある者は、浄信した心で、安楽のうちに臥す。聖者によって知らされた法（真理）において、賢者は、常に喜び楽しむ。",
    80: "まさに、治水者たちは、水を誘導し、矢作りたちは、矢を調整し、大工たちは、木を矯正し、賢者たちは、自己を調御する。",
    81: "たとえば、一なる厚き巌（いわお）が、風に動じないように、このように、賢者たちは、諸々の非難と賞賛にたいし、〔心が〕動かない。",
    82: "たとえば、また、深い湖が、澄浄で混濁なくあるように、このように、賢者たちは、諸々の法（教え）を聞いて浄信する。",
    83: "正なる人士たちは、まさに、一切所において施捨する。正しくある者たちは、欲を欲するままに談論しない。楽しいことに触れたとして、さらに、あるいは、苦しいことに〔触れたとして〕、賢者たちは、高下を見せない。",
    84: "自己を因とせず、他者を因とせず、子を求めず、財を〔求め〕ず、国土を〔求め〕ず、法（正義）ならざることによって、自己の繁栄を求めないなら、彼は、戒ある者として、智慧ある者として、法（正義）にかなう者として、〔世に〕存するであろう。",
    85: "彼ら、人として彼岸に至る者たち──人間たちにおいて、彼らは、僅かである。そこで、この、他の人々は、まさしく、岸辺を走り回っている（迷いの世界を輪廻している）。",
    86: "しかしながら、彼ら、まさに、正しく告げ知らされた法（教え）において、法（教え）に従い転じ行く者たち──彼らは、人として、極めて超え難い死魔の領域を〔超え渡って〕、彼岸に至り行くであろう。",
    87: "賢者は、黒の法（教え）を捨棄して、白〔の法〕を修めるであろう。家から家なきに至り来て、すなわち、〔世俗の者には〕喜び難きところである、遠離〔の境地〕において──",
    88: "そこにあって、諸々の欲望〔の対象〕を捨棄して、無一物となり、〔真の〕喜びを求めるであろう。賢者は、諸々の心の汚れ（煩悩）から、自己を遍く清めるであろう。",
    89: "彼らの心が、〔七つの〕正覚の支分（七覚支）において、正しく、善く修められたなら──彼らが、〔何も〕執取せずして、執取の放棄に喜びあるなら──彼らは、煩悩（漏）が滅尽した光輝ある者たちであり、〔この〕世において、完全なる涅槃に到達した者たちとなる。",
}

OBSERVE = {
    76: "罪過を指示し呵責する智者を見ば、かかる賢者と交わること、伏蔵を告ぐる人に於けるが如くせよ。 かかる人と交わる者には善きことありて、悪しきことなし。",
    77: "訓戒すべし、教示すべし。 不当の事より〔他人を〕遠ざくべし。 かかる人は実に善人の愛するところ、悪人の憎むところとなる。",
    78: "悪友と交わるべからず、下劣の人を友とすべからず。 善友と交わるべし、最上の人を友とすべし。",
    79: "法〔水〕を飲む者は、清澄なる心を以て快適に臥す。 賢者は常に聖者の説ける法を楽しむ。",
    80: "治水者は水を導き、箭匠は箭（や）を矯め、木匠は木を矯め、賢者は自己を調御（ちょうご）す。",
    81: "固き巌の風に揺るがざるが如く、賢者は毀誉の中に於て動かず。",
    82: "深き池の静かにして澄める如く、賢者は法を聞きて心清澄なり。",
    83: "善人はあらゆるものに於て離欲し、善人は欲を求めて語らず。 楽に触るるも、また苦に触るるも、賢者は動ずる色なし。",
    84: "自己の為にも他の為にも、子と財と国土とを望むべからず。 不法によりて自己の繁栄を願うべからず。 これ戒行・智慧・正法を備うる人なり。",
    85: "人間の中、彼岸（涅槃）に到達する人は少なし。 此方（生死界）にある他の衆生は、ただ岸に沿いて走るのみ。",
    86: "法の正しく説かれたる時、〔その〕法に従う人は彼岸に至らん。 死の境域（生死界）は実に越え難し。",
    87: "賢者は黒法（悪）を捨てて、白法（善）を修すべし。 家より〔出でて〕、家なき境界に至り、孤独にして〔欲〕楽なき処に、",
    88: "〔法〕楽を求むべし。 賢者は諸欲を捨て、無一物となり、自己を心垢より浄むべし。",
    89: "菩提（ぼだい）の支分（七菩提分）に於て心を正しく修養し、執着なく、貪着を捨つるを喜び、煩悩を滅尽して輝く人は、現世に於て涅槃に入れるなり。",
}

CHINESE = {
    76: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-001",
         "text": "深觀善惡，心知畏忌，畏而不犯，終吉無憂。", "satLocus": "大正蔵 T4.564c 明哲品第1頌"},
    77: {"status": "mapped", "pin": "好喜品（T210 第24品）", "t210": "T210-24-011",
         "text": "起從聖教，禁制不善，近道見愛，離道莫親。", "satLocus": "大正蔵 T4.567b 好喜品第11頌",
         "note": "パーリ賢者の章77はT210明哲品ではなく好喜品に対応（蘇錦坤對照表）。"},
    78: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-004",
         "text": "常避無義，不親愚人，思從賢友，狎附上士。", "satLocus": "大正蔵 T4.564c 明哲品第4頌"},
    79: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-005",
         "text": "喜法臥安，心悅意清，聖人演法，慧常樂行。", "satLocus": "大正蔵 T4.564c 明哲品第5頌"},
    80: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-007",
         "text": "弓工調角，水人調船，巧匠調木，智者調身。", "satLocus": "大正蔵 T4.564c 明哲品第7頌"},
    81: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-008",
         "text": "譬如厚石，風不能移，智者意重，毀譽不傾。", "satLocus": "大正蔵 T4.564c 明哲品第8頌"},
    82: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-009",
         "text": "譬如深淵，澄靜清明，慧人聞道，心淨歡然。", "satLocus": "大正蔵 T4.564c 明哲品第9頌"},
    83: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-010",
         "text": "大人體無欲，在所昭然明，雖或遭苦樂，不高現其智。", "satLocus": "大正蔵 T4.564c 明哲品第10頌"},
    84: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-011",
         "text": "大賢無世事，不願子財國，常守戒慧道，不貪邪富貴。", "satLocus": "大正蔵 T4.565a 明哲品第11頌"},
    85: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-013",
         "text": "世皆沒淵，鮮克度岸，如或有人，欲度必奔。", "satLocus": "大正蔵 T4.565a 明哲品第13頌"},
    86: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-014",
         "text": "誠貪道者，覽受正教，此近彼岸，脫死為上。", "satLocus": "大正蔵 T4.565a 明哲品第14頌"},
    87: {"status": "mapped", "pin": "放逸品（T210 第10品）", "t210": "T210-10-020",
         "text": "斷濁黑法，學惟清白，度淵不反，棄倚行止，不復染樂，欲斷無憂。", "satLocus": "大正蔵 T4.562c 放逸品第20頌",
         "note": "パーリ賢者の章87はT210明哲品ではなく放逸品に対応（蘇錦坤對照表）。"},
    88: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-016",
         "text": "抑制情欲，絕樂無為，能自拯濟，使意為慧。", "satLocus": "大正蔵 T4.565a 明哲品第16頌"},
    89: {"status": "mapped", "pin": "明哲品（T210 第14品）", "t210": "T210-14-017",
         "text": "學取正智，意惟正道，一心受諦，不起為樂，漏盡習除，是得度世。", "satLocus": "大正蔵 T4.565a 明哲品第17頌"},
}

VERSE_PRACTICE = {
    76: {"nidanaId": "contact", "pathFactors": ["正思惟", "正念"], "reason": "罪過を示す賢者と交わるのは伏蔵を告げる人に会う如し"},
    77: {"nidanaId": "clinging", "pathFactors": ["正語", "正業"], "reason": "訓戒し不当から遠ざければ善人に愛される"},
    78: {"nidanaId": "contact", "pathFactors": ["正思惟", "正念"], "reason": "悪友を避け、善友・最上の人と交わる"},
    79: {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "法を喜び、清澄な心で安楽に臥す"},
    80: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "賢者は自己を調御する"},
    81: {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "毀誉の中でも巌の如く動かない"},
    82: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "法を聞けば、深池の如く心が澄む"},
    83: {"nidanaId": "feeling", "pathFactors": ["正念", "正思惟"], "reason": "楽にも苦にも動ずる色を見せない"},
    84: {"nidanaId": "craving", "pathFactors": ["正見", "正業"], "reason": "非法で繁栄を求めず、戒・慧・法にかなう"},
    85: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "彼岸に至る人は少なく、多くは岸辺を走る"},
    86: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "正しく説かれた法に従う者は彼岸に至る"},
    87: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "黒法を捨て白法を修め、遠離へ出る"},
    88: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "諸欲を捨て無一物となり心垢を浄める"},
    89: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "七覚支を修め執着を捨て現世で涅槃に入る"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP6-P01", 76),
    ("DP6-P02", 77),
    ("DP6-P03", 78),
    ("DP6-P04", 79),
    ("DP6-P05", 80),
    ("DP6-P06", 81), ("DP6-P07", 81),
    ("DP6-P08", 82),
    ("DP6-P09", 83), ("DP6-P10", 83),
    ("DP6-P11", 84), ("DP6-P12", 84),
    ("DP6-P13", 85),  # 85–86 combined in text
    ("DP6-P14", 86),
    ("DP6-P15", 88),  # 87–88 combined; primary 88
    ("DP6-P16", 89), ("DP6-P17", 89),
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
    old = json.loads((DATA / "ch6.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        if pid == "DP6-P13":
            observe = OBSERVE[85] + " " + OBSERVE[86]
            quote = QUOTES[85] + " " + QUOTES[86]
            pali_locus = "小部・ダンマパダ 賢者の章 第85-86偈"
            modern_locus = "第６章・賢品 第85-86偈（#ch02-06）"
            zh = chinese_block(85)
        elif pid == "DP6-P15":
            observe = OBSERVE[87] + " " + OBSERVE[88]
            quote = QUOTES[87] + " " + QUOTES[88]
            pali_locus = "小部・ダンマパダ 賢者の章 第87-88偈"
            modern_locus = "第６章・賢品 第87-88偈（#ch02-06）"
            zh = chinese_block(88)
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 賢者の章 第{verse}偈"
            modern_locus = f"第６章・賢品 第{verse}偈（#ch02-06）"
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

    TITLE = "ダンマパダ 第6章・賢品（賢者の章）"
    SHORT = "賢品（賢者の章）"
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
            "pathLabel": "誰と交わるかを、触れた場で選ぶ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見方が、今朝の接触の土台になる",
            "toNext": "善友との接触は、法を澄ませる入口になる",
            "todayObserve": OBSERVE[78],
            "todayAction": actions["DP6-P03"],
            "when": ["誘いを受けた", "新しい人と会った"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[78][:40] + "…",
            "secondaryObserve": "罪過を示す賢者との交わりは、伏蔵を告げる人に会う如し",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "毀誉・苦楽の受を、巌の如く受け流す",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、快・不快と毀誉の受が立ち上がる",
            "toNext": "動じなければ欲しがりに落ちにくい",
            "todayObserve": OBSERVE[81],
            "todayAction": actions["DP6-P06"],
            "when": ["褒められた", "批判された"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[81][:40] + "…",
            "secondaryObserve": "楽にも苦にも、動ずる色を見せない",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正業"], "pathFactorIds": ["view", "action"],
            "pathLabel": "非法で繁栄を求める欲しがりを断つ",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、子・財・成功への欲しがりへ落ちる",
            "toNext": "止めないと掴みと慢心へ進む",
            "todayObserve": OBSERVE[84],
            "todayAction": actions["DP6-P11"],
            "when": ["楽して得たい", "不正が近道に見えた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[84][:40] + "…",
            "secondaryObserve": "戒・慧・正法を備える道を選ぶ",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正業"], "pathFactorIds": ["speech", "action"],
            "pathLabel": "訓戒と自制で、不当な掴みを離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、語り・行いに乗る手前",
            "toNext": "掴むと岸辺を走り回る迷いが続く",
            "todayObserve": OBSERVE[77],
            "todayAction": actions["DP6-P02"],
            "when": ["助言したくなった", "不当な行動が見えた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[77][:40] + "…",
            "secondaryObserve": "善人に愛され、悪人に憎まれる道を歩く",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "岸辺を走る迷いと、彼岸の少なさを見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、輪廻の岸辺を走り続ける",
            "toNext": "見れば、法に従って渡る道が開く",
            "todayObserve": OBSERVE[85],
            "todayAction": actions["DP6-P13"],
            "when": ["同じ岸を回っている", "進んでいる気がしない"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[85][:40] + "…",
            "secondaryObserve": "正しく説かれた法に従う者は彼岸に至る",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "mindfulness", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "黒法を捨て、自己を調御して離す",
            "chapterHint": SHORT,
            "fromPrev": "欲と執着が流れを加速させる",
            "toNext": "七覚支を修めれば、現世の涅槃に近づく",
            "todayObserve": OBSERVE[80],
            "todayAction": actions["DP6-P05"],
            "when": ["衝動が強い", "手放したいものがある"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[80][:40] + "…",
            "secondaryObserve": "諸欲を捨て、心垢を浄め、執着を離す",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "法を聞き澄んだ心と、手放せたものを振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の語り・行いは朝からの心の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE[82],
            "todayAction": actions["DP6-P17"],
            "when": ["一日を閉じるとき", "教えに触れた日"],
            "sources": by_nidana.get("review", []) or by_nidana.get("contact", [])[:2],
            "leadQuote": QUOTES[82][:40] + "…",
            "secondaryObserve": "手放せたものを一つ確認し、解放感を味わう",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 6,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第6章（賢品／賢者の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210明哲品、一部他品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・賢者の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第６章・賢品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・明哲品（T4.564c）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "賢品は自己調御・離欲・彼岸への道が中心。既定の焦点は離す。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch6.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch6.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 7):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch6", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])
    for k, v in entries.items():
        print(k, [(e["chapterId"], e["pairCount"]) for e in v])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 17
    assert all(p["id"] == f"DP6-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(76, 90))
    print("OK")


if __name__ == "__main__":
    main()
