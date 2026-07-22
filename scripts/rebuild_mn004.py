#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn004.json (怖駭経／恐怖と恐ろしさの経) to match MN1–3 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0125_%2C02%2C0665"
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
    "MN4-P01": (
        "貴君ゴータマよ、まさに、征服し難きは、まさに、諸々の林地や林野の辺境であり、諸々の辺地の臥坐所です。"
        "為し難きは、喜び難きは、遠離です。"
        "独りあるとき、思うに、諸々の林が、禅定を得ずにいる比丘の意を運び去るのです。"
    ),
    "MN4-P02": (
        "婆羅門よ、〔まさに〕その、わたしが歩行していると、その恐怖と恐ろしさがやってきます。"
        "婆羅門よ、それで、まさに、わたしは、すなわち、まさしく、歩行している〔わたし〕が、その恐怖と恐ろしさを取り除くまで、"
        "それまでは、まさしく、立たず、坐らず、横になりません。"
    ),
    "MN4-P03": (
        "強欲〔の思い〕ある者たちとして、諸々の欲望〔の対象〕にたいし強き貪染ある者たちとして、諸々の林地や林野の辺境を……受用するなら、"
        "……善ならざる恐怖と恐ろしさを招き寄せる。"
        "また、まさに、わたしは……強欲〔の思い〕なき者として、わたしは存している。"
    ),
    "MN4-P04": (
        "憎悪している心の者たちとして、〔憎しみや怒りなどの〕汚れた意と思惟ある者たちとして……"
        "善ならざる恐怖と恐ろしさを招き寄せる。"
        "また、まさに、わたしは……慈愛の心ある者として、わたしは存している。"
    ),
    "MN4-P05": (
        "〔心の〕沈滞と眠気（昏沈睡眠）に遍く取り囲まれた者たちとして……"
        "善ならざる恐怖と恐ろしさを招き寄せる。"
        "また、まさに、わたしは……〔心の〕沈滞と眠気が離れ去った者として、わたしは存している。"
    ),
    "MN4-P06": (
        "〔心が〕定められていない者たちとして、散乱した心の者たちとして……"
        "善ならざる恐怖と恐ろしさを招き寄せる。"
        "また、まさに、わたしは……禅定（定・三昧）を成就した者として、わたしは存している。"
    ),
    "MN4-P07": (
        "疑いある者たちとして、疑惑ある者たちとして……"
        "善ならざる恐怖と恐ろしさを招き寄せる。"
        "また、まさに、わたしは……疑惑〔の思い〕を超えた者として、わたしは存している。"
    ),
    "MN4-P08": (
        "あるいは、鹿がやってきたり、あるいは、孔雀が小枝を落とし、あるいは、風が落ち葉を揺らします。"
        "婆羅門よ、〔まさに〕その、わたしに、この〔思い〕が有りました。"
        "『これが、まちがいなく、その恐怖と恐ろしさとしてやってくるのだ』と。"
    ),
    "MN4-P09": (
        "わたしは、完全なる清浄ならざる身体の行業ある者ではなく……完全なる清浄の身体の行業ある者として、わたしは存している。"
        "……完全なる清浄の生き方ある者として、わたしは存している。"
        "婆羅門よ、わたしは、この……ことを、自己のうちに正しく見ながら、より一層の安寧を惹起しました──林における住のために。"
    ),
    "MN4-P10": (
        "それなら、さあ、わたしは、事実のとおりにあるわたしのもとに、その恐怖と恐ろしさが、事実のとおりにやってくるままに、"
        "まさしく、事実のとおりにある者として、その恐怖と恐ろしさを、事実のとおりに取り除くのだ。"
    ),
    "MN4-P11": (
        "〔まさに〕その、わたしが、このように知っていると、このように見ていると、"
        "欲望の煩悩からもまた、心は解脱し、生存の煩悩からもまた、心は解脱し、無明の煩悩からもまた、心は解脱しました。"
        "……『生は滅尽し、梵行は完成された。為すべきことは為された。……』と証知しました。"
    ),
}

OBSERVE = {
    "MN4-P01": (
        "林野・辺地の臥坐所は征服し難く、遠離は為し難い。"
        "定を得ぬまま独りいると、林が意を運び去る。"
    ),
    "MN4-P02": (
        "恐怖が来たら、その姿勢のまま取り除くまで姿勢を変えない。"
        "歩いているときは立ち・坐・臥に移らず、恐怖を事実のとおりに除く。"
    ),
    "MN4-P03": (
        "強欲・欲望への貪染は、不善の恐怖と恐ろしさを招く。"
        "無貪欲を自己に正しく見れば、林住の安寧が増す。"
    ),
    "MN4-P04": (
        "憎悪の心・汚れた意と思惟は、不善の恐怖を招く。"
        "慈愛の心を自己に正しく見れば、林住の安寧が増す。"
    ),
    "MN4-P05": (
        "昏沈・睡眠に取り囲まれた者は、不善の恐怖を招く。"
        "沈滞と眠気が離れ去った者として見れば、安寧が増す。"
    ),
    "MN4-P06": (
        "心が定まらず散乱していると、不善の恐怖を招く。"
        "禅定を成就した者として見れば、安寧が増す。"
    ),
    "MN4-P07": (
        "疑い・疑惑は、不善の恐怖を招く。"
        "疑惑を超えた者として見れば、安寧が増す。"
    ),
    "MN4-P08": (
        "鹿の足音・小枝・風の葉音などの接触に、"
        "『これが恐怖だ』と反応が乗る。"
    ),
    "MN4-P09": (
        "身・語・意・生き方の清浄を自己に正しく見る。"
        "清浄ならざる行業という汚点がなくなれば、林住の安寧が増す。"
    ),
    "MN4-P10": (
        "恐怖を待たず、事実のとおりにやってくるままに、"
        "事実のとおりにある者として取り除く。"
    ),
    "MN4-P11": (
        "定まった清浄心で四諦・諸漏を如実に証知すれば、"
        "欲漏・有漏・無明漏から心が解脱する。"
    ),
}

PRACTICE = {
    "MN4-P01": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "定なき独住が意を運び去り苦となる",
        "section": "林野·難",
        "category": "view",
    },
    "MN4-P02": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正精進"],
        "reason": "恐怖を姿勢のまま事実のとおりに除く",
        "section": "怖駭·除",
        "category": "mindfulness",
    },
    "MN4-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正命"],
        "reason": "強欲・貪染が恐怖を招く",
        "section": "強欲",
        "category": "intention",
    },
    "MN4-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正業"],
        "reason": "憎悪を掴まず慈愛で離す",
        "section": "憎悪·慈",
        "category": "intention",
    },
    "MN4-P05": {
        "nidanaId": "feeling",
        "pathFactors": ["正精進", "正念"],
        "reason": "昏沈睡眠の受に取り囲まれない",
        "section": "昏沈睡眠",
        "category": "effort",
    },
    "MN4-P06": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正念"],
        "reason": "散乱を離れ定を成就して安寧を得る",
        "section": "散乱·定",
        "category": "concentration",
    },
    "MN4-P07": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "疑惑という掴みを超える",
        "section": "疑惑",
        "category": "view",
    },
    "MN4-P08": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "音・風の接触に恐怖の名づけが乗る",
        "section": "触→怖",
        "category": "mindfulness",
    },
    "MN4-P09": {
        "nidanaId": "release",
        "pathFactors": ["正業", "正命"],
        "reason": "身口意・生き方の清浄で林住を安んずる",
        "section": "清浄行業",
        "category": "action",
    },
    "MN4-P10": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "今日の恐怖を事実のとおりに見直す",
        "section": "事実のとおり",
        "category": "mindfulness",
    },
    "MN4-P11": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正定"],
        "reason": "漏尽・解脱を見渡し日を閉じる",
        "section": "漏尽",
        "category": "view",
    },
}

CHINESE = {
    "MN4-P01": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-open",
        "text": "在閑居穴處甚爲苦哉。獨處隻歩用心甚難。",
        "satLocus": "大正蔵 T2.665c 増上品第三十一",
        "note": "閑居独歩の難しさ＝パーリの林野・遠離の難しさ。",
    },
    "MN4-P02": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-remove-fear",
        "text": "若我經行有畏怖來者。爾時我亦不坐臥要除畏怖然後乃坐。設我住時有畏怖來者。爾時我亦非經行亦復不坐。要使除其畏怖然後乃坐。",
        "satLocus": "大正蔵 T2.666a 増壹阿含",
        "note": "姿勢を変えず畏怖を除く＝パーリと同型。",
    },
    "MN4-P03": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-gains",
        "text": "諸有沙門求於利養不能自休。然我今日無有利養之求。……我今無求於人亦同知足。",
        "satLocus": "大正蔵 T2.666a 増壹阿含",
        "note": "漢訳は十六汚点を圧縮。強欲の近接として利養求・知足を対応。",
    },
    "MN4-P04": {
        "status": "unmapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": None,
        "text": None,
        "satLocus": "大正蔵 T2.665c–666b（増上品・生漏婆羅門）",
        "note": "パーリの憎悪／慈愛の教相は、増一はこの経で明示せず（十六点が圧縮）。",
    },
    "MN4-P05": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-sloth",
        "text": "諸有沙門。婆羅門心懷懈怠不勤精進。親近閑靜之處。彼非我有。所以然者。我今有勇猛之心故中不懈惓。",
        "satLocus": "大正蔵 T2.666a 増壹阿含",
        "note": "漢訳は昏沈睡眠ではなく懈怠・勇猛精進。内容上の近接対応。",
    },
    "MN4-P06": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-samadhi",
        "text": "諸有沙門婆羅門意亂不定。彼便有惡不善法。……然我今日意終不亂恒若一心。……我恒一心。設有賢聖心一定者。我最爲上首。",
        "satLocus": "大正蔵 T2.666a 増壹阿含",
        "note": "意乱不定／一心＝散乱と定。",
    },
    "MN4-P07": {
        "status": "unmapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": None,
        "text": None,
        "satLocus": "大正蔵 T2.665c–666b（増上品・生漏婆羅門）",
        "note": "パーリの疑惑の教相は、増一はこの経で明示せず（愚癡・智慧はある）。",
    },
    "MN4-P08": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-sounds",
        "text": "我當在閑居之中時設使樹木摧折鳥獸馳走。爾時我作是念。此是大畏之林。",
        "satLocus": "大正蔵 T2.666a 増壹阿含",
        "note": "音・動きへの反応＝パーリの鹿・孔雀・風。",
    },
    "MN4-P09": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-purity",
        "text": "我今所行身口意命清淨。……諸有阿羅漢身口意命清淨者。樂在閑靜之處。我最爲上首。……在閑靜之處時倍増喜悦。",
        "satLocus": "大正蔵 T2.665c–666a 増壹阿含",
        "note": "身口意命清淨＝パーリの身語意・生き方の清浄。",
    },
    "MN4-P10": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-as-is",
        "text": "設使畏怖來者。當求方便不復使來。……要使除其畏怖然後乃坐。",
        "satLocus": "大正蔵 T2.666a 増壹阿含",
        "note": "畏怖を除く方便＝事実のとおりに取り除く。",
    },
    "MN4-P11": {
        "status": "mapped",
        "pin": "増壹阿含31.1（T125）",
        "t26": "EA31.1-asava",
        "text": "當我爾時得此心時。欲漏有漏無明漏心得解脱。以得解脱便得解脱智。生死已盡梵行已立。所作已辦更不復受胎。如實知之。",
        "satLocus": "大正蔵 T2.666b 増壹阿含",
        "note": "三漏尽・解脱智。結語の帰依・歓喜奉行もあり。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部4経と増壹阿含31.1の内容対応（對照表: 法雨道場）。漢訳は十六汚点を圧縮。",
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
    old_path = DATA / "majjhima" / "mn004.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN4-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 4",
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
                    "locus": f"中部・恐怖と恐ろしさの経（MN4）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 怖駭経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第4経・怖駭経（恐怖と恐ろしさの経）"
    SHORT = "怖駭経（恐怖と恐ろしさの経）"
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
            "pathLabel": "音・動きの接触に『恐怖』と名づける瞬間を見る",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の接触の見方になる",
            "toNext": "接触のあと、快不快・眠気などの受が来る",
            "todayObserve": OBSERVE["MN4-P08"],
            "todayAction": actions["MN4-P08"],
            "when": ["突然の音", "暗い場所に入った"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN4-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN4-P01"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "effort", "nidanaLabel": "受ける",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "昏沈・睡眠の受に取り囲まれない",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、重さ・眠気の受が来る",
            "toNext": "受に乗ると欲しがり・拒みへ",
            "todayObserve": OBSERVE["MN4-P05"],
            "todayAction": actions["MN4-P05"],
            "when": ["眠気が来た", "体が重く沈んだ"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN4-P05"][:40] + "…",
            "secondaryObserve": "沈滞と眠気が離れ去った者として見る",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正命"], "pathFactorIds": ["intention", "livelihood"],
            "pathLabel": "強欲・貪染を名づけ、恐怖の因と見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、強欲が立ち上がる",
            "toNext": "止めないと憎悪・疑惑の掴みへ",
            "todayObserve": OBSERVE["MN4-P03"],
            "todayAction": actions["MN4-P03"],
            "when": ["欲が出た", "名声や利得を追った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN4-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN4-P04"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "憎悪・疑惑を掴まず、慈愛と超克へ",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、憎み・疑いが掴む手前",
            "toNext": "掴むと林住の苦・非難が見える",
            "todayObserve": OBSERVE["MN4-P04"],
            "todayAction": actions["MN4-P04"],
            "when": ["嗔が立った", "疑いが膨らんだ"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN4-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN4-P07"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "定なき独住が意を運び去る苦を見る",
            "chapterHint": SHORT,
            "fromPrev": "汚点を抱えた林住の結果として、意が運び去られる",
            "toNext": "見れば、清浄と事実のとおりの除きへ向き直る",
            "todayObserve": OBSERVE["MN4-P01"],
            "todayAction": actions["MN4-P01"],
            "when": ["一人で不安が膨らんだ", "定まらず散った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN4-P01"][:40] + "…",
            "secondaryObserve": "遠離は為し難く喜び難い",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "mindfulness", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "清浄・正念・定で恐怖を事実のとおりに除く",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、姿勢のまま除き、清浄を見る",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN4-P02"],
            "todayAction": actions["MN4-P02"],
            "when": ["恐れが来た", "散乱した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN4-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN4-P09"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "今日の恐怖を事実のとおりに見直し、漏を見る",
            "chapterHint": SHORT,
            "fromPrev": "一日の恐怖と汚点は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN4-P10"],
            "todayAction": actions["MN4-P10"],
            "when": ["一日を閉じるとき", "夜に不安が残った"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN4-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN4-P11"],
        },
    ]

    out = {
        "chapter": 4,
        "sutta": 4,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：恐怖と恐ろしさの経）",
        "suttas": ["MN 4 怖駭経（恐怖と恐ろしさの経）"],
        "source": {
            "primary": "パーリ・中部第4経（怖駭経／恐怖と恐ろしさの経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT増壹阿含31.1（T125）を段落対応でマッピング。"
                "對照表上、中阿含ではなく増一阿含対応。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・恐怖と恐ろしさの経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 増壹阿含31.1（T2.665c）",
                    "url": SAT_URL,
                    "note": "漢訳は十六汚点を圧縮。對照表: 法雨道場",
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
            "focusReason": "怖駭経は汚点を清めて林住の安寧を得、恐怖を事実のとおりに除くのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn004.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 4:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(4, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN4-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] != "mapped"]
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; unmapped {unmapped}; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
