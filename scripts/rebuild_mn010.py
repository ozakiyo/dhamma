#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn010.json (念処経／大いなる気づきの確立の経) to match MN1–9 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0582"
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
    "MN10-P01": (
        "比丘たちよ、これは、一路の道です──有情たちの清浄のための、諸々の憂いと嘆きの超越のための、"
        "諸々の苦痛と失意の滅至のための、正理の到達のための、涅槃の実証のための。"
        "すなわち、この、四つの気づきの確立（四念処・四念住）です。"
    ),
    "MN10-P02": (
        "彼は、まさしく、気づきある者として出息し、まさしく、気づきある者として入息します。"
        "あるいは、長く出息しつつ、『〔わたしは〕長く出息する』と覚知し、……短く入息しつつ、『〔わたしは〕短く入息する』と覚知します。"
        "『〔わたしは〕一切の身体の得知ある者として、出息するのだ』と学び……『身体の形成〔作用〕を静息させつつ、入息するのだ』と学びます。"
    ),
    "MN10-P03": (
        "比丘が、あるいは、赴いているなら、『〔わたしは〕赴く』と覚知し、あるいは、立っているなら、『立っている者として、〔わたしは〕存している』と覚知し、"
        "あるいは、坐っているなら、『坐っている者として、〔わたしは〕存している』と覚知し、"
        "あるいは、臥しているなら、『臥している者として、〔わたしは〕存している』と覚知します。"
    ),
    "MN10-P04": (
        "比丘が、前進しているとき、後進しているとき、正知を為す者として〔世に〕有り、……"
        "食べたとき、飲んだとき、……語っているとき、沈黙の状態のとき、正知を為す者として〔世に〕有ります。"
    ),
    "MN10-P05": (
        "比丘が、まさしく、この身体を、足の裏から上に、髪の頂から下に、皮膚を極限とし、種々なる流儀の不浄物に満ちているものと綿密に注視します。"
        "『この身体には、諸々の髪と諸々の毛と諸々の爪と諸々の歯と皮膚と肉と腱と骨……と尿が存在する』と。"
    ),
    "MN10-P06": (
        "比丘が、まさしく、この身体を、止住しているとおりに、作為されたとおりに、界域（界）〔の観点〕から、綿密に注視します。"
        "『この身体において、地の界域と水の界域と火の界域と風の界域が存在する』と。"
    ),
    "MN10-P07": (
        "比丘が、それは、たとえば、また、墓所に捨てられた肉体を見るとします──あるいは、死んで一日の……膨張し、青黒くなり、膿爛を生じたものを。"
        "彼は、まさしく、この身体に近しく集中します。"
        "『まさに、この身体もまた、このような法（性質）あるものであり、このような状態あるものであり、このような〔状態を〕超え行くことなきものである』と。"
    ),
    "MN10-P08": (
        "かくのごとく、あるいは、内に、身体における身体の随観ある者として〔世に〕住み、あるいは、外に……あるいは、内と外に……住みます。"
        "……『身体が存在する』と、彼に、気づきが現起するところと成り、そして、依存なき者として〔世に〕住み、さらに、何であれ、世において、〔何も〕執取しません。"
    ),
    "MN10-P09": (
        "比丘が、あるいは、安楽の感受（楽受）を感受しているなら、『〔わたしは〕安楽の感受を感受する』と覚知し、"
        "あるいは、苦痛の感受（苦受）を感受しているなら、『〔わたしは〕苦痛の感受を感受する』と覚知し、"
        "あるいは、苦でもなく楽でもない感受（不苦不楽受）を感受しているなら、『〔わたしは〕苦でもなく楽でもない感受を感受する』と覚知します。"
    ),
    "MN10-P10": (
        "比丘が、あるいは、貪欲を有する心を、『貪欲を有する心である』と覚知します。……貪欲を離れた心を……。"
        "あるいは、憤怒を有する心を……憤怒を離れた心を……。"
        "あるいは、散乱した心を、『散乱した心である』と覚知します。……定められた心を……解脱した心を……。"
    ),
    "MN10-P11": (
        "比丘が、五つの〔修行の〕妨害（五蓋）において、諸々の法（性質）における法（性質）の随観ある者として〔世に〕住みます。"
        "……内に、欲望〔の対象〕にたいする欲〔の思い〕が存在しているのを……覚知します。……憎悪……沈滞と眠気……高揚と悔恨……疑惑……を覚知します。"
    ),
    "MN10-P12": (
        "比丘が、七つの覚りの支分（七覚支）において、諸々の法（性質）における法（性質）の随観ある者として〔世に〕住みます。"
        "……内に、気づきという正覚の支分（念覚支）が存在しているのを……覚知します。"
        "……法（真理）の判別という正覚の支分（択法覚支）……精進……喜悦……静息……禅定……放捨……を覚知します。"
    ),
    "MN10-P13": (
        "比丘たちよ、まさに、彼が誰であれ、これらの四つの気づきの確立を、このように、七日のあいだ修めるなら、"
        "彼には、二つの果のなかのどちらか一つの果が期待できます。"
        "まさしく、所見の法（現世）における了知であり、あるいは、〔生存の〕依り所となる残りものが存しているなら、不還たることです。"
    ),
}

OBSERVE = {
    "MN10-P01": (
        "一路の道——清浄・憂悲の超越・苦滅・正理・涅槃のため。"
        "すなわち四つの気づきの確立（身・受・心・法）。"
    ),
    "MN10-P02": (
        "身念処の入口——気づきある出息・入息。"
        "長息・短息を知り、一切身を知り、身行を静息させる。"
    ),
    "MN10-P03": (
        "行く・立つ・坐る・臥す——そのとおりに身体を覚知する。"
    ),
    "MN10-P04": (
        "前進・後進・屈伸・食飲・語黙——すべてに正知を伴う。"
    ),
    "MN10-P05": (
        "この身は髪・毛・爪・歯・皮・肉・骨……不浄に満ちる集まり。"
        "執着の対象ではない。"
    ),
    "MN10-P06": (
        "この身に地・水・火・風の界がある——界域から綿密に注視する。"
    ),
    "MN10-P07": (
        "墓所の死体と同じく、この身もそのような法あり、超え行くことなきもの。"
    ),
    "MN10-P08": (
        "内・外・内外に身を随観し、知と気づきのためだけに『身体がある』と気づき、"
        "依存なく、世において何も執取しない。"
    ),
    "MN10-P09": (
        "楽受・苦受・不苦不楽受を、感受しているとおりに覚知する。"
    ),
    "MN10-P10": (
        "貪欲ある心・なき心、憤怒ある心・なき心、散乱・定・解脱の有無を、あるがままに知る。"
    ),
    "MN10-P11": (
        "五蓋——欲貪・瞋恚・昏沈睡眠・掉挙悪作・疑——の有無・生起・捨棄を覚知する。"
    ),
    "MN10-P12": (
        "七覚支——念・択法・精進・喜・軽安・定・捨——の有無と円満を覚知する。"
    ),
    "MN10-P13": (
        "四念処を七日修めれば、現法の了知か不還の果が期待できる。"
        "就寝前に、今日どの念処を修したかを振り返る。"
    ),
}

PRACTICE = {
    "MN10-P01": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "今日の修行を四念処の一路に結びつける",
        "section": "一路·概略",
        "category": "mindfulness",
    },
    "MN10-P02": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正定"],
        "reason": "呼吸の接触に気づきを置く",
        "section": "身·呼吸",
        "category": "concentration",
    },
    "MN10-P03": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正精進"],
        "reason": "姿勢という身体の接触を覚知する",
        "section": "身·姿勢",
        "category": "mindfulness",
    },
    "MN10-P04": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正思惟"],
        "reason": "正知で無益な行為に乗らない",
        "section": "身·正知",
        "category": "intention",
    },
    "MN10-P05": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "身体への執着を不浄観で緩める",
        "section": "身·不浄",
        "category": "view",
    },
    "MN10-P06": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "感覚を四界として見分け、身体観を立てる",
        "section": "身·四界",
        "category": "mindfulness",
    },
    "MN10-P07": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "この身も死を超え得ないと見て苦を認める",
        "section": "身·死想",
        "category": "view",
    },
    "MN10-P08": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正見"],
        "reason": "内・外に観ても依存なく執取しない",
        "section": "身·内外",
        "category": "mindfulness",
    },
    "MN10-P09": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "楽・苦・不苦不楽を名づけて受に乗らない",
        "section": "受",
        "category": "mindfulness",
    },
    "MN10-P10": {
        "nidanaId": "craving",
        "pathFactors": ["正念", "正見"],
        "reason": "貪・瞋・散乱の有無を知り、欲しがりに同化しない",
        "section": "心",
        "category": "mindfulness",
    },
    "MN10-P11": {
        "nidanaId": "craving",
        "pathFactors": ["正念", "正精進"],
        "reason": "五蓋を名づけ、生起と捨棄を見る",
        "section": "法·五蓋",
        "category": "effort",
    },
    "MN10-P12": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正精進"],
        "reason": "七覚支を育て、内面を清める",
        "section": "法·七覚支",
        "category": "effort",
    },
    "MN10-P13": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正精進"],
        "reason": "今日の四念処を振り返り、明日も続ける",
        "section": "果·結",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN10-P01": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-ekayana",
        "text": "有一道淨衆生。度憂畏滅苦惱斷啼哭得正法。謂四念處。",
        "satLocus": "大正蔵 T1.582b 念處経",
        "note": "一道＝一路の道。四念處。",
    },
    "MN10-P02": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-anapana",
        "text": "念入息即知念入息。念出息。即知念出息。入息長即知入息長。……學一切身息入。覺一切身息出。學止身行息入。",
        "satLocus": "大正蔵 T1.582c 念處経",
        "note": "長短息・一切身・止身行＝安般。",
    },
    "MN10-P03": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-iriyapatha",
        "text": "比丘者行則知行住則知住坐則知坐臥則知臥。眠則知眠寤則知寤。",
        "satLocus": "大正蔵 T1.582b 念處経",
        "note": "行住坐臥の覚知。",
    },
    "MN10-P04": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-sampajanna",
        "text": "比丘者正知出入善觀分別。屈伸低昂儀容庠序。善著僧伽梨及諸衣鉢。行住坐臥眠寤語默。皆正知之。",
        "satLocus": "大正蔵 T1.582b 念處経",
        "note": "正知＝sampajañña。",
    },
    "MN10-P05": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-asubha",
        "text": "從頭至足觀見種種不淨充滿。我此身中有髮髦爪齒。麤細薄膚皮肉筋骨。……涙汗涕唾膿血肪髓涎膽小便",
        "satLocus": "大正蔵 T1.583a 念處経",
        "note": "不淨観＝身の嫌悪随観。",
    },
    "MN10-P06": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-dhatu",
        "text": "觀身諸界。我此身中地界水界火界風界空界識界。",
        "satLocus": "大正蔵 T1.583a 念處経",
        "note": "漢訳は六界。パーリの四界に対応する核は地水火風。",
    },
    "MN10-P07": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-sivathika",
        "text": "觀彼死屍或一二日至六七日。烏鴟所啄豺狼所食。……見已自比。今我此身亦復如是倶有此法終不得離。",
        "satLocus": "大正蔵 T1.583a–b 念處経",
        "note": "死屍観＝九墓所の核。",
    },
    "MN10-P08": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-ajjhatta",
        "text": "如是比丘觀内身如身觀外身如身。立念在身。有知有見有明有達。",
        "satLocus": "大正蔵 T1.582b 念處経",
        "note": "内外観・立念。パーリの依存なく執取しない句は漢訳で圧縮。",
    },
    "MN10-P09": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-vedana",
        "text": "樂覺時便知覺樂覺。覺苦覺時便知覺苦覺。覺不苦不樂覺時。便知覺不苦不樂覺。",
        "satLocus": "大正蔵 T1.583c 念處経",
        "note": "覺＝受。",
    },
    "MN10-P10": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-citta",
        "text": "有欲心知有欲心如眞。無欲心知無欲心如眞。有恚無恚。有癡無癡……定不定。……有解脱心知解脱心如眞。",
        "satLocus": "大正蔵 T1.583c 念處経",
        "note": "心念処の諸心状態。",
    },
    "MN10-P11": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-nivarana",
        "text": "内實有疑知有疑如眞。……若已生疑滅不復生者知如眞。如是比丘觀内法如法。……謂五蓋也。",
        "satLocus": "大正蔵 T1.584a 念處経",
        "note": "五蓋の有無・生滅（睡眠調悔＝昏沈掉悔等を含む）。",
    },
    "MN10-P12": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-bojjhanga",
        "text": "内實有念覺支知有念覺支如眞。……如是法精進喜息定。比丘者。内實有捨覺支知有捨覺支如眞。",
        "satLocus": "大正蔵 T1.584a 念處経",
        "note": "七覚支。",
    },
    "MN10-P13": {
        "status": "mapped",
        "pin": "中阿含98・念處経（T26）",
        "t26": "T26-098-phala",
        "text": "若有比丘比丘尼。七日七夜立心正住四念處者。彼必得二果。或現法得究竟智。或有餘得阿那含。",
        "satLocus": "大正蔵 T1.584b 念處経",
        "note": "七日修習の二果。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部10経と中阿含98念處経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn010.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 14):
        pid = f"MN10-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 10",
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
                    "locus": f"中部・大いなる気づきの確立の経（MN10）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 念処経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第10経・念処経（大いなる気づきの確立の経）"
    SHORT = "念処経（大いなる気づきの確立の経）"
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
            "pathLabel": "呼吸・姿勢という身体の接触に気づきを置く",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の接触の念処になる",
            "toNext": "触のあと、受が立ち上がる",
            "todayObserve": OBSERVE["MN10-P02"],
            "todayAction": actions["MN10-P02"],
            "when": ["息に触れた", "姿勢が変わった"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN10-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN10-P03"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "楽・苦・不苦不楽を名づけて受に乗らない",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、三受が立つ",
            "toNext": "受に乗ると欲しがりへ",
            "todayObserve": OBSERVE["MN10-P09"],
            "todayAction": actions["MN10-P09"],
            "when": ["感情が動いた", "快・不快を感じた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN10-P09"][:40] + "…",
            "secondaryObserve": "受をあるがままに覚知する",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "心の貪瞋と五蓋を知り、欲しがりに同化しない",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、蓋と欲しがりが立つ",
            "toNext": "止めないと身体への掴みへ",
            "todayObserve": OBSERVE["MN10-P10"],
            "todayAction": actions["MN10-P10"],
            "when": ["貪・瞋が立った", "蓋が曇らせた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN10-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN10-P11"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "身体への執着を不浄観で緩める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、身への掴みが手前",
            "toNext": "掴むと死・苦が見える",
            "todayObserve": OBSERVE["MN10-P05"],
            "todayAction": actions["MN10-P05"],
            "when": ["身体に執着した", "外見に固まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN10-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN10-P06"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "この身も死を超え得ないと見て苦を認める",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、無常の苦が見える",
            "toNext": "見れば、依存なき随観へ向き直る",
            "todayObserve": OBSERVE["MN10-P07"],
            "todayAction": actions["MN10-P07"],
            "when": ["健やかさに安んじた", "死を忘れかけた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN10-P07"][:40] + "…",
            "secondaryObserve": "墓所の法はこの身にもある",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "mindfulness", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "依存なく執取せず、七覚支で清める",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、念処の実践へ戻る",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN10-P08"],
            "todayAction": actions["MN10-P08"],
            "when": ["執取しそうになった", "覚支を一つ立てた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN10-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN10-P12"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "今日の四念処を振り返り、明日の一路に結ぶ",
            "chapterHint": SHORT,
            "fromPrev": "一日の随観は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の念処になる",
            "todayObserve": OBSERVE["MN10-P13"],
            "todayAction": actions["MN10-P13"],
            "when": ["一日を閉じるとき", "念処が途切れた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN10-P13"][:40] + "…",
            "secondaryObserve": OBSERVE["MN10-P01"],
        },
    ]

    out = {
        "chapter": 10,
        "sutta": 10,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：大いなる気づきの確立の経）",
        "suttas": ["MN 10 念処経（大いなる気づきの確立の経）"],
        "source": {
            "primary": "パーリ・中部第10経（念処経／大いなる気づきの確立の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含98念處経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・大いなる気づきの確立の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・念處経（T1.582b）",
                    "url": SAT_URL,
                    "note": "漢訳は四念處。對照表: 法雨道場（長部22とも並行）",
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
            "focusReason": "念処経は接触の瞬間に身・受・心・法を随観する一路の道が主題。既定の焦点は接触。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn010.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 10:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(10, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 13
    assert all(p["id"] == f"MN10-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/13; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
