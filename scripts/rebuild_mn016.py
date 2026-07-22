#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn016.json (心荒野経／心の鬱積の経) to match MN1–15 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0780b16"
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
    "MN16-P01": (
        "比丘たちよ、彼が誰であれ、比丘の、五つの心の鬱積が〔いまだ〕捨棄されていないなら、"
        "五つの心の結縛が〔いまだ〕断絶されていないなら、彼が、まさに、この法（教え）と律において、"
        "増大を〔惹起し〕、成長を〔惹起し〕、広大を惹起するであろう、という、この状況は見出されません。"
    ),
    "MN16-P02": (
        "比丘たちよ、ここに、比丘が、教師にたいし、疑い、疑惑し、信念せず、正しく浄信しません。"
        "……彼の心は、熱情に、専念に、堅忍に、精励に、傾きません。"
        "……このように、彼の、この第一の心の鬱積が〔いまだ〕捨棄されていないものとして有ります。"
    ),
    "MN16-P03": (
        "比丘たちよ、さらに、また、他に、比丘が、法（教え）にたいし、疑い、疑惑し、信念せず、正しく浄信しません。"
        "……このように、彼には、この第二の心の鬱積が〔いまだ〕捨棄されていないものとして有ります。"
    ),
    "MN16-P04": (
        "比丘たちよ、さらに、また、他に、比丘が、僧団にたいし、疑い、疑惑し、信念せず、正しく浄信しません。"
        "……このように、彼には、この第三の心の鬱積が〔いまだ〕捨棄されていないものとして有ります。"
    ),
    "MN16-P05": (
        "比丘たちよ、さらに、また、他に、比丘が、学びにたいし、疑い、疑惑し、信念せず、正しく浄信しません。"
        "……彼の心は、熱情に、専念に、堅忍に、精励に、傾きません。"
        "……このように、彼には、この第四の心の鬱積が〔いまだ〕捨棄されていないものとして有ります。"
    ),
    "MN16-P06": (
        "比丘たちよ、さらに、また、他に、比丘が、梵行を共にする者たちにたいし、激情した者として、わが意を得ない者として、"
        "害心ある者として、鬱積が生じた者として、〔世に〕有ります。"
        "……このように、彼には、この第五の心の鬱積が〔いまだ〕捨棄されていないものとして有ります。"
    ),
    "MN16-P07": (
        "彼には、どのような五つの心の結縛が〔いまだ〕断絶されていないものとして有るのですか。"
        "（１）諸々の欲望〔の対象〕にたいし、貪り〔の思い〕を離れていない者……"
        "（２）身体にたいし……（３）色形にたいし……"
        "（４）〔欲の思いで〕義とするだけ腹一杯に食べて、横臥の楽しみに……睡眠の楽しみに、専念する者……"
        "（５）或るどこかの天の衆〔への再生〕を誓願して梵行を歩みます……。"
        "……五つの心の鬱積が〔いまだ〕捨棄されていないなら、これらの五つの心の結縛が〔いまだ〕断絶されていないなら……増大を……惹起するであろう、という、この状況は見出されません。"
    ),
    "MN16-P08": (
        "比丘たちよ、さらに、また、他に、比丘が、法（教え）にたいし、疑わず、疑惑せず、信念し、正しく浄信します。"
        "……彼の心は、熱情に、専念に、堅忍に、精励に、傾きます。"
        "……このように、彼には、この第二の心の鬱積が〔すでに〕捨棄されたものとして有ります。"
        "（教師・僧団・学びについても同様に、疑わず正しく浄信するなら、心は精励に傾きます。）"
    ),
    "MN16-P09": (
        "比丘たちよ、さらに、また、他に、比丘が、梵行を共にする者たちにたいし、激情した者ではなく、わが意を得ない者ではなく、"
        "害心なき者として、鬱積が生じない者として、〔世に〕有ります。"
        "……彼の心は、熱情に、専念に、堅忍に、精励に、傾きます。"
        "……このように、彼には、この第五の心の鬱積が〔すでに〕捨棄されたものとして有ります。"
    ),
    "MN16-P10": (
        "比丘たちよ、彼が誰であれ、比丘の、五つの心の鬱積が〔すでに〕捨棄されたなら、"
        "五つの心の結縛が〔すでに〕善く断絶されたなら、彼が、まさに、この法（教え）と律において、"
        "増大を〔惹起し〕、成長を〔惹起し〕、広大を惹起するであろう、という、この状況は見出されます。"
    ),
    "MN16-P11": (
        "彼は、欲〔の思い〕の禅定と精励の形成〔作用〕を具備した神通の足場を修めます。"
        "精進の禅定と……心の禅定と……審察の禅定と……まさしく、勤勇を、第五のものとして〔修めます〕。"
        "……勤勇とともに十五の支分を具備した比丘であるなら、孵化の可能ある者であり、正覚の可能ある者であり、"
        "束縛からの平安という無上なるものへの到達の可能ある者です。"
    ),
}

OBSERVE = {
    "MN16-P01": (
        "五つの心の鬱積と五つの心の結縛が残れば、法と律での増大はない——"
        "朝、今日「心の荒野（鬱積）」がないか一度問う。"
    ),
    "MN16-P02": (
        "教師への疑・疑惑・不浄信は第一の心の鬱積——心が精励に傾かない。"
        "教師·教えへの疑を一度認め、正見に向ける。"
    ),
    "MN16-P03": (
        "法への疑は第二の心の鬱積——"
        "疑を「此是苦·此是集·此是滅·此是道」の見へ向ける。"
    ),
    "MN16-P04": (
        "僧団への疑は第三の心の鬱積——"
        "共修・僧団への疑を一度手放す。"
    ),
    "MN16-P05": (
        "学びへの疑は第四の心の鬱積——心が精励に傾かない。"
        "学びへの疑を正精進へ向ける。"
    ),
    "MN16-P06": (
        "同梵行への激情・害心・鬱積は第五の心の鬱積——"
        "共修者への嗔が来たら「同清らかな修行への嗔」と名づける。"
    ),
    "MN16-P07": (
        "五つの心の結縛——欲・身・色への貪、飽食と睡眠の楽、天への誓願の梵行。"
        "五荒野（鬱積）のうち一つを特定し、対治する。"
    ),
    "MN16-P08": (
        "疑わず信念し正しく浄信すれば、心は熱情・精励に傾く——"
        "疑が来たら苦·集·滅·道の一つに意識を向ける。"
    ),
    "MN16-P09": (
        "同梵行にたいし害心なく鬱積が生じない者——心は精励に傾く。"
        "嗔が来たら、慈心を一呼吸向ける。"
    ),
    "MN16-P10": (
        "五鬱積を捨棄し五結縛を断絶すれば、法と律での増大・成長がある。"
        "夜、今日の心の荒野を一つ認め、明日手放す。"
    ),
    "MN16-P11": (
        "四神足と勤勇を加え十五支を具備すれば、正覚・軛安穏への可能ある者——"
        "疑·嗔を語る前に一度止まる。"
    ),
}

PRACTICE = {
    "MN16-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、心の鬱積・結縛の有無に触れて問う",
        "section": "五鬱積·五結縛",
        "category": "mindfulness",
    },
    "MN16-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "師への疑の受を認め、浄信・正見へ向ける",
        "section": "師への疑",
        "category": "view",
    },
    "MN16-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "法への疑・拒みを四諦の見へ転じる",
        "section": "法への疑",
        "category": "view",
    },
    "MN16-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "僧団への疑の掴みを手放す",
        "section": "僧への疑",
        "category": "view",
    },
    "MN16-P05": {
        "nidanaId": "clinging",
        "pathFactors": ["正精進", "正見"],
        "reason": "学びへの疑を精励へ向ける",
        "section": "学びへの疑",
        "category": "effort",
    },
    "MN16-P06": {
        "nidanaId": "feeling",
        "pathFactors": ["正思惟", "正念"],
        "reason": "同梵行への嗔の受に名を付ける",
        "section": "同梵行·嗔",
        "category": "intention",
    },
    "MN16-P07": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "鬱積と結縛が残れば増大がない苦を見る",
        "section": "結縛·患",
        "category": "view",
    },
    "MN16-P08": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "疑を捨て浄信し、心を精励へ傾ける",
        "section": "浄信·精励",
        "category": "view",
    },
    "MN16-P09": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正定"],
        "reason": "害心を離し、慈心で第五の鬱積を捨棄する",
        "section": "害心なき",
        "category": "intention",
    },
    "MN16-P10": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜に今日の鬱積を振り返り、捨棄の方向を見る",
        "section": "捨棄·増大",
        "category": "mindfulness",
    },
    "MN16-P11": {
        "nidanaId": "review",
        "pathFactors": ["正語", "正念"],
        "reason": "疑·嗔を語る前に止まり、十五支の精励へ戻る",
        "section": "十五支·語",
        "category": "speech",
    },
}

CHINESE = {
    "MN16-P01": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-intro",
        "text": "若比丘、比丘尼不拔心中五穢，不解心中五縛者，是為比丘、比丘尼說必退法。",
        "satLocus": "大正蔵 T1.780b 心穢経",
        "note": "五穢＝五鬱積、五縛＝五結縛。必退法＝増大なし。",
    },
    "MN16-P02": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-sattha",
        "text": "或有一疑世尊，猶豫、不開意、不解意、意不靖。若有一疑世尊……是謂不拔第一心穢，謂於世尊也。",
        "satLocus": "大正蔵 T1.780b 心穢経",
        "note": "疑世尊＝教師への疑。",
    },
    "MN16-P03": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-dhamma",
        "text": "如是法、戒、教。……不開意、不解意、意不靖。",
        "satLocus": "大正蔵 T1.780b 心穢経",
        "note": "漢訳は法・戒・教に圧縮。パーリ第二は法への疑。",
    },
    "MN16-P04": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-sangha",
        "text": "如是法、戒、教。……不開意、不解意、意不靖。",
        "satLocus": "大正蔵 T1.780b 心穢経",
        "note": "漢訳「戒」等に圧縮。パーリ第三は僧団への疑（増一では聖衆への疑）。",
    },
    "MN16-P05": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-sikkha",
        "text": "如是法、戒、教。……不開意、不解意、意不靖。",
        "satLocus": "大正蔵 T1.780b 心穢経",
        "note": "漢訳「教」≈学び（学）。",
    },
    "MN16-P06": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-sabrahmacari",
        "text": "若有諸梵行，世尊所稱譽，彼便責數、輕易、觸嬈、侵害，不開意、不解意、意不靖，是謂第五不拔心中穢，謂於梵行也。",
        "satLocus": "大正蔵 T1.780b 心穢経",
        "note": "於梵行＝同梵行への嗔・侵害。",
    },
    "MN16-P07": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-vinibandha",
        "text": "云何不解心中五縛？或有一身不離染……於欲不離染……數道俗共會……少有所得故，於其中間住，不復求昇進。……不拔此心中五穢，及不解此心中五縛者，是謂……必退法也。",
        "satLocus": "大正蔵 T1.780b–c 心穢経",
        "note": "五縛の列は漢訳でやや異なり、核は未離染・未昇進。",
    },
    "MN16-P08": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-pasada",
        "text": "云何善拔心中五穢？或有一不疑世尊，不猶豫、開意、意解、意靖。……如是法、戒、教。……開意、意解、意靖。",
        "satLocus": "大正蔵 T1.781a 心穢経",
        "note": "不疑・開意＝浄信。",
    },
    "MN16-P09": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-avyapada",
        "text": "若有梵行，世尊所稱譽，彼不責數、不輕易、不觸嬈、不侵害，開意、意解、意靖，是謂第五善拔心中穢，謂於梵行也。",
        "satLocus": "大正蔵 T1.781a 心穢経",
        "note": "不責数・不侵害＝害心なき。",
    },
    "MN16-P10": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-vuddhi",
        "text": "若有比丘、比丘尼善拔心中五穢，善解心中五縛者，是謂比丘、比丘尼清淨法。",
        "satLocus": "大正蔵 T1.780c–781a 心穢経",
        "note": "善抜・善解＝捨棄・断絶→清淨法（増大の側）。",
    },
    "MN16-P11": {
        "status": "mapped",
        "pin": "中阿含206・心穢経（T26）",
        "t26": "T26-206-iddhipada",
        "text": "彼住此十支已，復修習五法。……修欲定……精進定、心定、思惟定……堪任第五，彼成就此堪任等十五法。……猶如雞生十卵，或十二……自安隱出者……我說無不得涅槃。",
        "satLocus": "大正蔵 T1.781b 心穢経",
        "note": "十五法・鶏卵喩＝十五支・孵化。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部16経と中阿含206心穢経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn016.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN16-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 16",
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
                    "locus": f"中部・心の鬱積の経（MN16）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 心荒蕪経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第16経・心荒野経（心の鬱積の経）"
    SHORT = "心荒野経（心の鬱積の経）"
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
            "pathLabel": "朝、心の鬱積・結縛の有無に触れて問う",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の疑·嗔の接触を変える",
            "toNext": "触のあと、疑や嗔の受が見える",
            "todayObserve": OBSERVE["MN16-P01"],
            "todayAction": actions["MN16-P01"],
            "when": ["朝に心を問う", "疑が触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN16-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN16-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "師への疑と同梵行への嗔の受を名づける",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、疑·嗔の受が立つ",
            "toNext": "受に乗ると法への拒みや掴みへ",
            "todayObserve": OBSERVE["MN16-P02"],
            "todayAction": actions["MN16-P02"],
            "when": ["師を疑った", "共修者に嗔った"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN16-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN16-P06"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "法への疑・拒みを四諦の見へ転じる",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、法を拒む欲しがりが立つ",
            "toNext": "止めないと僧·学への掴みへ",
            "todayObserve": OBSERVE["MN16-P03"],
            "todayAction": actions["MN16-P03"],
            "when": ["法を疑った", "四諦へ向けた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN16-P03"][:40] + "…",
            "secondaryObserve": "如是法",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "僧·学への疑の掴みを手放し精励へ向ける",
            "chapterHint": SHORT,
            "fromPrev": "拒みのあと、共修と学びへの掴みが手前",
            "toNext": "掴むと増大なき苦が見える",
            "todayObserve": OBSERVE["MN16-P04"],
            "todayAction": actions["MN16-P04"],
            "when": ["僧を疑った", "学びを疑った"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN16-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN16-P05"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "鬱積と結縛が残れば法と律での増大がないと見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、必退・増大なしの患が見える",
            "toNext": "見れば、浄信と害心なき離しへ",
            "todayObserve": OBSERVE["MN16-P07"],
            "todayAction": actions["MN16-P07"],
            "when": ["荒野を一つ特定した", "結縛を思った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN16-P07"][:40] + "…",
            "secondaryObserve": "必退法",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "疑を浄信へ、嗔を害心なきへ転じて鬱積を捨棄する",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、四諦と慈へ向き直る",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN16-P08"],
            "todayAction": actions["MN16-P08"],
            "when": ["疑を四諦へ向けた", "慈心を向けた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN16-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN16-P09"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "捨棄と十五支を振り返り、疑·嗔の語りを止める",
            "chapterHint": SHORT,
            "fromPrev": "一日の疑·嗔は、朝からの鬱積の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN16-P10"],
            "todayAction": actions["MN16-P10"],
            "when": ["一日を閉じるとき", "疑·嗔を語りそうになった"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN16-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN16-P11"],
        },
    ]

    out = {
        "chapter": 16,
        "sutta": 16,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：心の鬱積の経）",
        "suttas": ["MN 16 心荒野経（心の鬱積の経）"],
        "source": {
            "primary": "パーリ・中部第16経（心荒野経／心の鬱積の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含206心穢経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・心の鬱積の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・心穢経（T1.780b）",
                    "url": SAT_URL,
                    "note": "五穢・五縛。對照表: 法雨道場",
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
            "focusReason": "心の鬱積の経は五鬱積の捨棄と五結縛の断絶により法と律での増大へ向かうのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn016.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 16:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(16, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN16-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
