#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn017.json (林薮経／林野の辺境の経) to match MN1–16 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E4%B8%AD%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E4%B8%AD%E9%83%A8%E7%B5%8C%E5%85%B8%E6%A0%B9%E6%9C%AC%E4%BA%94%E5%8D%81%E7%B5%8C%E7%AF%87%E4%B8%8A"
)
TB_URL = "https://true-buddhism.com/sutra/palisanzo/"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0596c26"
MAP_URL = "https://dhammarain.github.io/canon/sutta/M-vs-M-dhammarain.pdf"

LABEL_TO_ID = {
    "正見": "view",
    "正思惟": "intention",
    "正語": "speech",
    "正業": "action",
    "正命": "livelihood",
    "正精進": "effort",
    "正念": "mindfulness",
    "正定": "concentration",
}

QUOTES = {
    "MN17-P01": (
        "比丘たちよ、林野の辺境の教相を、あなたたちに説示しましょう。"
        "比丘たちよ、ここに、比丘が、或るどこかの林野の辺境に近しく依拠して〔世に〕住みます。"
        "……その比丘は、かくのごとく深慮するべきです。"
    ),
    "MN17-P02": (
        "彼が、その林野の辺境に近しく依拠して〔世に〕住んでいると、"
        "まさしく、そして、現起していない気づきは現起せず、かつまた、定められていない心は定められず、"
        "かつまた、完全に滅尽していない諸々の煩悩は完全なる滅尽に至らず、"
        "さらに、至り得ていない束縛からの平安という無上なるものに至り得ません。"
        "……その比丘は……その林野の辺境から立ち去るべきであり、〔そこに〕住するべきではありません。"
    ),
    "MN17-P03": (
        "……現起していない気づきは現起せず……定められていない心は定められず……"
        "完全に滅尽していない諸々の煩悩は完全なる滅尽に至らず……。"
        "さらに……衣料や〔行乞の〕施食や臥坐具や病のための日用品たる薬の必需品は、それらは、難少なくして将来されます。"
        "……わたしは、衣料を因として、家から家なきへと出家したのではない。……"
        "……〔かくのごとく〕究明してもまた、その林野の辺境から立ち去るべきであり、〔そこに〕住するべきではありません。"
    ),
    "MN17-P04": (
        "彼が、その林野の辺境に近しく依拠して〔世に〕住んでいると、"
        "まさしく、そして、現起していない気づきは現起し、かつまた、定められていない心は定められ、"
        "かつまた、完全に滅尽していない諸々の煩悩は完全なる滅尽に至り、"
        "さらに、至り得ていない束縛からの平安という無上なるものに至り得ます。"
        "……衣料や……薬の必需品は、それらは、困難をもって将来されます。"
        "……わたしは、衣料を因として……出家したのではない。……"
        "……〔かくのごとく〕究明してもまた、その林野の辺境に住するべきであり、〔そこから〕立ち去るべきではありません。"
    ),
    "MN17-P05": (
        "比丘たちよ、その比丘は、かくのごとく深慮するべきです。"
        "『わたしは、まさに、この林野の辺境に近しく依拠して〔世に〕住む。……"
        "現起していない気づきは現起し……定められていない心は定められ……"
        "諸々の煩悩は完全なる滅尽に至り……束縛からの平安という無上なるものに至り得る』と。"
    ),
    "MN17-P06": (
        "……現起していない気づきは現起せず、かつまた、定められていない心は定められず、"
        "かつまた、完全に滅尽していない諸々の煩悩は完全なる滅尽に至らず、"
        "さらに、至り得ていない束縛からの平安という無上なるものに至り得ません。"
        "……衣料や……薬の必需品は、それらは、困難をもって将来されます。"
        "……その比丘は、あるいは、夜分であれ、あるいは、日中であれ、その林野の辺境から立ち去るべきであり、〔そこに〕住するべきではありません。"
    ),
    "MN17-P07": (
        "……現起していない気づきは現起し……定められていない心は定められ……"
        "諸々の煩悩は完全なる滅尽に至り……束縛からの平安という無上なるものに至り得ます。"
        "……衣料や……薬の必需品は、それらは、難少なくして将来されます。"
        "……その比丘は、生あるかぎりであろうが、その林野の辺境に住するべきであり、〔そこから〕立ち去るべきではありません。"
    ),
    "MN17-P08": (
        "比丘たちよ、ここに、比丘が……或るひとりの人物に近しく依拠して〔世に〕住みます。"
        "……現起していない気づきは現起せず……煩悩は完全なる滅尽に至らず……。"
        "……その比丘にとって、その人物は、あるいは、夜分であれ、あるいは、日中であれ、"
        "断りなくして、立ち去るべき者であり、付き従うべき者ではありません。"
    ),
    "MN17-P09": (
        "……現起していない気づきは現起し、かつまた、定められていない心は定められ、"
        "かつまた、完全に滅尽していない諸々の煩悩は完全なる滅尽に至り、"
        "さらに、至り得ていない束縛からの平安という無上なるものに至り得ます。"
    ),
    "MN17-P10": (
        "……衣料や〔行乞の〕施食や臥坐具や病のための日用品たる薬の必需品は、それらは、難少なくして将来されます。"
        "……わたしは、衣料を因として、家から家なきへと出家したのではない。"
        "〔行乞の〕施食を因として……臥坐具を因として……薬の必需品を因として、家から家なきへと出家したのではない。"
        "そこで……気づきは現起せず……心は定められず……煩悩は完全なる滅尽に至らず……。"
        "……〔かくのごとく〕究明してもまた、その林野の辺境から立ち去るべきであり、〔そこに〕住するべきではありません。"
    ),
    "MN17-P11": (
        "……その人物に近しく依拠して〔世に〕住んでいると……気づきは現起し……心は定められ……"
        "煩悩は完全なる滅尽に至り……束縛からの平安という無上なるものに至り得ます。"
        "……その比丘にとって、その人物は、生あるかぎりであろうが、付き従うべき者であり、"
        "たとえ、しりぞけられながらもまた、立ち去るべき者ではありません。"
    ),
}

OBSERVE = {
    "MN17-P01": (
        "林野の辺境の教相——依処を深慮し、住むか去るかを決する。"
        "朝、今日の依処（場·関係）を一度観察する。"
    ),
    "MN17-P02": (
        "気づきが現起せず、心が定まらず、煩悩が滅尽せず、軛安穏に至らなければ去る——"
        "心が動いた瞬間に「進展があるか」と一度問う。"
    ),
    "MN17-P03": (
        "四資具が得やすくても、気づき·定·漏尽が進まなければ去る——"
        "染（未滅の煩悩）を名づけ、依処への執着を離す。"
    ),
    "MN17-P04": (
        "気づき·定·漏尽·軛安穏が進むなら、資具が難しくても住む——"
        "進展する善の方向を一つ増す。"
    ),
    "MN17-P05": (
        "依処について深慮する——気づきは現起するか、心は定まるか。"
        "一人の時間に、反芻ではなく自分の進展を観る。"
    ),
    "MN17-P06": (
        "気づき不現起·心不定·漏不尽、かつ資具も難し——夜でも昼でも去るべき。"
        "今日の苦を、依処の不適合の結果として一度見る。"
    ),
    "MN17-P07": (
        "気づき·定·漏尽が進み、資具も難少なら、生あるかぎり住む——"
        "夜、今日の依処で進展があったか振り返る。"
    ),
    "MN17-P08": (
        "人物に依拠して進展がなければ、断りなく立ち去るべきで、付き従うべきではない——"
        "語る·従う前に、その依処が進展を生むか問う。"
    ),
    "MN17-P09": (
        "依処の基準——気づきの現起、心の定、煩悩の滅尽、軛安穏——"
        "一つの行為に正念·正知（気づき）を置く。"
    ),
    "MN17-P10": (
        "出家は衣食のためではない——資具が易くても修行が進まなければ去る。"
        "外の環境に関わらず、内の進展を一度観察する。"
    ),
    "MN17-P11": (
        "進展する人物には、生あるかぎり付き従い、しりぞけられても去らない——"
        "染·停滞が来たら観察し、去るか住むかを一呼吸で決する。"
    ),
}

PRACTICE = {
    "MN17-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、今日の依処（場·関係）に触れて観察する",
        "section": "辺境の教相",
        "category": "mindfulness",
    },
    "MN17-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "気づき·定の受を見て、進展なき依処を離す",
        "section": "気づき·不定",
        "category": "mindfulness",
    },
    "MN17-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正命"],
        "reason": "資具への欲しがりより漏尽の不進を優先し去る",
        "section": "資具易·漏不尽",
        "category": "livelihood",
    },
    "MN17-P04": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正定"],
        "reason": "進展する依処に住み、資具の難を手放す",
        "section": "進展·住",
        "category": "effort",
    },
    "MN17-P05": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "独で深慮し、依処での進展を観る",
        "section": "深慮",
        "category": "mindfulness",
    },
    "MN17-P06": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "不適合の依処が気づき·定·漏尽を阻む苦を見る",
        "section": "去るべき患",
        "category": "view",
    },
    "MN17-P07": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正定"],
        "reason": "夜に今日の依処での進展を振り返る",
        "section": "生あるかぎり住",
        "category": "mindfulness",
    },
    "MN17-P08": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正業"],
        "reason": "不適合な人物への付き従いの掴みを離す",
        "section": "人物·去",
        "category": "speech",
    },
    "MN17-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正知"],
        "reason": "行為の接触に気づきを現起させる",
        "section": "気づき現起",
        "category": "mindfulness",
    },
    "MN17-P10": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正命"],
        "reason": "易い資具への掴みより、内の進展を基準にする",
        "section": "出家の因·資具",
        "category": "livelihood",
    },
    "MN17-P11": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "進展する依処・人物に付き従い、停滞を手放す",
        "section": "付き従う",
        "category": "effort",
    },
}

# Fix P09 pathFactors - 正知 is not in LABEL_TO_ID. Use 正念 only or 正念+正定
PRACTICE["MN17-P09"]["pathFactors"] = ["正念", "正定"]

CHINESE = {
    "MN17-P01": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-intro",
        "text": "比丘者，依一林住……彼比丘應作是觀……。",
        "satLocus": "大正蔵 T1.596c–597a 林経",
        "note": "依林住＋應作是觀＝辺境の教相・深慮。",
    },
    "MN17-P02": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-leave-hard",
        "text": "若無正念不得正念，其心不定不得定心，若不解脫不得解脫，諸漏不盡不得漏盡……學道者所須……甚難可得。……彼比丘如是觀已，即捨此林，夜半而去。",
        "satLocus": "大正蔵 T1.597b 林経",
        "note": "正念·定·解脫·漏尽が進まず資具も難→去る。",
    },
    "MN17-P03": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-leave-easy",
        "text": "若無正念不得正念……不得涅槃；學道者所須……易不難得。……我出家學道，不為衣被故……。彼比丘如是觀已，可捨此林去。",
        "satLocus": "大正蔵 T1.597a 林経",
        "note": "資具易でも進展なし→捨去。出家は衣食のためでない。",
    },
    "MN17-P04": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-stay-hard",
        "text": "或無正念便得正念，其心不定而得定心……諸漏不盡而得漏盡……則得涅槃；……諸生活具……甚難可得。……彼比丘如是觀已，可住此林。",
        "satLocus": "大正蔵 T1.597a–b 林経",
        "note": "進展あり資具難→住。",
    },
    "MN17-P05": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-paccavekkhana",
        "text": "彼比丘應作是觀：『我依此林住，或無正念便得正念……則得涅槃……。』",
        "satLocus": "大正蔵 T1.597a–c 林経",
        "note": "應作是觀＝深慮。",
    },
    "MN17-P06": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-dukkha-leave",
        "text": "若無正念不得正念……不得涅槃；……諸生活具……甚難可得。……即捨此林，夜半而去，莫與彼別。",
        "satLocus": "大正蔵 T1.597b 林経",
        "note": "両不利→夜半而去。",
    },
    "MN17-P07": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-lifelong",
        "text": "或無正念便得正念……則得涅槃；……諸生活具……易不難得。……依此林住，乃可終身至其命盡。",
        "satLocus": "大正蔵 T1.597b–c 林経",
        "note": "両利→終身住。",
    },
    "MN17-P08": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-puggala",
        "text": "如依林住，塚間、村邑、依於人住亦復如是。",
        "satLocus": "大正蔵 T1.597c 林経",
        "note": "依於人住も同則。パーリは断りなく去る場合を詳説。",
    },
    "MN17-P09": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-sati",
        "text": "或無正念便得正念，其心不定而得定心，若不解脫便得解脫，諸漏不盡而得漏盡……則得涅槃。",
        "satLocus": "大正蔵 T1.596c–597a 林経",
        "note": "正念·定心·漏尽＝依処の基準。",
    },
    "MN17-P10": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-not-for-requisites",
        "text": "我出家學道，不為衣被故，不為飲食、床榻、湯藥故，亦不為諸生活具故。然我依此林住……不得涅槃；……易不難得。……可捨此林去。",
        "satLocus": "大正蔵 T1.597a 林経",
        "note": "出家非為衣食。",
    },
    "MN17-P11": {
        "status": "mapped",
        "pin": "中阿含107・林経（T26）",
        "t26": "T26-107-follow",
        "text": "或無正念便得正念……則得涅槃；……易不難得。……依此林住，乃可終身至其命盡，如依林住……依於人住亦復如是。",
        "satLocus": "大正蔵 T1.597c 林経",
        "note": "終身依住・依人。パーリはしりぞけられても去らないを明記。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部17経と中阿含107–108林経の内容対応（對照表: 法雨道場）。",
        )
    return c


def rebuild_path_scene_for_mn(sutta_id, short, title, pairs):
    psi_path = DATA / "path-scene-index.json"
    psi = json.loads(psi_path.read_text(encoding="utf-8"))
    PATH_ORDER = list(LABEL_TO_ID.values())
    by_path = defaultdict(list)
    for p in pairs:
        for lab in p["pathFactors"]:
            by_path[LABEL_TO_ID[lab]].append(p["id"])
        by_path[p["category"]].append(p["id"])

    for pid in PATH_ORDER:
        ids = sorted(set(by_path[pid]), key=lambda x: int(x.split("-P")[1]))
        entries = [
            e for e in psi["entries"].setdefault(pid, [])
            if not (e.get("collectionId") == "majjhima" and e.get("chapterId") == sutta_id)
        ]
        if ids:
            entries.append({
                "collectionId": "majjhima",
                "collectionName": "中部",
                "chapterId": sutta_id,
                "shortTitle": short,
                "title": title,
                "pairCount": len(ids),
                "pairIds": ids,
            })
        psi["entries"][pid] = entries

    mns = set()
    for entries in psi["entries"].values():
        for e in entries:
            if e.get("collectionId") == "majjhima":
                mns.add(e["chapterId"])
    mns.add(sutta_id)
    mn_part = "+".join(f"mn{n}" for n in sorted(mns))
    psi["scope"] = f"dhammapada-ch1-ch26+majjhima-{mn_part}"

    psi_path.write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return psi["scope"]


def main():
    old_path = DATA / "majjhima" / "mn017.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN17-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 17",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー",
                    "locus": f"中部・林野の辺境の経（MN17）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 林薮経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第17経・林薮経（林野の辺境の経）"
    SHORT = "林薮経（林野の辺境の経）"
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
            "pathLabel": "今日の依処に触れ、気づきの現起を基準に観る",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の場·関係の接触を変える",
            "toNext": "触のあと、定まらない心の受が見える",
            "todayObserve": OBSERVE["MN17-P01"],
            "todayAction": actions["MN17-P01"],
            "when": ["場に入った朝", "関係に触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN17-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN17-P09"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "気づき·定の受を見て、進展なき依処を離す",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、定まらない・定まる受が立つ",
            "toNext": "受に乗ると資具への欲しがりへ",
            "todayObserve": OBSERVE["MN17-P02"],
            "todayAction": actions["MN17-P02"],
            "when": ["心が散った", "進展を問うた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN17-P02"][:40] + "…",
            "secondaryObserve": "其心不定",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "livelihood", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正命"], "pathFactorIds": ["view", "livelihood"],
            "pathLabel": "資具への欲しがりより、漏尽の不進を優先し去る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、衣食の欲しがりが立つ",
            "toNext": "止めないと易い資具への掴みへ",
            "todayObserve": OBSERVE["MN17-P03"],
            "todayAction": actions["MN17-P03"],
            "when": ["楽な場に留まりたかった", "煩悩が残った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN17-P03"][:40] + "…",
            "secondaryObserve": "不為衣被故",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "livelihood", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正命"], "pathFactorIds": ["view", "livelihood"],
            "pathLabel": "易い資具や不適合な人物への掴みを離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、場·人への掴みが手前",
            "toNext": "掴むと不適合の苦が見える",
            "todayObserve": OBSERVE["MN17-P10"],
            "todayAction": actions["MN17-P10"],
            "when": ["環境に固執した", "付き従いを選んだ"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN17-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN17-P08"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "不適合の依処が気づき·定·漏尽を阻む苦を見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、進展なき患が見える",
            "toNext": "見れば、去る·住むの離しへ向き直る",
            "todayObserve": OBSERVE["MN17-P06"],
            "todayAction": actions["MN17-P06"],
            "when": ["場が苦しかった", "漏尽が進まなかった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN17-P06"][:40] + "…",
            "secondaryObserve": "即捨此林",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正定"], "pathFactorIds": ["effort", "concentration"],
            "pathLabel": "進展する依処に住み、停滞する依処を手放す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、住むか去るかを決する",
            "toNext": "離せば、夜の深慮へつながる",
            "todayObserve": OBSERVE["MN17-P04"],
            "todayAction": actions["MN17-P04"],
            "when": ["進展する場に留まった", "停滞を手放した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN17-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN17-P11"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "深慮し、今日の依処での進展を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の場·関係は、朝からの依住の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN17-P07"],
            "todayAction": actions["MN17-P07"],
            "when": ["一日を閉じるとき", "独で深慮した日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN17-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN17-P05"],
        },
    ]

    out = {
        "chapter": 17,
        "sutta": 17,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：林野の辺境の経）",
        "suttas": ["MN 17 林薮経（林野の辺境の経）"],
        "source": {
            "primary": "パーリ・中部第17経（林薮経／林野の辺境の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含107–108林経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・林野の辺境の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・林経（T1.596c）",
                    "url": SAT_URL,
                    "note": "依林住の去住。對照表: 法雨道場（107–108）",
                },
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
            "focusReason": "林野の辺境の経は依処（林·村·人）に触れて気づき·定·漏尽の進展を深慮し住むか去るかを決するのが主題。既定の焦点は接触。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn017.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 17:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(17, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN17-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
