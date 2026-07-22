#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn006.json (願経／「望むなら」の経) to match MN1–5 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0595"
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

REFRAIN = (
    "まさしく、諸戒における円満成就を為す者として、"
    "内なる心の止寂（奢摩他・止）に専念する者として、"
    "瞑想（禅）を放却しない者として、"
    "〔あるがままの〕観察（毘鉢舎那・観）を具備した者として、"
    "諸々の空家の利用者として、〔世に〕存するべきです。"
)

QUOTES = {
    "MN6-P01": (
        "比丘たちよ、戒を成就した者たちとして、戒条（波羅提木叉）を成就した者たちとして、〔世に〕住みなさい。"
        "戒条による統御によって統御された者たちとして〔世に〕住みなさい。"
        "……諸々の微量の罪過について恐怖を見る者たちとして、〔戒を〕受持して、諸々の学びの境処において学びなさい。"
    ),
    "MN6-P02": (
        "比丘たちよ、もし、比丘が、『〔わたしは〕梵行を共にする者たちにとって、かつまた、愛しい者として、"
        "かつまた、意に適う者として、かつまた、重き者として、かつまた、尊ばれる者として、〔世に〕存するのだ』と望むなら、"
        + REFRAIN
    ),
    "MN6-P03": (
        "……内なる心の止寂に専念する者として、瞑想を放却しない者として、"
        "〔あるがままの〕観察を具備した者として、諸々の空家の利用者として、〔世に〕存するべきです。"
    ),
    "MN6-P04": (
        "比丘たちよ、もし、比丘が、『〔わたしは〕諸々の衣料や〔行乞の〕施食や臥坐具や病のための日用品たる薬の必需品の得者として〔世に〕存するのだ』と望むなら、"
        + REFRAIN
    ),
    "MN6-P05": (
        "比丘たちよ、もし、比丘が、『〔わたしは〕恐怖と恐ろしさを打ち負かす者として〔世に〕存するべきだ。"
        "そして、恐怖と恐ろしさはわたしを打ち負かすべきではなく、"
        "〔わたしは〕生起した恐怖と恐ろしさを征服しては征服して〔世に〕住むのだ』と望むなら、"
        + REFRAIN
    ),
    "MN6-P06": (
        "……〔あるがままの〕観察を具備した者として、諸々の空家の利用者として、〔世に〕存するべきです。"
    ),
    "MN6-P07": (
        "比丘たちよ、もし、比丘が、『〔わたしは〕不満〔の思い〕と歓楽〔の思い〕を打ち負かす者として〔世に〕存するべきだ。"
        "そして、不満〔の思い〕はわたしを打ち負かすべきではなく、"
        "〔わたしは〕生起した不満〔の思い〕を征服しては征服して〔世に〕住むのだ』と望むなら、"
        + REFRAIN
    ),
    "MN6-P08": (
        "比丘たちよ、もし、比丘が、『〔わたしは〕卓越の心のあり方であり、所見の法における安楽の住である、"
        "四つの瞑想（四禅）を、欲するままに得る者として、苦難なく得る者として、困難なく得る者として、〔世に〕存するのだ』と望むなら、"
        + REFRAIN
    ),
    "MN6-P09": (
        "比丘たちよ、もし、比丘が、『〔わたしは〕諸々の煩悩の滅尽あることから、煩悩なきものとして、"
        "〔止寂の〕心による解脱を、〔観察の〕智慧による解脱を、まさしく、所見の法において、自ら、証知して、実証して、成就して、〔世に〕住むのだ』と望むなら、"
        + REFRAIN
    ),
    "MN6-P10": (
        "『比丘たちよ、戒を成就した者たちとして、戒条を成就した者たちとして、〔世に〕住みなさい。……"
        "諸々の学びの境処において学びなさい』と、かくのごとく、〔わたしによって〕説かれた、すなわち、その〔言葉〕ですが、"
        "この〔言葉〕は、これを縁として説かれました。"
    ),
    "MN6-P11": (
        "比丘たちよ、もし、比丘が、『〔わたしは〕梵行を共にする者たちにとって、かつまた、愛しい者として、"
        "……尊ばれる者として、〔世に〕存するのだ』と望むなら、"
        "まさしく、諸戒における円満成就を為す者として……諸々の空家の利用者として、〔世に〕存するべきです。"
    ),
}

OBSERVE = {
    "MN6-P01": (
        "戒と戒条を成就し、統御された者として住む。"
        "微量の罪過にも恐怖を見て、学びの境処で学ぶ。"
    ),
    "MN6-P02": (
        "共住者に愛され尊ばれたいと望むなら——"
        "戒・止・禅を放けず・観・空家、という同じ道を歩け。"
    ),
    "MN6-P03": (
        "いかなる願いにも共通する中核——"
        "内なる心の止寂に専念し、禅を放けず、観を具備し、空家を用いる。"
    ),
    "MN6-P04": (
        "衣・食・臥具・薬の得者でありたいと望むならも、"
        "戒・止・禅・観・空家という同じ道である。"
    ),
    "MN6-P05": (
        "恐怖と恐ろしさを打ち負かしたいと望むならも、"
        "戒・止・禅・観・空家という同じ道である。"
    ),
    "MN6-P06": (
        "あるがままの観察（観）を具備することが、"
        "願いを道に変える条件の一つである。"
    ),
    "MN6-P07": (
        "不満の思いを打ち負かしたいと望むならも、"
        "戒・止・禅・観・空家という同じ道である。"
    ),
    "MN6-P08": (
        "四禅を欲するままに得たいと望むならも、"
        "戒・止・禅を放けず・観・空家という同じ道である。"
    ),
    "MN6-P09": (
        "漏尽・心解脱・慧解脱を現法で証したいと望むならも、"
        "戒・止・禅・観・空家という同じ道である。"
    ),
    "MN6-P10": (
        "冒頭の戒の勧めは、これらすべての願いを縁として説かれた。"
        "願いの土台は、戒を成就して学ぶことにある。"
    ),
    "MN6-P11": (
        "他者に愛され尊ばれたい願いも、比較ではなく、"
        "自分の戒・止・観・空家の実践から満たされる。"
    ),
}

PRACTICE = {
    "MN6-P01": {
        "nidanaId": "review",
        "pathFactors": ["正業", "正念"],
        "reason": "願いの土台は戒と微罪への怖畏",
        "section": "戒·勧",
        "category": "action",
    },
    "MN6-P02": {
        "nidanaId": "release",
        "pathFactors": ["正業", "正定"],
        "reason": "敬愛の願いも戒・止・観・空家の道",
        "section": "願·敬愛",
        "category": "action",
    },
    "MN6-P03": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正定"],
        "reason": "接触の場で止寂に専念し門を整える",
        "section": "止·空家",
        "category": "concentration",
    },
    "MN6-P04": {
        "nidanaId": "feeling",
        "pathFactors": ["正命", "正念"],
        "reason": "四事の受用を願うならも同じ道",
        "section": "願·四事",
        "category": "livelihood",
    },
    "MN6-P05": {
        "nidanaId": "suffering",
        "pathFactors": ["正念", "正精進"],
        "reason": "恐怖を征服したいならも同じ道",
        "section": "願·怖駭",
        "category": "mindfulness",
    },
    "MN6-P06": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正見"],
        "reason": "あるがままの観察を具備する",
        "section": "観",
        "category": "mindfulness",
    },
    "MN6-P07": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正精進"],
        "reason": "不満の思いを征服したいならも同じ道",
        "section": "願·不満",
        "category": "intention",
    },
    "MN6-P08": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正精進"],
        "reason": "四禅を得たいならも同じ道",
        "section": "願·四禅",
        "category": "concentration",
    },
    "MN6-P09": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正定"],
        "reason": "漏尽を願うならも同じ道——一歩を確認する",
        "section": "願·漏尽",
        "category": "view",
    },
    "MN6-P10": {
        "nidanaId": "review",
        "pathFactors": ["正業", "正念"],
        "reason": "戒の勧めは諸願を縁として説かれた",
        "section": "結·戒再",
        "category": "action",
    },
    "MN6-P11": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正業"],
        "reason": "他者への願いを比較の掴みにせず道に戻す",
        "section": "願·不比",
        "category": "intention",
    },
}

CHINESE = {
    "MN6-P01": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-open",
        "text": "當願世尊慰勞共我語言。爲我説法得具足戒而不廢禪。成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.595c 願経第九",
        "note": "漢訳は冒頭の戒勧が圧縮され、各願に『具足戒而不廢禪。成就觀行於空靜處』が反復。",
    },
    "MN6-P02": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-refrain",
        "text": "得具足戒而不廢禪。成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.595c–596a 願経",
        "note": "共通の道＝パーリの戒・止・不捨禅・観・空家。",
    },
    "MN6-P03": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-jhana-vipassana",
        "text": "得具足戒而不廢禪。成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.595c 願経",
        "note": "不廢禪・觀行・空靜處＝止・禅・観・空家。",
    },
    "MN6-P04": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-robes",
        "text": "比丘當願諸施我衣被飮食床榻湯藥諸生活具令彼此施有大功徳有大光明獲大果報。得具足戒而不廢禪。成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.595c 願経",
        "note": "衣被飲食等の願い。",
    },
    "MN6-P05": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-fear",
        "text": "比丘。當願我堪耐恐怖。若生恐怖心終不著。得具足戒而不廢禪。成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.596a 願経",
        "note": "堪耐恐怖＝パーリの怖駭征服。",
    },
    "MN6-P06": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-vipassana",
        "text": "成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.595c 願経",
        "note": "成就觀行＝あるがままの観察。",
    },
    "MN6-P07": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-discontent",
        "text": "比丘。當願我堪耐不樂。若生不樂心終不著。……比丘。當願我若生三惡不善之念欲念恚念害念。爲此三惡不善之念。心終不著。",
        "satLocus": "大正蔵 T1.596a 願経",
        "note": "不樂・欲恚害念＝パーリの不満征服に近接。",
    },
    "MN6-P08": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-jhana",
        "text": "比丘。當願我離欲離惡不善之法。至得第四禪成就遊。得具足戒而不廢禪。成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.596a 願経",
        "note": "至得第四禅＝四禅。",
    },
    "MN6-P09": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-asava",
        "text": "比丘。當願我如意足天耳智他心智宿命智生死智。諸漏已盡而得無漏。心解脱慧解脱。於現法中自知自覺自作證成就遊。",
        "satLocus": "大正蔵 T1.596a 願経",
        "note": "諸漏已尽・心解脱慧解脱。",
    },
    "MN6-P10": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-close",
        "text": "彼比丘受佛此教。閑居靜處宴坐思惟。修行精勤心無放逸。……於現法中自知自覺自作證成就遊。……佛説如是。彼諸比丘聞佛所説。歡喜奉行",
        "satLocus": "大正蔵 T1.596a–b 願経",
        "note": "教を受け閑居精勤し証を得る結。",
    },
    "MN6-P11": {
        "status": "mapped",
        "pin": "中阿含105・願経（T26）",
        "t26": "T26-105-same-path",
        "text": "得具足戒而不廢禪。成就觀行於空靜處。",
        "satLocus": "大正蔵 T1.595c 願経",
        "note": "いずれの願いも同じ道——比較ではなく実践。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部6経と中阿含105願経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn006.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN6-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 6",
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
                    "locus": f"中部・「望むなら」の経（MN6）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 願経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第6経・願経（「望むなら」の経）"
    SHORT = "願経（「望むなら」の経）"
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
            "id": "contact", "weekday": 1, "categoryId": "concentration", "nidanaLabel": "接触",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "接触の場で止寂に専念し空家に向かう",
            "chapterHint": SHORT,
            "fromPrev": "前夜の戒の見直しが、今朝の止寂の入り口になる",
            "toNext": "止まらねば受と欲しがりへ流れる",
            "todayObserve": OBSERVE["MN6-P03"],
            "todayAction": actions["MN6-P03"],
            "when": ["画面を開く前", "静かな場に入った"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN6-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN6-P01"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "livelihood", "nidanaLabel": "受ける",
            "pathFactors": ["正命", "正念"], "pathFactorIds": ["livelihood", "mindfulness"],
            "pathLabel": "四事の受を願うならも戒・止・観の道で受ける",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、衣食などの受が来る",
            "toNext": "受け方を誤ると欲しがりへ",
            "todayObserve": OBSERVE["MN6-P04"],
            "todayAction": actions["MN6-P04"],
            "when": ["食事の前", "道具を使うとき"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN6-P04"][:40] + "…",
            "secondaryObserve": "四事の得も同じ道",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正精進"], "pathFactorIds": ["intention", "effort"],
            "pathLabel": "不満・不善念を征服したいならも同じ道",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、不満や欲しがりが立つ",
            "toNext": "止めないと他者比較の掴みへ",
            "todayObserve": OBSERVE["MN6-P07"],
            "todayAction": actions["MN6-P07"],
            "when": ["不満が出た", "不善念が立った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN6-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN6-P05"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正業"], "pathFactorIds": ["intention", "action"],
            "pathLabel": "敬愛・比較の願いを掴まず道に戻す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、他者評価を掴む手前",
            "toNext": "掴むと願いが苦になる",
            "todayObserve": OBSERVE["MN6-P11"],
            "todayAction": actions["MN6-P11"],
            "when": ["他者と比べた", "認められたいと思った"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN6-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN6-P02"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "mindfulness", "nidanaLabel": "苦が太る",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "恐怖を征服したい願いも、道なきままでは苦",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、恐怖や不満が残る",
            "toNext": "見れば、戒・止・観・空家へ向き直る",
            "todayObserve": OBSERVE["MN6-P05"],
            "todayAction": actions["MN6-P05"],
            "when": ["不安が強い", "恐怖に負けそう"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN6-P05"][:40] + "…",
            "secondaryObserve": "恐怖征服も同じ道",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正定"], "pathFactorIds": ["view", "concentration"],
            "pathLabel": "願いを戒・止・禅・観・空家の道で離す／果へ",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、同じ道で一歩を踏む",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN6-P09"],
            "todayAction": actions["MN6-P09"],
            "when": ["願いを一歩に落とした", "禅・観に戻った"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN6-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN6-P08"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "action", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "戒の勧めで一日の願いを見直し、明日を決める",
            "chapterHint": SHORT,
            "fromPrev": "一日の願いは、戒と道を歩いたかの跡",
            "toNext": "見直しが、翌朝の止寂の土台になる",
            "todayObserve": OBSERVE["MN6-P10"],
            "todayAction": actions["MN6-P10"],
            "when": ["一日を閉じるとき", "願いが空想で終わった日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN6-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN6-P01"],
        },
    ]

    out = {
        "chapter": 6,
        "sutta": 6,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：「望むなら」の経）",
        "suttas": ["MN 6 願経（「望むなら」の経）"],
        "source": {
            "primary": "パーリ・中部第6経（願経／「望むなら」の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含105願経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・「望むなら」の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・願経（T1.595c）",
                    "url": SAT_URL,
                    "note": "漢訳は各願に共通句を反復。對照表: 法雨道場",
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
            "focusReason": "願経はいかなる願いも戒・止・禅・観・空家の道で果たすのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn006.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 6:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(6, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN6-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
