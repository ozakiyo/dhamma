#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn034.json (牧牛者小経／牧牛者の小経) to match MN1–33 source alignment.

実経: 愚かな牧牛は此岸·彼岸を観ず渡り中流で滅びる＝魔の領域に不巧な師。
巧みな牧牛は渡し場で順に渡す——牡牛＝阿羅漢、強牛＝不還、牡犢＝一來、
弱犢＝預流、新生子＝随法·随信。世尊は巧みな牧者——魔流を截り不死の門を開く。
旧スタブ「新天に簡潔」は虚構。actions は保持し実文へ橋渡し。
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0342a01"
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
    "MN34-P01": (
        "かつて、愚かな摩掲陀の牧牛者がいた。"
        "雨季の末·秋に、此岸も彼岸も観ず、渡し場なき所で牛を駆り渡らせ——"
        "牛は中流に群れ、そこで滅びた。"
        "（今朝置く「簡潔な法」＝此岸·彼岸·渡し場を観て渡る、という一事。）"
    ),
    "MN34-P02": (
        "此岸も彼岸も観ず、渡し場なき所で渡らせれば、中流で滅びる。"
        "……此世·他世、魔の領域·非領域、死の領域·非領域に不巧な沙門·婆羅門も、また同様である。"
        "（快い経験も、魔の流れの中流に過ぎないか——無常として一度見る。）"
    ),
    "MN34-P03": (
        "わたしは、此世·他世に巧み、魔の領域·非領域に巧み、死の領域·非領域に巧みである。"
        "……仏は不死の門を開き、安穏·涅槃を得るために。"
        "（彼岸へ渡る道として、八正道の一つを歩む。）"
    ),
    "MN34-P04": (
        "強健·調順の牛が恒河を安度したように——"
        "五下分結を尽し、化生し、そこで般涅槃し、その世から還らない者たち。"
        "彼らも魔の流れを截り、安穏に彼岸へ渡る。"
        "（天界·楽への願いを、還らない解脱·彼岸へ向ける。）"
    ),
    "MN34-P05": (
        "新生の犢が、母の鳴き声に促されて、なお恒河を安度したように——"
        "随法行·随信行の比丘たちも、魔の流れを截り、安穏に彼岸へ渡る。"
        "（法を伝えるときは、母の鳴くがごとく、簡潔に彼岸へ促す。）"
    ),
    "MN34-P06": (
        "此世と他世は、知る者によって明らかに説かれた。"
        "……魔の及ぶ所、死の及ばぬ所。"
        "仏は不死の門を開き……悪魔の流れは截られ、吹き払われ、刈られた。"
        "比丘たちよ、喜びに満ち、安穏に心を置け。"
    ),
    "MN34-P07": (
        "新生の犢が、母の鳴き声に促されて渡るように——"
        "随法行·随信行の者も、魔の流れを截り彼岸へ渡る。"
        "（旧語「新天」は混入。新しく聞いた法を、実践に結びつける。）"
    ),
    "MN34-P08": (
        "愚かな牧牛——此岸·彼岸を観ず中流で滅びる。"
        "巧みな牧牛——観て渡し場で順に渡す。"
        "（法を語るとき、要点＝此岸·彼岸·渡し場·彼岸の安穏を簡潔に語る。）"
    ),
    "MN34-P09": (
        "巧みな牧牛は此岸·彼岸を観て渡し場で渡す——"
        "領群の牡牛＝漏尽阿羅漢、強牛＝不還、牡犢＝一來、弱犢＝預流、新生子＝随法·随信。"
        "世尊は巧みな牧者である。"
    ),
    "MN34-P10": (
        "中流に群れ、そこで滅びる——"
        "魔の領域に不巧な師に従えば、自他ともに患難に遭う。"
        "（今日の楽も、魔の貪流の一部として一度見る。）"
    ),
    "MN34-P11": (
        "仏は不死の門を開き、安穏·涅槃を得るために。"
        "悪魔の流れは截られた。——比丘たちよ、喜びに満ち、安穏に心を置け。"
        "（目的は天界·楽ではなく、彼岸·解脱·安穏かと確認する。）"
    ),
}

OBSERVE = {
    "MN34-P01": (
        "此岸·彼岸を観ず渡れば中流で滅びる——簡潔な法＝観て渡る一事。"
        "朝、今日「簡潔な法」を一つ心に置く。"
    ),
    "MN34-P02": (
        "不観の渡りは中流の滅び——快も魔流の中か、無常として見る。"
        "今日、快い経験を「無常」と一度見る。"
    ),
    "MN34-P03": (
        "世尊は巧み——不死の門を開く。彼岸への道として八正道の一支を歩む。"
        "今日、八正道のうち一つを歩む。"
    ),
    "MN34-P04": (
        "不還は化生して還らず般涅槃——天界楽より彼岸·解脱へ願いを向ける。"
        "今日、天界·楽への願いを「解脱」に向ける。"
    ),
    "MN34-P05": (
        "母の鳴き声が犢を渡す——法を伝えるなら簡潔に彼岸へ促す。"
        "今日、法を誰かに伝える機会があれば、簡潔に伝える。"
    ),
    "MN34-P06": (
        "夜、此岸·彼岸·魔流·不死の門を振り返る。"
        "就寝前、今日学んだ「無常·八正道」を一つ振り返る。"
    ),
    "MN34-P07": (
        "随法·随信——新しく聞いた法を実践に結びつける。"
        "今日、新しく学んだ法を、実践に結びつける。"
    ),
    "MN34-P08": (
        "要点は此岸·彼岸·渡し場·安穏——簡潔に語る。"
        "今日、法を語るとき、簡潔に語る。"
    ),
    "MN34-P09": (
        "牧牛者小経——順に渡る四向四果·随信と、巧みな牧者＝如来。"
        "今日、牧牛者小経の教え（無常·八正道）を思い出す。"
    ),
    "MN34-P10": (
        "中流の滅び——楽も魔の貪流の一部と見る。"
        "今日の楽を「皆苦の一部」と一度見る。"
    ),
    "MN34-P11": (
        "目的は不死·安穏·涅槃。天界楽ではない。"
        "今日、目的が「解脱」か一度確認する。"
    ),
}

PRACTICE = {
    "MN34-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、観て渡る簡潔な法に触れて心に置く",
        "section": "愚かな渡り·導入",
        "category": "mindfulness",
    },
    "MN34-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "快い受を魔流·無常として見る",
        "section": "中流の滅び",
        "category": "view",
    },
    "MN34-P03": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "彼岸へ向け八正道の一支を歩む",
        "section": "巧みな世尊·道",
        "category": "view",
    },
    "MN34-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正見"],
        "reason": "天界楽への欲しがりを解脱·彼岸へ向ける",
        "section": "不還·彼岸",
        "category": "intention",
    },
    "MN34-P05": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正念"],
        "reason": "法に触れ、簡潔に彼岸へ促す",
        "section": "母の鳴き声·随信",
        "category": "speech",
    },
    "MN34-P06": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "夜、彼岸·魔流·不死の門を振り返る",
        "section": "夜の偈",
        "category": "view",
    },
    "MN34-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正精進"],
        "reason": "新しく聞いた法に触れ、実践に結ぶ",
        "section": "随法·随信",
        "category": "mindfulness",
    },
    "MN34-P08": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正念"],
        "reason": "冗長を離れ、要点を簡潔に語る",
        "section": "簡潔に語る",
        "category": "speech",
    },
    "MN34-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "順渡の教えに触れ一つ思い出す",
        "section": "導·四向四果",
        "category": "mindfulness",
    },
    "MN34-P10": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "楽を魔流·苦の一部として見る",
        "section": "魔の貪流",
        "category": "view",
    },
    "MN34-P11": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正思惟"],
        "reason": "天界楽への掴みを離れ、解脱か確認する",
        "section": "安穏·涅槃",
        "category": "view",
    },
}

CHINESE = {
    "MN34-P01": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-foolish",
        "text": "不善觀察恒水此岸，亦不善觀恒水彼岸，而駈群牛峻岸而下……中間洄澓，多起患難。",
        "satLocus": "大正蔵 T2.342a 牧牛者",
        "note": "不観此彼岸＝中流の患難。",
    },
    "MN34-P02": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-midstream",
        "text": "中間洄澓，謂境諸魔，自遭苦難。彼諸見者，習其所學，亦遭患難。",
        "satLocus": "大正蔵 T2.342b 牧牛者",
        "note": "中流＝魔境。",
    },
    "MN34-P03": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-buddha",
        "text": "摩竭提善牧牛者……謂如來、應、等正覺。如牧牛者善觀此岸，善觀彼岸，善度其牛……。",
        "satLocus": "大正蔵 T2.342b 牧牛者",
        "note": "善牧＝如来。",
    },
    "MN34-P04": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-anagami",
        "text": "（強牛に譬え——五下分結尽·不還。漢は斯陀含等の列で対応。）得斯陀含，一來此世，究竟苦邊，橫截於彼惡魔貪流，安隱得度生死彼岸。",
        "satLocus": "大正蔵 T2.342b 牧牛者",
        "note": "截魔流·度彼岸。階位の対応はパーリが詳しい。",
    },
    "MN34-P05": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-calf",
        "text": "新生犢子愛戀其母，亦隨得度。……斷三結，得須陀洹……橫截惡魔貪流，安隱得度生死彼岸。",
        "satLocus": "大正蔵 T2.342b–c 牧牛者",
        "note": "母を恋う新生犢＝促されて渡る。",
    },
    "MN34-P06": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-verse",
        "text": "「此世及他世，明智善顯現，諸魔得未得，乃至於死魔。……」",
        "satLocus": "大正蔵 T2.342c 牧牛者",
        "note": "此世他世·魔·死魔の偈。",
    },
    "MN34-P07": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-faith",
        "text": "新生犢子愛戀其母，亦隨得度。……安隱得度生死彼岸。",
        "satLocus": "大正蔵 T2.342b–c 牧牛者",
        "note": "聞き従い渡る——随信·随法の類。",
    },
    "MN34-P08": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-concise",
        "text": "不善觀……中間洄澓……。善觀此岸，善觀彼岸，善度其牛……。",
        "satLocus": "大正蔵 T2.342a–b 牧牛者",
        "note": "要点＝観岸·善度。",
    },
    "MN34-P09": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-stages",
        "text": "先度大牛能領群者……橫截惡魔世間貪流……得須陀洹……安隱得度生死彼岸。",
        "satLocus": "大正蔵 T2.342b–c 牧牛者",
        "note": "順度の譬喩。",
    },
    "MN34-P10": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-mara",
        "text": "中間洄澓，謂境諸魔，自遭苦難。",
        "satLocus": "大正蔵 T2.342b 牧牛者",
        "note": "魔境·患難。",
    },
    "MN34-P11": {
        "status": "mapped",
        "pin": "雑阿含1248・牧牛者（T99）",
        "t26": "SA1248-nibbana",
        "text": "聲聞能盡諸漏，乃至自知不受後有。橫截惡魔世間貪流……安隱得度生死彼岸。",
        "satLocus": "大正蔵 T2.342b 牧牛者",
        "note": "漏尽·不受後有＝解脱の目的。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部34経と雑阿含1248牧牛者の内容対応（EA43.6も類縁）。對照表: 法雨道場。",
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
    old_path = DATA / "majjhima" / "mn034.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN34-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 34",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・牧牛者の小経／パーリMN34）",
                    "locus": f"中部・牧牛者の小経（MN34）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 牧牛者小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第34経・牧牛者小経（牧牛者の小経）"
    SHORT = "牧牛者小経（牧牛者の小経）"
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
            "pathFactors": ["正念", "正語"], "pathFactorIds": ["mindfulness", "speech"],
            "pathLabel": "観て渡る法に触れ、簡潔に促す",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の渡し場の一歩を変える",
            "toNext": "触のあと、快い受が見える",
            "todayObserve": OBSERVE["MN34-P01"],
            "todayAction": actions["MN34-P01"],
            "when": ["簡潔な法を置いた", "新法を実践に結んだ"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN34-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN34-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "快い受を魔流·無常として見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、快の受が立つ",
            "toNext": "受に乗ると天界楽の欲しがりへ",
            "todayObserve": OBSERVE["MN34-P02"],
            "todayAction": actions["MN34-P02"],
            "when": ["快を無常と見た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN34-P02"][:40] + "…",
            "secondaryObserve": "中流＝魔境",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "天界楽への欲しがりを解脱·彼岸へ向ける",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、天界·楽の欲しがりが立つ",
            "toNext": "止めないと天界への掴みへ",
            "todayObserve": OBSERVE["MN34-P04"],
            "todayAction": actions["MN34-P04"],
            "when": ["願いを解脱へ向けた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN34-P04"][:40] + "…",
            "secondaryObserve": "不還·彼岸",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "天界楽への掴みを離れ、解脱か確認する",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、有漏楽への掴みが手前",
            "toNext": "掴むと魔流の苦が見える",
            "todayObserve": OBSERVE["MN34-P11"],
            "todayAction": actions["MN34-P11"],
            "when": ["目的が解脱か確認した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN34-P11"][:40] + "…",
            "secondaryObserve": "安穏·涅槃",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "楽を魔の貪流·苦の一部として見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、中流の患が見える",
            "toNext": "見れば、八正道·簡潔な語で離す",
            "todayObserve": OBSERVE["MN34-P10"],
            "todayAction": actions["MN34-P10"],
            "when": ["楽を苦の一部と見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN34-P10"][:40] + "…",
            "secondaryObserve": "魔の貪流",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正語"], "pathFactorIds": ["view", "speech"],
            "pathLabel": "八正道を歩み、要点を簡潔に語って彼岸へ離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、道を歩み簡潔に促す",
            "toNext": "離せば、夜の見直しへ",
            "todayObserve": OBSERVE["MN34-P03"],
            "todayAction": actions["MN34-P03"],
            "when": ["八正道の一支を歩んだ", "簡潔に語った"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN34-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN34-P08"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "彼岸·魔流·不死の門を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの渡し場の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN34-P06"],
            "todayAction": actions["MN34-P06"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN34-P06"][:40] + "…",
            "secondaryObserve": "安穏に心を置け",
        },
    ]

    out = {
        "chapter": 34,
        "sutta": 34,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：牧牛者の小経）",
        "suttas": ["MN 34 牧牛者小経（牧牛者の小経）"],
        "source": {
            "primary": "パーリ・中部第34経（牧牛者小経／牧牛者の小経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN34（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT雑阿含1248牧牛者（T99；EA43.6も類縁）。"
                "愚かな渡りは中流で滅び、巧みな渡りは阿羅漢〜随信を順に魔流から彼岸へ渡す。"
                "旧スタブの「新天に簡潔」は虚構。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・牧牛者の小経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 雑阿含・牧牛者（T2.342a）",
                    "url": SAT_URL,
                    "note": "此岸彼岸·洄澓魔境·順度·偈。對照表: 法雨道場（SA1248）",
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
            "focusReason": "牧牛者小経は魔の流れを截り、安穏·涅槃の彼岸へ渡るのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn034.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 34:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(34, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN34-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
