#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch15.json (安楽品) to match ch1–ch14 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-15"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0567"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap15/"
)

QUOTES = {
    197: "極めて安楽に、まさに、〔わたしたちは〕生きる──怨みある者たちのなかにいながら、怨みなき者たちとして。〔わたしたちは〕住む──怨みある人間たちのなかにいながら、怨みなき者たちとして。",
    198: "極めて安楽に、まさに、〔わたしたちは〕生きる──病いある者たちのなかにいながら、病いなき者たちとして。〔わたしたちは〕住む──病いある人間たちのなかにいながら、病いなき者たちとして。",
    199: "極めて安楽に、まさに、〔わたしたちは〕生きる──焦りある者たちのなかにいながら、焦りなき者たちとして。〔わたしたちは〕住む──焦りある人間たちのなかにいながら、焦りなき者たちとして。",
    200: "極めて安楽に、まさに、〔わたしたちは〕生きる──すなわち、わたしたちには、何も存在しない（無一物である）。〔わたしたちは〕喜悦を食物とする者たちとして〔世に〕有るのだ──あたかも、光音天〔の神々〕たちのように。",
    201: "勝者は、怨恨を生み、敗者は、苦痛のうちに臥す。勝敗を捨棄して、寂静となった者は、安楽のうちに臥す。",
    202: "貪欲（貪）に等しい火は、存在しない。憤怒（瞋）に等しい〔悪しき〕賽の目（罪悪）は、存在しない。〔五つの心身を構成する〕範疇（蘊）に等しい苦痛は、存在しない。寂静〔の境処〕の他に安楽は、存在しない。",
    203: "飢え（日々空腹になること）は、最高の病である。諸々の〔迷いの生存を〕形成する働き（行：生の輪廻を施設し造作する働き）は、最高の苦痛である。このことを事実のとおりに知って、涅槃は、最高の安楽である。",
    204: "無病は、最高の利得である。知足は、最高の財産である。信頼は、最高の親族である。涅槃は、最高の安楽である。",
    205: "遠離の味わいを飲み干して、さらに、寂止の味わいを〔飲み干して〕、懊悩なく悪なき者と成る──法（真理）の喜悦の味わいを飲み干しながら。",
    206: "聖者たちと会見あることは、善きことである。〔彼らと〕共に住むのは、常に、安楽である。愚者たちと会見なくあることで、まさしく、常に、安楽の者として存するであろう。",
    207: "まさに、愚者と集いあつまり〔世を〕歩む者は、長時にわたり、憂い悲しむ。愚者たちと共に住むのは、朋友ならざる者（敵対者）と〔共に住む〕ように、一切時において、苦痛である。しかしながら、慧者は、親族たちの集いのように、共に住むのが安楽である。",
    208: "まさに、それゆえに──かつまた、慧者としてあり、かつまた、智慧ある者としてあり、かつまた、多聞の者としてあり、忍耐強さを戒とし、〔善き〕掟ある、聖者と、そのような者である、正なる人士と、思慮深き者と、彼と親しくするべきである──星の道に、月が〔従い行く〕ように。",
}

OBSERVE = {
    197: "我らは、怨憎者の中にありて怨憎なく、実に安楽に生きん。 我らは怨憎を抱く人々の中にありて怨憎なく住せん。",
    198: "我らは、苦悩者の中にありて苦悩なく、実に安楽に生きん。 我らは苦悩ある人々の中にありて苦悩なく住せん。",
    199: "我らは、貪欲者の中にありて貪欲なく、実に安楽に生きん。 我らは貪欲ある人々の中にありて貪欲なく住せん。",
    200: "我らは、何物をも有せずして、安楽に生きん。 我らは光音天神の如く、歓喜を以て食となさん。",
    201: "勝利は怨憎を生じ、敗者は苦しみて臥す。 寂静に帰せる人は、勝敗を捨てて安楽に臥す。",
    202: "貪欲に等しき火なく、憎悪に等しき罪なく、〔五〕蘊（肉体的存在）に比すべき苦なく、寂静に勝る安楽なし。",
    203: "飢餓は最大の病にして、万象は最大の苦なり。 如実にこれを知れば、最上安楽の涅槃〔あり〕。",
    204: "無病は最上の利にして、満足は最上の財なり。 信頼は最上の親族にして、涅槃は最上の安楽なり。",
    205: "孤独の甘味と寂静の甘味とを飲みたる者は、法悦の甘味を飲みつつ畏怖を去り、悪を離る。",
    206: "聖者を見るは善く、〔これと〕共に住するは常に安楽なり。 愚者を見ざれば常に安楽なるべし。",
    207: "愚者と共に道を行く者は、実に長途の間憂愁す。 愚者と共に住するは、敵と共に〔住する〕が如く常に苦なり。 賢者は共に住して楽しく、あたかも親族との会合の如し。",
    208: "賢者、智者、博学の人、堅忍なる人、持戒者、聖者、この如き善良・賢明なる人に随うべし、あたかも月の星道に〔従う〕如く。",
}

CHINESE = {
    197: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-001",
          "text": "我生已安，不慍於怨，眾人有怨，我行無怨。", "satLocus": "大正蔵 T4.567c 安寧品第1頌"},
    198: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-002",
          "text": "我生已安，不病於病，眾人有病，我行無病。", "satLocus": "大正蔵 T4.567c 安寧品第2頌"},
    199: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-003",
          "text": "我生已安，不慼於憂，眾人有憂，我行無憂。", "satLocus": "大正蔵 T4.567c 安寧品第3頌"},
    200: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-004",
          "text": "我生已安，清淨無為，以樂為食，如光音天。", "satLocus": "大正蔵 T4.567c 安寧品第4頌"},
    201: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-006",
          "text": "勝則生怨，負則自鄙，去勝負心，無爭自安。", "satLocus": "大正蔵 T4.567c 安寧品第6頌"},
    202: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-007",
          "text": "熱無過婬，毒無過怒，苦無過身，樂無過滅。", "satLocus": "大正蔵 T4.567c 安寧品第7頌"},
    203: {"status": "mapped", "pin": "泥洹品（T210 第36品）", "t210": "T210-36-003",
          "text": "飢為大病，行為最苦，已諦知此，泥洹最樂。", "satLocus": "大正蔵 T4.570c 泥洹品第3頌",
          "note": "パーリ安楽の章203はT210安寧品ではなく泥洹品に対応（蘇錦坤對照表）。"},
    204: {"status": "mapped", "pin": "泥洹品（T210 第36品）", "t210": "T210-36-002",
          "text": "無病最利，知足最富，厚為最友，泥洹最快。", "satLocus": "大正蔵 T4.570c 泥洹品第2頌",
          "note": "パーリ安楽の章204はT210安寧品ではなく泥洹品に対応（蘇錦坤對照表）。"},
    205: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ安楽の章205はT210に対応なし（蘇錦坤對照表）。"},
    206: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-010",
          "text": "見聖人快，得依附快，得離愚人，為善獨快。", "satLocus": "大正蔵 T4.567c 安寧品第10頌"},
    207: {"status": "mapped", "pin": "安寧品（T210 第23品）", "t210": "T210-23-012",
          "text": "依賢居快，如親親會，近仁智者，多聞高遠。", "satLocus": "大正蔵 T4.567c 安寧品第12頌"},
    208: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ安楽の章208はT210に対応なし（蘇錦坤對照表）。出曜経・法集要頌経側に近い文言あり。"},
}

VERSE_PRACTICE = {
    197: {"nidanaId": "contact", "pathFactors": ["正念", "正思惟"], "reason": "怨みある中に、怨みなき者として住む"},
    198: {"nidanaId": "feeling", "pathFactors": ["正念", "正見"], "reason": "苦悩ある中に、苦悩なき者として住む"},
    199: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "貪欲ある中に、貪欲なき者として住む"},
    200: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "無一物にして安楽、歓喜を食とする"},
    201: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "勝敗を捨て、寂静に帰して安楽に臥す"},
    202: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "貪欲の火・憎悪の罪より、寂静の安楽へ"},
    203: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "飢餓と行は最大の苦、涅槃は最上の安楽"},
    204: {"nidanaId": "release", "pathFactors": ["正念", "正見"], "reason": "無病・知足・信頼・涅槃が最上"},
    205: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "孤独と寂静の甘味を飲み、法悦で悪を離る"},
    206: {"nidanaId": "contact", "pathFactors": ["正念", "正命"], "reason": "聖者と共に住し、愚者を見ざれば安楽"},
    207: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "愚者と共に住すれば苦、賢者と共に楽"},
    208: {"nidanaId": "review", "pathFactors": ["正念", "正精進"], "reason": "賢者・聖者に、月が星道に従う如く随う"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP15-P01", 197), ("DP15-P02", 197),
    ("DP15-P03", 198),
    ("DP15-P04", 199),
    ("DP15-P05", 200), ("DP15-P06", 200),
    ("DP15-P07", 201), ("DP15-P08", 201),
    ("DP15-P09", 202), ("DP15-P10", 202),
    ("DP15-P11", 203),
    ("DP15-P12", 204), ("DP15-P13", 204),
    ("DP15-P14", 205), ("DP15-P15", 205),
    ("DP15-P16", 206),
    ("DP15-P17", 207),
    ("DP15-P18", 208), ("DP15-P19", 208), ("DP15-P20", 208),
]


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
        )
    return c


def main():
    old = json.loads((DATA / "ch15.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        pairs.append({
            "id": pid,
            "category": LABEL_TO_ID[factors[0]],
            "verse": verse,
            "observe": OBSERVE[verse],
            "action": actions[pid],
            "quote": QUOTES[verse],
            "nidanaId": vp["nidanaId"],
            "pathFactors": factors,
            "pathReason": vp["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー",
                    "locus": f"小部・ダンマパダ 安楽の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第１５章・安楽品 第{verse}偈（#ch02-15）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第15章・安楽品（安楽の章）"
    SHORT = "安楽品（安楽の章）"
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
            "pathLabel": "怨みある場に触れても、怨みなき者として住む",
            "chapterHint": SHORT,
            "fromPrev": "前夜の良き交わりの見直しが、今朝の安楽の土台になる",
            "toNext": "接触のあと、苦悩・焦りの受が立ち上がる",
            "todayObserve": OBSERVE[197],
            "todayAction": actions["DP15-P01"],
            "when": ["恨みのある場にいる", "朝の始まり"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[197][:40] + "…",
            "secondaryObserve": "聖者と共に住し、愚者を見ざれば安楽",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "苦悩の受を、苦悩なき心で受け取る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、苦悩・病の受が来る",
            "toNext": "受けた不快を、貪欲の欲しがりへ落とさない",
            "todayObserve": OBSERVE[198],
            "todayAction": actions["DP15-P03"],
            "when": ["つらい状況にいる", "周囲が苦しんでいる"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[198][:40] + "…",
            "secondaryObserve": "苦悩ある中に、苦悩なく住する",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "貪欲ある中でも、貪欲なく住する",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、もっと欲しがる焦りへ落ちる",
            "toNext": "止めないと勝敗・憎悪の掴みへ進む",
            "todayObserve": OBSERVE[199],
            "todayAction": actions["DP15-P04"],
            "when": ["周囲が欲しがっている", "欲が燃えた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[199][:40] + "…",
            "secondaryObserve": "貪欲の火より、寂静の安楽へ",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "勝敗と愚者への掴みを捨て、寂静へ向かう",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、勝ち負け・悪い交わりとして掴む手前",
            "toNext": "掴むと怨憎と憂愁の苦が太る",
            "todayObserve": OBSERVE[201],
            "todayAction": actions["DP15-P07"],
            "when": ["勝ち負けにこだわった", "愚者と長く交わった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[201][:40] + "…",
            "secondaryObserve": "愚者と共に住すれば苦、賢者と共に楽",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "飢餓と行は最大の苦、涅槃は最上の安楽と知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、飢えと執着の苦が熟す",
            "toNext": "見れば、知足と寂静へ向き直る",
            "todayObserve": OBSERVE[203],
            "todayAction": actions["DP15-P11"],
            "when": ["満たされない苦しさ", "執着が重い"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[203][:40] + "…",
            "secondaryObserve": "如実にこれを知れば、最上安楽の涅槃あり",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "mindfulness", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "無一物と知足で、貪欲から離す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがる流れが安楽を奪う",
            "toNext": "離すと、法悦と良き交わりの見直しへつながる",
            "todayObserve": OBSERVE[200],
            "todayAction": actions["DP15-P05"],
            "when": ["持っていないものに囚われた", "足るを知りたい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[200][:40] + "…",
            "secondaryObserve": "無病・知足・信頼・涅槃が最上",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "孤独・寂静の甘味と、賢者に随ったかを見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の交わりは、安楽か憂愁かの跡",
            "toNext": "見直しが、翌朝の怨みなき接触になる",
            "todayObserve": OBSERVE[205],
            "todayAction": actions["DP15-P14"],
            "when": ["一日を閉じるとき", "良き交わりを確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[205][:40] + "…",
            "secondaryObserve": "賢者・聖者に、月が星道に従う如く随う",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 15,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第15章（安楽品／安楽の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210安寧品、一部泥洹品・未対応あり）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・安楽の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１５章・安楽品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・安寧品（T4.567c）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "craving",
            "focusReason": "安楽品は貪欲ある中でも貪欲なく住することが中心。既定の焦点は欲しがる。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch15.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch15.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 16):
        d = json.loads((DATA / f"ch{ch_id}.json").read_text(encoding="utf-8"))
        by_path = defaultdict(list)
        for p in d["pairs"]:
            labels = set(p.get("pathFactors") or [])
            cat = p.get("category")
            for lab, pid in LABEL_TO_ID.items():
                if lab in labels or cat == pid:
                    by_path[pid].append(p["id"])
        for pid in PATH_ORDER:
            ids = sorted(set(by_path[pid]), key=lambda x: int(x.split("-P")[1]))
            if not ids:
                continue
            entries[pid].append({
                "collectionId": "dhammapada",
                "collectionName": "ダンマパダ",
                "chapterId": ch_id,
                "shortTitle": d["shortTitle"],
                "title": d["title"],
                "pairCount": len(ids),
                "pairIds": ids,
            })

    psi = {"version": 1, "scope": "dhammapada-ch1-ch15", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 20
    assert all(p["id"] == f"DP15-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(197, 209))
    p14 = next(p for p in pairs if p["id"] == "DP15-P14")
    p18 = next(p for p in pairs if p["id"] == "DP15-P18")
    assert p14["alignment"]["chinese"]["status"] == "unmapped"
    assert p18["alignment"]["chinese"]["status"] == "unmapped"
    print("OK")


if __name__ == "__main__":
    main()
