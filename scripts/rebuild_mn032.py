#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn032.json (牛角林大経／牛角林の大経) to match MN1–31 source alignment.

実経: 牛角娑羅林の夜、何等の比丘が林を起発（荘厳）するか——
阿難＝多聞、離越＝独住·定、阿那律＝天眼、迦葉＝頭陀·少欲、目連＝法論（漢は神足に差）、
舎利弗＝心を御す、世尊＝食後結跏·正念·不取著まで漏尽。
旧スタブの「林·食·法友·法が快適」は虚構。actions は保持し quote·observe で実文へ。
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0726c01"
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
    "MN32-P01": (
        "牛角の娑羅林は、まことに愛楽すべきである。"
        "夜は月明かで、諸々の娑羅は妙香を敷き、天の香りが漂うようである。"
        "阿難よ、いかなる比丘が、この林を起発するであろうか。"
    ),
    "MN32-P02": (
        "尊者離越（レヴァタ）は答えた——"
        "独住を楽しみ、独住を愛し、内心の寂静に専心し、禅を廃せず、"
        "観を具し、空屋に親しむ比丘——このような比丘が、この林を起発する。"
        "（林の静けさ·美しさは、独住·定の器として味わう。）"
    ),
    "MN32-P03": (
        "尊者大迦葉は答えた——"
        "阿蘭若に住し、乞食のみを食し、糞掃衣を着け、三衣を持つ……。"
        "少欲·知足·遠離·精勤であり、これを称讃する比丘——"
        "このような比丘が、この林を起発する。"
        "（食事は清らかな修行の助け——乞食·適度として確かめる。）"
    ),
    "MN32-P04": (
        "尊者大目犍連は答えた——"
        "二人の比丘が法について論じ、互いに問い答え、滞らず、"
        "法の論が流れるように進む——このような比丘が、この林を起発する。"
        "（漢訳は神足の答えに差あり。パーリは法論。）"
    ),
    "MN32-P05": (
        "尊者阿難は答えた——"
        "広学多聞、守持して忘れず……法は初·中·後も妙、義·文あり、"
        "梵行を顕現する。四衆に説き、諸結を断ぜんとす——"
        "このような比丘が、この林を起発する。"
    ),
    "MN32-P06": (
        "世尊は言われた——"
        "食後、乞食より帰り、結跏趺坐し、身を正し、正念を現前に置き、思う——"
        "『わたしは、心が諸漏から不取著によって解脱するまで、この坐を解かない』と。"
        "このような比丘が、この林を起発する。"
    ),
    "MN32-P07": (
        "『わたしは、心が諸漏から不取著によって解脱するまで、この坐を解かない』——"
        "取著があれば林も起発せず、不取著あれば最上の起発である。"
        "（今日の苦を、取著の結果と一度見る。）"
    ),
    "MN32-P08": (
        "牛角の娑羅林は、夜月明かで愛楽すべきである……。"
        "不取著によって諸漏から解脱するまで坐を解かない——"
        "（就寝前、今日の取著を一つ認め、手放して眠る。）"
    ),
    "MN32-P09": (
        "世尊は言われた——「そなたたちは、おのおの自らの仕方で、よく語った。」"
        "……阿難は多聞……離越は独住……阿那律は天眼……"
        "迦葉は頭陀……目連は法の説者……舎利弗は心を御す——"
        "各自の見に随って正しく答えた。"
    ),
    "MN32-P10": (
        "二人の比丘が法について論じ、互いに問い答え、滞らず、"
        "法の論が流れるように進む。"
        "（争わず、和みて、各自の見を述べよ。）"
    ),
    "MN32-P11": (
        "食後、結跏趺坐し、身を正し、正念を現前に置き——"
        "『不取著によって諸漏から解脱するまで、この坐を解かない』と。"
        "尊者舎利弗は言う——心を御して、心に御されない。"
        "（一つの行為に正念·正知を置く。）"
    ),
}

OBSERVE = {
    "MN32-P01": (
        "牛角林の夜——いかなる比丘が林を起発するか。快適な林住＝起発する生き方。"
        "朝、今日「快適な林住」の心を一つ決める。"
    ),
    "MN32-P02": (
        "離越＝独住·内心の寂静·空屋。環境の静けさ·美しさを独住の器として味わう。"
        "今日、環境の静けさ·美しさを一度味わう。"
    ),
    "MN32-P03": (
        "迦葉＝乞食·少欲·知足。食事は適度に、清らかな修行の助け。"
        "食事を「適度に、清らかな修行の助けのため」と確認する。"
    ),
    "MN32-P04": (
        "目連（パーリ）＝二人の法論が滞らず流れる。法友と法を一度語る。"
        "今日、法友·共修者と法について一度語る。"
    ),
    "MN32-P05": (
        "阿難＝多聞·守持·四衆に説く。正しい法の一節を学び反芻する。"
        "今日、正しい法の一節を学び、反芻する。"
    ),
    "MN32-P06": (
        "世尊＝不取著によって漏尽まで坐を解かない。内の取著を一つ手放す。"
        "今日、内の執着（心配·反芻）を一つ手放す。"
    ),
    "MN32-P07": (
        "取著があれば起発せず——苦を取著の結果と見る。"
        "今日の苦を「執着の結果」と一度見る。"
    ),
    "MN32-P08": (
        "夜の林を思い、今日の取著を一つ認め手放す。"
        "就寝前、今日の執着を一つ認め、手放して眠る。"
    ),
    "MN32-P09": (
        "おのおの自らの仕方でよく語った——自分の見を述べ、他者の見も聴く。"
        "今日、自分の見を述べつつ、他者の見も聴く。"
    ),
    "MN32-P10": (
        "法論は滞らず流れる——争いの言葉を一度止める。"
        "今日、法について語るとき、争いの言葉を一度止める。"
    ),
    "MN32-P11": (
        "正念を現前に置き、不取著·漏尽へ。一つの行為に正念·正知。"
        "今日、一つの行為に「正念·正知」を置く。"
    ),
}

PRACTICE = {
    "MN32-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、林を起発する心に触れて一つ決める",
        "section": "牛角林·何等の比丘",
        "category": "mindfulness",
    },
    "MN32-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "環境の静けさの受を独住の器として味わう",
        "section": "離越·独住",
        "category": "concentration",
    },
    "MN32-P03": {
        "nidanaId": "feeling",
        "pathFactors": ["正命", "正念"],
        "reason": "食事の受を修行の助けとして適度に確かめる",
        "section": "迦葉·乞食·少欲",
        "category": "livelihood",
    },
    "MN32-P04": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正念"],
        "reason": "法友に触れ、法を一度語る",
        "section": "目連·法論",
        "category": "speech",
    },
    "MN32-P05": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "正しい法の一節に触れ、学び反芻する",
        "section": "阿難·多聞",
        "category": "view",
    },
    "MN32-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正精進"],
        "reason": "内の取著の掴みを一つ手放す",
        "section": "世尊·不取著",
        "category": "view",
    },
    "MN32-P07": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦を取著の結果と一度見る",
        "section": "取著と苦",
        "category": "view",
    },
    "MN32-P08": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜、今日の取著を認め手放す",
        "section": "夜·手放して眠る",
        "category": "mindfulness",
    },
    "MN32-P09": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正語"],
        "reason": "自分の見だけを通す欲しがりを抑え、他も聴く",
        "section": "各自よく語った",
        "category": "intention",
    },
    "MN32-P10": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正念"],
        "reason": "争いの言葉を一度止め、法論へ離す",
        "section": "和みて法を論ず",
        "category": "speech",
    },
    "MN32-P11": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正定"],
        "reason": "一つの行為に正念を置き、不取著へ離す",
        "section": "正念·心を御す",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN32-P01": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-nidana",
        "text": "此牛角娑羅林甚可愛樂，夜有明月，諸娑羅樹皆敷妙香……。何等比丘起發牛角娑羅林？",
        "satLocus": "大正蔵 T1.727a 牛角娑羅林",
        "note": "起發＝林を荘厳·輝かせる比丘とは誰か。",
    },
    "MN32-P02": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-revata",
        "text": "（離越哆の答え——独住·定に親しむ比丘が起発する。パーリ: enjoys retreat, absorption。）",
        "satLocus": "大正蔵 T1.727–728 牛角娑羅林",
        "note": "独住·禅定の器としての林。",
    },
    "MN32-P03": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-kassapa",
        "text": "自有知足稱說知足，自樂在遠離獨住稱說樂在遠離獨住，自修行精勤……。",
        "satLocus": "大正蔵 T1.727c 牛角娑羅林",
        "note": "迦葉系＝知足·遠離·精勤（パーリは乞食·糞掃衣等も明示）。",
    },
    "MN32-P04": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-moggallana",
        "text": (
            "（パーリ目連＝二人の法論。"
            "漢訳目連＝大如意足……——段差あり。実践ペアはパーリの法論に合わせる。）"
        ),
        "satLocus": "大正蔵 T1.727c 牛角娑羅林",
        "note": "漢は神足、パーリは法論——注記してパーリに従う。",
    },
    "MN32-P05": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-ananda",
        "text": "若有比丘廣學多聞，守持不忘……初妙、中妙、竟亦妙……欲斷諸結。如是比丘起發牛角娑羅林。",
        "satLocus": "大正蔵 T1.727a 牛角娑羅林",
        "note": "阿難＝多聞。",
    },
    "MN32-P06": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-buddha",
        "text": "不解結跏趺坐乃至漏盡，彼便不解結跏趺坐乃至漏盡。舍梨子！如是比丘起發牛角娑羅林。",
        "satLocus": "大正蔵 T1.729b 牛角娑羅林",
        "note": "世尊＝漏尽まで坐を解かない（パーリは不取著による解脱）。",
    },
    "MN32-P07": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-dukkha",
        "text": "不解結跏趺坐乃至漏盡……。如是比丘起發牛角娑羅林。",
        "satLocus": "大正蔵 T1.729b 牛角娑羅林",
        "note": "取著·漏が残れば起発の終極に至らない。",
    },
    "MN32-P08": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-night",
        "text": "此牛角娑羅林甚可愛樂，夜有明月……不解結跏趺坐乃至漏盡。",
        "satLocus": "大正蔵 T1.727a·729b 牛角娑羅林",
        "note": "夜の林と漏尽の決意。",
    },
    "MN32-P09": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-each",
        "text": "善哉！善哉！……實如阿難比丘所說。……（各尊者ごと「如其所說」と歎ず。）",
        "satLocus": "大正蔵 T1.728b 牛角娑羅林",
        "note": "各自の答えを善しとする。",
    },
    "MN32-P10": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-discuss",
        "text": "我及諸尊已各自說隨其所知。（パーリ目連の法論と、和みて各自述べる流れ。）",
        "satLocus": "大正蔵 T1.727c 牛角娑羅林",
        "note": "各自說隨所知——争わず述べる。",
    },
    "MN32-P11": {
        "status": "mapped",
        "pin": "中阿含184・牛角娑羅林（T26）",
        "t26": "T26-184-sati",
        "text": (
            "若有比丘隨用心自在而不隨心……。"
            "不解結跏趺坐乃至漏盡。"
        ),
        "satLocus": "大正蔵 T1.728a·729b 牛角娑羅林",
        "note": "舎利弗＝心自在。世尊＝正念·漏尽。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部32経と中阿含184牛角娑羅林の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn032.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN32-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 32",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・牛角林の大経／パーリMN32）",
                    "locus": f"中部・牛角林の大経（MN32）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 牛角林大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第32経・牛角林大経（牛角林の大経）"
    SHORT = "牛角林大経（牛角林の大経）"
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
            "pathLabel": "起発の心·法·法友に触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の起発の一歩を変える",
            "toNext": "触のあと、静けさ·食事の受が見える",
            "todayObserve": OBSERVE["MN32-P01"],
            "todayAction": actions["MN32-P01"],
            "when": ["起発の心を決めた", "法を学んだ", "法友と語った"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN32-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN32-P05"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正命"], "pathFactorIds": ["mindfulness", "livelihood"],
            "pathLabel": "静けさと食事の受を修行の器·助けとして味わう",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、環境·食事の受が立つ",
            "toNext": "受に乗ると自分の見だけ通す欲しがりへ",
            "todayObserve": OBSERVE["MN32-P02"],
            "todayAction": actions["MN32-P02"],
            "when": ["静けさを味わった", "食事を確かめた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN32-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN32-P03"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正語"], "pathFactorIds": ["intention", "speech"],
            "pathLabel": "自分の見だけ通す欲しがりを抑え、他も聴く",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、自説への欲しがりが立つ",
            "toNext": "止めないと取著の掴みへ",
            "todayObserve": OBSERVE["MN32-P09"],
            "todayAction": actions["MN32-P09"],
            "when": ["他者の見も聴いた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN32-P09"][:40] + "…",
            "secondaryObserve": "各自よく語った",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "内の取著の掴みを一つ手放す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、心配·反芻の掴みが手前",
            "toNext": "掴むと取著の苦が見える",
            "todayObserve": OBSERVE["MN32-P06"],
            "todayAction": actions["MN32-P06"],
            "when": ["取著を一つ手放した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN32-P06"][:40] + "…",
            "secondaryObserve": "不取著·漏尽",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "苦を取著の結果と一度見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、取著の苦が見える",
            "toNext": "見れば、争いの語を止め正念へ離す",
            "todayObserve": OBSERVE["MN32-P07"],
            "todayAction": actions["MN32-P07"],
            "when": ["取著の結果と見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN32-P07"][:40] + "…",
            "secondaryObserve": "取著あれば起発せず",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "mindfulness", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正語"], "pathFactorIds": ["mindfulness", "speech"],
            "pathLabel": "争いの語を止め、正念で不取著へ離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、語を止め正念に離す",
            "toNext": "離せば、夜の手放しの見直しへ",
            "todayObserve": OBSERVE["MN32-P11"],
            "todayAction": actions["MN32-P11"],
            "when": ["正念·正知を置いた", "争いの語を止めた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN32-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN32-P10"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "今日の取著を認め、手放して眠る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの起発の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN32-P08"],
            "todayAction": actions["MN32-P08"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN32-P08"][:40] + "…",
            "secondaryObserve": "夜月明の林",
        },
    ]

    out = {
        "chapter": 32,
        "sutta": 32,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：牛角林の大経）",
        "suttas": ["MN 32 牛角林大経（牛角林の大経）"],
        "source": {
            "primary": "パーリ・中部第32経（牛角林大経／牛角林の大経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN32（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含184牛角娑羅林（T26）。"
                "何等の比丘が林を起発するか——多聞·独住·天眼·頭陀·法論·心自在、"
                "世尊は不取著による漏尽まで坐を解かない比丘と答える。"
                "（目連の答えはパーリ＝法論、漢＝神足で段差あり。）"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・牛角林の大経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・牛角娑羅林（T1.726c）",
                    "url": SAT_URL,
                    "note": "起發·多聞·天眼·知足·心自在·漏尽。對照表: 法雨道場（中阿含184）",
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
            "focusReason": "牛角林大経は各自の徳を認めつつ、終極は不取著による漏尽まで坐を解かない比丘が林を起発すると説く。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn032.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 32:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(32, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN32-P{i:02d}" for i, p in enumerate(pairs, 1))
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
