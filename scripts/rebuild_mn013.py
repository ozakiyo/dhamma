#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn013.json (苦蘊大経／大いなる苦しみの範疇の経) to match MN1–12 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0587"
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
    "MN13-P01": (
        "比丘たちよ、このような論ある〔教えを〕他にする異教の遍歴遊行者たちは、このように説かれるべき者たちとして存するでしょう。"
        "『友よ、また、何が、諸々の欲望の悦楽であり、何が、〔諸々の欲望の〕危険であり、何が、〔諸々の欲望の〕出離なのですか。"
        "何が、諸々の色形の悦楽であり……何が、諸々の感受の悦楽であり……出離なのですか』と。"
    ),
    "MN13-P02": (
        "比丘たちよ、五つのものがあります。これらの欲望の属性（妙欲）です。"
        "眼によって識知されるべき諸々の色形で、好ましく愛らしく意に適い……貪るべきものであり、"
        "……耳……鼻……舌……身によって識知されるべき諸々の感触で……貪るべきものです。"
        "……これらの五つの欲望の属性を縁として生起する、安楽であり、悦意であるなら、これは、諸々の欲望の悦楽です。"
    ),
    "MN13-P03": (
        "〔世の人々は〕欲望を因として……剣と盾を掴んで……両軍のいる戦場に跳入します……。"
        "……〔家の〕境目をもまた断ち切り……泥棒をもまた為し……。"
        "……身体による悪しき行ないを行ない……身体の破壊ののち、死後において、悪所に、悪趣に、堕所に、地獄に、再生します。"
        "比丘たちよ、これはまた、諸々の欲望の危険です……。"
    ),
    "MN13-P04": (
        "もし、その良家の子息が……それらの財物が確保されるなら、彼は、それらの財物の守護を事因とする、苦痛と失意を得知します。"
        "『どのようにすると、わたしの諸々の財物を、まさしく、王たちが運び去らず、盗賊たちが運び去らず、火が焼かず……』と。"
        "……守護し、保護しつつも、それらの財物を……失うなら、彼は、憂い悲しみ……等しき迷妄を惹起します。"
    ),
    "MN13-P05": (
        "比丘たちよ、では、何が、諸々の欲望の出離なのですか。"
        "比丘たちよ、それが、まさに、諸々の欲望〔の対象〕において、欲〔の思い〕と貪り〔の思い〕の調伏（取り除き）であり、"
        "欲〔の思い〕と貪り〔の思い〕の捨棄であるなら、これは、欲望の出離です。"
    ),
    "MN13-P06": (
        "比丘たちよ、それが、まさに、これらの五つの欲望の属性を縁として生起する、安楽であり、悦意であるなら、"
        "これは、諸々の欲望の悦楽です。"
        "……欲望を因として、欲望を因縁として、欲望を事因として……苦が生起する。"
    ),
    "MN13-P07": (
        "それが、まさに、諸々の欲望〔の対象〕において、欲〔の思い〕と貪り〔の思い〕の調伏であり、"
        "欲〔の思い〕と貪り〔の思い〕の捨棄であるなら、これは、欲望の出離です。"
        "……諸々の色形において……諸々の感受において、欲〔の思い〕と貪り〔の思い〕の調伏であり、……捨棄であるなら、これは、……出離です。"
    ),
    "MN13-P08": (
        "比丘たちよ、では、何が、諸々の色形の悦楽なのですか。……十五歳の者が、あるいは、十六歳の者がいるとします……。"
        "……何が、諸々の色形の危険なのですか。……老い朽ち……病苦の者となり……墓所に捨てられた肉体を……。"
        "……何が、諸々の色形の出離なのですか。……諸々の色形において、欲〔の思い〕と貪り〔の思い〕の調伏であり、……捨棄であるなら、これは、色形の出離です。"
    ),
    "MN13-P09": (
        "比丘たちよ、では、何が、諸々の感受の悦楽なのですか。……第一の瞑想を成就して〔世に〕住むなら……加害〔の思い〕なき感受を感受します。"
        "……何が、諸々の感受の危険なのですか。すなわち、諸々の感受が、無常であり、苦痛であり、変化の法（性質）であるのは、これは、諸々の感受の危険です。"
        "……何が、諸々の感受の出離なのですか。……諸々の感受において、欲〔の思い〕と貪り〔の思い〕の調伏であり、……捨棄であるなら、これは、感受の出離です。"
    ),
    "MN13-P10": (
        "友よ、沙門ゴータマは、諸々の欲望の遍知を報知します。わたしたちもまた、諸々の欲望の遍知を報知します。……"
        "どのような差異があり……。『友よ、また、何が、諸々の欲望の悦楽であり、何が、……危険であり、何が、……出離なのですか』と。"
        "……尋ねられた〔教えを〕他にする異教の遍歴遊行者たちは、まさしく、そして、解答できず……。"
    ),
    "MN13-P11": (
        "比丘たちよ、まさに、彼らが誰であれ……諸々の欲望の、そして、悦楽を悦楽として、かつまた、危険を危険として、さらに、出離を出離として、"
        "事実のとおりに覚知しないなら、彼らが……諸々の欲望を遍知し……〔他者に〕正しく導くことは、その道理がない。"
        "……事実のとおりに覚知するなら……諸々の欲望を遍知し……正しく導くことは、その道理がある。"
        "（色形・感受についても同じく。）"
    ),
    "MN13-P12": (
        "諸々の欲望の、そして、悦楽を悦楽として、かつまた、危険を危険として、さらに、出離を出離として、事実のとおりに覚知する。"
        "諸々の色形の……諸々の感受の……悦楽・危険・出離を、事実のとおりに覚知する。"
    ),
    "MN13-P13": (
        "それが、まさに、諸々の欲望〔の対象〕において、欲〔の思い〕と貪り〔の思い〕の調伏であり、……捨棄であるなら、これは、欲望の出離です。"
        "……諸々の色形において……諸々の感受において……欲〔の思い〕と貪り〔の思い〕の捨棄であるなら、これは、……出離です。"
    ),
}

OBSERVE = {
    "MN13-P01": (
        "欲・色・受のそれぞれに——悦楽・危険・出離を問う。"
        "味・患・出要を如実に知ることが、苦蘊の遍知の入口。"
    ),
    "MN13-P02": (
        "五妙欲——眼・耳・鼻・舌・身の好ましく愛しい対象を縁として生ずる安楽・悦意が、欲望の悦楽。"
    ),
    "MN13-P03": (
        "欲望の危険——諍い・戦場・盗掠・悪行、のちに悪趣。"
        "快楽に近づきすぎたら、この危険を思い出し距離を置く。"
    ),
    "MN13-P04": (
        "財を得ても守護の苦——王・賊・火・水・相続への恐れ。"
        "『欲しい』の裏に、縛りと災害が見えているか。"
    ),
    "MN13-P05": (
        "欲望の出離——対象における欲と貪りの調伏・捨棄。"
    ),
    "MN13-P06": (
        "五妙欲を縁として悦楽が立ち、欲望を因縁として苦陰が現法・後世に立つ。"
        "今日の苦を、その一滴として見る。"
    ),
    "MN13-P07": (
        "『欲しい』『離れたい』の裏にあるのは、欲の思いと貪り。"
        "三処（欲・色・受）すべてで、その調伏が出離。"
    ),
    "MN13-P08": (
        "色の悦楽は美色による楽喜、危険は老病死・墓所の変壊、出離は色における欲貪の捨棄。"
    ),
    "MN13-P09": (
        "受の悦楽は禅の無害の受、危険は無常・苦・変壊、出離は受における欲貪の捨棄。"
    ),
    "MN13-P10": (
        "異学も「遍知」を称するが、味・患・出要を問えば答えられない。"
        "楽しみだけを知り、害・離れることを知らぬ遍知は誤り。"
    ),
    "MN13-P11": (
        "味・患・出要を如実に知れば、自ら遍知し、他をも正しく導きうる。"
        "知らねば、自らも他も断じえない。"
    ),
    "MN13-P12": (
        "夜に、欲・色・受の苦の範疇を味・患・出要として振り返る。"
    ),
    "MN13-P13": (
        "今日取った欲・色・受への貪りを一つ思い出し、出離として手放す。"
    ),
}

PRACTICE = {
    "MN13-P01": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "今日の快楽に味・患・出要のどれを見ているか問う",
        "section": "味患出要·問",
        "category": "view",
    },
    "MN13-P02": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "五妙欲との接触を名づける",
        "section": "五妙欲·味",
        "category": "mindfulness",
    },
    "MN13-P03": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "欲望の危険（諍い・戦場・悪趣）を見て距離を置く",
        "section": "欲·患",
        "category": "view",
    },
    "MN13-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "財・対象への守護の掴みに縛りと災害を見る",
        "section": "守護·患",
        "category": "view",
    },
    "MN13-P05": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "欲と貪りの調伏・捨棄を出離と名づける",
        "section": "欲·出要",
        "category": "effort",
    },
    "MN13-P06": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "五欲を縁とする悦意から苦陰への流れを見る",
        "section": "縁·苦陰",
        "category": "mindfulness",
    },
    "MN13-P07": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "欲しい・離れたいの裏の欲貪を見る",
        "section": "欲貪",
        "category": "intention",
    },
    "MN13-P08": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "色への掴みに味・患・出要を見る",
        "section": "色·味患出要",
        "category": "view",
    },
    "MN13-P09": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "三受に味・患・出要を見る",
        "section": "受·味患出要",
        "category": "mindfulness",
    },
    "MN13-P10": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正見"],
        "reason": "異論の「遍知」に味患出要が欠けていないか見る",
        "section": "異学·問",
        "category": "speech",
    },
    "MN13-P11": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "如実知により渇愛を除き苦陰を滅す方向へ",
        "section": "遍知",
        "category": "view",
    },
    "MN13-P12": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "今日の執着を苦の範疇の一環として手放す",
        "section": "結·反芻",
        "category": "mindfulness",
    },
    "MN13-P13": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正精進"],
        "reason": "取った欲貪を一つ思い出し、明日出離する",
        "section": "出要·総括",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN13-P01": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-q",
        "text": "云何欲味。云何欲患。云何欲出要。云何色味。云何色患。云何色出要。云何覺味。云何覺患。云何覺出要。",
        "satLocus": "大正蔵 T1.587a 苦陰経",
        "note": "欲・色・覺の味患出要。",
    },
    "MN13-P02": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-assada",
        "text": "云何欲味。謂因五欲功徳。生樂生喜。極是欲味無復過是所患甚多。",
        "satLocus": "大正蔵 T1.587a 苦陰経",
        "note": "五欲功徳＝五妙欲。",
    },
    "MN13-P03": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-adinava",
        "text": "因欲縁欲以欲爲本故……入在軍陣……或死或怖受極重苦。……身壞命終。必至惡處生地獄中。是謂後世苦陰。",
        "satLocus": "大正蔵 T1.587b–c 苦陰経",
        "note": "現法・後世の苦陰。火燒等の刑罰描写あり。",
    },
    "MN13-P04": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-rakkhana",
        "text": "若得錢財者。彼便愛惜守護密藏。……莫令王奪賊劫火燒腐壞亡失。……若有王奪賊劫火燒腐壞亡失。便生憂苦愁慼懊惱。",
        "satLocus": "大正蔵 T1.587a–b 苦陰経",
        "note": "守護の患＝火燒を含む。",
    },
    "MN13-P05": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-nissarana",
        "text": "云何欲出要。若斷除欲。捨離於欲滅欲欲盡度欲出要。是謂欲出要。",
        "satLocus": "大正蔵 T1.587c 苦陰経",
        "note": "欲出要＝欲貪の捨。",
    },
    "MN13-P06": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-nidana",
        "text": "是謂現法苦陰因欲縁欲以欲爲本。……是謂後世苦陰因欲縁欲以欲爲本。",
        "satLocus": "大正蔵 T1.587b–c 苦陰経",
        "note": "因欲縁欲＝欲を縁とする苦陰。",
    },
    "MN13-P07": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-chanda-raga",
        "text": "若斷除欲。捨離於欲……若斷除覺捨離於覺。滅覺覺盡度覺出要。",
        "satLocus": "大正蔵 T1.587c–588a 苦陰経",
        "note": "欲・覺の捨離＝欲貪の調伏。",
    },
    "MN13-P08": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-rupa",
        "text": "云何色味。……美色最妙。……生樂生喜。……云何色患。若見彼姝而於後時極大衰老……死或一二日至六七日。烏鴟所啄……火燒埋地悉爛腐壞。",
        "satLocus": "大正蔵 T1.587c–588a 苦陰経",
        "note": "色の味患。",
    },
    "MN13-P09": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-vedana",
        "text": "離欲離惡不善之法。至得第四禪成就遊。……是謂覺樂味。……覺者是無常法苦法滅法。是謂覺患。……斷除覺捨離於覺……是謂覺出要。",
        "satLocus": "大正蔵 T1.588a 苦陰経",
        "note": "覺＝受。漢訳は四禅まで圧縮。",
    },
    "MN13-P10": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-paribbajaka",
        "text": "若汝等作如是問者。彼等聞已便更互相難。説外餘事瞋諍轉増。必從座起默然而退。",
        "satLocus": "大正蔵 T1.587a 苦陰経",
        "note": "異学は味患出要の問に答えられない。",
    },
    "MN13-P11": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-yathabhuta",
        "text": "欲味欲患欲出要不知如眞者。彼終不能自斷其欲。況復能斷於他欲耶。若……知如眞者。彼既自能除亦能斷他欲。",
        "satLocus": "大正蔵 T1.587c 苦陰経",
        "note": "如実知が自他の断の条件。",
    },
    "MN13-P12": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-review",
        "text": "欲味欲患欲出要知如眞者。……色味色患色出要……覺味覺患覺出要知如眞者。",
        "satLocus": "大正蔵 T1.587c–588a 苦陰経",
        "note": "三処の如実知の総括。",
    },
    "MN13-P13": {
        "status": "mapped",
        "pin": "中阿含99・苦陰経（T26）",
        "t26": "T26-099-prahana",
        "text": "若斷除欲。捨離於欲滅欲欲盡度欲出要。……若斷除覺捨離於覺。滅覺覺盡度覺出要。",
        "satLocus": "大正蔵 T1.587c–588a 苦陰経",
        "note": "斷除・捨離＝手放し。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部13経と中阿含99苦陰経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn013.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 14):
        pid = f"MN13-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 13",
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
                    "locus": f"中部・大いなる苦しみの範疇の経（MN13）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 苦蘊大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第13経・苦蘊大経（大いなる苦しみの範疇の経）"
    SHORT = "苦蘊大経（大いなる苦しみの範疇の経）"
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
            "pathLabel": "五妙欲との接触を名づけ、異論の遍知を見分ける",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の接触の見方を変える",
            "toNext": "触のあと、悦意の受が立つ",
            "todayObserve": OBSERVE["MN13-P02"],
            "todayAction": actions["MN13-P02"],
            "when": ["好ましい対象に触れた", "異論の遍知を聞いた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN13-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN13-P10"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "五欲の悦意と三受に味・患・出要を見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、安楽・悦意の受が立つ",
            "toNext": "受に乗ると欲しがりへ",
            "todayObserve": OBSERVE["MN13-P09"],
            "todayAction": actions["MN13-P09"],
            "when": ["感情が動いた", "禅の楽を味わった"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN13-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN13-P06"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "欲しい・離れたいの裏の欲貪を見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、欲の思いと貪りが立つ",
            "toNext": "止めないと守護の掴みへ",
            "todayObserve": OBSERVE["MN13-P07"],
            "todayAction": actions["MN13-P07"],
            "when": ["欲しがった", "拒んだ"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN13-P07"][:40] + "…",
            "secondaryObserve": "欲貪の調伏が出離",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "財・色への掴みに縛りと災害を見る",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、守護と美色への掴みが手前",
            "toNext": "掴むと戦場・悪趣の苦が見える",
            "todayObserve": OBSERVE["MN13-P04"],
            "todayAction": actions["MN13-P04"],
            "when": ["守ろうと固まった", "美色に掴まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN13-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN13-P08"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "欲望の危険——諍い・戦場・悪趣の苦陰を認める",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、現法・後世の苦陰が見える",
            "toNext": "見れば、出離の実践へ向き直る",
            "todayObserve": OBSERVE["MN13-P03"],
            "todayAction": actions["MN13-P03"],
            "when": ["諍いに巻き込まれた", "快楽に近づきすぎた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN13-P03"][:40] + "…",
            "secondaryObserve": "因欲縁欲以欲爲本",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "欲・色・受における欲貪を調伏し出離する",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、出要の一歩を踏む",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN13-P05"],
            "todayAction": actions["MN13-P05"],
            "when": ["欲貪を一つ捨てた", "味患出要を知った"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN13-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN13-P11"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "今日の執着を苦の範疇として振り返り、出離を決める",
            "chapterHint": SHORT,
            "fromPrev": "一日の欲・色・受は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN13-P12"],
            "todayAction": actions["MN13-P12"],
            "when": ["一日を閉じるとき", "快楽に流れた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN13-P12"][:40] + "…",
            "secondaryObserve": OBSERVE["MN13-P01"],
        },
    ]

    out = {
        "chapter": 13,
        "sutta": 13,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：大いなる苦しみの範疇の経）",
        "suttas": ["MN 13 苦蘊大経（大いなる苦しみの範疇の経）"],
        "source": {
            "primary": "パーリ・中部第13経（苦蘊大経／大いなる苦しみの範疇の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含99苦陰経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・大いなる苦しみの範疇の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・苦陰経（T1.587a）",
                    "url": SAT_URL,
                    "note": "漢訳は欲・色・覺の味患出要。對照表: 法雨道場",
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
            "focusNodeId": "suffering",
            "focusReason": "苦蘊大経は欲・色・受の味・患・出要を知り現法・後世の苦陰を見るのが主題。既定の焦点は苦。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn013.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 13:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(13, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 13
    assert all(p["id"] == f"MN13-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/13; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
