#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn037.json (愛尽小経／渇愛の滅尽についての小経) to match MN1–36 source alignment.

実経: 帝釈が愛尽·解脱を略説で問う。世尊は「一切法は執著するに値せず」と聞き、
一切法を了知·遍知したうえで、楽·苦·不苦不楽の受を無常·離貪·滅·捨と観じ、
世間の何ものも執取せず、戦慄せず自ら涅槃を証する、と答える。
目連は帝釈が理解したかを試し、三十三天で宮殿を揺らし、教えの復唱を促す。
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
# 對照表: 雑阿含505 愛盡 · 増壹阿含19.3 斷愛（中阿含非収録）
SAT_SA505 = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0133b24"
SAT_EA193 = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0125_%2C02%2C0593c13"
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
    "MN37-P01": (
        "帝釈は問う——『略して言えば、比丘はいかにして愛尽·解脱し、"
        "究竟の安穏·梵行の究竟·人天最上となるか』と。"
        "世尊は答える——『比丘は聞く——一切法は執著するに値しない、と。"
        "かく聞いて一切法を了知し、遍知する』と。"
        "（朝、今日「執著するに値せず／非我·非我所」を一つ意識する。）"
    ),
    "MN37-P02": (
        "楽·苦·不苦不楽——いかなる受についても、"
        "無常と観じ、離貪と観じ、滅と観じ、捨と観じて住む。"
        "かく観じて、世間の何ものも執取しない。"
        "（今日、感じた受を「非我·非我所」と一度見る。）"
    ),
    "MN37-P03": (
        "執取すれば戦慄し、愛が続く。"
        "執取しなければ戦慄せず、自ら涅槃を証する——"
        "『生は尽きた。梵行は完成した。なすべきはなされた』と。"
        "（今日、執着を「私・私のもの」と見た瞬間を一つ手放す。）"
    ),
    "MN37-P04": (
        "受を「我が受」と取れば、掴みが立ち、苦が増す。"
        "受を無常·離貪·滅·捨と観じれば、執取せず、苦の滅に向かう。"
        "（苦い受を「非私の受」と見て、取らない。）"
    ),
    "MN37-P05": (
        "正見の比丘は、一切法を了知·遍知し、"
        "一切の受を無常·非執取として見る。"
        "（今日、一つの受を「非我·非我所」と見る練習をする。）"
    ),
    "MN37-P06": (
        "かく一切の受を執著するに値せずと見れば、愛尽·解脱に至る。"
        "（就寝前、今日「私・私のもの」と見た瞬間を一つ認め、「非我」と手放す。）"
    ),
    "MN37-P07": (
        "帝釈が略説を請い、世尊は簡潔に答える——"
        "一切法は執著するに値せず。受を無常·離貪·滅·捨と観じ、執取しなければ愛尽なり、と。"
        "（今日、法を誰かに伝える機会があれば、簡潔に「非我」を伝える。）"
    ),
    "MN37-P08": (
        "略説の核は短い——"
        "『一切法は執著するに値せず』と聞き、了知し、受を観じて執取しない。"
        "（今日、冗長に語らず、「非我」の要点を語る。）"
    ),
    "MN37-P09": (
        "世尊は帝釈に、愛尽·解脱の略説を示した——"
        "執著せず、受を観じ、戦慄なく涅槃を証する道である。"
        "（今日、愛尽小経の教え（非我·愛尽）を思い出す。）"
    ),
    "MN37-P10": (
        "楽受もまた、無常·離貪·滅·捨と観ずべきである。"
        "楽に執着すれば愛が生じ、苦が続く。"
        "（快い受を「非我·非我所」と見て、執着しない。）"
    ),
    "MN37-P11": (
        "触れて感じ、感じたところに欲しがりが立つ——"
        "触→受→愛。"
        "受を執著するに値せずと見れば、愛の鎖が断たれ、苦の滅に至る。"
        "（執着が来たら「触→受→愛」の流れを見て、「非我」と手放す。）"
    ),
}

OBSERVE = {
    "MN37-P01": (
        "愛尽小——一切法は執著するに値せず。朝、非我·非我所を一つ意識する。"
        "朝、今日「非我・非我所」を一つ意識する。"
    ),
    "MN37-P02": (
        "一切の受——無常·離貪·滅·捨と観じ、非我·非我所と見る。"
        "今日、感じた受を「非我・非我所」と一度見る。"
    ),
    "MN37-P03": (
        "執取すれば愛·戦慄。手放せば愛尽·解脱。"
        "今日、執着を「私・私のもの」と見た瞬間を一つ手放す。"
    ),
    "MN37-P04": (
        "受を「私の受」と取れば苦が増す——取らない。"
        "苦い受を「非私の受」と見て、取らない。"
    ),
    "MN37-P05": (
        "正見——一切法を了知し、受を非執取·非我と見る。"
        "今日、一つの受を「非我・非我所」と見る練習をする。"
    ),
    "MN37-P06": (
        "夜、愛尽を反芻——今日どこで「私・私のもの」と見たか。"
        "就寝前、今日「私・私のもの」と見た瞬間を一つ認め、「非我」と手放す。"
    ),
    "MN37-P07": (
        "帝釈の問——簡潔な略説で愛尽·解脱を示す。"
        "今日、法を誰かに伝える機会があれば、簡潔に「非我」を伝える。"
    ),
    "MN37-P08": (
        "簡潔な教え——「執著するに値せず／非我」の要点。"
        "今日、冗長に語らず、「非我」の要点を語る。"
    ),
    "MN37-P09": (
        "愛尽小経——受を観じ、執取せず愛尽へ。"
        "今日、愛尽小経の教え（非我・愛尽）を思い出す。"
    ),
    "MN37-P10": (
        "楽受も非執取——執着すれば愛が生じる。"
        "快い受を「非我・非我所」と見て、執着しない。"
    ),
    "MN37-P11": (
        "触→受→愛——受を非執取と見れば愛の鎖が断たれる。"
        "執着が来たら「触→受→愛」の流れを見て、「非我」と手放す。"
    ),
}

PRACTICE = {
    "MN37-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "朝、愛尽·非執取の教えに触れて一つ意識する",
        "section": "愛尽の略説",
        "category": "view",
    },
    "MN37-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "受を無常·非我として観じ、執取しない",
        "section": "受の観察",
        "category": "mindfulness",
    },
    "MN37-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "「私·私のもの」という欲しがりを一度手放す",
        "section": "執取と愛",
        "category": "intention",
    },
    "MN37-P04": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "受を我がものと取った苦を見て取らない",
        "section": "受の取着と苦",
        "category": "view",
    },
    "MN37-P05": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "正見で一つの受を非我·非我所と見る",
        "section": "正見の受観",
        "category": "view",
    },
    "MN37-P06": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "夜、「私·私のもの」と見た瞬間を認め手放す",
        "section": "夜の愛尽",
        "category": "mindfulness",
    },
    "MN37-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正見"],
        "reason": "帝釈への略説のように、簡潔に非我を伝える",
        "section": "帝釈の問",
        "category": "speech",
    },
    "MN37-P08": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正見"],
        "reason": "冗長を離れ、執著せずの要点だけを語る",
        "section": "簡潔な教え",
        "category": "speech",
    },
    "MN37-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "愛尽小経の教えに触れ、非我·愛尽を思い出す",
        "section": "教えの導",
        "category": "view",
    },
    "MN37-P10": {
        "nidanaId": "craving",
        "pathFactors": ["正念", "正思惟"],
        "reason": "楽受への欲しがりを非我と見て執着しない",
        "section": "楽受と愛",
        "category": "intention",
    },
    "MN37-P11": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正精進"],
        "reason": "触→受→愛の流れを見て掴みを手放す",
        "section": "縁起の切断",
        "category": "view",
    },
}

CHINESE = {
    "MN37-P01": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-ask",
        "text": "爾時，釋提桓因至世尊所。……白世尊曰：「云何比丘斷於愛欲，心得解脫，乃至究竟安隱之處……」爾時，世尊告釋提桓因曰：「於是，拘翼！若是比丘聞此空法解無所有，則得解了一切諸法……」",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "帝釈の問と「諸法を了知する」略説。對照表は雑阿含505·増壹19.3。",
        "satUrl": SAT_EA193,
    },
    "MN37-P02": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-vedana",
        "text": "身所覺知苦樂之法，若不苦不樂之法，即於此身觀悉無常，皆歸於空。彼已觀此不苦不樂之變，亦不起想，以無有想，則無恐怖……",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "苦·楽·不苦不楽の受を無常·空と観じ、想を起こさない。",
        "satUrl": SAT_EA193,
    },
    "MN37-P03": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-nibbana",
        "text": "以無有想，則無恐怖；以無恐怖，則般涅槃：生死已盡，梵行已立，所作已辦，更不復受有，如實知之。是謂……比丘斷於愛欲，心得解脫……",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "無恐怖→涅槃。執取しなければ愛尽·解脱。",
        "satUrl": SAT_EA193,
    },
    "MN37-P04": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）／類縁",
        "t26": "EA19.3-grasp",
        "text": "（受を観じて無所著——取らなければ恐怖なく解脱。パーリは受の無常·離貪·滅·捨観。）",
        "satLocus": "大正蔵 T2.593c 斷愛（類縁）",
        "note": "受の取着を離れる方向。漢は空·無所著の語で対応。",
        "satUrl": SAT_EA193,
    },
    "MN37-P05": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-view",
        "text": "若是比丘聞此空法解無所有，則得解了一切諸法，如實知之。……觀悉無常，皆歸於空。",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "空法を聞き一切法を如実に知る——正見の受観。",
        "satUrl": SAT_EA193,
    },
    "MN37-P06": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）／類縁",
        "t26": "EA19.3-review",
        "text": "（斷愛·解脫の略説を受けて住する——夜に「私·私のもの」を見直す実践根拠。）",
        "satLocus": "大正蔵 T2.593c 斷愛（類縁）",
        "note": "愛尽の振り返り。漢に夜の儀礼句はなく実践要約。",
        "satUrl": SAT_EA193,
    },
    "MN37-P07": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-sakka",
        "text": "釋提桓因……白世尊曰：「云何比丘斷於愛欲……」爾時，世尊告釋提桓因曰……是謂……比丘斷於愛欲，心得解脫……爾時，釋提桓因禮世尊足已，繞三匝而退。",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "帝釈の問と世尊の略答。雑阿含505は目連の追試が主。",
        "satUrl": SAT_EA193,
    },
    "MN37-P08": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-brief",
        "text": "聞此空法解無所有，則得解了一切諸法……觀悉無常……無恐怖，則般涅槃……是謂……斷於愛欲，心得解脫。",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "略説の核——空·無所有·無常観·無恐怖·涅槃。",
        "satUrl": SAT_EA193,
    },
    "MN37-P09": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-teach",
        "text": "一時，佛在舍衛國祇樹給孤獨園。爾時，釋提桓因至世尊所……世尊告……是謂……斷於愛欲，心得解脫……",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "愛尽·斷愛の教えの場。",
        "satUrl": SAT_EA193,
    },
    "MN37-P10": {
        "status": "mapped",
        "pin": "増壹阿含19.3・斷愛（T125）",
        "t26": "EA19.3-sukha",
        "text": "身所覺知苦樂之法，若不苦不樂之法，即於此身觀悉無常，皆歸於空。",
        "satLocus": "大正蔵 T2.593c 斷愛",
        "note": "楽受も含め無常·空と観ずる。",
        "satUrl": SAT_EA193,
    },
    "MN37-P11": {
        "status": "unmapped",
        "pin": "（漢訳に直接対応なし）",
        "t26": "",
        "text": "",
        "satLocus": "對照表: 雑阿含505·増壹19.3。『触→受→愛』の鎖の明示は実践要約。",
        "note": "縁起の切断としての実践対応。漢の略説は受観·無所著が中心。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c.setdefault("satUrl", SAT_EA193)
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部37経は中阿含非収録。對照表は雑阿含505愛盡・増壹阿含19.3斷愛。教えの核はEA19.3が近い。",
        )
    elif c.get("status") == "unmapped":
        c.setdefault(
            "note",
            "對照表は雑阿含505・増壹19.3。このペアはパーリMN37側の実践要約。",
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
    old_path = DATA / "majjhima" / "mn037.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN37-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 37",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・渇愛の滅尽についての小経／パーリMN37）",
                    "locus": f"中部・渇愛の滅尽についての小経（MN37）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 愛尽小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第37経・愛尽小経（渇愛の滅尽についての小経）"
    SHORT = "愛尽小経（渇愛の滅尽についての小経）"
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
            "pathLabel": "愛尽·非執取の教えに触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の非執取の一歩を変える",
            "toNext": "触のあと、受の観察が見える",
            "todayObserve": OBSERVE["MN37-P01"],
            "todayAction": actions["MN37-P01"],
            "when": ["教えに触れた", "非我を意識した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN37-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN37-P09"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "受を無常·非我として観る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、楽·苦·不苦不楽の受が立つ",
            "toNext": "受に乗ると欲しがりへ",
            "todayObserve": OBSERVE["MN37-P02"],
            "todayAction": actions["MN37-P02"],
            "when": ["受を非我と見た", "正見で受を観た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN37-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN37-P05"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "「私·私のもの」を手放し、楽受にも執着しない",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、欲しがり·楽への寄りが立つ",
            "toNext": "止めないと掴みへ",
            "todayObserve": OBSERVE["MN37-P03"],
            "todayAction": actions["MN37-P03"],
            "when": ["執着を手放した", "楽受に執着しなかった"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN37-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN37-P10"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "触→受→愛の流れを見て掴みを離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、掴む手前",
            "toNext": "掴むと苦が太る",
            "todayObserve": OBSERVE["MN37-P11"],
            "todayAction": actions["MN37-P11"],
            "when": ["縁起の流れを見た"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN37-P11"][:40] + "…",
            "secondaryObserve": "触→受→愛を見て手放す",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "受を取った結果の苦を見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、取着の苦が見える",
            "toNext": "見れば、簡潔な非執取へ離す",
            "todayObserve": OBSERVE["MN37-P04"],
            "todayAction": actions["MN37-P04"],
            "when": ["受を取らないと決めた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN37-P04"][:40] + "…",
            "secondaryObserve": "受を我がものと取れば苦が増す",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "speech", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正語", "正見"], "pathFactorIds": ["speech", "view"],
            "pathLabel": "冗長を離れ、非執取の要点を語る",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、執取の語りを離す",
            "toNext": "離せば、夜の愛尽の見直しへ",
            "todayObserve": OBSERVE["MN37-P08"],
            "todayAction": actions["MN37-P08"],
            "when": ["要点だけ語った"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN37-P08"][:40] + "…",
            "secondaryObserve": "簡潔に「非我」の要点を語る",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "「私·私のもの」と見た瞬間を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの非執取の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN37-P06"],
            "todayAction": actions["MN37-P06"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN37-P06"][:40] + "…",
            "secondaryObserve": "愛尽を反芻する",
        },
    ]

    out = {
        "chapter": 37,
        "sutta": 37,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：渇愛の滅尽についての小経）",
        "suttas": ["MN 37 愛尽小経（渇愛の滅尽についての小経）"],
        "source": {
            "primary": "パーリ・中部第37経（愛尽小経／渇愛の滅尽についての小経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN37（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝中阿含非収録；對照表は雑阿含505愛盡（T99）"
                "および増壹阿含19.3斷愛（T125）。教えの核はEA19.3が近く、SA505は目連の追試が詳しい。"
                "帝釈への愛尽略説、受の無常観、非執取·解脱が主題。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・渇愛の滅尽についての小経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 増壹阿含・斷愛（T2.593c）／雑阿含・愛盡（T2.133b）",
                    "url": SAT_EA193,
                    "note": "對照表: 中阿含非収録。SC類縁EA19.3・SA505",
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
            "focusReason": "愛尽小経は愛尽·非執取が主題。既定の焦点は欲しがる。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn037.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 37:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(37, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN37-P{i:02d}" for i, p in enumerate(pairs, 1))
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
