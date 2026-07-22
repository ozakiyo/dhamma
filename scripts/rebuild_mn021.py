#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn021.json (鋸喩経／鋸の喩えの経) to match MN1–20 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0744a06"
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
    "MN21-P01": (
        "比丘たちよ、たとえ、もし、卑しい盗賊たちが、両側に棒のある鋸（のこぎり）で、それぞれの手足を切り裂くも、"
        "そこで、また、その〔比丘〕が、意を汚すなら（怒りを起こすなら）、それによって、彼は、わたしの教えを為す者ではありません。"
        "……『まさしく、そして、わたしの心は、変化することなく有るのだ。かつまた、悪しき言葉を放たないのだ。"
        "さらに、利益と慈しみ〔の思い〕ある者として、慈愛の心ある者として、〔世に〕住むのだ──憤怒を内にする者として、ではなく』と。"
    ),
    "MN21-P02": (
        "比丘たちよ、それは、たとえば、また、人が、鋤と籠を携えて、やってくるとします。"
        "『わたしは、この大いなる地を、地ならざるものと為すのだ』と。……掘り崩し……唾を吐き……小便をします。"
        "……この大いなる地は、深遠で、量りようがない……地ならざるものと為すに為し易くはなく……その人は、疲弊と悩苦の分有者として存するでしょう。"
        "……『……さらに、彼を対象として、一切すべての世を……地に等しき心で充満して、〔世に〕住むのだ』と。"
    ),
    "MN21-P03": (
        "比丘たちよ、それは、たとえば、また、人が……塗料を……携えて、やってくるとします。"
        "『わたしは、この虚空において、色形を加工し、色形の出現を為すのだ』と。"
        "……この虚空は、色形なく、外見なくある……色形を加工し……為し易くはなく……疲弊と悩苦の分有者として存するでしょう。"
        "……『……虚空に等しき心で充満して、〔世に〕住むのだ』と。"
    ),
    "MN21-P04": (
        "比丘たちよ、それは、たとえば、また、人が、燃え盛る草の松明を携えて、やってくるとします。"
        "『わたしは、この燃え盛る草の松明で、ガンガー川を等しく熱し、等しく遍く熱するのだ』と。"
        "……ガンガー川は、深遠で、量りようがない……熱するに為し易くはなく……疲弊と悩苦の分有者として存するでしょう。"
        "……『……ガンガー川に等しき心で充満して、〔世に〕住むのだ』と。"
    ),
    "MN21-P05": (
        "……『まさしく、そして、わたしの心は、変化することなく有るのだ。かつまた、悪しき言葉を放たないのだ。"
        "さらに、利益と慈しみ〔の思い〕ある者として、慈愛の心ある者として、〔世に〕住むのだ──憤怒を内にする者として、ではなく。"
        "そして、その人物を、慈愛〔の思い〕を共具した心で充満して、〔世に〕住むのだ。"
        "さらに、彼を対象として、一切すべての世を……慈愛〔の思い〕を共具した心で充満して、〔世に〕住むのだ』と。"
    ),
    "MN21-P06": (
        "比丘たちよ、五つのものがあります。これらの言葉の道です。……"
        "あるいは、〔しかるべき〕時によって……あるいは、事実によって……あるいは、優しい〔言葉〕によって……"
        "あるいは、義を伴った〔言葉〕によって……あるいは、慈愛の心から……あるいは、憤怒を内にすることから。"
        "……『まさしく、そして、わたしの心は、変化することなく有るのだ。かつまた、悪しき言葉を放たないのだ……』と。"
    ),
    "MN21-P07": (
        "比丘たちよ、たとえ、もし、卑しい盗賊たちが、両側に棒のある鋸で、それぞれの手足を切り裂くも、"
        "そこで、また、その〔比丘〕が、意を汚すなら、それによって、彼は、わたしの教えを為す者ではありません。"
        "……慈愛〔の思い〕を共具した心で充満して、〔世に〕住むのだ。"
    ),
    "MN21-P08": (
        "……一部の比丘は、すなわち、諸々の意に適わない言葉の道が触れないかぎり……温和なるうえにも温和なる者として〔世に〕有ります。"
        "……しかしながら、すなわち、比丘に、諸々の意に適わない言葉の道が触れることから、そこで〔はじめて〕、比丘は、『温和なる者』と知られるべきです。"
        "（ヴェーデーヒカー主婦は、試されないあいだは温和と評され、奴婢に試されて激昂し、悪評を得た。）"
    ),
    "MN21-P09": (
        "比丘たちよ、そして、この鋸の喩えの教諭に、あなたたちが、幾度となく、意を為すなら……"
        "あなたたちが甘受できない、〔まさに〕その、言葉の道を……まさに、あなたたちは見ますか」と。"
        "「尊き方よ、まさに、このことは、さにあらず（見ません）」〔と〕。"
        "「……この鋸の喩えの教諭に、幾度となく、意を為しなさい。それは、あなたたちにとって、長夜にわたり、利益のために〔成り〕、安楽のために成るでしょう」と。"
    ),
    "MN21-P10": (
        "……鞣されたうえにも善く鞣され……柔和で綿のようで、サラサラと音のしない……猫皮があるとします。"
        "……小枝で……小石で、サラサラと〔音を〕為し……為すでしょうか」と。「……さにあらず」〔と〕。"
        "……『……猫皮に等しき心で充満して、〔世に〕住むのだ』と。"
        "（拳・石・杖・刃で打たれても、心を変えず悪しき言葉を放たない。）"
    ),
    "MN21-P11": (
        "比丘たちよ、それゆえに、ここに、この鋸の喩えの教諭に、幾度となく、意を為しなさい。"
        "それは、あなたたちにとって、長夜にわたり、利益のために〔成り〕、安楽のために成るでしょう。"
    ),
}

OBSERVE = {
    "MN21-P01": (
        "鋸の喩え——手足を鋸で切られても意を汚さず、心は変わらず、悪しき言葉を放たず、慈愛に住む。"
        "朝、今日「鋸喩」の心を一つ決める。"
    ),
    "MN21-P02": (
        "地の譬喩——掘り唾し小便しても地を非地にできない。心を地の如く充満して住む——"
        "非難·批判を受けても、一度「地の如く」と耐える。"
    ),
    "MN21-P03": (
        "虚空の譬喩——虚空に色を描けない。心を虚空の如く充満して住む——"
        "非難を受けても、一度「反応の跡を残さない（門の如く）」と決める。"
    ),
    "MN21-P04": (
        "ガンガーの譬喩——草松明で川を熱せない。心をガンガーの如く充満して住む——"
        "非難を受けても、一度「池の如く」清らかな心を保つ。"
    ),
    "MN21-P05": (
        "心は変わらず、悪しき言葉を放たず、利益と慈しみある者として住み、一切の世を慈愛で充満する——"
        "嫌いな人一人に慈心を一呼吸向ける。"
    ),
    "MN21-P06": (
        "五つの言葉の道——時·事実·柔粗·義·慈／瞋。どの道でも悪しき言葉を返さない——"
        "非難を受けても、報復の言葉を一度止める。"
    ),
    "MN21-P07": (
        "鋸で手足を切られても意を汚せば教えを為す者ではない——苦を受けても嗔を増やさない——"
        "今日の苦を「鋸喩の心」で一度受け止める。"
    ),
    "MN21-P08": (
        "意に適わない言葉が触れてはじめて、温和·謙譲·寂静が試される（ヴェーデーヒカーの物語）——"
        "小さな非難·不便に「忍辱」と耐える。"
    ),
    "MN21-P09": (
        "鋸の喩えの教諭に幾度となく意を為せば、甘受できない言葉の道は見えなくなる——"
        "夜、慈心を失いかけた瞬間を一つ認め、明日慈心を向ける。"
    ),
    "MN21-P10": (
        "猫皮の譬喩——よく鞣された皮は小枝·小石で音を立てない。打たれても心を変えず慈に住む——"
        "最も難しい対人関係に慈心を一呼吸向ける。"
    ),
    "MN21-P11": (
        "鋸の喩えの教諭に幾度となく意を為せ——長夜の利益と安楽のために——"
        "今日学んだ鋸喩を、声に出して一度読み返す。"
    ),
}

PRACTICE = {
    "MN21-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正思惟"],
        "reason": "朝、非難が触れる前に鋸喩の心を決める",
        "section": "鋸の教諭",
        "category": "mindfulness",
    },
    "MN21-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正定", "正念"],
        "reason": "批判の受を地の如く受け、心を地に等しく充満する",
        "section": "地の喩",
        "category": "concentration",
    },
    "MN21-P03": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正念"],
        "reason": "虚空の如く反応の跡を残さず離す",
        "section": "虚空の喩",
        "category": "intention",
    },
    "MN21-P04": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正念"],
        "reason": "ガンガーの如く熱せられない清らかさに住む",
        "section": "ガンガーの喩",
        "category": "concentration",
    },
    "MN21-P05": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正定"],
        "reason": "嫌いな人にも慈愛の心を充満して住む",
        "section": "慈愛",
        "category": "intention",
    },
    "MN21-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正語", "正念"],
        "reason": "五つの言葉の道への報復の掴みを止める",
        "section": "五つの言葉の道",
        "category": "speech",
    },
    "MN21-P07": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦を受けても意を汚さず、鋸喩で嗔の増大を見る",
        "section": "鋸·苦",
        "category": "view",
    },
    "MN21-P08": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "小さな非難に触れても、温和の欲しがりではなく法への素直さで耐える",
        "section": "試される温和",
        "category": "intention",
    },
    "MN21-P09": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜に鋸喩を振り返り、慈心を失いかけた瞬間を認める",
        "section": "幾度も意を為す",
        "category": "mindfulness",
    },
    "MN21-P10": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正定"],
        "reason": "最も難しい対人で猫皮の如く音を立てず慈に住む",
        "section": "猫皮の喩",
        "category": "intention",
    },
    "MN21-P11": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "鋸喩を読み返し、長夜の利益のために保持する",
        "section": "教諭の保持",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN21-P01": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-kakaca",
        "text": "若有賊來，以利鋸刀節節解截……心不變易，口無惡言向割截人，緣彼起慈愍心，心與慈俱，遍滿一方成就遊……遍滿一切世間成就遊。",
        "satLocus": "大正蔵 T1.746a 牟犁破群那経",
        "note": "利鋸刀節節解截＝鋸の喩え。",
    },
    "MN21-P02": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-pathavi",
        "text": "猶如有人持大鏵鍬來……『我能令此大地，使作非地。』……不能令此大地使作非地。……心行如地，無結無怨，無恚無諍……遍滿一切世間成就遊。",
        "satLocus": "大正蔵 T1.745b 牟犁破群那経",
        "note": "心行如地＝地に等しき心。",
    },
    "MN21-P03": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-akasa",
        "text": "猶如畫師……『我於此虛空畫作形像，以彩莊染。』……不能於虛空畫作形像……心行如虛空……遍滿一切世間成就遊。",
        "satLocus": "大正蔵 T1.745c 牟犁破群那経",
        "note": "虛空＝パーリの虚空喩。旧「門喩」は経典にない。",
    },
    "MN21-P04": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-ganga",
        "text": "猶如有人持大草炬……『我以此草炬，用熱恒伽水，令作沸湯。』……不能令恒伽水熱……心行如恒伽水……遍滿一切世間成就遊。",
        "satLocus": "大正蔵 T1.745b–c 牟犁破群那経",
        "note": "恒伽水＝ガンガー。旧「池喩」は経典にない。",
    },
    "MN21-P05": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-metta",
        "text": "心不變易，口無惡言，向怨家人緣彼起慈愍心，心與慈俱，遍滿一方成就遊……遍滿一切世間成就遊。如是悲、喜心與捨俱……。",
        "satLocus": "大正蔵 T1.745b 牟犁破群那経",
        "note": "慈愍·四無量。",
    },
    "MN21-P06": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-vacana",
        "text": "復次，有互言道，若他說者，或時或非時，或真或非真，或軟或堅，或慈或恚，或有義或無義。……心不變易，口無惡言。",
        "satLocus": "大正蔵 T1.745a–b 牟犁破群那経",
        "note": "互言道＝五つの言葉の道。",
    },
    "MN21-P07": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-dukkha",
        "text": "若有賊來，以利鋸刀節節解截時，或心變易者，或口惡言者，我說汝等因此必衰。……心不變易，口無惡言……緣彼起慈愍心。",
        "satLocus": "大正蔵 T1.746a 牟犁破群那経",
        "note": "心変易＝意を汚す。",
    },
    "MN21-P08": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-vedehika",
        "text": "昔時有居士婦，名鞞陀提……忍辱堪耐溫和……婢名黑……試……便大瞋恚……頭破血流……便有極大惡名……惡性急弊麤獷。",
        "satLocus": "大正蔵 T1.744c–745a 牟犁破群那経",
        "note": "鞞陀提＝ヴェーデーヒカー。試されてはじめて顕れる。",
    },
    "MN21-P09": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-anussati",
        "text": "汝等當數數念利鋸刀喻沙門教……汝等頗見他不愛惡語言向我，我聞已，不堪耐耶？……不也。",
        "satLocus": "大正蔵 T1.746a 牟犁破群那経",
        "note": "數數念利鋸刀喻＝幾度となく意を為す。",
    },
    "MN21-P10": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-bilara",
        "text": "猶如猫皮囊柔治極軟……拳扠石擲杖打刀斫……無復有［車／瓦］聲。……心行如猫皮囊……遍滿一切世間成就遊。",
        "satLocus": "大正蔵 T1.745c–746a 牟犁破群那経",
        "note": "猫皮囊＝猫皮。",
    },
    "MN21-P11": {
        "status": "mapped",
        "pin": "中阿含193・牟犁破群那経（T26）",
        "t26": "T26-193-hold",
        "text": "汝等當數數念利鋸刀喻沙門教……必得安樂，無眾苦患……晝夜增長善法而不衰退……於二果中必得其一。",
        "satLocus": "大正蔵 T1.746a–b 牟犁破群那経",
        "note": "數數念の保持と利益。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部21経と中阿含193牟犁破群那経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn021.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN21-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 21",
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
                    "locus": f"中部・鋸の喩えの経（MN21）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 鋸喩経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第21経・鋸喩経（鋸の喩えの経）"
    SHORT = "鋸喩経（鋸の喩えの経）"
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
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "朝、非難が触れる前に鋸喩の心を決める",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の言葉の接触を変える",
            "toNext": "触のあと、批判の受が見える",
            "todayObserve": OBSERVE["MN21-P01"],
            "todayAction": actions["MN21-P01"],
            "when": ["朝に心を決めた", "非難が触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN21-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN21-P08"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "concentration", "nidanaLabel": "受ける",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "批判の受を地の如く受け、心を地に等しく充満する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、意に適わない言葉の受が立つ",
            "toNext": "受に乗ると報復の欲しがりへ",
            "todayObserve": OBSERVE["MN21-P02"],
            "todayAction": actions["MN21-P02"],
            "when": ["批判を受けた", "地の如く耐えた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN21-P02"][:40] + "…",
            "secondaryObserve": "心行如地",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "小さな非難に触れても、温和の見せかけではなく法への素直さで耐える",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、怒りたい欲しがりが立つ",
            "toNext": "止めないと報復の言葉の掴みへ",
            "todayObserve": OBSERVE["MN21-P08"],
            "todayAction": actions["MN21-P08"],
            "when": ["小さな非難があった", "試された"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN21-P08"][:40] + "…",
            "secondaryObserve": "鞞陀提",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正念"], "pathFactorIds": ["speech", "mindfulness"],
            "pathLabel": "報復の言葉と難しい対人への掴みを、猫皮の如く離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、言い返す掴みが手前",
            "toNext": "掴むと意を汚す苦が見える",
            "todayObserve": OBSERVE["MN21-P06"],
            "todayAction": actions["MN21-P06"],
            "when": ["報復したくなった", "難しい対人に触れた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN21-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN21-P10"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "苦を受けても意を汚さず、嗔の増大を鋸喩で見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、意を汚す患が見える",
            "toNext": "見れば、虚空·ガンガー·慈の離しへ",
            "todayObserve": OBSERVE["MN21-P07"],
            "todayAction": actions["MN21-P07"],
            "when": ["苦を受けた", "嗔が増えそう"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN21-P07"][:40] + "…",
            "secondaryObserve": "心變易則必衰",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "intention", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正思惟", "正定"], "pathFactorIds": ["intention", "concentration"],
            "pathLabel": "虚空·ガンガーの如く反応せず、慈愛で充満して住む",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、清らかさと慈へ向き直る",
            "toNext": "離せば、夜の鋸喩の見直しへ",
            "todayObserve": OBSERVE["MN21-P05"],
            "todayAction": actions["MN21-P05"],
            "when": ["慈心を向けた", "反応しなかった"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN21-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN21-P03"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "鋸喩を幾度も意に為し、慈心を失いかけた瞬間を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の対人は、朝からの鋸喩の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN21-P09"],
            "todayAction": actions["MN21-P09"],
            "when": ["一日を閉じるとき", "鋸喩を読み返した日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN21-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN21-P11"],
        },
    ]

    out = {
        "chapter": 21,
        "sutta": 21,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：鋸の喩えの経）",
        "suttas": ["MN 21 鋸喩経（鋸の喩えの経）"],
        "source": {
            "primary": "パーリ・中部第21経（鋸喩経／鋸の喩えの経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含193牟犁破群那経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・鋸の喩えの経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・牟犁破群那経（T1.744a）",
                    "url": SAT_URL,
                    "note": "破群那·利鋸刀喻。對照表: 法雨道場",
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
            "focusNodeId": "feeling",
            "focusReason": "鋸の喩えの経は意に適わない言葉の道が触れても心を変えず慈愛に住むのが主題。既定の焦点は受ける。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn021.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 21:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(21, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN21-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
