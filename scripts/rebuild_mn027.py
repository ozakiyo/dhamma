#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn027.json (象跡喩小経／象跡の喩えの小経) to match MN1–26 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0656c01"
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
    "MN27-P01": (
        "婆羅門よ、象跡の喩えは、まだ詳細に完成されていません。……"
        "熟練した牡象の追跡者は、長大で広大な大きな象の足跡を見ても、"
        "いまだ、『これは、まさに、大きな牡象である』と結論を下しません。"
        "……矮小な牝象……高い牝象……母象……にも大きな足跡があるからです。"
        "……根もとに、あるいは、露地に、歩み·立ち·坐り·横たわっている、その牡象を見るとき、"
        "そこで、『これは、かの大きな牡象である』と結論を下します。"
    ),
    "MN27-P02": (
        "在家者、あるいは、在家の子……が、その法を聞きます。"
        "……『在家の生活は、狭く、塵労の処である。出家は、露わで広大である。"
        "……わたしは、いま、在家にあって、鎖に鎖されている。……"
        "それなら、さあ、わたしは……剃除して袈裟を着け、信をもって家から家なきへ出家しよう』と。"
    ),
    "MN27-P03": (
        "彼は、出家して……禁戒を修習し、別解脱を守護します。"
        "……威儀·礼節を善く摂し、微細な罪をも見て畏怖を懐き、学処を受持します。"
    ),
    "MN27-P04": (
        "……時ならぬ食を捨て……歌舞·音楽·演劇の観覧を遠ざける……。"
        "（聖なる戒聚の一部——享楽·装飾·金銀等から離れる学処。）"
    ),
    "MN27-P05": (
        "彼は、この聖なる戒聚を成就して、さらに、きわめて知足を行じます。"
        "衣は形を覆うために取り、食は躯を充たすために取ります。"
        "……あたかも、また、鷹が、両翼とともに空中を飛翔するように。"
    ),
    "MN27-P06": (
        "……さらに、諸々の根を守護し……正念によって閉塞し……恒に正知を起こします。"
        "もし、眼によって色を見るも、想を受けず、また、色を味わわず……眼根を守護します。"
        "……耳·鼻·舌·身·意についても、また、同様です。"
    ),
    "MN27-P07": (
        "……さらに、出入に正知し……屈伸·低仰……衣鉢を善く著け、"
        "行·住·坐·臥、眠·寤·語·黙、すべてにおいて正知します。"
    ),
    "MN27-P08": (
        "彼は、この五蓋——心の穢れであり、慧を羸弱にするもの——を断じ、"
        "諸々の欲望から離れ、諸々の不善の法から離れ、"
        "有覚·有観、離より生じる喜·楽ある、初禅を成就して遊行します。"
        "婆羅門よ、これが、『如来の足跡』……と説かれます。"
        "しかしながら、聖なる弟子は、いまだ、これをもって結論を下しません。"
    ),
    "MN27-P09": (
        "……第二禅……第三禅……第四禅……。"
        "婆羅門よ、これが、『如来の足跡』……と説かれます。"
        "しかしながら、聖なる弟子は、いまだ、『世尊は正等覚である。"
        "法は善く説かれ、僧伽は善く趣いている』と結論を下しません。"
        "（結論へ向かいつつあるが、いまだ至っていない。）"
    ),
    "MN27-P10": (
        "このように定心が……不動と成ったとき、彼は、宿命智通の証得へ心を向けます。"
        "彼は、多くの種類の過去の生を……特徴と詳細とともに随念します。"
        "婆羅門よ、これもまた、『如来の足跡』……と説かれます。"
        "しかしながら、聖なる弟子は、いまだ、これをもって結論を下しません。"
    ),
    "MN27-P11": (
        "……彼は、有情の死と再生の智へ心を向けます。"
        "……業の差異により、有情が劣った処·勝れた処へ趣くことを、あるがままに見ます。"
        "婆羅門よ、これもまた、『如来の足跡』……と説かれます。"
        "しかしながら、聖なる弟子は、いまだ、これをもって結論を下しません。"
    ),
    "MN27-P12": (
        "……彼は、漏尽智通の証得へ心を向けます。"
        "『これは、諸々の漏である』……『これは、漏の滅尽へ至る道である』と、如実に了知します。"
        "……欲漏……有漏……無明漏から心が解脱します。"
        "……『生は滅尽し、梵行は完成された。為すべきことは為された。〔もはや〕他に、この場へと〔赴くことは〕ない』と了知します。"
        "婆羅門よ、ここで、聖なる弟子は、結論に至ります——"
        "『世尊は正等覚である。法は善く説かれ、僧伽は善く趣いている』と。"
        "……この点において、象跡の喩えは、詳細に完成されました。"
    ),
}

OBSERVE = {
    "MN27-P01": (
        "熟練の象追跡者——大きな足跡だけでは「大きな牡象」と結論しない。実物を見るまで追う——"
        "修行の次の段階に飛びつかず、今の段階を確認する。"
    ),
    "MN27-P02": (
        "在家は狭く塵労——信を得て家から家なきへ。障害を一つ減らす——"
        "在家の中で障害を一つ減らす行いをする。"
    ),
    "MN27-P03": (
        "出家して学処·別解脱を守護し、微細な罪にも畏怖を懐く——"
        "五戒·語四のうち守るべき一つを意識する。"
    ),
    "MN27-P04": (
        "時ならぬ食·歌舞観覧等を遠ざける聖戒——"
        "今日、一つの享楽（SNS·娯楽）を節度する。"
    ),
    "MN27-P05": (
        "衣は覆形、食は充躯——鷹が翼とともに飛ぶように知足——"
        "足りているものに目を向け、欲を一段減らす。"
    ),
    "MN27-P06": (
        "諸根を守護——色を見ても想を味わわず、眼門を護る——"
        "スマホを開く前に「眼の門を護る」と一呼吸置く。"
    ),
    "MN27-P07": (
        "出入·屈伸·飲食·語黙に正知——"
        "食事の最初の三口に、覚知を置く。"
    ),
    "MN27-P08": (
        "五蓋を断じ初禅——如来の足跡だが、いまだ結論しない——"
        "修行を妨げた蓋を一つ名づけ、対治する。"
    ),
    "MN27-P09": (
        "二·三·四禅も足跡——小さな進歩に満足せず、結論を急がない——"
        "小さな進歩に満足せず、次の段階を謙虚に見る。"
    ),
    "MN27-P10": (
        "宿命随念の智——足跡だがいまだ結論ではない。行いが来世の因になりうるか——"
        "今日の行いが「来世の因」になりうるか、静かに問う。"
    ),
    "MN27-P11": (
        "有情の死·再生の智——業の差異をあるがままに見る。身口意は善か不善か——"
        "今日の身口意の行いが、善業か不善業か確かめる。"
    ),
    "MN27-P12": (
        "漏尽——ここで初めて「正等覚·法善説·僧善趣」の結論。未証を知ったと言わない——"
        "未証のことを「知った」と言わない。"
    ),
}

PRACTICE = {
    "MN27-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "足跡に触れても結論を急がず、今の段階を確認する",
        "section": "象跡·結論を急がない",
        "category": "mindfulness",
    },
    "MN27-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正命"],
        "reason": "在家の塵労への欲しがりを減らし、障害を一つ落とす",
        "section": "在家·出家",
        "category": "intention",
    },
    "MN27-P03": {
        "nidanaId": "contact",
        "pathFactors": ["正業", "正念"],
        "reason": "学処に触れ、守るべき戒を一つ意識する",
        "section": "学処·戒",
        "category": "action",
    },
    "MN27-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "享楽への欲しがりを節度する",
        "section": "享楽を遠ざける",
        "category": "intention",
    },
    "MN27-P05": {
        "nidanaId": "feeling",
        "pathFactors": ["正命", "正念"],
        "reason": "足りている衣食の受に知足し、欲を一段減らす",
        "section": "知足",
        "category": "livelihood",
    },
    "MN27-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正念", "正思惟"],
        "reason": "眼門への掴みを護り、相を味わわない",
        "section": "根の守護",
        "category": "mindfulness",
    },
    "MN27-P07": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "飲食の受に正知を置く",
        "section": "正知",
        "category": "mindfulness",
    },
    "MN27-P08": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正精進"],
        "reason": "五蓋を名づけ対治し、初禅の足跡へ離す",
        "section": "五蓋·初禅",
        "category": "concentration",
    },
    "MN27-P09": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "禅定の進歩を足跡として見直し、結論を急がない",
        "section": "禅定·いまだ結論せず",
        "category": "view",
    },
    "MN27-P10": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "行いが苦の因になりうるかを宿命の視点で見る",
        "section": "宿命智",
        "category": "view",
    },
    "MN27-P11": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正業"],
        "reason": "身口意の業が趣の苦·楽を分けると見る",
        "section": "死生智",
        "category": "view",
    },
    "MN27-P12": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "漏尽の結論まで未証を知ったと言わず見直す",
        "section": "漏尽·結論の完成",
        "category": "view",
    },
}

CHINESE = {
    "MN27-P01": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-tracker",
        "text": (
            "卑盧異學說象跡喻，猶不善作，亦不具足……。"
            "譬善象師……見大象跡……或不信……及見彼象……便作是念：『若有此跡，必是大象。』"
        ),
        "satLocus": "大正蔵 T1.656c 象跡喻経",
        "note": "不善作不具足＝まだ詳細に完成されていない。",
    },
    "MN27-P02": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-pabbajja",
        "text": "在家至狹，塵勞之處，出家學道，發露曠大。……至信、捨家、無家、學道。",
        "satLocus": "大正蔵 T1.656c–657a 象跡喻経",
        "note": "在家至狭·出家曠大。",
    },
    "MN27-P03": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-sila",
        "text": "出家已……修習禁戒，守護從解脫。……見纖芥罪，常懷畏怖，受持學戒。",
        "satLocus": "大正蔵 T1.657a 象跡喻経",
        "note": "禁戒·從解脱＝学処·別解脱。",
    },
    "MN27-P04": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-restraint",
        "text": "（聖戒聚の中に、非時食·観聴等を離れる学処が含まれる。）",
        "satLocus": "大正蔵 T1.657a–b 象跡喻経",
        "note": "享楽を遠ざける戒支。",
    },
    "MN27-P05": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-santutthi",
        "text": "復行極知足，衣取覆形，食取充軀……猶如鷹鳥，與兩翅俱，飛翔空中。",
        "satLocus": "大正蔵 T1.657b 象跡喻経",
        "note": "極知足·鷹鳥の喩。",
    },
    "MN27-P06": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-indriya",
        "text": "復守護諸根……若眼見色，然不受想，亦不味色……守護眼根。",
        "satLocus": "大正蔵 T1.657b 象跡喻経",
        "note": "守護諸根。",
    },
    "MN27-P07": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-sampajanna",
        "text": "復正知出入……行住坐臥，眠寤語默，皆正知之。",
        "satLocus": "大正蔵 T1.657c 象跡喻経",
        "note": "正知出入。",
    },
    "MN27-P08": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-jhana",
        "text": (
            "彼斷此五蓋、心穢、慧羸，離欲、離惡不善之法……逮初禪成就遊。"
            "是謂如來所屈……然彼不以此為訖……。"
        ),
        "satLocus": "大正蔵 T1.657c 象跡喻経",
        "note": "五蓋·初禅·不以此為訖。",
    },
    "MN27-P09": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-not-yet",
        "text": "逮第二禪……第三……第四……。然彼不以此為訖，世尊……等正覺……聖眾善趣。",
        "satLocus": "大正蔵 T1.657c–658a 象跡喻経",
        "note": "不以此為訖＝いまだ結論せず。",
    },
    "MN27-P10": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-pubbe",
        "text": "（定心清淨已，趣向宿命智通——漢訳も三明の流れで説く。）",
        "satLocus": "大正蔵 T1.658a 象跡喻経",
        "note": "宿命智＝如来所屈の一だが未だ訖に非ず。",
    },
    "MN27-P11": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-cutupapata",
        "text": "（趣向生死智——業により趣くを如実に見る。）",
        "satLocus": "大正蔵 T1.658a 象跡喻経",
        "note": "死生智。",
    },
    "MN27-P12": {
        "status": "mapped",
        "pin": "中阿含146・象跡喻経（T26）",
        "t26": "T26-146-asava",
        "text": (
            "趣向漏盡智通作證……解脫已，便知解脫，生已盡，梵行已立，所作已辦，不更受有，知如真。"
            "彼以此為訖，世尊……等正覺，世尊所說法善，如來弟子聖眾善趣。"
        ),
        "satLocus": "大正蔵 T1.658a 象跡喻経",
        "note": "以此為訖＝ここで結論が完成。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部27経と中阿含146象跡喻経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn027.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 13):
        pid = f"MN27-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 27",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・象跡の喩えの小経／パーリMN27）",
                    "locus": f"中部・象跡の喩えの小経（MN27）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 象跡喩小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第27経・象跡喩小経（象跡の喩えの小経）"
    SHORT = "象跡喩小経（象跡の喩えの小経）"
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
            "pathLabel": "足跡に触れても結論を急がず、学処を意識する",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の段階確認を変える",
            "toNext": "触のあと、衣食·飲食の受が見える",
            "todayObserve": OBSERVE["MN27-P01"],
            "todayAction": actions["MN27-P01"],
            "when": ["段階を確認した", "戒を意識した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN27-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN27-P03"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正命"], "pathFactorIds": ["mindfulness", "livelihood"],
            "pathLabel": "知足と飲食の正知で受を見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、足りる·味わう受が立つ",
            "toNext": "受に乗ると享楽·在家の欲しがりへ",
            "todayObserve": OBSERVE["MN27-P05"],
            "todayAction": actions["MN27-P05"],
            "when": ["足りていると見た", "食事に正知した"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN27-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN27-P07"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "在家の塵労と享楽への欲しがりを減らす",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、障害·娯楽への欲しがりが立つ",
            "toNext": "止めないと眼門の掴みへ",
            "todayObserve": OBSERVE["MN27-P02"],
            "todayAction": actions["MN27-P02"],
            "when": ["障害を一つ減らした", "享楽を節度した"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN27-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN27-P04"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "眼門への掴みを護り、相を味わわない",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、色·相の掴みが手前",
            "toNext": "掴むと業の苦が見える",
            "todayObserve": OBSERVE["MN27-P06"],
            "todayAction": actions["MN27-P06"],
            "when": ["スマホを開く前", "眼門を護った"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN27-P06"][:40] + "…",
            "secondaryObserve": "守護眼根",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正業"], "pathFactorIds": ["view", "action"],
            "pathLabel": "行い·業が苦の趣を分けると見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、業の患が見える",
            "toNext": "見れば、五蓋の対治と定へ",
            "todayObserve": OBSERVE["MN27-P11"],
            "todayAction": actions["MN27-P11"],
            "when": ["善不善を確かめた", "来世の因を問うた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN27-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN27-P10"],
        },
        {
            "id": "release", "weekday": 6, "categoryId": "concentration", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正定", "正精進"], "pathFactorIds": ["concentration", "effort"],
            "pathLabel": "五蓋を対治し、如来の足跡としての定へ離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、蓋を名づけて離す",
            "toNext": "離せば、結論を急がない見直しへ",
            "todayObserve": OBSERVE["MN27-P08"],
            "todayAction": actions["MN27-P08"],
            "when": ["蓋を名づけた", "定に向かった"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN27-P08"][:40] + "…",
            "secondaryObserve": "如來所屈",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "進歩を足跡として見直し、漏尽まで結論を急がない",
            "chapterHint": SHORT,
            "fromPrev": "一日の段階は、朝からの追跡の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN27-P09"],
            "todayAction": actions["MN27-P09"],
            "when": ["一日を閉じるとき", "未証を言わなかった夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN27-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN27-P12"],
        },
    ]

    out = {
        "chapter": 27,
        "sutta": 27,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：象跡の喩えの小経）",
        "suttas": ["MN 27 象跡喩小経（象跡の喩えの小経）"],
        "source": {
            "primary": "パーリ・中部第27経（象跡喩小経／象跡の喩えの小経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN27（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含146象跡喻経（T26）。"
                "足跡だけでは結論せず、漏尽で初めて「正等覚·法善説·僧善趣」と結論する。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・象跡の喩えの小経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・象跡喻経（T1.656c）",
                    "url": SAT_URL,
                    "note": "善象師·在家出家·戒·知足·根·禅·漏尽。對照表: 法雨道場",
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
            "focusNodeId": "review",
            "focusReason": "象跡喩小経は足跡だけでは結論せず、漏尽で初めて結論するのが主題。既定の焦点は見直す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn027.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 27:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(27, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 12
    assert all(p["id"] == f"MN27-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/12; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
