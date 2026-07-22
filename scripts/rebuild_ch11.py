#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch11.json (老品) to match ch1–ch10 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-11"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0566"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap11/"
)

QUOTES = {
    146: "いったい、何の笑いがあるというのだろう、何の喜びがあるというのだろう──常に燃え盛るものとして、〔世界が〕存しているときに。暗黒に覆われているのに、〔あなたたちは〕灯明を探し求めない。",
    147: "見よ──彩りあざやかに作り為された〔欲の〕幻影を──寄せ集めの、傷ある身体を──病んだ、妄想多きものを。それに、常恒と止住は、〔何であれ〕存在しない。",
    148: "老い朽ちた、この色形（色：肉体）は、病の巣となり、壊れ崩れるものとしてある。腐敗の肉身は、朽ち果てる。まさに、死という終極あるのが、生命である。",
    149: "すなわち、秋に投げ捨てられた、これらの瓜のように、まさしく、諸々の灰白色の骨があるなら、それらを見て、何の歓楽があるというのだろう。",
    150: "肉と血を塗り付け、諸々の骨で作られた城──そこにおいては、かつまた、老が、かつまた、死魔が、〔我想の〕思量（慢）が、そして、〔虚栄の〕偽装（覆）が、安置されている。",
    151: "美しく彩りあざやかな諸々の王車は、まさに、老い朽ちる。さらに、肉体もまた、老に近づく。しかしながら、正しくある者たちの法（教え）は、老に近づかない。正しくある者たちは、まさに、正しくある者たちと、〔不滅の法を、互いが互いに〕知らしめる。",
    152: "この少聞の人は、荷牛のように老い朽ちる。彼の諸々の肉は増え行くが、彼の智慧は増え行くことがない。",
    153: "無数なる生の輪廻を、〔わたしは〕流転してきた──〔何も〕得ることなく、家の作り手を探し求めながら。生〔の輪廻〕は、繰り返し、苦しみである。",
    154: "家の作り手よ、〔おまえは〕存している──〔あるがままに〕見られたものとして。ふたたび、〔おまえが〕家を作ることはないであろう。おまえの全ての梁は壊され、家の屋根は働きを為さない。心は、〔迷いの生存を〕形成する働き（行：生の輪廻を施設し造作する働き）を離れるに至り、諸々の渇愛（愛）の滅尽に到達した。",
    155: "梵行（禁欲清浄行）を歩まずして、若いときに財を得ずして、まさしく、魚の尽きた沼地にいる、老いた白鷺たちのように、〔彼らは〕痩せ衰える。",
    156: "梵行を歩まずして、若いときに財を得ずして、諸々の過去のことを泣き悲しみながら、使い古された諸々の弓のように、〔彼らは、地に〕臥す。",
}

OBSERVE = {
    146: "何の喜びぞ、何の歓びぞ、〔世は〕常に燃えつつあるを。 汝らは暗黒に覆わる。 何ぞ灯明を求めざる。",
    147: "見よ粉飾せる形骸を。 〔そは〕傷痍の積集（しゃくじゅう）にして病患絶えず、多欲にして、堅固・常住ならず。",
    148: "この形骸は衰退す、病苦の巣窟にして壊れ易し。 汚穢（おわい）の積集（しゃくじゅう）は遂に壊る。 生は必ず死に終わればなり。",
    149: "秋到りて〔捨てられし〕瓢箪（ひょうたん）の如く、委棄せられしこれらの白骨を見て、何の喜びありや。",
    150: "城郭（形骸）は骨を以て造られ、塗るに肉と血とを以てす。 その中には老と死と慢と偽と蔵（かく）せらる。",
    151: "美しく飾られたる王車も必ず朽ち、肉体もまた遂に老ゆ。 然れども善人の法は老ゆることなし。 実に善人はこれを善人と相伝う。",
    152: "寡聞の人（愚者）は雄牛の如くに老ゆ。 彼の肉は増せども、彼の智は増すことなし。",
    153: "われ屋舎を作るもの（輪廻の原因）を求めて〔これを〕見出さず、多生の流転を経たり。 生を受くること数次〔みな〕苦なり。",
    154: "屋舎を作るものよ。 汝は見出されたり。 再び屋舎を作ることなけん。 汝のすべての椽桷は毀たれ、棟梁は砕かれたり。 心は万象を離れて愛欲を滅尽し得たり。",
    155: "壮時梵行（ぼんぎょう）を修せず、財宝を獲得せざりし者は、魚なき池の老鷺の如くに死滅す。",
    156: "壮時梵行（ぼんぎょう）を修せず、財宝を獲得せざりし者は、折れたる弓の如く、過去を偲び歎きて横たわる。",
}

CHINESE = {
    146: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-001",
          "text": "何喜何笑？命常熾然，深蔽幽冥，如不求錠。", "satLocus": "大正蔵 T4.566b 老耗品第1頌"},
    147: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-002",
          "text": "見身形範，倚以為安，多想致病，豈知非真？", "satLocus": "大正蔵 T4.566b 老耗品第2頌"},
    148: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-003",
          "text": "老則色衰，病無光澤，皮緩肌縮，死命近促。", "satLocus": "大正蔵 T4.566b 老耗品第3頌",
          "note": "對照表では無常品（T210-01-014）にも対応。主対応は老耗品第3頌。"},
    149: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ老の章149はT210に対応なし（蘇錦坤對照表）。出曜経・法集要頌経側に近い文言あり。"},
    150: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-005",
          "text": "身為如城，骨幹肉塗，生至老死，但藏恚慢。", "satLocus": "大正蔵 T4.566b 老耗品第5頌"},
    151: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-006",
          "text": "老則形變，喻如故車。法能除苦，宜以力學。", "satLocus": "大正蔵 T4.566b 老耗品第6頌"},
    152: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-007",
          "text": "人之無聞，老若特牛，但長肌肥，無有福慧。", "satLocus": "大正蔵 T4.566b 老耗品第7頌"},
    153: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-008",
          "text": "生死無聊，往來艱難，意猗貪身，生苦無端。", "satLocus": "大正蔵 T4.566b 老耗品第8頌"},
    154: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-009",
          "text": "慧以見苦，是故棄身，滅意斷行，愛盡無生。", "satLocus": "大正蔵 T4.566b 老耗品第9頌"},
    155: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-010",
          "text": "不修梵行，又不富財，老如白鷺，守伺空池。", "satLocus": "大正蔵 T4.566b 老耗品第10頌"},
    156: {"status": "mapped", "pin": "老耗品（T210 第19品）", "t210": "T210-19-011",
          "text": "既不守戒，又不積財，老羸氣竭，思故何逮？", "satLocus": "大正蔵 T4.566b 老耗品第11頌"},
}

VERSE_PRACTICE = {
    146: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "常に燃える世で、暗黒の中に灯明を求める"},
    147: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "粉飾の身に執着せず、堅固・常住ならざるを見る"},
    148: {"nidanaId": "feeling", "pathFactors": ["正念", "正見"], "reason": "この身は壊れ易く、生は必ず死に終わる"},
    149: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "白骨を見て、何の喜びがあるかを問う"},
    150: {"nidanaId": "clinging", "pathFactors": ["正念", "正見"], "reason": "身の中に老・死・慢・偽が蔵されていると知る"},
    151: {"nidanaId": "release", "pathFactors": ["正見", "正精進"], "reason": "肉体は老いても、善人の法は老いない"},
    152: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "肉が増えても智が増えねば、寡聞の老い"},
    153: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "家の作り手を求め流転し、生は繰り返し苦"},
    154: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "作り手を見れば、再び家は作られない"},
    155: {"nidanaId": "review", "pathFactors": ["正精進", "正念"], "reason": "壮時に梵行を修せねば、魚なき池の老鷺の如し"},
    156: {"nidanaId": "review", "pathFactors": ["正精進", "正念"], "reason": "折れた弓のように過去を嘆く前に、今精進する"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP11-P01", 146), ("DP11-P02", 146), ("DP11-P03", 146),
    ("DP11-P04", 147), ("DP11-P05", 147),
    ("DP11-P06", 148),
    ("DP11-P07", 149),
    ("DP11-P08", 150), ("DP11-P09", 150),
    ("DP11-P10", 151), ("DP11-P11", 151), ("DP11-P12", 151),
    ("DP11-P13", 152), ("DP11-P14", 152),
    ("DP11-P15", 153), ("DP11-P16", 153),  # 153–154
    ("DP11-P17", 155), ("DP11-P18", 155), ("DP11-P19", 155),  # 155–156
]

COMBINED = {
    153: (153, 154),
    155: (155, 156),
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


def main() -> None:
    old = json.loads((DATA / "ch11.json").read_text(encoding="utf-8"))
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
            pali_locus = f"小部・ダンマパダ 老の章 第{a}-{b}偈"
            modern_locus = f"第１１章・老品 第{a}-{b}偈（#ch02-11）"
            zh = chinese_block(a)
            verse_out = a
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 老の章 第{verse}偈"
            modern_locus = f"第１１章・老品 第{verse}偈（#ch02-11）"
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

    TITLE = "ダンマパダ 第11章・老品（老の章）"
    SHORT = "老品（老の章）"
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
            "pathLabel": "燃える世に触れ、暗黒の中に灯明を求める",
            "chapterHint": SHORT,
            "fromPrev": "前夜の精進の見直しが、今朝の灯明になる",
            "toNext": "身体への接触は、欲しがりと執着へ傾きやすい",
            "todayObserve": OBSERVE[146],
            "todayAction": actions["DP11-P01"],
            "when": ["無関心でいそう", "朝の始まり"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[146][:40] + "…",
            "secondaryObserve": "肉が増えても智が増えねば、寡聞の老い",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "病苦・衰弱の受を、無常として受け取る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、老い・病の受が立ち上がる",
            "toNext": "受けた不快を、身体への欲しがりへ落とさない",
            "todayObserve": OBSERVE[148],
            "todayAction": actions["DP11-P06"],
            "when": ["身体の不調を感じた", "老いを意識した"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[148][:40] + "…",
            "secondaryObserve": "生は必ず死に終わる",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "粉飾の身への欲しがりを、白骨の観で緩める",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、外見・若さへの欲しがりへ落ちる",
            "toNext": "止めないと慢・偽の掴みへ進む",
            "todayObserve": OBSERVE[147],
            "todayAction": actions["DP11-P04"],
            "when": ["外見に執着した", "身体を飾ろうとした"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[147][:40] + "…",
            "secondaryObserve": "白骨を見て、何の喜びがあるかを問う",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "身の中の慢・偽を掴まず、正直に見る",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、慢心・虚偽として掴む手前",
            "toNext": "掴むと老死の苦が太る",
            "todayObserve": OBSERVE[150],
            "todayAction": actions["DP11-P08"],
            "when": ["自分を良く見せようとした", "慢心を感じた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[150][:40] + "…",
            "secondaryObserve": "身の中に老・死・慢・偽が蔵されている",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "老・死と輪廻の家作りが苦であると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、老いと流転の苦が熟す",
            "toNext": "見れば、朽ちない法と渇愛の滅へ向き直る",
            "todayObserve": OBSERVE[153],
            "todayAction": actions["DP11-P15"],
            "when": ["老いを実感した", "輪廻の苦しさを感じた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[153][:40] + "…",
            "secondaryObserve": "家の作り手を求め流転し、生は繰り返し苦",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "朽ちない法に依り、渇愛の家作りから離す",
            "chapterHint": SHORT,
            "fromPrev": "老死への執着が流れを加速させる",
            "toNext": "離すと、今の精進の見直しへつながる",
            "todayObserve": OBSERVE[151],
            "todayAction": actions["DP11-P10"],
            "when": ["法の実践を思い出したい", "執着を手放したい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[151][:40] + "…",
            "secondaryObserve": "作り手を見れば、再び家は作られない",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "effort", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "今の精進を見直し、老鷺・折れた弓の後悔を防ぐ",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、壮時の梵行の積み重ね",
            "toNext": "見直しが、翌朝の灯明になる",
            "todayObserve": OBSERVE[155],
            "todayAction": actions["DP11-P17"],
            "when": ["一日を閉じるとき", "精進を確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[155][:40] + "…",
            "secondaryObserve": "折れた弓のように過去を嘆く前に、今精進する",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 11,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第11章（老品／老の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210老耗品、149は対応なし）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・老の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１１章・老品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・老耗品（T4.566b）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "suffering",
            "focusReason": "老品は老・死・無常の苦の認識が中心。既定の焦点は苦が太る。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch11.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch11.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 12):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch11", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 19
    assert all(p["id"] == f"DP11-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(146, 157))
    p07 = next(p for p in pairs if p["id"] == "DP11-P07")
    assert p07["alignment"]["chinese"]["status"] == "unmapped"
    assert all(
        p["alignment"]["chinese"]["status"] in ("mapped", "unmapped") for p in pairs
    )
    print("OK")


if __name__ == "__main__":
    main()
