#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn024.json (伝車経／乗り継ぎ車の経) to match MN1–23 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0429a01"
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
    "MN24-P01": (
        "友よ、まさしく、このように、まさに、戒の清浄は、心の清浄を義（目的）とする、まさしく、そのかぎりのものであり、"
        "心の清浄は、見解の清浄を義（目的）とする……知見の清浄は、〔何も〕執取せずして〔到達する〕完全なる涅槃を義（目的）とする、"
        "まさしく、そのかぎりのものです。"
        "友よ、まさに、〔何も〕執取せずして〔到達する〕完全なる涅槃を義（目的）として、世尊のもと、梵行は住されます。"
    ),
    "MN24-P02": (
        "「友よ、いったい、まさに、どうなのでしょう、戒の清浄を義（目的）として、世尊のもと、梵行が住されるのですか」と。"
        "「友よ、まさに、このことは、さにあらず」と。"
        "……戒の清浄は、心の清浄を義（目的）とする、まさしく、そのかぎりのものであり……。"
    ),
    "MN24-P03": (
        "「友よ、また、どうなのでしょう、心（瞑想）の清浄を義（目的）として、世尊のもと、梵行が住されるのですか」と。"
        "「友よ、まさに、このことは、さにあらず」と。"
        "……心の清浄は、見解の清浄を義（目的）とする、まさしく、そのかぎりのものであり……。"
    ),
    "MN24-P04": (
        "「友よ、いったい、まさに、どうなのでしょう、見解の清浄を義（目的）として、世尊のもと、梵行が住されるのですか」と。"
        "「友よ、まさに、このことは、さにあらず」と。"
        "……見解の清浄は、疑いの超渡の清浄を義（目的）とする、まさしく、そのかぎりのものであり……。"
    ),
    "MN24-P05": (
        "「友よ、また、どうなのでしょう、疑いの超渡の清浄を義（目的）として、世尊のもと、梵行が住されるのですか」と。"
        "「友よ、まさに、このことは、さにあらず」と。"
        "……疑いの超渡の清浄は、道と道ならざるものの知見の清浄を義（目的）とする、まさしく、そのかぎりのものであり……。"
    ),
    "MN24-P06": (
        "「友よ、いったい、まさに、どうなのでしょう、道と道ならざるものの知見の清浄を義（目的）として、"
        "世尊のもと、梵行が住されるのですか」と。"
        "「友よ、まさに、このことは、さにあらず」と。"
        "……道と道ならざるものの知見の清浄は、〔実践の〕道の知見の清浄を義（目的）とする……。"
    ),
    "MN24-P07": (
        "「友よ、また、どうなのでしょう、〔実践の〕道の知見の清浄を義（目的）として……"
        "知見の清浄を義（目的）として、世尊のもと、梵行が住されるのですか」と。"
        "「友よ、まさに、このことは、さにあらず」と。"
        "……〔実践の〕道の知見の清浄は、知見の清浄を義（目的）とする……"
        "知見の清浄は、〔何も〕執取せずして〔到達する〕完全なる涅槃を義（目的）とする……。"
    ),
    "MN24-P08": (
        "「友よ、それでは、何を義（目的）として、世尊のもと、梵行が住されるのですか」と。"
        "「友よ、まさに、〔何も〕執取せずして〔到達する〕完全なる涅槃を義（目的）として、世尊のもと、梵行は住されます」と。"
    ),
    "MN24-P09": (
        "友よ、それは、たとえば、また、コーサラ〔国〕のパセーナディ王が……七つの乗り継ぎ車を調達します。"
        "……第一の乗り継ぎ車に乗ります。第一の乗り継ぎ車から、第二の乗り継ぎ車に至り得ます。"
        "第一の乗り継ぎ車を捨て、第二の乗り継ぎ車に乗ります。……第七の乗り継ぎ車から、サーケータの内宮の門に到着した。"
        "（一車だけでは到れない——段階を飛ばせば到着しない。）"
    ),
    "MN24-P10": (
        "戒の清浄は、心の清浄を義（目的）とする……知見の清浄は、〔何も〕執取せずして〔到達する〕完全なる涅槃を義（目的）とする……。"
        "友よ、まさに、〔何も〕執取せずして〔到達する〕完全なる涅槃を義（目的）として、世尊のもと、梵行は住されます。"
    ),
    "MN24-P11": (
        "友よ、めったにないことです。……尊者プンナ・マンターニプッタによって、諸々の深遠なるうえにも深遠なる問いが、"
        "〔それらに〕触れては触れて、説き明かされました。"
        "……『ああ、まさに、教師に適する弟子を相手に話し合っていながら、まさに、知らなかったとは。"
        "「尊者サーリプッタである」と。』"
        "（法の乗り継ぎ——正しく問い、正しく説き明かす。）"
    ),
}

OBSERVE = {
    "MN24-P01": (
        "七つの清浄は次へ乗り継ぐため——最終目的は無執取の完全なる涅槃——"
        "朝、今日の修行が「伝車のどの段階か」を一度問う。"
    ),
    "MN24-P02": (
        "戒の清浄——それ自体が梵行の目的ではなく、心の清浄を義とする、そのかぎりのもの——"
        "今日、戒（不殺·不盗·不淫·不妄·不酒）の一つを意識する。"
    ),
    "MN24-P03": (
        "心の清浄——梵行の目的ではなく、見解の清浄を義とする。根門を護る実践は心の清浄への助け——"
        "スマホを開く前に「眼根を護る」と一呼吸置く。"
    ),
    "MN24-P04": (
        "見解の清浄——次の疑いの超渡へ乗り継ぐ、そのかぎりのもの。今の一歩を正しく用いる——"
        "食事を「清らかな修行の助けのため」と確認する。"
    ),
    "MN24-P05": (
        "疑いの超渡の清浄——道と道ならざるものの知見へ乗り継ぐ。散漫を引き戻し疑を超える精進——"
        "今日、散漫な心を「正精進」で一度引き戻す。"
    ),
    "MN24-P06": (
        "道と道ならざるものの知見の清浄——実践の道の知見へ。定に心を向け、道·非道を見分ける土台——"
        "今日、一呼吸で「離生喜楽」の方向に心を向ける。"
    ),
    "MN24-P07": (
        "実践の道の知見の清浄→知見の清浄——いずれも無執取の涅槃を義とする、そのかぎりのもの——"
        "今日の経験を「知と見」として一度見る。"
    ),
    "MN24-P08": (
        "梵行の目的は〔何も〕執取せずして到達する完全なる涅槃——各清浄は終点ではない——"
        "今日、執着を一つ手放し、解脱の方向に心を向ける。"
    ),
    "MN24-P09": (
        "パセーナディ王の七乗り継ぎ車——一車だけではサーケータに到れない。段階を飛ばせば清浄は伝わらない——"
        "今日、飛ばした段階（戒·根門等）がないか一度問う。"
    ),
    "MN24-P10": (
        "夜、七清浄の乗り継ぎを振り返る——今日どの清浄を歩み、何を次の義としたか——"
        "就寝前、今日歩んだ「伝車の段階」を一つ振り返る。"
    ),
    "MN24-P11": (
        "サーリプッタの深遠な問いとプンナ・マンターニプッタの説き明かし——法を正しく乗り継いで伝える——"
        "今日、誰かに法を伝える機会があれば、段階を踏んで伝える。"
    ),
}

PRACTICE = {
    "MN24-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、今日の修行が七清浄のどの乗り継ぎか問う",
        "section": "七清浄·目的",
        "category": "mindfulness",
    },
    "MN24-P02": {
        "nidanaId": "contact",
        "pathFactors": ["正業", "正念"],
        "reason": "戒の清浄に触れ、心の清浄へ乗り継ぐ土台を置く",
        "section": "戒の清浄",
        "category": "action",
    },
    "MN24-P03": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "眼根への受を護り、心の清浄へ向かう",
        "section": "心の清浄",
        "category": "mindfulness",
    },
    "MN24-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正命", "正見"],
        "reason": "食事への欲しがりを修行の助けと見、見解の清浄へ用いる",
        "section": "見解の清浄",
        "category": "livelihood",
    },
    "MN24-P05": {
        "nidanaId": "suffering",
        "pathFactors": ["正精進", "正見"],
        "reason": "散漫·疑いの苦を精進で引き戻し、疑いの超渡へ",
        "section": "疑いの超渡の清浄",
        "category": "effort",
    },
    "MN24-P06": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正見"],
        "reason": "定に心を向け、道と道ならざるものを見分け離す",
        "section": "道と道ならざるものの知見",
        "category": "concentration",
    },
    "MN24-P07": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正念"],
        "reason": "経験を知と見として見て、知見の清浄へ乗り継ぐ",
        "section": "道の知見·知見の清浄",
        "category": "view",
    },
    "MN24-P08": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正思惟"],
        "reason": "無執取の涅槃へ——執着を一つ手放す",
        "section": "無執取の涅槃",
        "category": "view",
    },
    "MN24-P09": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正精進"],
        "reason": "段階飛ばしの掴みを見て、乗り継ぎを確認する",
        "section": "七乗り継ぎ車",
        "category": "view",
    },
    "MN24-P10": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜、今日歩んだ清浄の段階を一つ振り返る",
        "section": "夜の乗り継ぎ",
        "category": "mindfulness",
    },
    "MN24-P11": {
        "nidanaId": "review",
        "pathFactors": ["正語", "正見"],
        "reason": "法を伝えるとき、段階を踏んで正しく説き明かす",
        "section": "問いと説き明かし",
        "category": "speech",
    },
}

CHINESE = {
    "MN24-P01": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-purpose",
        "text": (
            "以戒淨故，得心淨；以心淨故，得見淨；以見淨故，得疑蓋淨；"
            "以疑蓋淨故，得道非道知見淨；以道非道知見淨故，得道跡知見淨；"
            "以道跡知見淨故，得道跡斷智淨；以道跡斷智淨故，世尊施設無餘涅槃。"
        ),
        "satLocus": "大正蔵 T1.430c–431a 七車経",
        "note": "七淨→無餘涅槃。パーリは知見の清浄→無執取の完全なる涅槃。",
    },
    "MN24-P02": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-sila",
        "text": "「云何，賢者！以戒淨故，從沙門瞿曇修梵行耶？」答曰：「不也。」……「但以戒淨故，得心淨。」",
        "satLocus": "大正蔵 T1.430a–c 七車経",
        "note": "戒淨は目的ではなく心淨のためのもの。",
    },
    "MN24-P03": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-citta",
        "text": "「以心淨故……從沙門瞿曇修梵行耶？」答曰：「不也。」……「以心淨故，得見淨。」",
        "satLocus": "大正蔵 T1.430a–c 七車経",
        "note": "心淨＝パーリの心の清浄。",
    },
    "MN24-P04": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-ditthi",
        "text": "「以見淨故……？」答曰：「不也。」……「以見淨故，得疑蓋淨。」",
        "satLocus": "大正蔵 T1.430a–c 七車経",
        "note": "見淨＝見解の清浄。旧「受用の車」は経典にない。",
    },
    "MN24-P05": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-doubt",
        "text": "「以疑蓋淨故……？」答曰：「不也。」……「以疑蓋淨故，得道非道知見淨。」",
        "satLocus": "大正蔵 T1.430a–c 七車経",
        "note": "疑蓋淨＝疑いの超渡の清浄。旧「精進の車」は経典にない。",
    },
    "MN24-P06": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-maggamagga",
        "text": "「以道非道知見淨故……？」答曰：「不也。」……「以道非道知見淨故，得道跡知見淨。」",
        "satLocus": "大正蔵 T1.430a–c 七車経",
        "note": "道非道知見淨。旧「禅の車」は経典にない。",
    },
    "MN24-P07": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-nanadassana",
        "text": (
            "「以道跡知見淨故……以道跡斷智淨故……？」答曰：「不也。」……"
            "「以道跡知見淨故，得道跡斷智淨；以道跡斷智淨故，世尊施設無餘涅槃。」"
        ),
        "satLocus": "大正蔵 T1.430a–c 七車経",
        "note": "道跡知見淨·道跡斷智淨≈実践の道の知見·知見の清浄。",
    },
    "MN24-P08": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-nibbana",
        "text": "「然以何義，從沙門瞿曇修梵行耶？」答曰：「賢者！以無餘涅槃故。」",
        "satLocus": "大正蔵 T1.430b 七車経",
        "note": "無餘涅槃＝パーリの無執取の完全なる涅槃に対応。",
    },
    "MN24-P09": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-seven-cars",
        "text": (
            "從舍衛國出，至初車，乘初車；至第二車，捨初車，乘第二車；……"
            "至第七車，捨第六車，乘第七車，於一日中至婆雞帝。"
            "『云何，天王乘第一車，一日從舍衛國至婆雞帝耶？』王曰：『不也。』"
        ),
        "satLocus": "大正蔵 T1.430c–431a 七車経",
        "note": "一車だけでは到れない＝段階飛ばし不可。",
    },
    "MN24-P10": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-review",
        "text": (
            "如是，賢者！以戒淨故，得心淨……以道跡斷智淨故，世尊施設無餘涅槃。"
        ),
        "satLocus": "大正蔵 T1.431a 七車経",
        "note": "七淨の連鎖の振り返り。",
    },
    "MN24-P11": {
        "status": "mapped",
        "pin": "中阿含9・七車経（T26）",
        "t26": "T26-9-dialogue",
        "text": (
            "尊者舍梨子問尊者滿慈子。……「賢者名何等？……」"
            "（舍梨子·滿慈子の法談——正しく問い正しく答える。）"
        ),
        "satLocus": "大正蔵 T1.429c–431a 七車経",
        "note": "舍梨子＝サーリプッタ、滿慈子＝プンナ・マンターニプッタ。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部24経と中阿含9七車経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn024.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN24-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 24",
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
                    "locus": f"中部・乗り継ぎ車の経（MN24）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 伝車経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第24経・伝車経（乗り継ぎ車の経）"
    SHORT = "伝車経（乗り継ぎ車の経）"
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
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "朝、七清浄のどの乗り継ぎか問い、戒に触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の修行の接触を変える",
            "toNext": "触のあと、根門の受が見える",
            "todayObserve": OBSERVE["MN24-P01"],
            "todayAction": actions["MN24-P01"],
            "when": ["朝に段階を問うた", "戒を意識した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN24-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN24-P02"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "眼根への受を護り、心の清浄へ向かう",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、好ましい色などの受が立つ",
            "toNext": "受に乗ると食事·対象への欲しがりへ",
            "todayObserve": OBSERVE["MN24-P03"],
            "todayAction": actions["MN24-P03"],
            "when": ["スマホを開く前", "眼根を護った"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN24-P03"][:40] + "…",
            "secondaryObserve": "心淨",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "livelihood", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正命", "正見"], "pathFactorIds": ["livelihood", "view"],
            "pathLabel": "食事への欲しがりを修行の助けと見て見解へ用いる",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、食·楽への欲しがりが立つ",
            "toNext": "止めないと段階飛ばしの掴みへ",
            "todayObserve": OBSERVE["MN24-P04"],
            "todayAction": actions["MN24-P04"],
            "when": ["食事の前", "助けのためと確認した"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN24-P04"][:40] + "…",
            "secondaryObserve": "見淨",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "段階飛ばしや一車での到達という掴みを離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、近道·終点化の掴みが手前",
            "toNext": "掴むと疑い·散漫の苦が見える",
            "todayObserve": OBSERVE["MN24-P09"],
            "todayAction": actions["MN24-P09"],
            "when": ["飛ばしたくなった", "一段階で足りると掴んだ"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN24-P09"][:40] + "…",
            "secondaryObserve": "乘第一車一日……不也",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "effort", "nidanaLabel": "苦が太る",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "散漫·疑いの苦を精進で引き戻し、疑いの超渡へ",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、疑い·散漫の患が見える",
            "toNext": "見れば、道·非道の知見と定へ",
            "todayObserve": OBSERVE["MN24-P05"],
            "todayAction": actions["MN24-P05"],
            "when": ["散漫になった", "疑いで止まった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN24-P05"][:40] + "…",
            "secondaryObserve": "疑蓋淨",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正定"], "pathFactorIds": ["view", "concentration"],
            "pathLabel": "道·非道を見分け、知見へ乗り継ぎ、無執取の涅槃へ手放す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、定と知見で次の車へ乗り継ぐ",
            "toNext": "離せば、夜の段階の見直しへ",
            "todayObserve": OBSERVE["MN24-P08"],
            "todayAction": actions["MN24-P08"],
            "when": ["執着を手放した", "定·知見に向けた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN24-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN24-P06"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正語"], "pathFactorIds": ["mindfulness", "speech"],
            "pathLabel": "今日の乗り継ぎを振り返り、法を段階的に伝える",
            "chapterHint": SHORT,
            "fromPrev": "一日の清浄は、朝からの乗り継ぎの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN24-P10"],
            "todayAction": actions["MN24-P10"],
            "when": ["一日を閉じるとき", "法を伝えた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN24-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN24-P11"],
        },
    ]

    out = {
        "chapter": 24,
        "sutta": 24,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：乗り継ぎ車の経）",
        "suttas": ["MN 24 伝車経（乗り継ぎ車の経）"],
        "source": {
            "primary": "パーリ・中部第24経（伝車経／乗り継ぎ車の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含9七車経（T26）を段落対応でマッピング。"
                "旧スタブの「根門·受用·精進·禅」等を車とする段階名は経典にないため、七清浄に差し替え。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・乗り継ぎ車の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・七車経（T1.429a）",
                    "url": SAT_URL,
                    "note": "舍梨子·滿慈子·七車·無餘涅槃。對照表: 法雨道場",
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
            "focusReason": "乗り継ぎ車の経は各清浄を掴まず無執取の涅槃へ乗り継ぐのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn024.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 24:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(24, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN24-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    # ensure stub wrong stage names not in quotes as fact
    blob = json.dumps(out, ensure_ascii=False)
    assert "第一の車、戒なり" not in blob
    print(f"OK chinese mapped {mapped}/11; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
