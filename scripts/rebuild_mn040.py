#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn040.json (馬邑小経／小なる馬の町の経) to match MN1–39 source alignment.

実経: 同じく馬邑で世尊は説く——「沙門」の名に相応しく沙門道跡を学べ。
外形（袈裟·裸形·編髪·一食等）だけでは沙門ではない。
貪伺·恚·瞋·結·慳·嫉·諛諂·無慚無愧·悪欲·邪見などの沙門垢を息しなければ非沙門。
利斧を僧伽梨に包んだような者である。垢を息し、身口意清浄·五蓋断·四無量心へ。
四方から来て浴池で垢を洗う者のように、四姓いずれも内止すれば真の沙門。
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
# 對照表: 中阿含183 馬邑経（T1.725c）
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0725c"
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
    "MN40-P01": (
        "世尊は馬邑で告げる——"
        "『人は汝らを「沙門」と認め、汝らも自称する。"
        "だから沙門道跡を学べ。真諦の沙門·不虚の沙門となれ』と。"
        "外形の装いと、不善を離れる浄行は別である。"
        "（朝、今日の修行が「身を傷つける苦行」か「不善を離れる浄行」か問う。）"
    ),
    "MN40-P02": (
        "身が清浄でなければ、沙門道跡ではない。"
        "戒を成就し身を清浄にし、殺生·不与取·邪行を離れよ。"
        "（今日、殺生·盗み·邪行のいずれかを意識的に避ける。）"
    ),
    "MN40-P03": (
        "口が清浄でなければ、沙門道跡ではない。"
        "口を清浄にし、虚妄·両舌·粗悪·綺語を離れよ。"
        "（今日、嘘·両舌·粗語·雑語の一つを止める。）"
    ),
    "MN40-P04": (
        "意が清浄でなければ、沙門道跡ではない。"
        "貪伺を息し、恚·瞋を息し、心を慈と倶ならしめよ。"
        "（今日、他者の幸せを願う思いを一つ置く。）"
    ),
    "MN40-P05": (
        "沙門垢——貪伺·恚·瞋·慳·嫉·諛諂·無慚無愧·悪欲·邪見——"
        "これらを息さなければ、袈裟をまとっても非沙門である。"
        "利斧を僧伽梨に包んだような者だ、と世尊は説く。"
        "（快楽の裏に、他者への害がないか一度見る。）"
    ),
    "MN40-P06": (
        "袈裟·裸形·編髪·一食·持水——外形の印だけでは沙門ではない。"
        "垢を息して初めて、その印は真実となる。"
        "世間の印と、修行者の実質は別である。"
        "（今日、自分の行いがどちらの印に近いか問う。）"
    ),
    "MN40-P07": (
        "垢を息し、正念正智にして、心を慈·悲·喜·捨と倶ならしめ、"
        "一方·四方·上下·一切世間に遍満して遊べ——"
        "これが内なる修習の方向である。"
        "（今日、七覚支の一つ（念·擇法·精進等）を意識する。）"
    ),
    "MN40-P08": (
        "外形の苦行·装いだけでは、沙門垢は尽きない。"
        "正見は、漏を知って尽くすことにある——"
        "苦·集·滅·道、漏·習·滅·道を如実に知る。"
        "（正しい見は「苦·集·滅·道」にあると確認する。）"
    ),
    "MN40-P09": (
        "無衣·編髪·持水などの外形を取る者にも、"
        "世尊は「外形だけでは非沙門。垢を息せば沙門」と正しく示す——"
        "誹謗ではなく、道跡を示す。"
        "（異論の相手にも、正しい行いを静かに示す。）"
    ),
    "MN40-P10": (
        "身口意が清浄でも、なお五蓋——貪伺·瞋恚·睡眠·掉挙·疑——を断ぜよ。"
        "外の苦行では心の穢れは除けない。内で浄除する。"
        "（今日、五盖の一つを名づけ、手放す。）"
    ),
    "MN40-P11": (
        "村の近くに清泉の浴池があるように——"
        "東西南北から来た者が垢を洗い渇きを除く。"
        "四姓いずれも、内行して内止を得れば、沙門·梵志·聖·浄浴である。"
        "（就寝前、今日の身語意を善業として一つ振り返る。）"
    ),
}

OBSERVE = {
    "MN40-P01": (
        "馬邑小——外形の苦行か、不善を離れる浄行か。"
        "朝、今日の修行が「身を傷つける苦行」か「不善を離れる浄行」か問う。"
    ),
    "MN40-P02": (
        "身の清浄——殺生·盗み·邪行を離れる。"
        "今日、殺生・盗み・邪行のいずれかを意識的に避ける。"
    ),
    "MN40-P03": (
        "語の清浄——虚妄·両舌·粗語·綺語を離れる。"
        "今日、嘘・両舌・粗語・雑語の一つを止める。"
    ),
    "MN40-P04": (
        "意の清浄——貪恚を息し、慈を置く。"
        "今日、他者の幸せを願う思いを一つ置く。"
    ),
    "MN40-P05": (
        "沙門垢——息さなければ袈裟も利斧の包み。"
        "快楽の裏に、他者への害がないか一度見る。"
    ),
    "MN40-P06": (
        "外形の印だけでは非沙門——世間の印か修行者の印か。"
        "今日、自分の行いがどちらの印に近いか問う。"
    ),
    "MN40-P07": (
        "四無量·正念——内なる修習の方向。"
        "今日、七覚支の一つ（念・擇法・精進等）を意識する。"
    ),
    "MN40-P08": (
        "外形苦行では正見に至らず——苦·集·滅·道を確認する。"
        "正しい見は「苦・集・滅・道」にあると確認する。"
    ),
    "MN40-P09": (
        "外形行者にも——垢を息せば沙門、と正しく示す。"
        "異論の相手にも、正しい行いを静かに示す。"
    ),
    "MN40-P10": (
        "五蓋は心の穢れ——外の苦行では除けない。"
        "今日、五盖の一つを名づけ、手放す。"
    ),
    "MN40-P11": (
        "浴池のたとえ——内止すれば沙門。身語意を善として振り返る。"
        "就寝前、今日の身語意を善業として一つ振り返る。"
    ),
}

PRACTICE = {
    "MN40-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "朝、苦行か浄行かを問う教えに触れる",
        "section": "沙門道跡",
        "category": "view",
    },
    "MN40-P02": {
        "nidanaId": "clinging",
        "pathFactors": ["正業", "正念"],
        "reason": "身の不善への掴みを意識的に避ける",
        "section": "身清浄",
        "category": "action",
    },
    "MN40-P03": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正念"],
        "reason": "不善な語への掴みを一つ止める",
        "section": "語清浄",
        "category": "speech",
    },
    "MN40-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "貪恚を息し、他者の幸せを願う",
        "section": "意清浄·慈",
        "category": "intention",
    },
    "MN40-P05": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "快楽の裏の害·沙門垢を見て苦の種を知る",
        "section": "沙門垢",
        "category": "view",
    },
    "MN40-P06": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正命"],
        "reason": "世間の印か修行者の印かを問う",
        "section": "外形と実質",
        "category": "view",
    },
    "MN40-P07": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "念·擇法等、内なる修習の一つを意識する",
        "section": "四無量·正念",
        "category": "mindfulness",
    },
    "MN40-P08": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "外形苦行を離れ、苦集滅道の正見を確認する",
        "section": "正見·四諦",
        "category": "view",
    },
    "MN40-P09": {
        "nidanaId": "speech",
        "pathFactors": ["正語", "正見"],
        "reason": "異論の相手にも正しい行いを静かに示す",
        "section": "正しく示す",
        "category": "speech",
    },
    "MN40-P10": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正精進"],
        "reason": "五蓋の一つを名づけ手放す",
        "section": "五蓋",
        "category": "mindfulness",
    },
    "MN40-P11": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜、身語意を善業として振り返る",
        "section": "浴池·結",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN40-P01": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-path",
        "text": "人見汝等沙門……汝自稱沙門耶？……當學沙門道跡，莫非沙門；學沙門道跡已，要是真諦沙門、不虛沙門。",
        "satLocus": "大正蔵 T1.725c 馬邑経",
        "note": "沙門道跡を学べ。真諦·不虚の沙門。",
        "satUrl": SAT_URL,
    },
    "MN40-P02": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-body",
        "text": "彼如是成就戒，身清淨，口、意清淨……",
        "satLocus": "大正蔵 T1.726b 馬邑経",
        "note": "戒を成就し身を清浄にする。",
        "satUrl": SAT_URL,
    },
    "MN40-P03": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-speech",
        "text": "彼如是成就戒，身清淨，口、意清淨……",
        "satLocus": "大正蔵 T1.726b 馬邑経",
        "note": "口の清浄。",
        "satUrl": SAT_URL,
    },
    "MN40-P04": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-metta",
        "text": "無有貪伺，心中無恚……彼心與慈俱，遍滿一方成就遊。……如是悲、喜心與捨俱……",
        "satLocus": "大正蔵 T1.726b 馬邑経",
        "note": "貪恚を息し、慈悲喜捨を遍満する。",
        "satUrl": SAT_URL,
    },
    "MN40-P05": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-defilements",
        "text": "若有貪伺不息貪伺，有恚不息恚……有邪見不息邪見，此沙門垢……趣至惡處未盡已，學非沙門道跡，非沙門。猶如鉞斧……僧伽梨所裹……",
        "satLocus": "大正蔵 T1.725c–726a 馬邑経",
        "note": "沙門垢と利斧·僧伽梨のたとえ。",
        "satUrl": SAT_URL,
    },
    "MN40-P06": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-outer",
        "text": "持僧伽梨，我不說是沙門。……如是無衣、編髮、不坐、一食、常揚水、持水，持水者，我說非是沙門。",
        "satLocus": "大正蔵 T1.726a–b 馬邑経",
        "note": "袈裟·裸形等の外形だけでは非沙門。",
        "satUrl": SAT_URL,
    },
    "MN40-P07": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）／類縁",
        "t26": "T26-183-brahmavihara",
        "text": "正念正智，無有愚癡，彼心與慈俱……如是悲、喜心與捨俱……遍滿一切世間成就遊。",
        "satLocus": "大正蔵 T1.726b 馬邑経（類縁）",
        "note": "正念正智·四無量。七覚支の明示はパーリ実践対応。",
        "satUrl": SAT_URL,
    },
    "MN40-P08": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-asava",
        "text": "彼如是知、如是見已，則欲漏心解脫，有漏、無明漏心解脫……生已盡，梵行已立，所作已辦……",
        "satLocus": "大正蔵 T1.726b–c 馬邑経",
        "note": "如実知見による漏尽。四諦の方向。",
        "satUrl": SAT_URL,
    },
    "MN40-P09": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-teach",
        "text": "如是無衣、編髮……持水者，我說非是沙門。若持水，有貪伺息貪伺……者……是謂沙門道跡，非不沙門。",
        "satLocus": "大正蔵 T1.726a–b 馬邑経",
        "note": "外形行者にも——垢を息せば沙門道跡。",
        "satUrl": SAT_URL,
    },
    "MN40-P10": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-nivaranas",
        "text": "無有貪伺，心中無恚，無有睡眠，無掉憍慠，斷疑度惑，正念正智……",
        "satLocus": "大正蔵 T1.726b 馬邑経",
        "note": "五蓋に相当する心穢の浄除。",
        "satUrl": SAT_URL,
    },
    "MN40-P11": {
        "status": "mapped",
        "pin": "中阿含183・馬邑経（T26）",
        "t26": "T26-183-pond",
        "text": "猶去村不遠，有好浴池……或於東方有一人來……入池快浴，去垢除熱……如是，剎利族姓子……內行止，令得內止，內止者，我說沙門……",
        "satLocus": "大正蔵 T1.726c 馬邑経",
        "note": "浴池のたとえ——四姓いずれも内止すれば沙門。",
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
            "パーリ中部40経の對照は中阿含183馬邑経（T26）。沙門垢·外形非沙門·四無量·浴池喩。",
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
    # speech is not a valid nidana — fix
    PRACTICE["MN40-P09"]["nidanaId"] = "release"

    old_path = DATA / "majjhima" / "mn040.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN40-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 40",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・小なる馬の町の経／パーリMN40）",
                    "locus": f"中部・小なる馬の町の経（MN40）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 馬邑小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第40経・馬邑小経（小なる馬の町の経）"
    SHORT = "馬邑小経（小なる馬の町の経）"
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
            "pathLabel": "沙門道跡·外形と実質に触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の浄行の一歩を変える",
            "toNext": "触のあと、蓋·慈の受が見える",
            "todayObserve": OBSERVE["MN40-P01"],
            "todayAction": actions["MN40-P01"],
            "when": ["苦行か浄行か問うた", "印を問うた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN40-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN40-P06"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "五蓋を手放し、念·四無量へ",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、蓋の受が立つ",
            "toNext": "蓋に乗ると貪恚の欲しがりへ",
            "todayObserve": OBSERVE["MN40-P10"],
            "todayAction": actions["MN40-P10"],
            "when": ["五蓋を手放した", "念を意識した"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN40-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN40-P07"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "貪恚を息し、慈を願う",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、貪伺·害意が立つ",
            "toNext": "止めないと身語への掴みへ",
            "todayObserve": OBSERVE["MN40-P04"],
            "todayAction": actions["MN40-P04"],
            "when": ["慈を一つ置いた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN40-P04"][:40] + "…",
            "secondaryObserve": "意を清浄にする",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "action", "nidanaLabel": "掴む",
            "pathFactors": ["正業", "正語"], "pathFactorIds": ["action", "speech"],
            "pathLabel": "身·語の不善への掴みを止める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、身語の掴みが手前",
            "toNext": "掴むと沙門垢の苦が見える",
            "todayObserve": OBSERVE["MN40-P02"],
            "todayAction": actions["MN40-P02"],
            "when": ["不善を避けた", "不善語を止めた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN40-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN40-P03"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "沙門垢·害の種としての苦を見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、垢の苦が見える",
            "toNext": "見れば、正見·正しく示すへ離す",
            "todayObserve": OBSERVE["MN40-P05"],
            "todayAction": actions["MN40-P05"],
            "when": ["害がないか見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN40-P05"][:40] + "…",
            "secondaryObserve": "利斧を袈裟に包むな",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正語"], "pathFactorIds": ["view", "speech"],
            "pathLabel": "外形苦行を離れ、正見を示し確認する",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、外形執着を離す",
            "toNext": "離せば、夜の浴池の振り返りへ",
            "todayObserve": OBSERVE["MN40-P08"],
            "todayAction": actions["MN40-P08"],
            "when": ["四諦を確認した", "正しく示した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN40-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN40-P09"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "身語意を善業·内止として振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの浄行の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN40-P11"],
            "todayAction": actions["MN40-P11"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN40-P11"][:40] + "…",
            "secondaryObserve": "浴池で垢を洗うように振り返る",
        },
    ]

    out = {
        "chapter": 40,
        "sutta": 40,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：小なる馬の町の経）",
        "suttas": ["MN 40 馬邑小経（小なる馬の町の経）"],
        "source": {
            "primary": "パーリ・中部第40経（馬邑小経／小なる馬の町の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN40（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝中阿含183馬邑経（T26）。"
                "外形だけでは非沙門、沙門垢の息止、四無量、浴池のたとえが主題。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・小なる馬の町の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・馬邑経（T1.725c）",
                    "url": SAT_URL,
                    "note": "對照表: 中阿含183 馬邑経",
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
            "focusReason": "馬邑小経は外形を離れ沙門垢を息して真の沙門となるのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn040.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 40:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(40, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN40-P{i:02d}" for i, p in enumerate(pairs, 1))
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
