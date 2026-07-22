#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn002.json (一切漏経) to match MN1 / dhammapada source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0431"
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
    "MN2-P01": (
        "比丘たちよ、わたしは、〔あるがままに〕知っている者に、〔あるがままに〕見ている者に、"
        "諸々の煩悩の滅尽を説きます──〔あるがままに〕知っていない者に、ではなく、〔あるがままに〕見ていない者に、ではなく。"
    ),
    "MN2-P02": (
        "比丘たちよ、根源のままならずに意を為していると、まさしく、そして、諸々の〔いまだ〕生起していない煩悩が生起し、"
        "さらに、諸々の〔すでに〕生起した煩悩が増大します。"
    ),
    "MN2-P03": (
        "しかしながら、まさに、根源のままに意を為していると、まさしく、そして、諸々の〔いまだ〕生起していない煩悩は生起せず、"
        "さらに、諸々の〔すでに〕生起した煩悩は捨棄されます。"
    ),
    "MN2-P04": (
        "比丘たちよ、見〔の観点〕から捨棄されるべき諸々の煩悩が存在し、統御〔の観点〕から捨棄されるべき諸々の煩悩が存在し、"
        "受用〔の観点〕から捨棄されるべき諸々の煩悩が存在し、耐え忍ぶ〔観点〕から捨棄されるべき諸々の煩悩が存在し、"
        "遍く避ける〔観点〕から捨棄されるべき諸々の煩悩が存在し、除去〔の観点〕から捨棄されるべき諸々の煩悩が存在し、"
        "修行〔の観点〕から捨棄されるべき諸々の煩悩が存在します。"
    ),
    "MN2-P05": (
        "彼が、このように、根源のままならずに意を為していると、六つの見解のなかのどれか一つの見解が生起します。"
        "あるいは、『わたしの自己は存在する』と……あるいは、『わたしの自己は存在しない』と……"
        "『すなわち、わたしのこの自己は……常住であり、常恒であり……止住するであろう』と。"
    ),
    "MN2-P06": (
        "比丘たちよ、見解の束縛によって束縛された無聞の凡夫は、生から、老から、死から、諸々の憂いから、諸々の嘆きから、"
        "諸々の苦痛から、諸々の失意から、諸々の葛藤から、完全に解き放たれません。"
        "『〔彼は〕苦しみから完全に解き放たれない』と、〔わたしは〕説きます。"
    ),
    "MN2-P07": (
        "比丘たちよ、ここに、比丘が、根源のままに審慮して〔そののち〕、眼の機能（眼根）における統御によって統御された者として〔世に〕住みます。"
        "……眼の機能における統御によって統御されていない者として〔世に〕住んでいると、諸々の煩悩が〔生起し〕、諸々の悩苦と苦悶が生起するでしょうが、"
        "このように、彼が……統御された者として〔世に〕住んでいると、諸々の煩悩も、諸々の悩苦と苦悶も、それらは有りません。"
    ),
    "MN2-P08": (
        "根源のままに審慮して〔そののち〕、〔行乞の〕施食を受用します──まさしく、戯れのためではなく、驕りのためではなく、"
        "装うことのためではなく、飾ることのためではなく、この身体の、止住のために、存続のために、悩害の止息のために、"
        "梵行（禁欲清浄行）の資助のために、まさしく、そのかぎりにおいて。"
    ),
    "MN2-P09": (
        "比丘たちよ、ここに、比丘が、根源のままに審慮して〔そののち〕、生起した欲望の思考を甘受せず、捨棄し、除去し、"
        "終息を為し、状態なきへと至らしめます。……生起した憎悪の思考を……生起した悩害の思考を……"
        "生起した諸々の悪しき善ならざる法（性質）を甘受せず、捨棄し、除去し、終息を為し、状態なきへと至らしめます。"
    ),
    "MN2-P10": (
        "比丘たちよ、ここに、比丘が、根源のままに審慮して〔そののち〕、遠離に依拠し、離貪に依拠し、止滅に依拠し、"
        "放棄に向かわせるものである、気づきという正覚の支分（念覚支）を修めます。……択法覚支……精進覚支……喜覚支……"
        "軽安覚支……定覚支……放捨という正覚の支分（捨覚支）を修めます。"
    ),
    "MN2-P11": (
        "有聞の聖なる弟子は……諸々の意を為すべき法（性質）を覚知し、諸々の意を為すべきではない法（性質）を覚知します。"
        "彼は……それらが、諸々の意を為すべきではない法（性質）であるなら、それらの法（性質）に意を為さず、"
        "それらが、諸々の意を為すべき法（性質）であるなら、それらの法（性質）に意を為します。"
    ),
    "MN2-P12": (
        "彼は、『これは、苦しみである』と、根源のままに意を為し、『これは、苦しみの集起である』と、根源のままに意を為し、"
        "『これは、苦しみの止滅である』と、根源のままに意を為し、『これは、苦しみの止滅に至る〔実践の〕道である』と、根源のままに意を為します。"
        "彼が、このように、根源のままに意を為していると、三つの束縛するもの（三結）が捨棄されます──"
        "身体を有するという見解（有身見）が、疑惑〔の思い〕（疑）が、戒や掟への偏執（戒禁取）が。"
    ),
}

OBSERVE = {
    "MN2-P01": (
        "わたしは、ありのままに知り・見る者に諸漏の尽きを説く。"
        "知らぬ者・見ぬ者にではない。"
    ),
    "MN2-P02": (
        "根源のままならずに意を向けると、まだ生じていない煩悩が生じ、すでに生じた煩悩が増す。"
    ),
    "MN2-P03": (
        "根源のままに意を向けると、まだ生じていない煩悩は生じず、すでに生じた煩悩は捨てられる。"
    ),
    "MN2-P04": (
        "煩悩は七つの門から捨てられる──見・統御（護）・受用・忍・避・除・修習。"
    ),
    "MN2-P05": (
        "不正な作意から、六つの見のいずれかが起きる。"
        "『わたしの自己はある／ない』『この自己は常住だ』などと取り違える。"
    ),
    "MN2-P06": (
        "見解の束縛に縛られた無聞の凡夫は、生・老・死・憂悲苦悩から完全には解き放たれない。"
    ),
    "MN2-P07": (
        "眼などの門を護らねば、煩悩・悩苦・苦悶が起きる。"
        "護れば、それらは生じない。"
    ),
    "MN2-P08": (
        "衣・食・臥具・薬を、驕りや飾りのためではなく、身体の維持・梵行の資助のために正しく受ける。"
    ),
    "MN2-P09": (
        "すでに生じた欲の思考・憎悪・害意を甘受せず、捨て、除き、終息させる。"
    ),
    "MN2-P10": (
        "七つの覚支（念・択法・精進・喜・軽安・定・捨）を、離・離貪・滅尽・放棄に向かうよう修める。"
    ),
    "MN2-P11": (
        "聖なる弟子は、意を向けるべき法に意を向け、向けるべきでない法には意を向けない。"
    ),
    "MN2-P12": (
        "『これは苦・集・滅・道である』と根源のままに意を向ければ、有身見・疑・戒禁取の三結が捨てられる。"
    ),
}

PRACTICE = {
    "MN2-P01": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正念"],
        "reason": "知と見によって漏を捨てる入口",
        "section": "導",
        "category": "view",
    },
    "MN2-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "非如理作意が漏を生じ増やす",
        "section": "作意·非如理",
        "category": "intention",
    },
    "MN2-P03": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正念"],
        "reason": "如理作意が漏を生じさせず捨てる",
        "section": "作意·如理",
        "category": "intention",
    },
    "MN2-P04": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "七門から漏を捨てる全体像",
        "section": "七法",
        "category": "effort",
    },
    "MN2-P05": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "六見・自己見として掴む",
        "section": "見·六見",
        "category": "view",
    },
    "MN2-P06": {
        "nidanaId": "suffering",
        "pathFactors": ["正見"],
        "reason": "見解の束縛が苦から解けない",
        "section": "見·結縛",
        "category": "view",
    },
    "MN2-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正精進"],
        "reason": "根門の接触を護って漏を防ぐ",
        "section": "護",
        "category": "mindfulness",
    },
    "MN2-P08": {
        "nidanaId": "feeling",
        "pathFactors": ["正命", "正念"],
        "reason": "四事の受用を正しくして漏を防ぐ",
        "section": "用",
        "category": "livelihood",
    },
    "MN2-P09": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "生じた不善尋を除遣して離す",
        "section": "除",
        "category": "effort",
    },
    "MN2-P10": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正精進"],
        "reason": "七覚支の修習で漏を捨てる",
        "section": "修習",
        "category": "concentration",
    },
    "MN2-P11": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "応作意と不応作意を弁える",
        "section": "聖弟子",
        "category": "mindfulness",
    },
    "MN2-P12": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正念"],
        "reason": "四諦の如理作意で三結を捨てる",
        "section": "四諦",
        "category": "view",
    },
}

CHINESE = {
    "MN2-P01": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-open",
        "text": "以知以見故諸漏得盡。非不知非不見也。",
        "satLocus": "大正蔵 T1.431c 漏盡経第十",
        "note": "パーリ『知と見によって漏尽』に直対応。場は漢訳が拘楼（パーリは舎衛）。",
    },
    "MN2-P02": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-ayoniso",
        "text": "若不正思惟者。未生欲漏而生。已生便増廣。未生有漏無明漏而生。已生便増廣。",
        "satLocus": "大正蔵 T1.431c–432a 漏盡経",
        "note": "不正思惟＝非如理作意。",
    },
    "MN2-P03": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-yoniso",
        "text": "若正思惟者。未生欲漏而不生。已生便滅。未生有漏無明漏而不生。已生便滅。",
        "satLocus": "大正蔵 T1.431c–432a 漏盡経",
        "note": "正思惟＝如理作意。",
    },
    "MN2-P04": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-seven",
        "text": "有七斷漏煩惱憂慼法。云何爲七。有漏從見斷。有漏從護斷。有漏從離斷。有漏從用斷。有漏從忍斷。有漏從除斷。有漏從思惟斷。",
        "satLocus": "大正蔵 T1.432a 漏盡経",
        "note": "七門の順序は漢訳で離／用がパーリ（用・忍・避）とやや異なる。内容対応。",
    },
    "MN2-P05": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-sixviews",
        "text": "彼作如是不正思惟。於六見中。隨其見生而生眞有神。此見生而生眞無神。……是謂見之弊。爲見所動見結所繋。",
        "satLocus": "大正蔵 T1.432a 漏盡経",
        "note": "六見・神我見。",
    },
    "MN2-P06": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-dukkha",
        "text": "凡夫愚人以是之故。便受生老病死苦也。",
        "satLocus": "大正蔵 T1.432a 漏盡経",
        "note": "見結に繋がれて苦を受ける＝パーリの見解の束縛。",
    },
    "MN2-P07": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-guard",
        "text": "比丘。眼見色護眼根者。……若不護者。則生煩惱憂慼。護則不生煩惱憂慼。",
        "satLocus": "大正蔵 T1.432a–b 漏盡経",
        "note": "護斷＝統御（根門）。",
    },
    "MN2-P08": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-use",
        "text": "若用飮食。非爲利故。非以貢高故。非爲肥悦故。但爲令身久住除煩惱憂慼故。以行梵行故。",
        "satLocus": "大正蔵 T1.432b 漏盡経",
        "note": "用斷＝受用。衣食臥具湯薬。",
    },
    "MN2-P09": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-remove",
        "text": "比丘。生欲念不除斷捨離。生恚念害念不除斷捨離。若不除者則生煩惱憂慼。除則不生煩惱憂慼。",
        "satLocus": "大正蔵 T1.432b–c 漏盡経",
        "note": "除斷＝除去。",
    },
    "MN2-P10": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-bhavana",
        "text": "比丘。思惟初念覺支。依離依無欲依於滅盡。起至出要。……思惟第七捨覺支。依離依無欲依於滅盡。趣至出要。",
        "satLocus": "大正蔵 T1.432c 漏盡経",
        "note": "思惟斷＝修行（七覚支）。漢訳は『思惟』と表記。",
    },
    "MN2-P11": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-disciple",
        "text": "多聞聖弟子……知如眞法已。不應念法不念。應念法便念。",
        "satLocus": "大正蔵 T1.432a 漏盡経",
        "note": "応念／不応念＝応作意／不応作意。",
    },
    "MN2-P12": {
        "status": "mapped",
        "pin": "中阿含10・漏盡経（T26）",
        "t26": "T26-010-sacca",
        "text": "知苦如眞。知苦習知苦滅知苦滅道如眞。如是知如眞已則三結盡。身見戒取疑三結盡已。",
        "satLocus": "大正蔵 T1.432a 漏盡経",
        "note": "四諦如実知で三結尽。パーリの如理作意四諦と対応。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部2経と中阿含10漏盡経の内容対応（對照表: 法雨道場）。七門の順序はずれうる。",
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

    # expand scope tag
    scope = psi.get("scope", "")
    tag = f"majjhima-mn{sutta_id}"
    if tag not in scope:
        if "majjhima-mn" in scope:
            # replace trailing mnN or append
            if "+majjhima-mn" in scope:
                base = scope.split("+majjhima-")[0]
                # collect existing mn numbers from entries
                mns = set()
                for entries in psi["entries"].values():
                    for e in entries:
                        if e.get("collectionId") == "majjhima":
                            mns.add(e["chapterId"])
                mns.add(sutta_id)
                mn_part = "+".join(f"mn{n}" for n in sorted(mns))
                psi["scope"] = f"{base}+majjhima-{mn_part}"
            else:
                psi["scope"] = f"{scope}+{tag}"
        else:
            psi["scope"] = f"{scope}+{tag}" if scope else tag
    else:
        # recompute clean scope
        mns = set()
        for entries in psi["entries"].values():
            for e in entries:
                if e.get("collectionId") == "majjhima":
                    mns.add(e["chapterId"])
        base = "dhammapada-ch1-ch26"
        mn_part = "+".join(f"mn{n}" for n in sorted(mns))
        psi["scope"] = f"{base}+majjhima-{mn_part}"

    psi_path.write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return psi["scope"]


def main():
    old_path = DATA / "majjhima" / "mn002.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES)

    pairs = []
    for i in range(1, 13):
        pid = f"MN2-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 2",
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
                    "locus": f"中部・一切の煩悩の経（MN2）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 一切漏経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第2経・一切漏経（一切の煩悩の経）"
    SHORT = "一切漏経（一切の煩悩の経）"
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
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "根門の接触を護り、漏の入口を塞ぐ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の根門の護りになる",
            "toNext": "護らねば受と不正作意が立ち上がる",
            "todayObserve": OBSERVE["MN2-P07"],
            "todayAction": actions["MN2-P07"],
            "when": ["画面を開く前", "音や声に触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN2-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN2-P01"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "livelihood", "nidanaLabel": "受ける",
            "pathFactors": ["正命", "正念"], "pathFactorIds": ["livelihood", "mindfulness"],
            "pathLabel": "衣食などの受を正しく受け、漏を増やさない",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、空腹・寒暑・快不快の受が来る",
            "toNext": "受け方を誤ると欲しがり・不正作意へ",
            "todayObserve": OBSERVE["MN2-P08"],
            "todayAction": actions["MN2-P08"],
            "when": ["食事の前", "道具を使うとき"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN2-P08"][:40] + "…",
            "secondaryObserve": "肥悦・虚飾のためではなく梵行の助けとして",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "不正作意を名づけ、漏の増殖に乗らない",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、非如理の意が漏を増やす",
            "toNext": "止めないと六見・自己見の掴みへ",
            "todayObserve": OBSERVE["MN2-P02"],
            "todayAction": actions["MN2-P02"],
            "when": ["反芻が始まった", "未来の心配が膨らんだ"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN2-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN2-P03"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "六見・『わたしの自己』を掴まず離す",
            "chapterHint": SHORT,
            "fromPrev": "不正作意が、自己見として掴む手前",
            "toNext": "掴むと生老病死の苦が見える",
            "todayObserve": OBSERVE["MN2-P05"],
            "todayAction": actions["MN2-P05"],
            "when": ["過去の私を追った", "自己を固定したくなった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN2-P05"][:40] + "…",
            "secondaryObserve": "常住の自己見は見の捕捉",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見"], "pathFactorIds": ["view"],
            "pathLabel": "見解の束縛が苦から解けないと見る",
            "chapterHint": SHORT,
            "fromPrev": "見に縛られた結果として、憂悲苦悩が続く",
            "toNext": "見れば、如理作意と七門の実践へ向き直る",
            "todayObserve": OBSERVE["MN2-P06"],
            "todayAction": actions["MN2-P06"],
            "when": ["見に縛られて重い", "形式だけに固まった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN2-P06"][:40] + "…",
            "secondaryObserve": "見結所繋の凡夫は苦際を得ない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "知見・如理・七門・四諦で漏を捨てる",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、漏を捨てる実践へ向き直る",
            "toNext": "捨てれば、応作意の見直しへつながる",
            "todayObserve": OBSERVE["MN2-P01"],
            "todayAction": actions["MN2-P01"],
            "when": ["知ったか推測かを分ける", "不善尋を除く"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN2-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN2-P12"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "今日の応作意と不応作意を見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の作意は、漏が増えたか減ったかの跡",
            "toNext": "見直しが、翌朝の根門の護りになる",
            "todayObserve": OBSERVE["MN2-P11"],
            "todayAction": actions["MN2-P11"],
            "when": ["一日を閉じるとき", "反芻が多かった日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN2-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN2-P03"],
        },
    ]

    out = {
        "chapter": 2,
        "sutta": 2,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：一切の煩悩の経）",
        "suttas": ["MN 2 一切漏経（一切の煩悩の経）"],
        "source": {
            "primary": "パーリ・中部第2経（一切漏経／一切の煩悩の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含10漏盡経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・一切の煩悩の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・漏盡経（T1.431c）",
                    "url": SAT_URL,
                    "note": "漢訳対応は段落ごとに異なる。對照表: 法雨道場",
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
            "focusReason": "一切漏経は知見と七門による漏の捨断が主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn002.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 2:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(2, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 12
    assert all(p["id"] == f"MN2-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    assert set(by_nidana) == valid
    print("OK all chinese mapped; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
