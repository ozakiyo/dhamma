#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn038.json (愛尽大経／渇愛の滅尽についての大経) to match MN1–37 source alignment.

実経: 漁夫の子サーティ（嗏帝）が「この識は流転し同一を保つ」と誤解。
比丘たちが諫め、世尊は識は縁により生じ縁なければ不生と説く。
四食・十二縁起の順逆、清浄なる見への執着を戒め（筏のたとえ）、愛尽へ導く。
"""
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
# 對照表: 中阿含201 嗏帝経（T1.766c）
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0766c"
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
    "MN38-P01": (
        "サーティ（嗏帝）は悪見を起こす——"
        "『この識は流転し輪廻し、常に自己の同一を保つ』と世尊が説いた、と。"
        "比丘たちはこれを聞き、正しくない理解だと知る。"
        "（今日「一つの原因だけで全てが説明できる」と思わない。）"
    ),
    "MN38-P02": (
        "世尊は種種の方便で縁生の識を説かれた——"
        "識は因縁により起り、有縁ならば生じ、無縁ならば滅する。"
        "縁を除けば識は不生である。"
        "（今日、複雑な問題を一因に還元しようとする思考を止める。）"
    ),
    "MN38-P03": (
        "いかなる縁によりても識は生ずる。"
        "眼と色を縁として識が生じれば、それを眼識と名づける。"
        "耳·鼻·舌·身·意もまた同様である。火が薪に随って名づけられるように。"
        "（心と対象が触れ合う瞬間、「触→識」を一瞬見る。）"
    ),
    "MN38-P04": (
        "食は四つある——摶食（麤細）、触食、意思食、識食。"
        "この四食は、愛を因·習·生·有とする。渇愛が根本である。"
        "（今日、意識を養う「触·意思·識」の入力を一つ減らす。）"
    ),
    "MN38-P05": (
        "愛の縁により取あり、取の縁により有あり、"
        "有の縁により生あり、生の縁により老死·愁悲苦憂悩がある。"
        "このようにして全苦蘊が集起する。"
        "（今日強く「欲しい」と感じた対象の執着を、一度緩める。）"
    ),
    "MN38-P06": (
        "識の縁により名色あり、名色の縁により識あり——"
        "心と身体と識は相互に依存して立つ。"
        "（心と身体が切り離せない一瞬を観察する。）"
    ),
    "MN38-P07": (
        "比丘たちはサーティを諫める——"
        "『世尊を誣謗するな。識は因縁により起る』と。"
        "サーティはなお固執し、世尊が面と向かって呵責し、縁起を説く。"
        "（今日、誰かの教えを聞くとき、自分の解釈を一度保留する。）"
    ),
    "MN38-P08": (
        "此有故彼有、此生故彼生——"
        "無明緣行、行緣識……愛緣取、取緣有……"
        "このようにして全苦の集まりの集起がある。一因ではない。"
        "（今日、議論で「唯一の原因」を主張する言葉を一度止める。）"
    ),
    "MN38-P09": (
        "此無故彼無、此滅故彼滅——"
        "無明滅故行滅……愛滅故取滅……"
        "このようにして全苦の集まりの滅がある。"
        "（今日、無明を一つ認め、正知に向かう一歩を踏む。）"
    ),
    "MN38-P10": (
        "もし清浄なるこの見を執着し、惜しみ、守り、捨てたくないならば——"
        "長夜に説かれた筏のたとえを理解した者ではない。"
        "取らず、自慢せず、捨てることを欲する者が、筏のたとえを知る。"
        "（「これは私の正しい見解」と感じた瞬間、執着する手を緩める。）"
    ),
}

OBSERVE = {
    "MN38-P01": (
        "サーティの誤見——識が同一体で流転する、という一因的理解。"
        "今日「一つの原因だけで全てが説明できる」と思わない。"
    ),
    "MN38-P02": (
        "識は縁起により生じ、縁を除けば不生——一因説は誤り。"
        "今日、複雑な問題を一因に還元しようとする思考を止める。"
    ),
    "MN38-P03": (
        "眼·色を縁として眼識——触→識を一瞬見る。"
        "心と対象が触れ合う瞬間、「触→識」を一瞬見る。"
    ),
    "MN38-P04": (
        "四食——摶·触·意思·識。根源は渇愛。"
        "今日、意識を養う「触・意思・識」の入力を一つ減らす。"
    ),
    "MN38-P05": (
        "愛→取→有→生→老死——渇愛が再生の縁。"
        "今日強く「欲しい」と感じた対象の執着を、一度緩める。"
    ),
    "MN38-P06": (
        "識緣名色、名色緣識——心と身体と識は相互依存。"
        "心と身体が切り離せない一瞬を観察する。"
    ),
    "MN38-P07": (
        "サーティの誤見は聞き違い——諫めと世尊の縁起説。"
        "今日、誰かの教えを聞くとき、自分の解釈を一度保留する。"
    ),
    "MN38-P08": (
        "此有故彼有——一因ではなく多縁から苦の集起。"
        "今日、議論で「唯一の原因」を主張する言葉を一度止める。"
    ),
    "MN38-P09": (
        "逆観——無明滅故行滅……全苦の集まりの滅。"
        "今日、無明を一つ認め、正知に向かう一歩を踏む。"
    ),
    "MN38-P10": (
        "清浄な見への執着は筏のたとえに非ず——取らず自慢せず。"
        "「これは私の正しい見解」と感じた瞬間、執着する手を緩める。"
    ),
}

PRACTICE = {
    "MN38-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "誤見·一因説に触れず、複雑さを一因に還元しない",
        "section": "サーティの誤見",
        "category": "view",
    },
    "MN38-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "縁生の識を見て、一因還元の欲しがりを止める",
        "section": "縁生の識",
        "category": "view",
    },
    "MN38-P03": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "触→識の瞬間を見て、縁起に気づく",
        "section": "六識の縁",
        "category": "mindfulness",
    },
    "MN38-P04": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正精進"],
        "reason": "四食の入力を一つ減らし、渇愛の養いを弱める",
        "section": "四食",
        "category": "effort",
    },
    "MN38-P05": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "強く欲しがる対象への執着を一度緩める",
        "section": "愛·取·有",
        "category": "intention",
    },
    "MN38-P06": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "心と身体が切り離せない一瞬を観察する",
        "section": "識と名色",
        "category": "mindfulness",
    },
    "MN38-P07": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正見"],
        "reason": "教えを聞くとき自分の解釈への掴みを保留する",
        "section": "諫めと呵責",
        "category": "speech",
    },
    "MN38-P08": {
        "nidanaId": "suffering",
        "pathFactors": ["正語", "正見"],
        "reason": "唯一原因を主張する言葉を止め、多縁の苦集を見る",
        "section": "此有故彼有",
        "category": "speech",
    },
    "MN38-P09": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "無明を一つ認め、正知へ向かう一歩で離す",
        "section": "逆観·滅",
        "category": "view",
    },
    "MN38-P10": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "正しい見解への執着を緩め、筏のたとえを見直す",
        "section": "筏のたとえ",
        "category": "view",
    },
}

CHINESE = {
    "MN38-P01": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-wrong-view",
        "text": "爾時，［口＊荼］帝比丘雞和哆子生如是惡見：「我知世尊如是說法：『今此識，往生不更異。』」",
        "satLocus": "大正蔵 T1.766c 嗏帝経",
        "note": "嗏帝（サーティ）の悪見——識が往生しても異ならない。",
        "satUrl": SAT_URL,
    },
    "MN38-P02": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-conditioned",
        "text": "今此識，因緣故起，世尊無量方便說識因緣故起，有緣則生，無緣則滅。",
        "satLocus": "大正蔵 T1.766c–767a 嗏帝経",
        "note": "識は因縁により起り、無縁ならば滅する。",
        "satUrl": SAT_URL,
    },
    "MN38-P03": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-six-vinnana",
        "text": "識隨所緣生，即彼緣。說緣眼色生識，生識已說眼識，如是耳、鼻、舌、身，意法生識，生識已說意識。猶若如火，隨所緣生……",
        "satLocus": "大正蔵 T1.767a–b 嗏帝経",
        "note": "眼色→眼識。火のたとえ。",
        "satUrl": SAT_URL,
    },
    "MN38-P04": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-four-food",
        "text": "此所說觀，一曰摶食麤細，二曰更樂，三曰意念，四曰識也。此四食……因愛、習愛，從愛而生，由愛有也。",
        "satLocus": "大正蔵 T1.767c 嗏帝経",
        "note": "四食——摶·更楽·意念·識。因は愛。",
        "satUrl": SAT_URL,
    },
    "MN38-P05": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-craving",
        "text": "緣覺有愛，緣愛有受，緣受有有，緣有有生，緣生有老死、愁慼、啼哭、憂苦、懊惱，如是此等大苦陰生。",
        "satLocus": "大正蔵 T1.768a 嗏帝経",
        "note": "愛→取（受）→有→生→老死。漢は「受」が取に相当する用例あり。",
        "satUrl": SAT_URL,
    },
    "MN38-P06": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-namarupa",
        "text": "緣識有名色……名色者，因識習識，從識而生，由識有也。",
        "satLocus": "大正蔵 T1.768a 嗏帝経",
        "note": "識緣名色。相互依存の名色·識。",
        "satUrl": SAT_URL,
    },
    "MN38-P07": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-rebuke",
        "text": "時，諸比丘訶［口＊荼］帝比丘曰：「汝莫作是說，莫誣謗世尊……今此識，因緣故起……汝可速捨此惡見也。」……世尊呵曰：「［口＊荼］帝！汝云何知我如是說法？……汝愚癡人！」",
        "satLocus": "大正蔵 T1.766c–767b 嗏帝経",
        "note": "比丘の諫めと世尊の呵責。",
        "satUrl": SAT_URL,
    },
    "MN38-P08": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-arising",
        "text": "是為緣無明有行，緣行有識，緣識有名色……緣覺有愛，緣愛有受……如是此等大苦陰生。",
        "satLocus": "大正蔵 T1.768a–b 嗏帝経",
        "note": "十二縁起の順観——大苦陰の集起。",
        "satUrl": SAT_URL,
    },
    "MN38-P09": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-cessation",
        "text": "生滅則老死滅……愛滅則受滅……無明滅則行滅……如是此淳大苦陰滅。",
        "satLocus": "大正蔵 T1.768b–c 嗏帝経",
        "note": "十二縁起の逆観——大苦陰の滅。",
        "satUrl": SAT_URL,
    },
    "MN38-P10": {
        "status": "mapped",
        "pin": "中阿含201・嗏帝経（T26）",
        "t26": "T26-201-raft",
        "text": "若汝等如是知、如是見，謂我此見如是清淨，著彼、惜彼、守彼，不欲令捨者，汝等知我長夜說栰喻法，知已所塞流開耶？」比丘答曰：「不也。世尊！」",
        "satLocus": "大正蔵 T1.767c 嗏帝経",
        "note": "清浄見への執着を戒め、筏（栰）のたとえ。",
        "satUrl": SAT_URL,
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c.setdefault("satUrl", SAT_URL)
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部38経の對照は中阿含201嗏帝経（T26）。サーティの誤見と縁起·四食·筏喩。",
        )
    elif c.get("status") == "unmapped":
        c.setdefault(
            "note",
            "對照表は中阿含201。このペアはパーリMN38側の実践要約。",
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
    old_path = DATA / "majjhima" / "mn038.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 11):
        pid = f"MN38-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 38",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・渇愛の滅尽についての大経／パーリMN38）",
                    "locus": f"中部・渇愛の滅尽についての大経（MN38）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 愛尽大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第38経・愛尽大経（渇愛の滅尽についての大経）"
    SHORT = "愛尽大経（渇愛の滅尽についての大経）"
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
            "pathLabel": "誤見に触れず、触→識を見る",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の縁起の見を変える",
            "toNext": "触のあと、四食·名色の受が見える",
            "todayObserve": OBSERVE["MN38-P01"],
            "todayAction": actions["MN38-P01"],
            "when": ["一因で説明しようとした", "触→識を見た"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN38-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN38-P03"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "四食の入力を減らし、名色を観察する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、食·名色の受が立つ",
            "toNext": "受に乗ると愛への欲しがりへ",
            "todayObserve": OBSERVE["MN38-P04"],
            "todayAction": actions["MN38-P04"],
            "when": ["入力を一つ減らした", "身心を観察した"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN38-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN38-P06"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "一因還元と強欲を緩め、縁生を見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、欲しがり·一因への寄りが立つ",
            "toNext": "止めないと解釈への掴みへ",
            "todayObserve": OBSERVE["MN38-P05"],
            "todayAction": actions["MN38-P05"],
            "when": ["執着を緩めた", "一因還元を止めた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN38-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN38-P02"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正見"], "pathFactorIds": ["speech", "view"],
            "pathLabel": "自分の解釈への掴みを保留する",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、解釈への掴みが手前",
            "toNext": "掴むと唯一原因の苦が見える",
            "todayObserve": OBSERVE["MN38-P07"],
            "todayAction": actions["MN38-P07"],
            "when": ["解釈を保留した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN38-P07"][:40] + "…",
            "secondaryObserve": "教えを聞くとき解釈を保留する",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "speech", "nidanaLabel": "苦が太る",
            "pathFactors": ["正語", "正見"], "pathFactorIds": ["speech", "view"],
            "pathLabel": "唯一原因の主張が生む苦を見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、一因主張の苦が見える",
            "toNext": "見れば、逆観で離す",
            "todayObserve": OBSERVE["MN38-P08"],
            "todayAction": actions["MN38-P08"],
            "when": ["唯一原因の主張を止めた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN38-P08"][:40] + "…",
            "secondaryObserve": "多縁から苦の集起を見る",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "無明を認め、正知へ向かって離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、無明を離して滅へ",
            "toNext": "離せば、夜の筏の見直しへ",
            "todayObserve": OBSERVE["MN38-P09"],
            "todayAction": actions["MN38-P09"],
            "when": ["無明を一つ認めた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN38-P09"][:40] + "…",
            "secondaryObserve": "逆観で全苦の滅へ",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "正しい見解への執着を見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの縁起の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN38-P10"],
            "todayAction": actions["MN38-P10"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN38-P10"][:40] + "…",
            "secondaryObserve": "筏のたとえ——見を取らない",
        },
    ]

    out = {
        "chapter": 38,
        "sutta": 38,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：渇愛の滅尽についての大経）",
        "suttas": ["MN 38 愛尽大経（渇愛の滅尽についての大経）"],
        "source": {
            "primary": "パーリ・中部第38経（愛尽大経／渇愛の滅尽についての大経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN38（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝中阿含201嗏帝経（T26）。"
                "サーティの誤見（識の同一流転）、縁生の識、四食、十二縁起の順逆、筏のたとえが主題。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・渇愛の滅尽についての大経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・嗏帝経（T1.766c）",
                    "url": SAT_URL,
                    "note": "對照表: 中阿含201 嗏帝経",
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
            "focusNodeId": "craving",
            "focusReason": "愛尽大経はサーティの誤見を正し、縁起·愛尽へ向かうのが主題。既定の焦点は欲しがる。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn038.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 38:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(38, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 10
    assert all(p["id"] == f"MN38-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] != "mapped"]
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/10; unmapped {unmapped}; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
