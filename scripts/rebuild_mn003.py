#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn003.json (法嗣経／法の相続者の経) to match MN1–2 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0569"
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
    "MN3-P01": (
        "比丘たちよ、わたしの法（教え）の相続者たちと成りなさい。"
        "財貨の相続者たちと〔成っては〕いけません。"
        "わたしには、あなたたちにたいする慈しみ〔の思い〕が存在します。"
    ),
    "MN3-P02": (
        "二者の比丘が、飢えと力の衰えに打ち負かされ、やってくるとします。"
        "彼らに、わたしは、このように説くとします。"
        "『……わたしの、この〔行乞の〕施食は、超過の法（性質）あるものとして、捨てるべき法（性質）あるものとして、存しています。"
        "それで、もし、望むなら、〔それを〕食べなさい』と。"
    ),
    "MN3-P03": (
        "たとえ、何であれ、その比丘が、その〔行乞の〕施食を食べて……過ごすとして、"
        "そこで、まさに、わたしにとって、まさしく、この最初の比丘は、かつまた、より供養されるべき者であり、かつまた、より賞賛されるべき者です。"
        "……それは、その比丘にとって、長夜にわたり、少なき欲求たること（少欲）のために、満ち足りていること（知足）のために、……精進勉励のために、等しく転起するであろうからです。"
    ),
    "MN3-P04": (
        "教師が遠離し、〔世に〕住んでいるとき、弟子たちとして、遠離に随学しない……"
        "教師が、それらの法（性質）の捨棄を言ったのに、しかしながら、それらの法（性質）を捨棄しない……"
        "贅沢の者たちとして、緩慢なる者たちとして、……遠離〔の境地〕にたいし荷を置いた者たちとしてある——"
        "長老の比丘たちは、これらの三つの状況によって非難されるべき者たちと成ります。"
    ),
    "MN3-P05": (
        "教師が遠離し、〔世に〕住んでいるとき、弟子たちとして、遠離に随学します。"
        "かつまた、教師が、それらの法（性質）の捨棄を言ったなら、そして、それらの法（性質）を捨棄します。"
        "さらに、贅沢の者たちではなく、緩慢なる者たちではなく、……遠離〔の境地〕における先行者たちとして、〔世に〕有ります。"
    ),
    "MN3-P06": (
        "友よ、そこで、そして、貪欲（貪）は悪しきものであり、さらに、憤怒（瞋）は悪しきものです。"
        "そして、貪欲の捨棄のために、さらに、憤怒の捨棄のために、中なる〔実践の〕道（中道）が存在し、"
        "眼を作り為すものとして、知恵を作り為すものとして、寂止のために、証知のために、正覚のために、涅槃のために、等しく転起します。"
    ),
    "MN3-P07": (
        "まさしく、この、聖なる八つの支分ある道（八正道・八聖道）です。"
        "それは、すなわち、この、正しい見解（正見）であり、正しい思惟（正思惟）であり、正しい言葉（正語）であり、"
        "正しい行業（正業）であり、正しい生き方（正命）であり、正しい努力（正精進）であり、"
        "正しい気づき（正念）であり、正しい禅定（正定）です。"
    ),
    "MN3-P08": (
        "友よ、そこで、そして、忿激（忿）は悪しきものであり、さらに、怨恨（恨）は悪しきものです。……"
        "そして、嫉妬（嫉）は悪しきものであり、さらに、物惜（慳）は悪しきものです。……"
        "そして、思量（慢）は悪しきものであり、さらに、高慢（過慢）は悪しきものです。……"
        "そして、驕慢（驕）は悪しきものであり、さらに、放逸は悪しきものです。"
    ),
    "MN3-P09": (
        "そして、驕慢の捨棄のために、さらに、放逸の捨棄のために、中なる〔実践の〕道が存在し、"
        "眼を作り為すものとして、知恵を作り為すものとして、寂止のために、証知のために、正覚のために、涅槃のために、等しく転起します。"
    ),
    "MN3-P10": (
        "比丘たちよ、それゆえに、ここに、わたしの法（教え）の相続者たちと成りなさい。"
        "財貨の相続者たちと〔成っては〕いけません。"
        "わたしには、あなたたちにたいする慈しみ〔の思い〕が存在します。"
        "『どのようなわけであれ、弟子たちは、わたしの法（教え）の相続者たちと成るべきである──財貨の相続者たち、ではなく』」と。"
    ),
    "MN3-P11": (
        "尊者サーリプッタは、この〔言葉〕を言いました。"
        "わが意を得たそれらの比丘たちは、尊者サーリプッタの語ったことを大いに喜んだ、ということです。"
    ),
}

OBSERVE = {
    "MN3-P01": (
        "法（教え）の相続者たれ。財貨の相続者になるな。"
        "師は弟子への慈しみから、そう説く。"
    ),
    "MN3-P02": (
        "飢えに打ち負かされた二人の比丘に、世尊は残った施食を勧める。"
        "食は、捨てるべき・超過の法としてある。"
    ),
    "MN3-P03": (
        "残食を取らず飢えとともに過ごす比丘の方が、より供養・賞賛に値する。"
        "少欲・知足・謹厳・精進のために長く転起するからである。"
    ),
    "MN3-P04": (
        "師が遠離に住むのに弟子が随学せず、捨べき法を捨てず、贅沢・緩慢で遠離に荷を置く——"
        "その三事で非難される。"
    ),
    "MN3-P05": (
        "師が遠離に住むとき弟子も随学し、捨べき法を捨て、贅沢・緩慢でなく遠離の先行者となる——"
        "その三事で賞賛される。"
    ),
    "MN3-P06": (
        "貪欲と憤怒は悪しきもの。"
        "それらを捨てるために、眼・智を作り寂止・正覚・涅槃へ向かう中道がある。"
    ),
    "MN3-P07": (
        "その中道とは聖なる八支道——"
        "正見・正思惟・正語・正業・正命・正精進・正念・正定である。"
    ),
    "MN3-P08": (
        "忿・恨・嫉・慳・慢・過慢・驕・放逸なども悪しきもの。"
        "掴まず、中道によって捨てるべきである。"
    ),
    "MN3-P09": (
        "驕・放逸の捨棄のためにも中道があり、"
        "寂止・証知・正覚・涅槃のために等しく転起する。"
    ),
    "MN3-P10": (
        "それゆえ再び——法の相続者たれ。財貨の相続者になるな。"
        "師の慈しみは、弟子が法を継ぐことにある。"
    ),
    "MN3-P11": (
        "サーリプッタの説法を聞いて、比丘たちは大いに喜んだ。"
    ),
}

PRACTICE = {
    "MN3-P01": {
        "nidanaId": "release",
        "pathFactors": ["正命", "正見"],
        "reason": "財ではなく法を継ぐ入口",
        "section": "法相続",
        "category": "livelihood",
    },
    "MN3-P02": {
        "nidanaId": "contact",
        "pathFactors": ["正命", "正念"],
        "reason": "残食・飢えとの接触で財の誘惑が現れる",
        "section": "残食·提示",
        "category": "livelihood",
    },
    "MN3-P03": {
        "nidanaId": "feeling",
        "pathFactors": ["正命", "正精進"],
        "reason": "飢えの受を耐えて少欲・知足を選ぶ",
        "section": "残食·少欲",
        "category": "livelihood",
    },
    "MN3-P04": {
        "nidanaId": "suffering",
        "pathFactors": ["正精進", "正念"],
        "reason": "遠離に随学せず非難される三事",
        "section": "遠離·非難",
        "category": "effort",
    },
    "MN3-P05": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "遠離に随学し賞賛される三事",
        "section": "遠離·賞賛",
        "category": "effort",
    },
    "MN3-P06": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正見"],
        "reason": "貪・瞋という欲しがり／拒みを名づける",
        "section": "貪瞋",
        "category": "intention",
    },
    "MN3-P07": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正定"],
        "reason": "捨のために八正道という中道を立てる",
        "section": "八正道",
        "category": "view",
    },
    "MN3-P08": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正精進"],
        "reason": "忿恨嫉慳慢放逸を掴まず捨てる",
        "section": "忿恨等",
        "category": "intention",
    },
    "MN3-P09": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正見"],
        "reason": "中道が寂止・涅槃へ転起する",
        "section": "中道·果",
        "category": "concentration",
    },
    "MN3-P10": {
        "nidanaId": "review",
        "pathFactors": ["正命", "正念"],
        "reason": "一日の終わりに法相続を見直す",
        "section": "法相続·再",
        "category": "livelihood",
    },
    "MN3-P11": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正語"],
        "reason": "聞法して喜ぶ・保持する",
        "section": "結",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN3-P01": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-open",
        "text": "汝等當行求法。莫行求飮食。所以者何。我慈愍弟子故。欲令行求法不行求飮食。",
        "satLocus": "大正蔵 T1.570a 求法経第二",
        "note": "漢訳は『求法／求飲食』。パーリ『法の相続／財貨の相続』に対応。",
    },
    "MN3-P02": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-leftover",
        "text": "我飽食訖食事已辦猶有殘食。於後有二比丘來飢渇力羸。我語彼曰。我飽食訖。食事已辦猶有殘食。汝等欲食者便取食之。",
        "satLocus": "大正蔵 T1.570a 求法経",
        "note": "残食の譬喩の設定。",
    },
    "MN3-P03": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-appamada",
        "text": "彼比丘不取此食已雖一日一夜苦而不安隱。但彼比丘因不取此食故。得可佛意。所以者何。彼比丘因不取此食故。得少欲得知足。……亦得涅槃。",
        "satLocus": "大正蔵 T1.570a–b 求法経",
        "note": "取らぬ比丘が少欲・知足等で仏意にかなう＝パーリのより賞賛。",
    },
    "MN3-P04": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-blame",
        "text": "若有法律尊師樂住遠離。上弟子不樂住遠離者。上弟子有三事可毀。云何爲三。尊師樂住遠離。上弟子不學捨離。……尊師若説可斷法。上弟子不斷彼法。……所可受證。上弟子而捨方便。",
        "satLocus": "大正蔵 T1.570c–571a 求法経",
        "note": "遠離に随学しない三可毀。",
    },
    "MN3-P05": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-praise",
        "text": "若有法律尊師樂住遠離。上弟子亦樂住遠離者。上弟子有三事可稱。云何爲三。尊師樂住遠離。上弟子亦學捨離。……尊師若説可斷法。上弟子便斷彼法。……所可受證。上弟子精進勤學不捨方便。",
        "satLocus": "大正蔵 T1.571a 求法経",
        "note": "遠離に随学する三可稱。",
    },
    "MN3-P06": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-greed",
        "text": "諸賢。念欲惡。惡念欲亦惡。彼斷念欲亦斷惡念欲。如是恚怨結慳嫉。……諸賢。貪亦惡著亦惡。彼斷貪亦斷著。諸賢。是謂中道能得心住。得定得樂……亦得涅槃。",
        "satLocus": "大正蔵 T1.571a–b 求法経",
        "note": "貪・恚等の悪と中道。パーリの貪瞋＋中道に対応。",
    },
    "MN3-P07": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-eightfold",
        "text": "謂八支聖道。正見乃至正定是爲八。諸賢。是謂復有中道能得心住。得定得樂順法次法。得通得覺亦得涅槃。",
        "satLocus": "大正蔵 T1.571b 求法経",
        "note": "八支聖道＝八正道。",
    },
    "MN3-P08": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-defilements",
        "text": "如是恚怨結慳嫉。欺誑諛諂。無慚無愧慢最上慢貢高放逸。豪貴憎諍。",
        "satLocus": "大正蔵 T1.571b 求法経",
        "note": "忿恨・嫉慳・誑諂・慢放逸等の列挙。",
    },
    "MN3-P09": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-fruit",
        "text": "有中道能得心住。得定得樂順法次法。得通得覺亦得涅槃。",
        "satLocus": "大正蔵 T1.571a–b 求法経",
        "note": "中道の果：心住・定・通・覚・涅槃。",
    },
    "MN3-P10": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-restate",
        "text": "是謂諸弟子。爲行求法故而依佛行。非爲求飮食。",
        "satLocus": "大正蔵 T1.570b 求法経",
        "note": "残食譬喩の結語で求法を再勧奨。",
    },
    "MN3-P11": {
        "status": "mapped",
        "pin": "中阿含88・求法経（T26）",
        "t26": "T26-088-close",
        "text": "佛説如是。尊者舍梨子及諸比丘聞佛所説。歡喜奉行",
        "satLocus": "大正蔵 T1.571b 求法経",
        "note": "漢訳は世尊讃嘆ののち比丘歓喜。パーリはサーリプッタ説法への歓喜。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部3経と中阿含88求法経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn003.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN3-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 3",
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
                    "locus": f"中部・法の相続者の経（MN3）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 法嗣経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第3経・法嗣経（法の相続者の経）"
    SHORT = "法嗣経（法の相続者の経）"
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
            "id": "contact", "weekday": 1, "categoryId": "livelihood", "nidanaLabel": "接触",
            "pathFactors": ["正命", "正念"], "pathFactorIds": ["livelihood", "mindfulness"],
            "pathLabel": "残食・財の誘惑との接触を見る",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の財か法かの分岐になる",
            "toNext": "接触のあと、飢え・快不快の受が来る",
            "todayObserve": OBSERVE["MN3-P02"],
            "todayAction": actions["MN3-P02"],
            "when": ["余分なものを勧められた", "空腹や疲れが強い"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN3-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN3-P01"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "livelihood", "nidanaLabel": "受ける",
            "pathFactors": ["正命", "正精進"], "pathFactorIds": ["livelihood", "effort"],
            "pathLabel": "飢えの受を耐えて少欲・知足を選ぶ",
            "chapterHint": SHORT,
            "fromPrev": "残食や財の接触のあと、受が立ち上がる",
            "toNext": "受け方を誤ると欲しがりへ",
            "todayObserve": OBSERVE["MN3-P03"],
            "todayAction": actions["MN3-P03"],
            "when": ["少し足りないと感じた", "余分を取ろうとした"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN3-P03"][:40] + "…",
            "secondaryObserve": "少欲・知足のために長夜転起する",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "貪・瞋を名づけ、中道で乗らない",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、貪欲と憤怒が立ち上がる",
            "toNext": "止めないと忿恨等の掴みへ",
            "todayObserve": OBSERVE["MN3-P06"],
            "todayAction": actions["MN3-P06"],
            "when": ["欲が出た", "怒りが立った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN3-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN3-P07"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正精進"], "pathFactorIds": ["intention", "effort"],
            "pathLabel": "忿恨嫉慳慢放逸を掴まず捨てる",
            "chapterHint": SHORT,
            "fromPrev": "貪瞋のあと、忿恨等が掴む手前",
            "toNext": "掴むと非難・苦が見える",
            "todayObserve": OBSERVE["MN3-P08"],
            "todayAction": actions["MN3-P08"],
            "when": ["悔しさを抱えた", "慢心や放逸が出た"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN3-P08"][:40] + "…",
            "secondaryObserve": "中道によって捨てる",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "effort", "nidanaLabel": "苦が太る",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "遠離に随学せず非難される三事を見る",
            "chapterHint": SHORT,
            "fromPrev": "随学せず捨ず贅沢・緩慢の結果として非難が来る",
            "toNext": "見れば、随学と八正道へ向き直る",
            "todayObserve": OBSERVE["MN3-P04"],
            "todayAction": actions["MN3-P04"],
            "when": ["教えから離れて重い", "怠けて後悔した"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN3-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN3-P05"],
        },
        {
            "id": "release", "weekday": 6, "categoryId": "livelihood", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正命", "正見"], "pathFactorIds": ["livelihood", "view"],
            "pathLabel": "法を継ぎ、遠離に随学し、八正道で離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、法相続と中道へ向き直る",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN3-P01"],
            "todayAction": actions["MN3-P01"],
            "when": ["財か法かを選ぶ", "八正道の一つを立てる"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN3-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN3-P07"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正命"], "pathFactorIds": ["mindfulness", "livelihood"],
            "pathLabel": "今日、法の相続者として何をしたかを見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の選択は、財を継いだか法を継いだかの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN3-P10"],
            "todayAction": actions["MN3-P10"],
            "when": ["一日を閉じるとき", "聞法できた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN3-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN3-P11"],
        },
    ]

    out = {
        "chapter": 3,
        "sutta": 3,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：法の相続者の経）",
        "suttas": ["MN 3 法嗣経（法の相続者の経）"],
        "source": {
            "primary": "パーリ・中部第3経（法嗣経／法の相続者の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含88求法経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・法の相続者の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・求法経（T1.569c）",
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
            "focusReason": "法嗣経は法を継ぎ財を継がず、遠離と八正道で貪瞋等を捨てるのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn003.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 3:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(3, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN3-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    missing = valid - set(by_nidana)
    assert not missing, missing
    print("OK all chinese mapped; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
