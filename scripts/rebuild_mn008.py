#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn008.json (削減経／謹厳の経) to match MN1–7 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0573"
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
    "MN8-P01": (
        "チュンダよ、また、まさに、ここに、あなたたちによって、謹厳が為されるべきです。"
        "『他者たちが、誤った見解ある者たちとして〔世に〕有るも、わたしたちは、ここにおいて、正しい見解ある者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
        "……『他者たちが、誤った禅定ある者たちとして〔世に〕有るも、わたしたちは、ここにおいて、正しい禅定ある者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
    ),
    "MN8-P02": (
        "チュンダよ、これらの見解が、そして、そこにおいて生起し、かつまた、そこにおいて悪習となり、さらに、そこにおいて慣行となるも、"
        "それを、『これは、わたしのものではない。これは、わたしとして存在しない。これは、わたしの自己ではない』と、"
        "このように、このことを、事実のとおりに、正しい智慧によって見ていると、"
        "このように、これらの見解に捨棄が有り、このように、これらの見解に放棄が有ります。"
    ),
    "MN8-P03": (
        "『他者たちが、誤った見解ある者たちとして〔世に〕有るも、わたしたちは、ここにおいて、正しい見解ある者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
    ),
    "MN8-P04": (
        "『他者たちが、害する者たちとして〔世に〕有るも、わたしたちは、ここにおいて、害さない者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
        "『他者たちが、命あるものを殺す者たちとして〔世に〕有るも、わたしたちは、ここにおいて、命あるものを殺すことから離間した者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
    ),
    "MN8-P05": (
        "チュンダよ、また、まさに、この状況は見出されます。すなわち、ここに、一部の比丘が……第一の瞑想を成就して〔世に〕住み、"
        "彼に、このような〔思いが〕存することです。『〔わたしは〕謹厳によって〔世に〕住む』と。"
        "チュンダよ、また、まさに、これらのものは、聖者の律において、謹厳と説かれません。"
        "これらのものは、聖者の律において、所見の法（現世）における安楽の住と説かれます。"
    ),
    "MN8-P06": (
        "……第四の瞑想を成就して〔世に〕住み、彼に、このような〔思いが〕存することです。"
        "『〔わたしは〕謹厳によって〔世に〕住む』と。"
        "チュンダよ、また、まさに、これらのものは、聖者の律において、謹厳と説かれません。"
        "これらのものは、聖者の律において、所見の法（現世）における安楽の住と説かれます。"
    ),
    "MN8-P07": (
        "『他者たちが、虚偽を説く者たちとして〔世に〕有るも、わたしたちは、ここにおいて、虚偽を説くことから離間した者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
        "『他者たちが、中傷の言葉ある者たちとして〔世に〕有るも……粗暴な言葉ある者たちとして〔世に〕有るも……雑駁な虚論ある者たちとして〔世に〕有るも、"
        "わたしたちは、ここにおいて、……離間した者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
    ),
    "MN8-P08": (
        "『他者たちが、命あるものを殺す者たちとして〔世に〕有るも、わたしたちは、ここにおいて、命あるものを殺すことから離間した者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
        "『他者たちが、与えられていないものを取る者たちとして〔世に〕有るも……梵行なき者たちとして〔世に〕有るも、"
        "わたしたちは、ここにおいて、……離間した者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
    ),
    "MN8-P09": (
        "チュンダよ、それは、たとえば、また、それらが何であれ、諸々の善ならざる法（性質）は、それらの全てが、下なる域に至るべきものであり、"
        "それらが何であれ、諸々の善なる法（性質）は、それらの全てが、上なる域に至るべきものであるように、"
        "……害さない〔生き方〕は、上なる域のために成ります。……正しい見解は、上なる域のために成ります。"
    ),
    "MN8-P10": (
        "チュンダよ、かくのごとく、まさに、わたしによって、謹厳の教相が説示され、心の生起の教相が説示され、"
        "回避の教相が説示され、上なる域の教相が説示され、完全なる涅槃の教相が説示されました。"
        "チュンダよ、これらの木の根元があります。これらの空家があります。"
        "チュンダよ、瞑想しなさい。〔気づきを〕怠ってはいけません。のちに後悔ある者たちと成ってはいけません。"
    ),
    "MN8-P11": (
        "『他者たちが、誤った生き方ある者たちとして〔世に〕有るも、わたしたちは、ここにおいて、正しい生き方ある者たちとして〔世に〕有るのだ』と、謹厳が為されるべきです。"
    ),
}

OBSERVE = {
    "MN8-P01": (
        "謹厳とは——他者が邪道にあっても、ここにおいて正見から正定までを歩むこと。"
        "禅定そのものを謹厳と呼んではならない。"
    ),
    "MN8-P02": (
        "自己論・世論の見解が慣行となっても、"
        "『これはわたしのものではない・わたしではない・わたしの自己ではない』と如実に見れば、捨棄される。"
    ),
    "MN8-P03": (
        "他者が誤った見解あっても、ここにおいて正しい見解ある者として謹厳する。"
    ),
    "MN8-P04": (
        "他者が害し殺しても、ここにおいて不害・不殺として謹厳する。"
        "不善を削り落とすのが謹厳である。"
    ),
    "MN8-P05": (
        "初禅等に住んで『謹厳だ』と思っても、それは謹厳ではない。"
        "聖者の律では、現法の安楽の住と説かれる。"
    ),
    "MN8-P06": (
        "四禅の安楽に住んでも、それを謹厳と呼んではならない。"
        "安楽の住と謹厳（不善の削減）を取り違えない。"
    ),
    "MN8-P07": (
        "他者が妄語・両舌・粗語・綺語あっても、"
        "ここにおいてそれらから離間した者として謹厳する。"
    ),
    "MN8-P08": (
        "他者が殺生・不与取・非梵行あっても、"
        "ここにおいてそれらから離間した者として謹厳する。"
    ),
    "MN8-P09": (
        "不善法は全て下なる域へ、善法は全て上なる域へ向かう。"
        "道の一支が弱ければ、上域への道が細る。"
    ),
    "MN8-P10": (
        "五つの教相——謹厳・心の生起・回避・上域・涅槃——が説かれた。"
        "木の根元・空家で瞑想し、怠らず、後悔なき者となれ。"
    ),
    "MN8-P11": (
        "他者が誤った生き方あっても、ここにおいて正しい生き方ある者として謹厳する。"
    ),
}

PRACTICE = {
    "MN8-P01": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正定"],
        "reason": "今日の謹厳＝八正道の一支を立てる",
        "section": "謹厳·八支",
        "category": "view",
    },
    "MN8-P02": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "自己論・世論の見解を『我のものではない』と見る",
        "section": "見解·捨",
        "category": "view",
    },
    "MN8-P03": {
        "nidanaId": "release",
        "pathFactors": ["正見"],
        "reason": "正見として謹厳する",
        "section": "正見·謹厳",
        "category": "view",
    },
    "MN8-P04": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正業"],
        "reason": "不害・不殺として不善を削る",
        "section": "不害·謹厳",
        "category": "effort",
    },
    "MN8-P05": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正定"],
        "reason": "禅の接触を謹厳と取り違えない",
        "section": "禅≠謹厳",
        "category": "mindfulness",
    },
    "MN8-P06": {
        "nidanaId": "feeling",
        "pathFactors": ["正定", "正念"],
        "reason": "四禅の安楽は現法楽住であって謹厳ではない",
        "section": "安楽の住",
        "category": "concentration",
    },
    "MN8-P07": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正精進"],
        "reason": "妄語等から離間して謹厳する",
        "section": "正語·謹厳",
        "category": "speech",
    },
    "MN8-P08": {
        "nidanaId": "release",
        "pathFactors": ["正業", "正精進"],
        "reason": "殺盗淫から離間して謹厳する",
        "section": "正業·謹厳",
        "category": "action",
    },
    "MN8-P09": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正精進"],
        "reason": "不善は下域——弱い支を補い上域へ",
        "section": "上下域",
        "category": "view",
    },
    "MN8-P10": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正精進"],
        "reason": "五教相を振り返り、瞑想を怠らない",
        "section": "五教相·結",
        "category": "mindfulness",
    },
    "MN8-P11": {
        "nidanaId": "craving",
        "pathFactors": ["正命", "正見"],
        "reason": "誤った生き方への欲しがりを正し命で削る",
        "section": "正命·謹厳",
        "category": "livelihood",
    },
}

CHINESE = {
    "MN8-P01": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-sallekha",
        "text": "當學漸損。……周那。他有惡欲念欲。我無惡欲念欲。當學漸損。……他有不信懈怠無念無定而有惡慧。我無惡慧當學漸損。",
        "satLocus": "大正蔵 T1.573c–574a 周那問見経",
        "note": "漸損＝パーリの謹厳（sallekha）。無念無定惡慧の対＝正念正定等。",
    },
    "MN8-P02": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-views",
        "text": "世中諸見生而生。謂計有神。計有衆生有人有壽有命有世。……若使諸法滅盡無餘者。如是知如是見令此見得滅得捨離而令餘見不續不受。",
        "satLocus": "大正蔵 T1.573c 周那問見経",
        "note": "諸見の滅捨＝パーリの非我所・非我・非我我所の如実見。",
    },
    "MN8-P03": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-rightview",
        "text": "他有不信懈怠無念無定而有惡慧。我無惡慧當學漸損。",
        "satLocus": "大正蔵 T1.574a 周那問見経",
        "note": "漢訳は八正道を一括圧縮。惡慧の対としての慧＝正見に近接。",
    },
    "MN8-P04": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-harmless",
        "text": "周那。他有害意瞋。我無害意瞋。當學漸損。周那。他有殺生不與取非梵行。我無非梵行。當學漸損。",
        "satLocus": "大正蔵 T1.573c–574a 周那問見経",
        "note": "無害・不殺＝不害の謹厳。",
    },
    "MN8-P05": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-not-jhana",
        "text": "比丘者離欲離惡不善之法。至得第四禪成就遊。彼作是念我行漸損。周那。於聖法律中不但是漸損。有四増上心現法樂居。",
        "satLocus": "大正蔵 T1.573c 周那問見経",
        "note": "四禅は漸損ではなく現法楽居。",
    },
    "MN8-P06": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-sukhavihara",
        "text": "至得第四禪成就遊。彼作是念我行漸損。周那。於聖法律中不但是漸損。有四増上心現法樂居。",
        "satLocus": "大正蔵 T1.573c 周那問見経",
        "note": "現法楽居≠漸損。",
    },
    "MN8-P07": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-speech",
        "text": "周那。他有妄言兩舌麤言綺語惡戒。我無惡戒。當學漸損。",
        "satLocus": "大正蔵 T1.574a 周那問見経",
        "note": "妄言両舌麤言綺語＝正語の謹厳。",
    },
    "MN8-P08": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-action",
        "text": "周那。他有殺生不與取非梵行。我無非梵行。當學漸損。",
        "satLocus": "大正蔵 T1.574a 周那問見経",
        "note": "殺生不与取非梵行＝正業の謹厳。",
    },
    "MN8-P09": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-upari",
        "text": "若但發心。念欲求學諸善法者。則多所饒益。況復身口行善法耶。",
        "satLocus": "大正蔵 T1.574a 周那問見経",
        "note": "善法発心＝上域への志向（パーリの上なる域に近接）。",
    },
    "MN8-P10": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-close",
        "text": "周那。我已説漸損法。説發心法。説昇上法。説般涅槃法。……當學閑居靜處宴坐思惟。莫得放逸。莫令後悔。此是我教勅。説是法已。尊者大周那。及諸比丘聞佛所説。歡喜奉行",
        "satLocus": "大正蔵 T1.574b–c 周那問見経",
        "note": "漸損・発心・昇上・涅槃＋閑居思惟の結。",
    },
    "MN8-P11": {
        "status": "mapped",
        "pin": "中阿含91・周那問見経（T26）",
        "t26": "T26-091-livelihood",
        "text": "周那。他行非法惡行。我行是法妙行。當學漸損。",
        "satLocus": "大正蔵 T1.574a 周那問見経",
        "note": "非法惡行／是法妙行＝正命・正業の近接。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部8経と中阿含91周那問見経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn008.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN8-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 8",
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
                    "locus": f"中部・謹厳の経（MN8）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 削減経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第8経・削減経（謹厳の経）"
    SHORT = "削減経（謹厳の経）"
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
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "禅の安楽との接触を謹厳と取り違えない",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の見定めになる",
            "toNext": "安楽の受に乗ると欲しがりへ",
            "todayObserve": OBSERVE["MN8-P05"],
            "todayAction": actions["MN8-P05"],
            "when": ["静けさに入った", "定を感じた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN8-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN8-P06"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "concentration", "nidanaLabel": "受ける",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "四禅の安楽は現法楽住——謹厳ではない",
            "chapterHint": SHORT,
            "fromPrev": "禅の接触のあと、喜楽の受が来る",
            "toNext": "安楽を謹厳と誤ると削減が止まる",
            "todayObserve": OBSERVE["MN8-P06"],
            "todayAction": actions["MN8-P06"],
            "when": ["喜楽を味わった", "定に満足した"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN8-P06"][:40] + "…",
            "secondaryObserve": "安楽の住≠謹厳",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "livelihood", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正命", "正見"], "pathFactorIds": ["livelihood", "view"],
            "pathLabel": "誤った生き方への欲しがりを正命で削る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、不正な生計への欲しがりが立つ",
            "toNext": "止めないと見解の掴みへ",
            "todayObserve": OBSERVE["MN8-P11"],
            "todayAction": actions["MN8-P11"],
            "when": ["稼ぎ方を選ぶ", "楽な不正に傾いた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN8-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN8-P04"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "自己論・世論の見解を『我のものではない』と離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、見解が掴む手前",
            "toNext": "掴むと下域の苦が見える",
            "todayObserve": OBSERVE["MN8-P02"],
            "todayAction": actions["MN8-P02"],
            "when": ["自己を固定した", "世間論に固まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN8-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN8-P03"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "不善は下域——弱い支を補い上域へ向かう",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、下域への傾きが見える",
            "toNext": "見れば、謹厳の実践へ向き直る",
            "todayObserve": OBSERVE["MN8-P09"],
            "todayAction": actions["MN8-P09"],
            "when": ["道が途切れた", "不善が増えた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN8-P09"][:40] + "…",
            "secondaryObserve": "善法は上域のために成る",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正業"], "pathFactorIds": ["effort", "action"],
            "pathLabel": "他者が不善でも、ここにおいて不害・正語・正業で削る",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、謹厳の一歩を踏む",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN8-P04"],
            "todayAction": actions["MN8-P04"],
            "when": ["不善を一つ捨てた", "正語・正業に戻った"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN8-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN8-P07"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "五教相を振り返り、明日の謹厳を決める",
            "chapterHint": SHORT,
            "fromPrev": "一日の削減は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の見定めになる",
            "todayObserve": OBSERVE["MN8-P10"],
            "todayAction": actions["MN8-P10"],
            "when": ["一日を閉じるとき", "禅と謹厳を取り違えた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN8-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN8-P01"],
        },
    ]

    out = {
        "chapter": 8,
        "sutta": 8,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：謹厳の経）",
        "suttas": ["MN 8 削減経（謹厳の経）"],
        "source": {
            "primary": "パーリ・中部第8経（削減経／謹厳の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含91周那問見経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・謹厳の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・周那問見経（T1.573c）",
                    "url": SAT_URL,
                    "note": "漢訳は漸損法。對照表: 法雨道場",
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
            "focusReason": "削減経は不善を削り落とす謹厳が主題（禅定は謹厳ではない）。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn008.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 8:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(8, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN8-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
