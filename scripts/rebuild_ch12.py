#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch12.json (自己品) to match ch1–ch11 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-12"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0566"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap12/"
)

QUOTES = {
    157: "もし、自己を、愛しいものと知るなら、それを、善く守られたものとして、守るがよい。〔若年と壮年と老年の〕三つのなかの、どれか一つの時期を、賢者は、〔眠らずに〕起きているもの（若年・壮年・老年という、人生における三つの区分の、すくなくとも、どれか一つにおいて、人は目覚めるべきである）。",
    158: "第一に、自己こそを、適所において確たるものとするがよい。そこで、他者に教え示すがよい。賢者は、〔世事には〕汚されないもの。",
    159: "すなわち、他者に教え示すように、もし、そのとおり、自己に為すなら（自己みずから実践するなら）、〔自己が〕善く調御された者は、まさに、〔他者を〕調御するであろう。なぜなら、自己は、まさに、調御し難くあるからである。",
    160: "まさに、自己は、自己の主（あるじ）。まさに、他者の誰が、主として存するというのだろう。まさに、善く調御された自己によって、得難き主を得る。",
    161: "まさに、自己によって為された悪が、自己から生じ自己から発生する〔悪〕が、思慮浅き者を打ち砕く──金剛（ダイアモンド）が、石から作られる宝珠を〔打ち砕く〕ように。",
    162: "蔓草が、〔それに〕覆われたサーラ〔樹〕を〔打ち負かす〕ように、彼に、徹底して下劣な戒があるなら、あたかも、〔彼の〕敵が、彼に求めるように、彼は、そのように、自己に為す（自滅する）。",
    163: "為し易きは、諸々の善ならざること、そして、自己にとって諸々の益ならざること。それが、まさに、かつまた、〔自己にとって〕益となり、かつまた、善となるなら、それは、まさに、最高に為し難い。",
    164: "すなわち、阿羅漢（人格完成者）たちの教えを、法（真理）によって生きる聖者たちの〔教えを〕、悪しき見解に依存して、思慮浅き者が非難するなら、カッタカ〔草〕の諸果のように、自己を滅ぼすために、〔悪しき報いが〕結果する。",
    165: "まさに、自己によって為された悪は、自己によって汚れ、自己によって為されなかった悪は、まさしく、自己によって清まる。清浄と清浄ならざるは、各自のこと。他者が他者を清めることはない（自己が自己を清める）。",
    166: "たとえ、他者の義（道理）が多くあるも、自己の義（道理）を失わないように。自己の義（道理）を証知して、自らの義（道理）を追求する者として存するように。",
}

OBSERVE = {
    157: "もし自己の愛すべきを知らば、よくこれを獲るべし。 賢者は夜の三分（人生の三期）の中、一分は覚醒してあるべし。",
    158: "先ず自己を適所に置き、然る後他を教えよ。 〔かかる〕賢者は悩むことなからん。",
    159: "もし他を教うる如く自ら行わば、〔自ら〕よく調御（ちょうご）せられて、〔他を〕調御（ちょうご）し得べし。 実に自己は調御（ちょうご）し難ければなり。",
    160: "自己の依所は自己のみなり。 他にいかなる依所あらんや。 自己のよく調御（ちょうご）せられたる時、人は得難き依所を獲得す。",
    161: "自己のなせる悪業は、自己より生じ、自己より起れるものにして、愚者を粉砕すること、金剛石の宝石に於けるが如し。",
    162: "破戒甚だしき人は、あたかもつる草がその覆える沙羅樹に〔枯死を望む〕が如く自己に破滅を望む仇敵の意に従って、自ら挙動す（すなわち破滅す）。",
    163: "不善にして自己に害あることは行い易く、〔自己に〕益ありてかつ善なることは極めて行い難し。",
    164: "正法に従って生くる尊き阿羅漢の教えを、邪見に拠りて謗る愚者は、自己の破滅の為に〔業〕果を結ぶこと、あたかもカッタカ草（葦の一種）の果が〔実りてかえって自ら滅ぶが〕如し。",
    165: "自ら悪をなして自ら汚れ、自ら悪をなさずして自ら浄し。 各々自ら浄となり不浄となる。 人は他を浄むることあたわず。",
    166: "たといいかに大〔事〕なりとも、他の為に尽くして自己の義務を忽諸（こっしょ）にすべからず。 自己の義務を知りて常に自己の義務に専心なるべし。",
}

CHINESE = {
    157: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-001",
          "text": "自愛身者，慎護所守，希望欲解，學正不寐。", "satLocus": "大正蔵 T4.566c 愛身品第1頌"},
    158: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-002",
          "text": "身為第一，常自勉學，利乃誨人，不惓則智。", "satLocus": "大正蔵 T4.566c 愛身品第2頌"},
    159: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-003",
          "text": "學先自正，然後正人，調身入慧，必遷為上。", "satLocus": "大正蔵 T4.566c 愛身品第3頌"},
    160: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-004",
          "text": "身不能利，安能利人？心調體正，何願不至？", "satLocus": "大正蔵 T4.566c 愛身品第4頌"},
    161: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-005",
          "text": "本我所造，後我自受，為惡自更，如剛鑽珠。", "satLocus": "大正蔵 T4.566c 愛身品第5頌"},
    162: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-006",
          "text": "人不持戒，滋蔓如藤，逞情極欲，惡行日增。", "satLocus": "大正蔵 T4.566c 愛身品第6頌"},
    163: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-007",
          "text": "惡行危身，愚以為易，善最安身，愚以為難。", "satLocus": "大正蔵 T4.566c 愛身品第7頌"},
    164: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-008",
          "text": "如真人教，以道法身，愚者疾之，見而為惡，行惡得惡，如種苦種。", "satLocus": "大正蔵 T4.566c 愛身品第8頌"},
    165: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-009",
          "text": "惡自受罪，善自受福，亦各須熟，彼不自代，習善得善，亦如種甜。", "satLocus": "大正蔵 T4.566c 愛身品第9頌"},
    166: {"status": "mapped", "pin": "愛身品（T210 第20品）", "t210": "T210-20-010",
          "text": "自利利人，益而不費，欲知利身，戒聞為最。", "satLocus": "大正蔵 T4.566c 愛身品第10頌"},
}

VERSE_PRACTICE = {
    157: {"nidanaId": "contact", "pathFactors": ["正念", "正精進"], "reason": "自己を愛し守るなら、人生の一期は覚醒してあれ"},
    158: {"nidanaId": "contact", "pathFactors": ["正念", "正業"], "reason": "まず自己を適所に置き、然る後他を教える"},
    159: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "他に教えるように自ら行い、自己を調御する"},
    160: {"nidanaId": "feeling", "pathFactors": ["正念", "正見"], "reason": "自己の依所は自己のみ、調御された自己が得難き依所"},
    161: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "自己の悪業が、金剛の如く自己を粉砕する"},
    162: {"nidanaId": "clinging", "pathFactors": ["正業", "正念"], "reason": "破戒はつる草のように自己を滅ぼす"},
    163: {"nidanaId": "craving", "pathFactors": ["正精進", "正念"], "reason": "不善は易く善は難いからこそ、善を選ぶ"},
    164: {"nidanaId": "clinging", "pathFactors": ["正語", "正念"], "reason": "正法を謗れば、自己破滅の業果を結ぶ"},
    165: {"nidanaId": "review", "pathFactors": ["正念", "正業"], "reason": "自ら汚れ自ら浄まる、人は他を浄められない"},
    166: {"nidanaId": "review", "pathFactors": ["正念", "正精進"], "reason": "他のために自己の義務を軽んじるな"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP12-P01", 157), ("DP12-P02", 157),
    ("DP12-P03", 158), ("DP12-P04", 158),
    ("DP12-P05", 159), ("DP12-P06", 159),
    ("DP12-P07", 160), ("DP12-P08", 160),
    ("DP12-P09", 161), ("DP12-P10", 161),
    ("DP12-P11", 162),
    ("DP12-P12", 163), ("DP12-P13", 163),
    ("DP12-P14", 164),
    ("DP12-P15", 165), ("DP12-P16", 165),
    ("DP12-P17", 166), ("DP12-P18", 166),
]


def chinese_block(verse: int) -> dict:
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    c.setdefault(
        "note",
        "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
    )
    return c


def main() -> None:
    old = json.loads((DATA / "ch12.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 自己の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第１２章・自己品 第{verse}偈（#ch02-12）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第12章・自己品（自己の章）"
    SHORT = "自己品（自己の章）"
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
            "pathLabel": "自己を守る接触として、まず自分を適所に置く",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の自己護持になる",
            "toNext": "自己への接触のあと、依所を求める受が来る",
            "todayObserve": OBSERVE[157],
            "todayAction": actions["DP12-P01"],
            "when": ["朝の始まり", "人に教えようとした"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[157][:40] + "…",
            "secondaryObserve": "先ず自己を適所に置き、然る後他を教えよ",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "不安の受を、調御された自己という依所で受ける",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、誰かに頼りたい受が立ち上がる",
            "toNext": "受けた不安を、楽な不善への欲しがりへ落とさない",
            "todayObserve": OBSERVE[160],
            "todayAction": actions["DP12-P07"],
            "when": ["誰かに頼り過ぎている", "不安を感じた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[160][:40] + "…",
            "secondaryObserve": "調御された自己が、得難き依所となる",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "effort", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "易い不善を欲しがらず、難い善を選ぶ",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、楽で有害な選択への欲しがりへ",
            "toNext": "止めないと破戒・謗法の掴みへ進む",
            "todayObserve": OBSERVE[163],
            "todayAction": actions["DP12-P12"],
            "when": ["楽な悪い選択をしたくなった", "善が難しいと感じた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[163][:40] + "…",
            "secondaryObserve": "不善は易く、善は極めて行い難し",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "action", "nidanaLabel": "掴む",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "破戒と謗法を掴まず、自己を滅ぼす蔓を断つ",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、破戒・誹謗として掴む手前",
            "toNext": "掴むと自己の悪業が苦となって返る",
            "todayObserve": OBSERVE[162],
            "todayAction": actions["DP12-P11"],
            "when": ["戒を破りそう", "正法を軽んじそう"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[162][:40] + "…",
            "secondaryObserve": "正法を謗れば、自己破滅の業果を結ぶ",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "自己の悪業が自己を粉砕すると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、自己の業が苦として熟す",
            "toNext": "見れば、自己調御と清浄へ向き直る",
            "todayObserve": OBSERVE[161],
            "todayAction": actions["DP12-P09"],
            "when": ["苦しんでいる", "外を責めそうになった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[161][:40] + "…",
            "secondaryObserve": "自己の苦は自己の業から来る",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "mindfulness", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "他に教えるように自ら行い、自己調御で離す",
            "chapterHint": SHORT,
            "fromPrev": "自己を疎かにする流れが苦を加速させる",
            "toNext": "離すと、清浄と義務の見直しへつながる",
            "todayObserve": OBSERVE[159],
            "todayAction": actions["DP12-P05"],
            "when": ["人に勧めたことを自分がしていない", "自己調御を取り戻したい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[159][:40] + "…",
            "secondaryObserve": "自己は調御し難し。まず自ら行う",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "自ら浄めたか汚したか、自己の義務を見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、自己が自己を清めた跡",
            "toNext": "見直しが、翌朝の自己護持になる",
            "todayObserve": OBSERVE[165],
            "todayAction": actions["DP12-P15"],
            "when": ["一日を閉じるとき", "自己の義務を確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[165][:40] + "…",
            "secondaryObserve": "他のために自己の義務を軽んじるな",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 12,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第12章（自己品／自己の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210愛身品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・自己の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１２章・自己品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・愛身品（T4.566c）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "自己品は自ら浄め自ら汚す見直しが中心。既定の焦点は見直す。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch12.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch12.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 13):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch12", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 18
    assert all(p["id"] == f"DP12-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(157, 167))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    print("OK")


if __name__ == "__main__":
    main()
