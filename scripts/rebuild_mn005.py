#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn005.json (無穢経／穢れなき者の経) to match MN1–4 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0566"
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
    "MN5-P01": (
        "友よ、四つのものがあります。これらの人物たちが、世において等しく見出されつつ存しています。"
        "……穢れを有する者として……『わたしの内に、穢れが存在する』と、事実のとおりに覚知しない……"
        "……覚知する……穢れなき者として……覚知しない……覚知する……"
        "覚知しない者は下劣なる人、覚知する者は最勝の人と告げ知らされます。"
    ),
    "MN5-P02": (
        "まさしく、穢れなき者として〔世に〕存しつつ、『わたしの内に、穢れは存在しない』と、事実のとおりに覚知しない、この人物ですが、"
        "彼には、このことが待っています。浄美の形相に意を為すでしょうし、浄美の形相へと意を為すことから、"
        "貪欲〔の思い〕が、彼の心を転落させるでしょう。"
    ),
    "MN5-P03": (
        "『さてまた、まさに、〔わたしは〕罪を犯した者として存している。しかしながら、わたしのことを、比丘たちは、「罪を犯した者である」〔と〕知るべきにあらず』と。"
        "……比丘たちが、『罪を犯した者である』と知ることです。"
        "……かくのごとく、彼は、激情した者と成り、満足しない者と〔成ります〕。"
        "友よ、まさしく、そして、まさに、その激情は、さらに、その不興は、これは、両者ともに、穢れです。"
    ),
    "MN5-P04": (
        "『ああ、まさに、まさしく、わたしが、諸々の精妙なる衣料の得者として存するべきである。"
        "他の比丘は、諸々の精妙なる衣料の得者として存するべきではない』と。"
        "……『他の比丘が……得者として存する。わたしは……存さない』と、かくのごとく、彼は、激情した者と成り、満足しない者と〔成ります〕。"
        "……その激情は、さらに、その不興は、これは、両者ともに、穢れです。"
    ),
    "MN5-P05": (
        "友よ、『穢れ』『穢れ』と説かれます。友よ、いったい、まさに、これは、何の同義語なのですか。すなわち、この、『穢れ』〔とは〕」と。"
        "「友よ、まさに、これは、諸々の悪しき善ならざる欲求の行境（活動範囲）の同義語です。すなわち、この、『穢れ』とは。"
    ),
    "MN5-P06": (
        "まさしく、穢れなき者として〔世に〕存しつつ、『わたしの内に、穢れは存在しない』と、事実のとおりに覚知する、この人物ですが、"
        "彼には、このことが待っています。浄美の形相に意を為さないでしょうし、"
        "浄美の形相へと意を為さないことから、貪欲〔の思い〕が、彼の心を転落させることはないでしょう。"
    ),
    "MN5-P07": (
        "まさしく、穢れを有する者として〔世に〕存しつつ、『わたしの内に、穢れが存在する』と、事実のとおりに覚知する、この人物ですが、"
        "この者は、……最勝の人と告げ知らされます。"
        "……その穢れの捨棄のために、欲〔の思い〕を生じさせるでしょうし、努力するでしょうし、精進に励むでしょう。"
    ),
    "MN5-P08": (
        "まさしく、穢れを有する者として〔世に〕存しつつ、『わたしの内に、穢れが存在する』と、事実のとおりに覚知しない、この人物ですが、"
        "……その穢れの捨棄のために、欲〔の思い〕を生じさせないでしょうし、努力しないでしょうし、精進に励まないでしょう。"
        "彼は、貪欲を有し、憤怒を有し、迷妄を有し、穢れを有する者として、汚染された心の者として、命を終えるでしょう。"
    ),
    "MN5-P09": (
        "『わたしのことを、比丘たちは、僧団の中において叱責する──内密に、ではなく』と、かくのごとく、彼は、激情した者と成り、満足しない者と〔成ります〕。"
        "友よ、まさしく、そして、まさに、その激情は、さらに、その不興は、これは、両者ともに、穢れです。"
    ),
    "MN5-P10": (
        "〔まさに〕その、この〔銅の鉢〕を、主人たちが、まさしく、そして、遍く受益し、かつまた、遍く清め、さらに、それを、塵ある道のうえに捨て置きません。"
        "友よ、まさに、このように〔為すなら〕、その銅の鉢は、他時にあって、より完全なる清浄のものとなり、完全なる清白のものとして存するでしょうか。"
    ),
    "MN5-P11": (
        "その穢れの捨棄のために、欲〔の思い〕（意欲・意向）を生じさせるでしょうし、努力するでしょうし、精進に励むでしょう。"
        "彼は、貪欲なく、憤怒なく、迷妄なく、穢れなき者として、汚染されていない心の者として、命を終えるでしょう。"
    ),
}

OBSERVE = {
    "MN5-P01": (
        "世に四種の人がいる——穢れの有無と、それを事実のとおりに覚知するか否か。"
        "覚知しない者は下劣、覚知する者は最勝と告げ知らされる。"
    ),
    "MN5-P02": (
        "穢れなしと気づかぬまま、浄美の形相に意を向けると、"
        "貪欲が心を転落させ、再び穢れを有する者となる。"
    ),
    "MN5-P03": (
        "『罪を知られたくない』という欲求が阻まれると、激情と不興が起きる。"
        "その激情と不興こそが穢れである。"
    ),
    "MN5-P04": (
        "精妙な衣・食・臥具・薬を自分だけが得たいという欲求が阻まれると、"
        "激情と不興が起きる——それも穢れである。"
    ),
    "MN5-P05": (
        "『穢れ』とは、諸々の悪しき善ならざる欲求の行境の同義語である。"
    ),
    "MN5-P06": (
        "穢れなしと事実のとおりに覚知する者は、浄美の形相に意を向けない。"
        "ゆえに貪欲が心を転落させることはない。"
    ),
    "MN5-P07": (
        "内に穢れがあると事実のとおりに覚知する者は、最勝である。"
        "捨棄のために意欲・努力・精進が起きるからである。"
    ),
    "MN5-P08": (
        "穢れがあると気づかず捨てようとしない者は、"
        "貪欲・憤怒・迷妄を有し、汚染された心のまま命を終える。"
    ),
    "MN5-P09": (
        "衆中で叱責されたなど、思いどおりにならないとき起きる激情と不興——"
        "それも両者ともに穢れである。"
    ),
    "MN5-P10": (
        "錆びた銅鉢も、使い清めれば清浄になる。"
        "穢れを知り、捨てるために洗う者の譬喩である。"
    ),
    "MN5-P11": (
        "穢れの捨棄のために意欲を起こし、努力し、精進すれば、"
        "貪瞋癡なく穢れなき者として命を終える。"
    ),
}

PRACTICE = {
    "MN5-P01": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "四種人——穢れの有無と如実知を弁える",
        "section": "四種人",
        "category": "view",
    },
    "MN5-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正思惟", "正念"],
        "reason": "浄美の形相への作意が貪欲を起こす",
        "section": "浄美·作意",
        "category": "intention",
    },
    "MN5-P03": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正語"],
        "reason": "知られたくない欲求が激情・不興になる",
        "section": "罪·隠蔽",
        "category": "intention",
    },
    "MN5-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正命", "正思惟"],
        "reason": "精妙な四事への欲求が穢れとなる",
        "section": "衣食等",
        "category": "livelihood",
    },
    "MN5-P05": {
        "nidanaId": "review",
        "pathFactors": ["正見"],
        "reason": "穢れ＝悪しき欲求の行境と名づける",
        "section": "穢の定義",
        "category": "view",
    },
    "MN5-P06": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正精進"],
        "reason": "浄美の接触に意を向けず門を護る",
        "section": "護·不向",
        "category": "mindfulness",
    },
    "MN5-P07": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "自分の穢れを如実に見てから他を見る",
        "section": "如実知",
        "category": "mindfulness",
    },
    "MN5-P08": {
        "nidanaId": "suffering",
        "pathFactors": ["正見"],
        "reason": "気づかず捨てぬ穢れが汚染心の命終となる",
        "section": "汚染·命終",
        "category": "view",
    },
    "MN5-P09": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正思惟"],
        "reason": "叱責・言葉への激情不興を穢れと見る",
        "section": "激情·不興",
        "category": "speech",
    },
    "MN5-P10": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正精進"],
        "reason": "銅鉢の譬喩で今日の清めを振り返る",
        "section": "銅鉢·清",
        "category": "mindfulness",
    },
    "MN5-P11": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正思惟"],
        "reason": "捨棄のために意欲・努力・精進する",
        "section": "捨棄·精進",
        "category": "effort",
    },
}

CHINESE = {
    "MN5-P01": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-four",
        "text": "世有四種人。云何爲四。或有一人内實有穢不自知。……或有一人内實無穢自知。内無穢知如眞。……有穢不知如眞者。……爲最下賤。……有穢知如眞者。……爲最勝也。",
        "satLocus": "大正蔵 T1.566a 穢経第一",
        "note": "四種人・下賤／最勝＝パーリの下劣／最勝。",
    },
    "MN5-P02": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-beauty",
        "text": "若有一人我内無穢。我内實無此穢不知如眞者。當知彼人不護由眼耳所知法。彼因不護由眼耳所知法故。則爲欲心纒。",
        "satLocus": "大正蔵 T1.566c 穢経",
        "note": "漢訳は眼耳所知法を護らぬ＝パーリの浄美の形相への作意。",
    },
    "MN5-P03": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-hide",
        "text": "或有一人心生如是欲。我所犯戒莫令他人知我犯戒。……或有他人知彼犯戒。彼因他人知犯戒故心便生惡。若彼心生惡及心生欲者。倶是不善。",
        "satLocus": "大正蔵 T1.567a 穢経",
        "note": "犯戒を知られたくない欲求と心生惡＝激情・不興。",
    },
    "MN5-P04": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-robes",
        "text": "或有一人心生如是欲令我得衣被飮食床褥湯藥諸生活具。莫令餘比丘得衣被飮食床褥湯藥諸生活具。……心便生惡。若彼心生惡及心生欲者。倶是不善。",
        "satLocus": "大正蔵 T1.567c 穢経",
        "note": "衣食床褥湯薬への欲求。",
    },
    "MN5-P05": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-def",
        "text": "所説穢者何等爲穢。尊者舍梨子答比丘曰。賢者。無量惡不善法。從欲生。謂之穢。",
        "satLocus": "大正蔵 T1.567a 穢経",
        "note": "穢＝從欲生の惡不善法。",
    },
    "MN5-P06": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-guard",
        "text": "若有一人我内無穢。我内實無此穢知如眞者。當知彼人護由眼耳所知法。彼因護由眼耳所知法故。則不爲欲心纒。",
        "satLocus": "大正蔵 T1.566c–567a 穢経",
        "note": "眼耳所知法を護る＝浄美に意を向けない。",
    },
    "MN5-P07": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-know",
        "text": "若有一人我内有穢。我内實有此穢知如眞者。當知彼人欲斷此穢。求方便精勤學。彼便無穢不穢汚心命終。",
        "satLocus": "大正蔵 T1.566b 穢経",
        "note": "有穢知如眞→欲斷・精勤。",
    },
    "MN5-P08": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-death",
        "text": "若有一人内實有穢不自知。内有穢不知如眞者。當知彼人不欲斷穢。不求方便不精勤學。彼便有穢穢汚心命終。",
        "satLocus": "大正蔵 T1.566b 穢経",
        "note": "不知・不斷→穢汚心命終。",
    },
    "MN5-P09": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-rebuke",
        "text": "或有一人心生如是欲。我所犯戒當令他人於屏處訶。莫令在衆訶我犯戒。……或有他人於衆中訶不在屏處。……心便生惡。若彼心生惡及心生欲者。倶是不善。",
        "satLocus": "大正蔵 T1.567a 穢経",
        "note": "衆中訶への心生惡。",
    },
    "MN5-P10": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-bowl",
        "text": "猶如有人或從市肆或從銅作家。買銅槃來塵垢所汚。彼持來已數數洗塵數數揩拭。數數日炙不著饒塵處如是銅槃便極淨潔。",
        "satLocus": "大正蔵 T1.566b 穢経",
        "note": "銅槃を洗う譬喩。",
    },
    "MN5-P11": {
        "status": "mapped",
        "pin": "中阿含87・穢経（T26）",
        "t26": "T26-087-abandon",
        "text": "當知彼人欲斷此穢。求方便精勤學。彼便無穢不穢汚心命終彼因無穢不穢汚心命終故。便賢死生善處。",
        "satLocus": "大正蔵 T1.566b 穢経",
        "note": "欲斷・精勤→無穢命終。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部5経と中阿含87穢経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn005.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN5-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 5",
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
                    "locus": f"中部・穢れなき者の経（MN5）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 無穢経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第5経・無穢経（穢れなき者の経）"
    SHORT = "無穢経（穢れなき者の経）"
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
            "pathLabel": "浄美の接触に意を向けず門を護る",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の接触の護りになる",
            "toNext": "護らねば快の受と貪欲へ",
            "todayObserve": OBSERVE["MN5-P06"],
            "todayAction": actions["MN5-P06"],
            "when": ["美しいものを見た", "画面を開く前"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN5-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN5-P05"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "intention", "nidanaLabel": "受ける",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "浄美の受に意を向けると貪欲が転落する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、好ましい形相の受が来る",
            "toNext": "作意すれば欲しがりへ",
            "todayObserve": OBSERVE["MN5-P02"],
            "todayAction": actions["MN5-P02"],
            "when": ["好ましい形に心が取られた", "快に乗った"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN5-P02"][:40] + "…",
            "secondaryObserve": "気づかぬまま浄美に意を向ける危険",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "livelihood", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正命", "正思惟"], "pathFactorIds": ["livelihood", "intention"],
            "pathLabel": "精妙な四事への欲求を穢れと名づける",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、衣食などの欲しがりが立つ",
            "toNext": "阻まれると激情の掴みへ",
            "todayObserve": OBSERVE["MN5-P04"],
            "todayAction": actions["MN5-P04"],
            "when": ["上等なものを欲しがった", "自分が得たいと思った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN5-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN5-P05"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正思惟"], "pathFactorIds": ["speech", "intention"],
            "pathLabel": "隠蔽・叱責への激情不興を掴まず見る",
            "chapterHint": SHORT,
            "fromPrev": "欲求が阻まれ、激情と不興が掴む手前",
            "toNext": "掴むと汚染心の苦が見える",
            "todayObserve": OBSERVE["MN5-P03"],
            "todayAction": actions["MN5-P03"],
            "when": ["知られたくないと思った", "叱責に腹が立った"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN5-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN5-P09"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見"], "pathFactorIds": ["view"],
            "pathLabel": "気づかず捨てぬ穢れが汚染心の命終となる",
            "chapterHint": SHORT,
            "fromPrev": "穢れを知らず精進せぬ結果として、汚染が残る",
            "toNext": "見れば、如実知と捨棄の精進へ向き直る",
            "todayObserve": OBSERVE["MN5-P08"],
            "todayAction": actions["MN5-P08"],
            "when": ["穢れを認められなかった", "心が重く残った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN5-P08"][:40] + "…",
            "secondaryObserve": "下劣なる人の帰結",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正思惟"], "pathFactorIds": ["effort", "intention"],
            "pathLabel": "穢れの捨棄のために意欲・努力・精進する",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、洗って捨てる実践へ",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN5-P11"],
            "todayAction": actions["MN5-P11"],
            "when": ["穢れを一つ特定した", "手放す一歩を踏む"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN5-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN5-P07"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "今日の穢れを如実に知り、銅鉢のように洗う",
            "chapterHint": SHORT,
            "fromPrev": "一日の欲求と激情は、穢れの跡",
            "toNext": "見直しが、翌朝の接触の護りになる",
            "todayObserve": OBSERVE["MN5-P10"],
            "todayAction": actions["MN5-P10"],
            "when": ["一日を閉じるとき", "他者を評価したくなった日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN5-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN5-P01"],
        },
    ]

    out = {
        "chapter": 5,
        "sutta": 5,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：穢れなき者の経）",
        "suttas": ["MN 5 無穢経（穢れなき者の経）"],
        "source": {
            "primary": "パーリ・中部第5経（無穢経／穢れなき者の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含87穢経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・穢れなき者の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・穢経（T1.566a）",
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
            "focusReason": "無穢経は穢れを如実に知り、捨棄のために精進するのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn005.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 5:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(5, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN5-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
