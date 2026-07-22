#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn039.json (馬邑大経／大いなる馬の町の経) to match MN1–38 source alignment.

実経: 鴦伽の町アッサプラ（馬邑）で世尊は比丘たちに説く——人は汝らを「沙門」と呼ぶ。
名に相応しく、沙門法·梵志法を学ばよ。身·口·意·命の清浄、諸根守護、正知、
独住して五蓋を断じ、四禅·漏尽へ。途中で「もう足りた」と退失するな。
真の沙門·梵志·聖·浄浴は、悪不善法·諸漏を息止·遠離·浄浴することにある。
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
# 對照表: 中阿含182 馬邑経（T1.724c）／増壹阿含49.8
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0724c"
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
    "MN39-P01": (
        "世尊は馬邑で比丘たちに告げる——"
        "『人は汝らを「沙門」と認め、汝らも「沙門」と自称する。"
        "だから沙門法·梵志法を学び、名が真実となり、出家が実りあるものとなるようにせよ』と。"
        "外形·名称だけで「足りた」と思ってはならない。"
        "（朝、自分の「修行」を苦行と浄行に分けて一度見直す。）"
    ),
    "MN39-P02": (
        "身行を清浄にせよ——仰いで発露し、善く護り、欠けなきように。"
        "この清浄をもって自らを挙げず、他を下げない。"
        "殺生·不与取·邪行を離れることが、身における正しい法である。"
        "（今日、他者の生命·所有·関係を害さないよう一つ意識する。）"
    ),
    "MN39-P03": (
        "身が清浄でも、なお上に学ぶべきことがある——"
        "口行を清浄にせよ。嘘·両舌·粗語·綺語を離れ、善く護れ。"
        "「もう足りた」と退失するな。"
        "（今日、事実でないこと·仲を裂く言葉を一度止める。）"
    ),
    "MN39-P04": (
        "身·口が清浄でも、なお上に学ぶべきことがある——"
        "意行を清浄にせよ。貪伺·瞋恚·害意を浄除し、善く護れ。"
        "他者の財を欲し「あれが私のものであれば」と思う心を離れよ。"
        "（今日、他者の所有を欲する心·害意を一度見る。）"
    ),
    "MN39-P05": (
        "身·口·意が清浄でも、なお命行（正命）を清浄にせよ。"
        "不善を離れ、善を修し、自らを挙げず他を下げない——"
        "これが沙門法·梵志法である。"
        "（今日、身語意の一つを「離すべき不善業」と結びつける。）"
    ),
    "MN39-P06": (
        "独住し、樹下·空閑に坐して、五蓋を断ぜよ——"
        "貪伺·瞋恚·睡眠·掉悔·疑。"
        "五蓋·心の穢れを断じて、離欲·離不善法から四禅に入り、漏尽へ向かう。"
        "（今日、五盖の一つを名づけ、対治を一つ選ぶ。）"
    ),
    "MN39-P07": (
        "人は汝らを「沙門」と呼ぶ。自称も「沙門」である。"
        "名に相応しい行——身口意命の清浄と上への学——があって初めて、"
        "その呼び名は真実となる。世間の呼び名と、修行者の実質は別である。"
        "（今日、自分の行いが「世間の印」か「修行者の印」か問う。）"
    ),
    "MN39-P08": (
        "身·口·意·命が清浄でも、「所作已辦、無復上作」と思ってはならない。"
        "沙門義を求めて沙門義を失うな。さらに諸根守護·正知·五蓋断·漏尽がある。"
        "道の目標は苦·漏の滅にある。"
        "（正しい道は「苦の滅」にあると一度確認する。）"
    ),
    "MN39-P09": (
        "真の沙門とは、悪不善法·諸漏を息止する者である。"
        "梵志·聖·浄浴もまた、それらを遠離·浄浴する者である——"
        "誹謗ではなく、名に相応しい法を正しく示す。"
        "（意見の異なる相手にも、正しい見方を静かに示す。）"
    ),
    "MN39-P10": (
        "諸漏は当来の有の本であり、煩熱·苦報、生·老·病·死の因である。"
        "悪不善の行は苦趣へ導く。外形の装いだけでは救われない。"
        "（苦を感じたら、身語意のどこに因があるか一つ辿る。）"
    ),
    "MN39-P11": (
        "沙門·梵志·聖·浄浴——悪不善法·諸漏を息止·遠離·浄浴すること。"
        "身·口·意を離不善·修善として一日を閉じる。"
        "（就寝前、今日の身語意を「離不善·修善」として振り返る。）"
    ),
}

OBSERVE = {
    "MN39-P01": (
        "馬邑——「沙門」の名に相応しく学べ。外形だけで足りたと思わない。"
        "朝、自分の「修行」を苦行と浄行に分けて一度見直す。"
    ),
    "MN39-P02": (
        "身行清浄——殺生·不与取·邪行を離れ、自ら挙げず他を下げない。"
        "今日、他者の生命・所有・関係を害さないよう一つ意識する。"
    ),
    "MN39-P03": (
        "口行清浄——虚妄·両舌等を離れ、なお上へ学べ。"
        "今日、事実でないこと・仲を裂く言葉を一度止める。"
    ),
    "MN39-P04": (
        "意行清浄——貪伺·害意を浄除する。"
        "今日、他者の所有を欲する心・害意を一度見る。"
    ),
    "MN39-P05": (
        "離不善·修善——身口意命の清浄が沙門法。"
        "今日、身語意の一つを「離すべき不善業」と結びつける。"
    ),
    "MN39-P06": (
        "五蓋を断じ、四禅·漏尽へ——蓋の一つを名づけ対治する。"
        "今日、五盖の一つを名づけ、対治を一つ選ぶ。"
    ),
    "MN39-P07": (
        "呼び名と実質——世間の「沙門」印か、修行者の印か。"
        "今日、自分の行いが「世間の印」か「修行者の印」か問う。"
    ),
    "MN39-P08": (
        "途中で退失するな——目標は苦·漏の滅。"
        "正しい道は「苦の滅」にあると一度確認する。"
    ),
    "MN39-P09": (
        "真の沙門·梵志——諸漏を息止·遠離する法を正しく示す。"
        "意見の異なる相手にも、正しい見方を静かに示す。"
    ),
    "MN39-P10": (
        "諸漏は苦報·生死の因——身語意に因を辿る。"
        "苦を感じたら、身語意のどこに因があるか一つ辿る。"
    ),
    "MN39-P11": (
        "結——離不善·修善として一日の身語意を振り返る。"
        "就寝前、今日の身語意を「離不善・修善」として振り返る。"
    ),
}

PRACTICE = {
    "MN39-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "朝、沙門の名と実質·浄行を見直す教えに触れる",
        "section": "沙門の名",
        "category": "view",
    },
    "MN39-P02": {
        "nidanaId": "action",
        "pathFactors": ["正業", "正念"],
        "reason": "身で他者の生命·所有·関係を害さない",
        "section": "身行清浄",
        "category": "action",
    },
    "MN39-P03": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正念"],
        "reason": "虚妄·両舌の言葉への掴みを一度止める",
        "section": "口行清浄",
        "category": "speech",
    },
    "MN39-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "他者の所有への欲しがり·害意を一度見る",
        "section": "意行清浄",
        "category": "intention",
    },
    "MN39-P05": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正業"],
        "reason": "身語意の一つを離不善として離す",
        "section": "離不善·修善",
        "category": "effort",
    },
    "MN39-P06": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "五蓋の一つを名づけ対治し、定の方向へ",
        "section": "五蓋の断",
        "category": "mindfulness",
    },
    "MN39-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正命"],
        "reason": "世間の呼び名か修行者の実質かを問う",
        "section": "名と実質",
        "category": "view",
    },
    "MN39-P08": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正精進"],
        "reason": "途中満足の苦を見て、目標は苦の滅と確認する",
        "section": "退失するな",
        "category": "view",
    },
    "MN39-P09": {
        "nidanaId": "speech",
        "pathFactors": ["正語", "正見"],
        "reason": "異なる相手にも正しい見を静かに示す",
        "section": "沙門·梵志の義",
        "category": "speech",
    },
    "MN39-P10": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦の因を身語意に一つ辿る",
        "section": "漏と苦報",
        "category": "view",
    },
    "MN39-P11": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜、身語意を離不善·修善として振り返る",
        "section": "夜の振り返り",
        "category": "mindfulness",
    },
}

# note: nidanaId "action" and "speech" are NOT valid - must use the 7 nidanas
# Fix: action -> clinging or release; speech as path factor is fine but nidanaId must be from origin nodes
# Valid: contact, feeling, craving, clinging, suffering, release, review
# I used "action" and "speech" as nidanaId by mistake - need to fix!

CHINESE = {
    "MN39-P01": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-name",
        "text": "人見汝等沙門，是沙門，人問汝等沙門，汝自稱沙門耶？……當學如沙門法及如梵志法……要是真諦沙門、不虛沙門。",
        "satLocus": "大正蔵 T1.724c 馬邑経",
        "note": "「沙門」の名に相応しく沙門法·梵志法を学べ。",
        "satUrl": SAT_URL,
    },
    "MN39-P02": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-body",
        "text": "身行清淨，仰向發露，善護無缺，因此清淨，不自舉，不下他，無穢無濁，為諸智梵行者所共稱譽。",
        "satLocus": "大正蔵 T1.724c–725a 馬邑経",
        "note": "身行清浄。自ら挙げず他を下げない。",
        "satUrl": SAT_URL,
    },
    "MN39-P03": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-speech",
        "text": "若身清淨，當復作何等？當學口行清淨，仰向發露，善護無缺。……莫令求沙門義失沙門義。",
        "satLocus": "大正蔵 T1.725a 馬邑経",
        "note": "口行清浄。なお上へ学べ。",
        "satUrl": SAT_URL,
    },
    "MN39-P04": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-mind",
        "text": "當學意行清淨……見他財物、諸生活具，不起貪伺，欲令我得，彼於貪伺淨除其心。如是瞋恚……",
        "satLocus": "大正蔵 T1.725a–b 馬邑経",
        "note": "意行清浄·貪伺·瞋恚の浄除。",
        "satUrl": SAT_URL,
    },
    "MN39-P05": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-livelihood",
        "text": "當學命行清淨，仰向發露，善護無缺。因此命行清淨，不自舉，不下他……",
        "satLocus": "大正蔵 T1.725a 馬邑経",
        "note": "命行（正命）清浄。離不善の方向。",
        "satUrl": SAT_URL,
    },
    "MN39-P06": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-nivaranas",
        "text": "斷除貪伺……如是瞋恚、睡眠、掉悔，斷疑度惑……彼斷此五蓋、心穢、慧羸，離欲、離惡不善之法，至得第四禪成就遊。",
        "satLocus": "大正蔵 T1.725b 馬邑経",
        "note": "五蓋を断じ四禅へ。",
        "satUrl": SAT_URL,
    },
    "MN39-P07": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-true-name",
        "text": "人見汝等沙門……汝自稱沙門耶？……學如沙門法及如梵志法已，要是真諦沙門、不虛沙門。",
        "satLocus": "大正蔵 T1.724c 馬邑経",
        "note": "真諦沙門·不虚沙門——名と実質。",
        "satUrl": SAT_URL,
    },
    "MN39-P08": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-more",
        "text": "若汝作是念：『我身行清淨，我所作已辦，不復更學……無復上作。』比丘！我為汝說，莫令求沙門義失沙門義。",
        "satLocus": "大正蔵 T1.725a 馬邑経",
        "note": "「もう足りた」と退失するな。",
        "satUrl": SAT_URL,
    },
    "MN39-P09": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-definition",
        "text": "云何沙門？謂息止諸惡不善之法、諸漏穢污……是謂沙門。云何梵志？謂遠離諸惡不善之法……是謂梵志。",
        "satLocus": "大正蔵 T1.725c 馬邑経",
        "note": "沙門·梵志の定義——諸漏の息止·遠離。",
        "satUrl": SAT_URL,
    },
    "MN39-P10": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-asava",
        "text": "諸漏穢污，為當來有本，煩熱苦報，生、老、病、死因……",
        "satLocus": "大正蔵 T1.725c 馬邑経",
        "note": "諸漏は当来有·苦報·生死の因。",
        "satUrl": SAT_URL,
    },
    "MN39-P11": {
        "status": "mapped",
        "pin": "中阿含182・馬邑経（T26）",
        "t26": "T26-182-close",
        "text": "是謂沙門，是謂梵志，是謂為聖，是謂淨浴。……彼諸比丘聞佛所說，歡喜奉行。",
        "satLocus": "大正蔵 T1.725c 馬邑経",
        "note": "沙門·梵志·聖·浄浴としての結。",
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
            "パーリ中部39経の對照は中阿含182馬邑経（T26）。漸次学·五蓋断·沙門義。",
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
    # Fix invalid nidanaIds from draft
    PRACTICE["MN39-P02"]["nidanaId"] = "clinging"
    PRACTICE["MN39-P09"]["nidanaId"] = "release"

    old_path = DATA / "majjhima" / "mn039.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN39-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 39",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・大いなる馬の町の経／パーリMN39）",
                    "locus": f"中部・大いなる馬の町の経（MN39）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 馬邑大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第39経・馬邑大経（大いなる馬の町の経）"
    SHORT = "馬邑大経（大いなる馬の町の経）"
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
            "pathLabel": "沙門の名と実質の教えに触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の浄行の一歩を変える",
            "toNext": "触のあと、蓋·意の受が見える",
            "todayObserve": OBSERVE["MN39-P01"],
            "todayAction": actions["MN39-P01"],
            "when": ["修行を見直した", "名と実質を問うた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN39-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN39-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "五蓋を名づけ対治する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、蓋の受が立つ",
            "toNext": "蓋に乗ると欲しがりへ",
            "todayObserve": OBSERVE["MN39-P06"],
            "todayAction": actions["MN39-P06"],
            "when": ["五蓋を名づけた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN39-P06"][:40] + "…",
            "secondaryObserve": "五蓋を断じ定へ",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "他者の所有への欲しがり·害意を見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、貪伺·害意が立つ",
            "toNext": "止めないと身語への掴みへ",
            "todayObserve": OBSERVE["MN39-P04"],
            "todayAction": actions["MN39-P04"],
            "when": ["貪伺·害意を見た"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN39-P04"][:40] + "…",
            "secondaryObserve": "意行を清浄にする",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "action", "nidanaLabel": "掴む",
            "pathFactors": ["正業", "正語"], "pathFactorIds": ["action", "speech"],
            "pathLabel": "身·語の不善への掴みを止める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、身語の掴みが手前",
            "toNext": "掴むと退失·苦報が見える",
            "todayObserve": OBSERVE["MN39-P02"],
            "todayAction": actions["MN39-P02"],
            "when": ["害さないと意識した", "虚妄を止めた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN39-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN39-P03"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "退失と漏の苦報を見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、退失·苦報が見える",
            "toNext": "見れば、離不善へ離す",
            "todayObserve": OBSERVE["MN39-P08"],
            "todayAction": actions["MN39-P08"],
            "when": ["苦の滅を確認した", "因を辿った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN39-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN39-P10"],
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "離不善·修善し、沙門義を示す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、不善を離す",
            "toNext": "離せば、夜の振り返りへ",
            "todayObserve": OBSERVE["MN39-P05"],
            "todayAction": actions["MN39-P05"],
            "when": ["不善を離した", "正しい見を示した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN39-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN39-P09"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "身語意を離不善·修善として振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの浄行の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN39-P11"],
            "todayAction": actions["MN39-P11"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN39-P11"][:40] + "…",
            "secondaryObserve": "沙門·梵志として振り返る",
        },
    ]

    out = {
        "chapter": 39,
        "sutta": 39,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：大いなる馬の町の経）",
        "suttas": ["MN 39 馬邑大経（大いなる馬の町の経）"],
        "source": {
            "primary": "パーリ・中部第39経（馬邑大経／大いなる馬の町の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN39（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝中阿含182馬邑経（T26）。"
                "「沙門」の名に相応しい漸次学——身口意命の清浄、諸根守護、五蓋断、四禅·漏尽が主題。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・大いなる馬の町の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・馬邑経（T1.724c）",
                    "url": SAT_URL,
                    "note": "對照表: 中阿含182 馬邑経（類縁EA49.8）",
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
            "focusNodeId": "release",
            "focusReason": "馬邑大経は沙門の名に相応しく、不善を離れ上へ学ぶ漸次学が主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn039.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 39:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(39, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN39-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] != "mapped"]
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; unmapped {unmapped}; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
