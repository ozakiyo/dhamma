#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn031.json (牛角林小経／牛角林の小経) to match MN1–30 source alignment.

実経: 阿那律·難提·金毘羅の水乳調和、慈身口意、身別心一、托鉢の無言協力、
四禅〜想受滅·漏尽。旧P06「天眼」は誤り（他心を知ったのは阿那律の返答側）。
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0729b27"
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
    "MN31-P01": (
        "そのとき、尊者阿那律·尊者難提·尊者金毘羅は、牛角の娑羅林に住していた。"
        "……世尊は問う——「そなたたちは、和合し、互いに喜び、争わず、"
        "水と乳のように混じり、互いに慈眼をもって見ているか」と。"
    ),
    "MN31-P02": (
        "世尊！わたしたちは、和合し、互いに喜び、争わず、"
        "水と乳のように混じり、互いに慈眼をもって見ています。"
        "……わたしは、これら尊者たちに、公·私ともに、身·口·意によって慈を行じます。"
    ),
    "MN31-P03": (
        "世尊は法話をもって教え·励まし·奮い立たせ·喜ばせた。"
        "（三尊者の共住は、教義の争いではなく、身口意の慈と不放逸の行で示される。）"
    ),
    "MN31-P04": (
        "世尊！わたしたちは、不放逸·熱心·精励に住しています。"
        "托鉢から先に帰る者が座·飲水·塵捨てを整え……。"
        "水が空なら手招きで助け合い、そのために語を破らない——"
        "このように不放逸に住します。"
    ),
    "MN31-P05": (
        "欲から離れ、不善の法から離れ、……初禅に入り住む。"
        "……第二禅……第三禅……第四禅に入り住む。"
        "これは、不放逸·熱心·精励に住しつつ得た、人上の法·安楽住である。"
    ),
    "MN31-P06": (
        "世尊！わたしは、これら尊者たちに、公·私ともに、身·口·意によって慈を行じます。"
        "……『わたしは、いま、自分の心を捨て、彼らの心に随おう』と。"
        "身は別でも、心は一である——わたしには、そう見えます。"
        "（他者の心を推量する前に、まず自分の慈心を観る。）"
    ),
    "MN31-P07": (
        "和合し、互いに喜び、争わず、水と乳のように混じり、慈眼をもって見る。"
        "……不放逸に住し、四禅乃至想受滅·漏尽に至る——"
        "共住の安楽は、調和·協力·定にある。"
    ),
    "MN31-P08": (
        "和合し、争わず、水乳のごとく、慈眼をもって見る。"
        "不放逸·熱心·精励に住する——"
        "（夜に、今日の調和·協力を一つ振り返る。）"
    ),
    "MN31-P09": (
        "水が空なら手招きで助け合い、そのために語を破らない。"
        "……公·私ともに、口によって慈を行じる。"
        "（争いの言葉を返さず、和みて住む。）"
    ),
    "MN31-P10": (
        "尊者阿那律·難提·金毘羅は、牛角の娑羅林に住し、"
        "和合·無諍·水乳·慈眼·不放逸·人上の法に安楽住した。"
        "……ヴァッジの人々は、まことに幸いである——"
        "これら三尊者がそこに住むがゆえに。"
    ),
    "MN31-P11": (
        "わたしは、自分の心を捨て、彼らの心に随う——"
        "わたしには、いまだかつて、ひとつも不可の心がない。"
        "（調和は外の条件より、内の争わない心·不可の心を手放すことに依る。）"
    ),
}

OBSERVE = {
    "MN31-P01": (
        "牛角林の三尊者——和合·水乳·慈眼。朝、調和して法を生きる心を一つ決める。"
        "朝、今日「調和して法を論ず」心を一つ決める。"
    ),
    "MN31-P02": (
        "争わず、水と乳のように混じり、慈眼で見る——身口意の慈。"
        "今日、共修者·家族と争わず、和みて過ごす。"
    ),
    "MN31-P03": (
        "共住の法は教義争いではなく、慈と不放逸の実践で示される。"
        "今日、誰かと法·修行について語る機会があれば、実践を論ず。"
    ),
    "MN31-P04": (
        "不放逸——托鉢の段取りを無言で助け合う。一つの行為に念·正知。"
        "今日、一つの行為に「念·正知」を置く。"
    ),
    "MN31-P05": (
        "不放逸に住しつつ四禅に入る——離生喜楽の方向。"
        "今日、一呼吸で「離生喜楽」の方向に心を向ける。"
    ),
    "MN31-P06": (
        "身は別でも心は一——他心を推量する前に、自分の慈·捨己心を観る。"
        "（旧語「天眼」は本経の主題ではない。）"
        "今日、他者の心を「推量」する前に、自分の心を観る。"
    ),
    "MN31-P07": (
        "共住の喜び——和合·無言の協力·定·漏尽への道。"
        "今日、共住者·家族との時間を「調和·法論」として過ごす。"
    ),
    "MN31-P08": (
        "夜、水乳の調和と不放逸を振り返る。"
        "就寝前、今日「調和·法論」した瞬間を一つ振り返る。"
    ),
    "MN31-P09": (
        "語を破らず、口の慈——争いの言葉を一度止める。"
        "今日、法について語るとき、争いの言葉を一度止める。"
    ),
    "MN31-P10": (
        "阿那律·難提·金毘羅をモデルに、調和を一つ実践する。"
        "今日、牛角林の三比丘を思い出し、調和を一つ実践する。"
    ),
    "MN31-P11": (
        "不可の心を手放し、彼らの心に随う——内の争いたい心を離す。"
        "今日、内の「争いたい心」を一度手放す。"
    ),
}

PRACTICE = {
    "MN31-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正思惟"],
        "reason": "朝、和合の心に触れて一つ決める",
        "section": "牛角林·三尊者",
        "category": "mindfulness",
    },
    "MN31-P02": {
        "nidanaId": "suffering",
        "pathFactors": ["正思惟", "正業"],
        "reason": "争いは苦を太らせる——和みて過ごす",
        "section": "水乳·慈眼",
        "category": "intention",
    },
    "MN31-P03": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正念"],
        "reason": "法に触れるときは実践を論じ、争いを避ける",
        "section": "実践を論ず",
        "category": "speech",
    },
    "MN31-P04": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正業"],
        "reason": "一つの行為の受に念·正知を置く",
        "section": "不放逸·無言の協力",
        "category": "mindfulness",
    },
    "MN31-P05": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正精進"],
        "reason": "欲·不善から離れ、離生喜楽の方向へ",
        "section": "四禅",
        "category": "concentration",
    },
    "MN31-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正念", "正見"],
        "reason": "他心への掴みより、まず自分の慈心を観る",
        "section": "身別心一",
        "category": "mindfulness",
    },
    "MN31-P07": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正思惟"],
        "reason": "共住の時を調和の受として過ごす",
        "section": "共住の安楽",
        "category": "mindfulness",
    },
    "MN31-P08": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "夜、調和·法論の瞬間を一つ振り返る",
        "section": "夜の調和",
        "category": "view",
    },
    "MN31-P09": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正念"],
        "reason": "争いの言葉を一度止め、口の慈へ離す",
        "section": "語を破らず",
        "category": "speech",
    },
    "MN31-P10": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正業"],
        "reason": "三尊者のモデルに触れ、調和を一つ実践する",
        "section": "導·三尊者の幸い",
        "category": "mindfulness",
    },
    "MN31-P11": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "内の争いたい欲しがりを一度手放す",
        "section": "不可の心を手放す",
        "category": "intention",
    },
}

CHINESE = {
    "MN31-P01": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-nidana",
        "text": "尊者阿那律陀、尊者難提、尊者金毘羅……常共和合，安隱無諍，一心一師，合一水乳。",
        "satLocus": "大正蔵 T1.729c–730a 牛角娑羅林",
        "note": "三尊者·合一無諍·水乳。",
    },
    "MN31-P02": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-metta",
        "text": "我常向彼梵行行慈身業，見與不見，等無有異，行慈口業，行慈意業，見與不見，等無有異。",
        "satLocus": "大正蔵 T1.730a 牛角娑羅林",
        "note": "慈身口意·見不見等。",
    },
    "MN31-P03": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-practice",
        "text": "常共和合，安隱無諍……得人上之法，而有差降安樂住止。",
        "satLocus": "大正蔵 T1.730a–b 牛角娑羅林",
        "note": "和合の実践＝人上の法の安楽住。",
    },
    "MN31-P04": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-duties",
        "text": "若彼乞食有前還者，便敷床汲水……若不能者，則以手招，共抬舉之，但不相語。",
        "satLocus": "大正蔵 T1.729c–730a 牛角娑羅林",
        "note": "托鉢の段取り·手招·不相語。",
    },
    "MN31-P05": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-jhana",
        "text": "我等離欲、離惡不善之法，至得第四禪成就遊。",
        "satLocus": "大正蔵 T1.730b 牛角娑羅林",
        "note": "至第四禅成就遊。",
    },
    "MN31-P06": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-one-mind",
        "text": "我今寧可自捨己心，隨彼諸賢心。我便自捨己心，隨彼諸賢心，我未曾有一不可心。",
        "satLocus": "大正蔵 T1.730a 牛角娑羅林",
        "note": "捨己心隨彼心＝身別心一。天眼ではない。",
    },
    "MN31-P07": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-sukha",
        "text": "常共和合，安隱無諍，一心一師，合一水乳，得人上之法，而有差降安樂住止。",
        "satLocus": "大正蔵 T1.730a–b 牛角娑羅林",
        "note": "安樂住止＝共住の安楽。",
    },
    "MN31-P08": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-review",
        "text": "常共和合，安隱無諍，一心一師，合一水乳。",
        "satLocus": "大正蔵 T1.730a 牛角娑羅林",
        "note": "夜の見直しの根拠＝常共和合。",
    },
    "MN31-P09": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-speech",
        "text": "則以手招，共抬舉之，但不相語。……行慈口業，見與不見，等無有異。",
        "satLocus": "大正蔵 T1.729c–730a 牛角娑羅林",
        "note": "不相語·慈口業。",
    },
    "MN31-P10": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-model",
        "text": "尊者阿那律陀、尊者難提、尊者金毘羅……常共和合，安隱無諍。",
        "satLocus": "大正蔵 T1.729c–730a 牛角娑羅林",
        "note": "三尊者を調和のモデルとする。",
    },
    "MN31-P11": {
        "status": "mapped",
        "pin": "中阿含185・牛角娑羅林（T26）",
        "t26": "T26-185-let-go",
        "text": "自捨己心，隨彼諸賢心，我未曾有一不可心。……常安隱，無有所乏。",
        "satLocus": "大正蔵 T1.730a 牛角娑羅林",
        "note": "未曾有一不可心＝争いたい心を手放す。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部31経と中阿含185牛角娑羅林の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn031.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN31-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 31",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・牛角林の小経／パーリMN31）",
                    "locus": f"中部・牛角林の小経（MN31）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 牛角林小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第31経・牛角林小経（牛角林の小経）"
    SHORT = "牛角林小経（牛角林の小経）"
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
            "pathLabel": "和合の心に触れ、実践として語る",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の調和の一歩を変える",
            "toNext": "触のあと、共住·行為の受が見える",
            "todayObserve": OBSERVE["MN31-P01"],
            "todayAction": actions["MN31-P01"],
            "when": ["調和の心を決めた", "三尊者を思い出した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN31-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN31-P10"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "行為と共住の時に念を置き、調和の受として過ごす",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、共住の受が立つ",
            "toNext": "受に乗ると争いたい欲しがりへ",
            "todayObserve": OBSERVE["MN31-P04"],
            "todayAction": actions["MN31-P04"],
            "when": ["念·正知を置いた", "調和として過ごした"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN31-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN31-P07"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "内の争いたい欲しがりを手放す",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、争いたい心が立つ",
            "toNext": "止めないと他心への掴みへ",
            "todayObserve": OBSERVE["MN31-P11"],
            "todayAction": actions["MN31-P11"],
            "when": ["争いたい心を手放した"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN31-P11"][:40] + "…",
            "secondaryObserve": "未曾有一不可心",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "他心への掴みより、まず自分の慈心を観る",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、他心推量の掴みが手前",
            "toNext": "掴むと争いの苦が見える",
            "todayObserve": OBSERVE["MN31-P06"],
            "todayAction": actions["MN31-P06"],
            "when": ["推量の前に自分の心を観た"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN31-P06"][:40] + "…",
            "secondaryObserve": "身別心一",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "intention", "nidanaLabel": "苦が太る",
            "pathFactors": ["正思惟", "正業"], "pathFactorIds": ["intention", "action"],
            "pathLabel": "争いは苦——水乳·慈眼で和む",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、争いの苦が見える",
            "toNext": "見れば、争いの語を止め定へ離す",
            "todayObserve": OBSERVE["MN31-P02"],
            "todayAction": actions["MN31-P02"],
            "when": ["争わず和みた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN31-P02"][:40] + "…",
            "secondaryObserve": "水乳·慈眼",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "concentration", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正定", "正語"], "pathFactorIds": ["concentration", "speech"],
            "pathLabel": "争いの語を止め、欲から離れて定へ",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、語を止め離生喜楽へ",
            "toNext": "離せば、夜の調和の見直しへ",
            "todayObserve": OBSERVE["MN31-P05"],
            "todayAction": actions["MN31-P05"],
            "when": ["離生喜楽へ向けた", "争いの語を止めた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN31-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN31-P09"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "調和·法論の瞬間を一つ振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの水乳の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN31-P08"],
            "todayAction": actions["MN31-P08"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN31-P08"][:40] + "…",
            "secondaryObserve": "常共和合",
        },
    ]

    out = {
        "chapter": 31,
        "sutta": 31,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：牛角林の小経）",
        "suttas": ["MN 31 牛角林小経（牛角林の小経）"],
        "source": {
            "primary": "パーリ・中部第31経（牛角林小経／牛角林の小経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN31（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含185牛角娑羅林（T26）。"
                "阿那律·難提·金毘羅の水乳調和、慈身口意、身別心一、托鉢の無言協力、四禅〜想受滅·漏尽。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・牛角林の小経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・牛角娑羅林（T1.729b）",
                    "url": SAT_URL,
                    "note": "合一無諍·慈身口意·第四禅。對照表: 法雨道場（中阿含185）",
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
            "focusReason": "牛角林小経は水乳·慈眼·身口意の慈で和合して住むのが主題。既定の焦点は接触。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn031.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 31:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(31, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN31-P{i:02d}" for i, p in enumerate(pairs, 1))
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
