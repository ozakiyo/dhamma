#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn014.json (苦蘊小経／小なる苦しみの範疇の経) to match MN1–13 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0586"
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
    "MN14-P01": (
        "マハー・ナーマよ、五つのものがあります。これらの欲望の属性です。"
        "眼によって識知されるべき諸々の色形で……身によって識知されるべき諸々の感触で……貪るべきものです。"
        "……これらの五つの欲望の属性を縁として生起する、安楽であり、悦意であるなら、これは、諸々の欲望の悦楽です。"
    ),
    "MN14-P02": (
        "『諸々の欲望〔の対象〕は、悦楽少なきもの、苦痛多きもの、葛藤多きもの、ここにおいて、より一層の危険がある』と、"
        "マハー・ナーマよ、かくのごとく、もし、また、聖なる弟子に、事実のとおりに、正しい智慧によって善く見られたものと成るも、"
        "しかしながら、彼が、まさしく、諸々の欲望〔の対象〕より他の……喜悦と安楽に到達しないなら……誘引なくある者と成りません。"
    ),
    "MN14-P03": (
        "〔世の人々は〕欲望を因として……母もまた、子と論争し……道友もまた、道友と論争します。"
        "彼らは、そこにおいて、紛争と口論と論争を惹起し、互いに他を……攻撃します。"
        "彼らは、そこにおいて、死にもまた遭遇し、死ぬほどの苦しみにもまた〔遭遇します〕。"
    ),
    "MN14-P04": (
        "彼は、それらの財物の守護を事因とする、苦痛と失意を得知します。"
        "『どのようにすると、わたしの諸々の財物を……火が焼かず……』と。"
        "……あるいは、火が焼き……彼は、憂い悲しみ……等しき迷妄を惹起します。"
    ),
    "MN14-P05": (
        "身体による悪しき行ないを行なって……身体の破壊ののち、死後において、悪所に、悪趣に、堕所に、地獄に、再生します。"
        "マハー・ナーマよ、これもまた、諸々の欲望の危険です。未来のものであり、苦しみの範疇であり……。"
    ),
    "MN14-P06": (
        "欲望を因として……王たちもまた、王たちと論争し……。"
        "……〔家の〕境目をもまた断ち切り……王たちは捕捉して、様々な種類の行罰刑を執行します。"
        "……ラーフの口の刑をもまた為し、火鬘の刑をもまた為し……。"
    ),
    "MN14-P07": (
        "しかしながら、すなわち、まさに、聖なる弟子に、『諸々の欲望〔の対象〕は、悦楽少なきもの、苦痛多きもの……』と……善く見られたものと成り、"
        "そして、彼が、まさしく、諸々の欲望〔の対象〕より他の、諸々の善ならざる法（性質）より他の、喜悦と安楽に到達することから、"
        "あるいは、それより他の、より寂静なるものに〔到達することから〕、そこで、まさに、彼は、諸々の欲望〔の対象〕にたいし誘引なくある者と成ります。"
    ),
    "MN14-P08": (
        "たしかに、尊者たちによって、ニガンタたちによって、無理やり、審慮なき言葉が語られました。"
        "……『たしかに、わたしたちによって、無理やり、審慮なき言葉が語られました……』と。"
        "……しかしながら、また、このことは、さておくとしましょう。今やまた、わたしたちは、尊者ゴータマに尋ねます……。"
    ),
    "MN14-P09": (
        "長夜にわたり、わたしは……了知しています。『貪欲は、心の、付随する〔心の〕汚れである。……』と。"
        "……しかしながら、わたしに、或る時には、諸々の貪欲の法（性質）もまた、心を完全に奪い去って止住し……。"
        "マハー・ナーマよ、まさに、あなたに、まさしく、その法（性質）が、内に〔いまだ〕捨棄されずにあるのです。"
        "……それゆえに、あなたは、家に居住し、諸々の欲望〔の対象〕を遍く受益するのです。"
    ),
    "MN14-P10": (
        "『諸々の欲望〔の対象〕は、悦楽少なきもの、苦痛多きもの、葛藤多きもの、ここにおいて、より一層の危険がある』と……。"
        "……欲望を因として……論争し……戦場に跳入し……火が焼き……ラーフの口の刑をもまた為し……地獄に、再生します。"
    ),
    "MN14-P11": (
        "身体による悪しき行ないを行なって……地獄に、再生します。"
        "……これもまた、諸々の欲望の危険です。未来のものであり、苦しみの範疇であり……。"
        "わたしは、まさに、身体を動かすことなく、言葉を語ることなく……七つの夜と昼のあいだ、一方的な安楽の得知者として〔世に〕住むことができます。"
    ),
}

OBSERVE = {
    "MN14-P01": (
        "五妙欲——眼・耳・鼻・舌・身の好ましく愛しい対象。"
        "朝、今日執着しやすい欲の対象を一つ挙げる。"
    ),
    "MN14-P02": (
        "欲は悦楽少なく、苦痛多く、葛藤多く、ここにより一層の危険がある——"
        "正しい智慧で見ても、より上の喜楽に達するまでは誘引が残る。"
    ),
    "MN14-P03": (
        "欲望を因として、親子・道友まで互いに争う。"
        "欲の対象を、争いを招く肉のように一瞬見る。"
    ),
    "MN14-P04": (
        "財の守護の苦——王・賊・火・水への恐れ。"
        "快楽の裏に、火に焼かれる危険を思い出す。"
    ),
    "MN14-P05": (
        "欲を因とする悪行は、死後に悪趣・地獄へ——"
        "今日の苦を、欲の過害の結果として見る。"
    ),
    "MN14-P06": (
        "欲望から諍い・行罰が生じる——ラーフの口の刑など。"
        "他者との争いの根に欲がないか問う。"
    ),
    "MN14-P07": (
        "欲の危険を見、かつ欲以外の喜悦・安楽（またはより寂静）に達して初めて、欲に誘引なき者と成る。"
        "今日、欲の対象から一度距離を置く。"
    ),
    "MN14-P08": (
        "ニガンタは審慮なき言葉を語った——欲や安楽を語る前に、執着と軽率がないか止まる。"
    ),
    "MN14-P09": (
        "貪瞋痴を知っていても、内に未捨の法があれば心を奪われる——"
        "在家で欲を遍く受益するゆえ。夜に、今日欲に執着した瞬間を一つ認める。"
    ),
    "MN14-P10": (
        "苦蘊小経の核——少味多苦の見、守護・諍い・戦場・火・ラーフ・地獄の危険。"
        "欲の過害を一つ思い出す。"
    ),
    "MN14-P11": (
        "欲の後世の危険は地獄の苦受。"
        "仏は七昼夜の一方的安楽に住しうる——苦行による安楽ではない。"
        "快楽の裏に、この汚れた過害を一瞬思い出す。"
    ),
}

PRACTICE = {
    "MN14-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "今日執着しやすい五妙欲の対象を名づける",
        "section": "五妙欲",
        "category": "mindfulness",
    },
    "MN14-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "少味多苦を智慧で見、より上の喜楽を欠く限り誘引が残ると知る",
        "section": "少味多苦",
        "category": "view",
    },
    "MN14-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "欲望を因とする諍いを見て欲しがりを緩める",
        "section": "諍い·患",
        "category": "intention",
    },
    "MN14-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "財の守護と火焼の恐れに掴みの危険を見る",
        "section": "守護·火",
        "category": "view",
    },
    "MN14-P05": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "欲の過害が悪趣の苦陰になると見る",
        "section": "後世·苦陰",
        "category": "view",
    },
    "MN14-P06": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正業"],
        "reason": "争いとラーフ等の行罰の根に欲を見る",
        "section": "諍·ラーフ",
        "category": "action",
    },
    "MN14-P07": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正見"],
        "reason": "欲以外の喜悦・寂静へ向き、誘引から離れる",
        "section": "誘引なき",
        "category": "concentration",
    },
    "MN14-P08": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正思惟"],
        "reason": "審慮なき語りを止め、執着なく問う",
        "section": "ニガンタ·語",
        "category": "speech",
    },
    "MN14-P09": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "未捨の随煩悩と今日の欲執着を振り返る",
        "section": "マハーナーマ·問",
        "category": "mindfulness",
    },
    "MN14-P10": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "少味多苦と諸患を一つ思い出し出離の入口にする",
        "section": "過害·総",
        "category": "view",
    },
    "MN14-P11": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正定"],
        "reason": "地獄の苦受と対比し、禅の一方的安楽の方向を見る",
        "section": "地獄·安楽",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN14-P01": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-pancakamaguna",
        "text": "有五欲功徳可愛可念歡喜。欲相應而使人樂。……眼知色耳知聲鼻知香舌知味身知觸。……極是欲味無復過是。所患甚多。",
        "satLocus": "大正蔵 T1.586b 苦陰経",
        "note": "五欲功徳＝五妙欲。",
    },
    "MN14-P02": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-appassada",
        "text": "是故當知欲一向無樂無量苦患。多聞聖弟子不見如眞者。彼爲欲所覆。不得捨樂及無上息。……我知欲無樂無量苦患。我知如眞已……便得捨樂及無上息。",
        "satLocus": "大正蔵 T1.586c 苦陰経",
        "note": "欲無楽・多苦患＋捨楽無上息＝少味多苦と上の喜楽。",
    },
    "MN14-P03": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-vivada",
        "text": "因欲縁欲以欲爲本故。母共子諍子共母諍。父子兄弟姐妹親族展轉共諍。……王王共諍……國國共諍。",
        "satLocus": "大正蔵 T1.586b 苦陰経",
        "note": "欲因の諍い。",
    },
    "MN14-P04": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-aggi",
        "text": "我此財物莫令王奪賊劫火燒腐壞亡失。……若使王奪賊劫火燒腐壞亡失。彼便生憂苦愁慼懊惱。",
        "satLocus": "大正蔵 T1.586b 苦陰経",
        "note": "火燒＝守護の患。",
    },
    "MN14-P05": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-niraya",
        "text": "身壞命終。必至惡處生地獄中。摩訶男。是謂後世苦陰因欲縁欲以欲爲本。",
        "satLocus": "大正蔵 T1.586c 苦陰経",
        "note": "後世苦陰。",
    },
    "MN14-P06": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-rahu",
        "text": "母共子諍……展轉共諍。……以種種器仗轉相加害。……或死或怖受極重苦。",
        "satLocus": "大正蔵 T1.586b 苦陰経",
        "note": "諍いの患。パーリのラーフの口の刑は漢訳で刑罰描写に圧縮。",
    },
    "MN14-P07": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-nissarana",
        "text": "我知欲無樂無量苦患。我知如眞已。摩訶男。不爲欲所覆亦不爲惡所纒。便得捨樂及無上息。摩訶男。是故我不因欲退轉。",
        "satLocus": "大正蔵 T1.586c 苦陰経",
        "note": "捨楽・無上息に達し欲に覆われない。",
    },
    "MN14-P08": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-nigantha",
        "text": "汝等癡狂所説無義。所以者何。汝等不善無所曉了而不知時謂汝作是説。",
        "satLocus": "大正蔵 T1.586c–587a 苦陰経",
        "note": "尼揵の無義・不知時の語。",
    },
    "MN14-P09": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-mahanama",
        "text": "我如是知世尊法令我心中得滅三穢。染心穢恚心穢癡心穢……然我心中復生染法恚法癡法。……汝有一法不滅。謂汝住在家。不至信捨家無家學道。",
        "satLocus": "大正蔵 T1.586a–b 苦陰経",
        "note": "摩訶男の問いと在家未捨。",
    },
    "MN14-P10": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-summary",
        "text": "極是欲味無復過是。所患甚多。……現法苦陰因欲縁欲以欲爲本。……後世苦陰因欲縁欲以欲爲本。",
        "satLocus": "大正蔵 T1.586b–c 苦陰経",
        "note": "欲味と甚多の患の総括。",
    },
    "MN14-P11": {
        "status": "mapped",
        "pin": "中阿含100・苦陰経（T26）",
        "t26": "T26-100-sukha",
        "text": "必至惡處生地獄中。……我可得如意靜默無言。因是……七日七夜得歡喜快樂耶。尼揵答曰。如是瞿曇。",
        "satLocus": "大正蔵 T1.586c–587a 苦陰経",
        "note": "地獄の患と七日の歡喜快樂。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部14経と中阿含100苦陰経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn014.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN14-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 14",
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
                    "locus": f"中部・小なる苦しみの範疇の経（MN14）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 苦蘊小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第14経・苦蘊小経（小なる苦しみの範疇の経）"
    SHORT = "苦蘊小経（小なる苦しみの範疇の経）"
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
            "pathLabel": "今日執着しやすい五妙欲の対象を名づける",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の欲の接触を変える",
            "toNext": "触のあと、少味多苦の受が見える",
            "todayObserve": OBSERVE["MN14-P01"],
            "todayAction": actions["MN14-P01"],
            "when": ["好ましい対象に触れた", "在家の欲に触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN14-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN14-P02"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "少味多苦を見、地獄の苦受と禅の安楽を対比する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、悦意と苦痛の両方が見える",
            "toNext": "受に乗ると諍いの欲しがりへ",
            "todayObserve": OBSERVE["MN14-P02"],
            "todayAction": actions["MN14-P02"],
            "when": ["快楽を味わった", "過害を思い出した"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN14-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN14-P11"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "欲望を因とする諍いを見て欲しがりを緩める",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、争う欲しがりが立つ",
            "toNext": "止めないと財の掴みへ",
            "todayObserve": OBSERVE["MN14-P03"],
            "todayAction": actions["MN14-P03"],
            "when": ["欲しがって争った", "肉のように奪い合った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN14-P03"][:40] + "…",
            "secondaryObserve": "因欲縁欲以欲爲本",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "財の守護と火焼の恐れに掴みの危険を見る",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、守護の掴みが手前",
            "toNext": "掴むと後世の苦陰が見える",
            "todayObserve": OBSERVE["MN14-P04"],
            "todayAction": actions["MN14-P04"],
            "when": ["守ろうと固まった", "火焼を恐れた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN14-P04"][:40] + "…",
            "secondaryObserve": "王奪賊劫火燒",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "欲の過害——諍い・ラーフ・地獄の苦陰を認める",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、現法・後世の苦陰が見える",
            "toNext": "見れば、誘引なき出離へ向き直る",
            "todayObserve": OBSERVE["MN14-P05"],
            "todayAction": actions["MN14-P05"],
            "when": ["争いの根に欲を見た", "悪趣を思った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN14-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN14-P06"],
        },
        {
            "id": "release", "weekday": 6, "categoryId": "concentration", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正定", "正見"], "pathFactorIds": ["concentration", "view"],
            "pathLabel": "欲以外の喜悦・寂静へ向き、審慮なく語らない",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、距離を置き上の喜楽へ",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN14-P07"],
            "todayAction": actions["MN14-P07"],
            "when": ["欲から距離を置いた", "審慮なく語りそうになった"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN14-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN14-P08"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "未捨の随煩悩と今日の欲執着を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の欲は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN14-P09"],
            "todayAction": actions["MN14-P09"],
            "when": ["一日を閉じるとき", "貪瞋痴に奪われた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN14-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN14-P10"],
        },
    ]

    out = {
        "chapter": 14,
        "sutta": 14,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：小なる苦しみの範疇の経）",
        "suttas": ["MN 14 苦蘊小経（小なる苦しみの範疇の経）"],
        "source": {
            "primary": "パーリ・中部第14経（苦蘊小経／小なる苦しみの範疇の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含100苦陰経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・小なる苦しみの範疇の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・苦陰経（T1.586a）",
                    "url": SAT_URL,
                    "note": "釈摩訶男問答。對照表: 法雨道場",
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
            "focusReason": "苦蘊小経は欲の少味多苦を見、欲以外の喜悦・寂静に達して誘引なき者と成ることが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn014.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 14:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(14, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN14-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
