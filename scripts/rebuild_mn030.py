#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn030.json (心材喩小経／心材の喩えの小経) to match MN1–29 source alignment.

對照表: 北傳無相当。SCはEA43.4を類縁とするが、ピンガラコッチャの六師問·
智見より上の禅定系列はパーリ固有。心材段階（利得·戒·定·智見·解脱）はEAと重なる。
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0125_%2C02%2C0759a29"
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
    "MN30-P01": (
        "やめよ、婆羅門。このことは、これで十分である。……"
        "わたしは、あなたに法を説こう。よく聞き、よく作意せよ。わたしは語る。"
        "（ピンガラコッチャが六師の証知を問うたとき——世尊は問いを置き、法を説く。）"
    ),
    "MN30-P02": (
        "心材を求める者が、心材ある大樹の前に至り、"
        "心材·膚材·皮·嫩芽を過ぎ、枝葉を切り『心材』と思い持ち帰る——"
        "彼は心材を知らない。心材で作るべきことを成就できない。"
        "……利得·恭敬·名声で怠惰に堕ちる者を、わたしは枝葉を心材と誤る者と言う。"
    ),
    "MN30-P03": (
        "『わたしは生·老·病·死·愁·悲·苦·憂·悩に堕ち、苦に陷り、苦に征服された者である。"
        "願わくは、この一切の苦の集まりの作終結を知りたい』——"
        "このように思って、在家から家なきへ出家する。"
    ),
    "MN30-P04": (
        "利得·恭敬·名声が生じ、……自らを讃え他を軽蔑する。"
        "……利得·恭敬·名声のゆえに怠惰·弛緩し、"
        "より上·より勝れた法の証得のために欲を生じず努力しない。"
        "わたしは、この人を枝葉を心材と誤る者と言う。"
    ),
    "MN30-P05": (
        "戒具足に達しても、怠惰·弛緩せず、"
        "より上·より勝れた法の証得のために欲を生じ、努力すべきである。"
        "（戒で止まれば、嫩芽を心材と誤る。）"
    ),
    "MN30-P06": (
        "定具足に達しても、怠惰·弛緩せず、"
        "より上·より勝れた法の証得のために欲を生じ、努力すべきである。"
        "（定の快さで止まれば、皮を心材と誤る。）"
    ),
    "MN30-P07": (
        "智見より上·より勝れた法とは何か。"
        "……初禅……第二禅……第三禅……第四禅……"
        "……非想非非想処を超え、想受滅に入り住し、慧をもって諸漏を尽くす——"
        "これらが、智見より上·より勝れた法である。"
        "（『知っている』で止まれば、膚材を心材と誤る。）"
    ),
    "MN30-P08": (
        "心材を求める者が、心材ある大樹の前に至り、"
        "心材のみを切り、『心材』と知って持ち帰る——"
        "彼は心材を知る。心材をもって心材の責務を果たす者は、その目的を成就する。"
    ),
    "MN30-P09": (
        "婆羅門よ、この梵行は、利得·恭敬·名声のためでも、"
        "戒具足のためでも、定具足のためでも、智見のためでもない。"
        "この不動の心の解脱——これこそが梵行の目的であり、心材であり、終極である。"
    ),
    "MN30-P10": (
        "この不動の心の解脱——これこそが梵行の目的であり、心材であり、終極である。"
        "（途中の成果——枝葉·嫩芽·皮·膚材——で満足せず、心材まで進む。）"
    ),
}

OBSERVE = {
    "MN30-P01": (
        "六師の証知の問いはいったん置く——先に法を聞け。"
        "今日「誰が正しいか」の議論より、自分の心の状態を一つ観る。"
    ),
    "MN30-P02": (
        "心材を求めて枝葉を誤る——利得·名声で満足して止まる。"
        "今日の成果一つに「これ心材か、枝葉か」と問う。"
    ),
    "MN30-P03": (
        "出家の動機——一切の苦の集まりの作終結を知りたい。"
        "苦が来たら「これ苦の集まりの一部」と一瞬認め、終止を思い出す。"
    ),
    "MN30-P04": (
        "利得·恭敬·名声で自らを讃え他を軽蔑——枝葉を誤った修行者。"
        "今日、自分より劣ると感じた相手を軽蔑していないか一度問う。"
    ),
    "MN30-P05": (
        "戒具足に達しても止まらず——より上·勝れた法の証得を求む。"
        "今日の善行一つについて、それが目的か手段かを見分ける。"
    ),
    "MN30-P06": (
        "定具足に達しても止まらず——定の快さは皮であり心材ではない。"
        "瞑想や集中の快さに「これ心材ではない」と一瞬付け加える。"
    ),
    "MN30-P07": (
        "智見より上·勝れた法——初禅から想受滅まで。『知っている』で止めない。"
        "「知っている」という確信が、観察を止めていないか問う。"
    ),
    "MN30-P08": (
        "心材のみを切り知って持ち帰る——目的を成就する。"
        "今日、修行の「心材」（解脱）に向けた一歩を踏む。"
    ),
    "MN30-P09": (
        "梵行の目的は利得·戒·定·智見ではない——不動の心の解脱が心材。"
        "執着の対象一つに「これ枝葉、心材は解脱」と見分ける。"
    ),
    "MN30-P10": (
        "途中の成果で満足せず、心材まで進む。"
        "就寝前、今日「枝葉で止まった」箇所一つを認め、明日は一歩進む。"
    ),
}

PRACTICE = {
    "MN30-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "議論に触れず、自分の心の状態を一つ観る",
        "section": "問いを置き法を聞く",
        "category": "mindfulness",
    },
    "MN30-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "成果への欲しがりが枝葉か心材か問う",
        "section": "枝葉を心材と誤る",
        "category": "view",
    },
    "MN30-P03": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦を集まりの一部と認め、終止を思い出す",
        "section": "苦の集まり·出家の動機",
        "category": "view",
    },
    "MN30-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正念"],
        "reason": "他者への軽蔑の掴みを一度問う",
        "section": "利得·自讃他毀",
        "category": "intention",
    },
    "MN30-P05": {
        "nidanaId": "release",
        "pathFactors": ["正業", "正精進"],
        "reason": "善行を目的とせず手段として、上へ離す",
        "section": "戒具足でも止まらず",
        "category": "action",
    },
    "MN30-P06": {
        "nidanaId": "feeling",
        "pathFactors": ["正定", "正念"],
        "reason": "定の快さの受に「心材ではない」と付ける",
        "section": "定具足でも止まらず",
        "category": "concentration",
    },
    "MN30-P07": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "『知っている』が観察を止めていないか見直す",
        "section": "智見より上·勝れた法",
        "category": "view",
    },
    "MN30-P08": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正見"],
        "reason": "心材＝解脱へ向けた一歩を踏む",
        "section": "心材を知る",
        "category": "effort",
    },
    "MN30-P09": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "執着を枝葉と見分け、心材は解脱と見る",
        "section": "不動の心の解脱",
        "category": "view",
    },
    "MN30-P10": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "枝葉で止まった箇所を認め、明日一歩進む",
        "section": "夜·心材まで",
        "category": "view",
    },
}

CHINESE = {
    "MN30-P01": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-related-nidana",
        "text": "（對照表: 北傳無相当。パーリはピンガラコッチャの六師証知の問いを置き法を説く——漢にこの導入はない。）",
        "satLocus": "大正蔵 T2.759（類縁EA43.4）",
        "note": "六師問·法を説けはパーリ固有。漢は提婆達多の利養を機縁とする。",
    },
    "MN30-P02": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-leaves",
        "text": "往詣大樹……持枝葉而還。今此比丘亦復如是，貪著利養……則不果其願。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "枝葉＝利養で願不果。中阿含無相当。",
    },
    "MN30-P03": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-related-dukkha",
        "text": "（パーリの出家動機＝一切苦蘊の作終結。漢EAは提婆達多·求樹の譬喩が中心で、同文の出家動機は薄い。）",
        "satLocus": "大正蔵 T2.759b（類縁）",
        "note": "苦蘊終結の出家動機はパーリ側が詳しい。",
    },
    "MN30-P04": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-boast",
        "text": "貪著利養，由此利養，向他自譽，毀呰他人，比丘所行宜，則不果其願。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "自譽毀他＝枝葉。",
    },
    "MN30-P05": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-sila",
        "text": "自稱說：『我是持戒之人，彼是犯戒之士。』比丘所願者而不果獲……。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "持戒で止ま·自譽＝嫩芽を誤る側。パーリは上へ精進せよと説く。",
    },
    "MN30-P06": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-samadhi",
        "text": "好修三昧……自譽：『我今得定，餘人無定。』比丘所應行法亦不果獲。",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "定で自譽＝皮を誤る側。",
    },
    "MN30-P07": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-panna",
        "text": (
            "漸行智慧。夫智慧者，於此法中最為第一。"
            "（パーリは智見より上として初禅〜想受滅を列挙——漢にこの系列はない。）"
        ),
        "satLocus": "大正蔵 T2.759c 提婆達",
        "note": "漢は智慧第一。禅定·想受滅の列挙はパーリ固有。",
    },
    "MN30-P08": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-root",
        "text": "望其實，捨其枝葉，取其根持還。智者見已……：『此人別其根。』",
        "satLocus": "大正蔵 T2.759b 提婆達",
        "note": "漢は根。パーリは心材＝不動心解脱。",
    },
    "MN30-P09": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-goal",
        "text": "戒律之法者，世俗常數；三昧成就者，亦是世俗常數……智慧成就者，此是第一之義。",
        "satLocus": "大正蔵 T2.759c 提婆達",
        "note": "途中を世俗とし第一義へ。パーリ結は不動心解脱が心材。",
    },
    "MN30-P10": {
        "status": "mapped",
        "pin": "増壹阿含43.4・提婆達（T125）／類縁",
        "t26": "EA43.4-review",
        "text": "「智慧最為上，無憂無所慮，久畢獲等見，斷於生死有。」",
        "satLocus": "大正蔵 T2.759c 提婆達",
        "note": "第一義へ進む——夜の見直しの類縁。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "對照表は北傳無相当。SC類縁は増壹阿含43.4（MN29と共有）。法雨道場對照表参照。",
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
    old_path = DATA / "majjhima" / "mn030.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 11):
        pid = f"MN30-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 30",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・心材の喩えの小経／パーリMN30）",
                    "locus": f"中部・心材の喩えの小経（MN30）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 心材喩小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第30経・心材喩小経（心材の喩えの小経）"
    SHORT = "心材喩小経（心材の喩えの小経）"
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
            "pathLabel": "議論を置き、自分の心の状態に触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の心の観方を変える",
            "toNext": "触のあと、定の快さの受が見える",
            "todayObserve": OBSERVE["MN30-P01"],
            "todayAction": actions["MN30-P01"],
            "when": ["議論より心を観た"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN30-P01"][:40] + "…",
            "secondaryObserve": "法を聞け",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "concentration", "nidanaLabel": "受ける",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "定の快さの受に「心材ではない」と付ける",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、集中の快さの受が立つ",
            "toNext": "受に乗ると成果·執着の欲しがりへ",
            "todayObserve": OBSERVE["MN30-P06"],
            "todayAction": actions["MN30-P06"],
            "when": ["定の快さに心材ではないと付けた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN30-P06"][:40] + "…",
            "secondaryObserve": "皮≠心材",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "成果·執着を枝葉か心材か見分ける",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、成果への欲しがりが立つ",
            "toNext": "止めないと他者軽蔑の掴みへ",
            "todayObserve": OBSERVE["MN30-P02"],
            "todayAction": actions["MN30-P02"],
            "when": ["心材か枝葉か問うた", "枝葉と見分けた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN30-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN30-P09"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "他者への軽蔑の掴みを問う",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、自讃·他毀の掴みが手前",
            "toNext": "掴むと苦の集まりが見える",
            "todayObserve": OBSERVE["MN30-P04"],
            "todayAction": actions["MN30-P04"],
            "when": ["軽蔑していないか問うた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN30-P04"][:40] + "…",
            "secondaryObserve": "自讃他毀",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "苦を集まりの一部と認め、終止を思い出す",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、苦の集まりが見える",
            "toNext": "見れば、戒·定で止まらず上へ離す",
            "todayObserve": OBSERVE["MN30-P03"],
            "todayAction": actions["MN30-P03"],
            "when": ["苦の集まりと認めた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN30-P03"][:40] + "…",
            "secondaryObserve": "作終結を思い出す",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "途中段階で止まらず、心材＝解脱へ離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、目的と手段を分けて離す",
            "toNext": "離せば、智見·夜の見直しへ",
            "todayObserve": OBSERVE["MN30-P05"],
            "todayAction": actions["MN30-P05"],
            "when": ["目的か手段か見分けた", "心材へ一歩踏んだ"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN30-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN30-P08"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "『知っている』と枝葉で止まった箇所を見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの心材の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN30-P07"],
            "todayAction": actions["MN30-P07"],
            "when": ["知っているで止まったか", "枝葉で止まった夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN30-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN30-P10"],
        },
    ]

    out = {
        "chapter": 30,
        "sutta": 30,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：心材の喩えの小経）",
        "suttas": ["MN 30 心材喩小経（心材の喩えの小経）"],
        "source": {
            "primary": "パーリ・中部第30経（心材喩小経／心材の喩えの小経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN30（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝對照表は北傳無相当；SC類縁は増壹阿含43.4提婆達（T125）。"
                "ピンガラコッチャに心材喩を説き、利得·戒·定·智見で止まらず、智見より上の禅定系列を経て"
                "不動の心の解脱＝心材·終極へ導く。（MN29は提婆達多離反後の誡め、本経は婆羅門への法説。）"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・心材の喩えの小経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 増壹阿含・提婆達（T2.759a）／類縁",
                    "url": SAT_URL,
                    "note": "對照表: 北傳無相当。SC類縁EA43.4（利養·戒·定·智慧）",
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
            "focusReason": "心材喩小経は利得·戒·定·智見で止まらず、より上·勝れた法へ精進し不動の心の解脱＝心材へ離すのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn030.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 30:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(30, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 10
    assert all(p["id"] == f"MN30-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/10; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
