#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn035.json (薩遮迦小経／薩遮迦との小経) to match MN1–34 source alignment.

実経: 薩遮迦は五蘊＝我と主張。王は領内に自在だが、色が我なら「色を斯くあれ」と自在か——
黙して金剛神に脅され答う。無常→苦→「我所·我·我我所」に相応せず。
苦に近づき執着する者は苦を究竟し得ない。弟子は一切蘊を「我所に非ず」と見る。
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0035a01"
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
    "MN35-P01": (
        "阿湿波誓は説く——『色·受·想·行·識は無常である。"
        "色·受·想·行·識は無我である。一切の行は無常、一切の法は無我である』と。"
        "（朝、五蘊に我なしを一つ意識する。）"
    ),
    "MN35-P02": (
        "色は無常か、常住か。……無常ならば、苦か楽か。……"
        "無常·苦·変壊の法であるのに、『これは私のもの、これは私、これは私の我である』と見るに相応しいか——"
        "「いいえ、尊師。」受·想·行·識についても、また同様である。"
    ),
    "MN35-P03": (
        "『受は私の我である』と言う者よ——あなたは、その受に対して自在であるか。"
        "『私の受は斯くあれ。斯くあらざれ』と。"
        "……受は無常·苦·変壊——『我所·我·我我所』に相応せず。"
        "（感じた受を苦·楽·不苦不楽の一つとして見る。）"
    ),
    "MN35-P04": (
        "薩遮迦は言う——『色は人の我であり……識は人の我である。"
        "それらに依って善悪が生じる』と。"
        "世尊は問う——『色は私の我である』と言う者よ、あなたは色に自在であるか。"
        "『私の色は斯くあれ。斯くあらざれ』と。——「いいえ、尊師。」"
    ),
    "MN35-P05": (
        "苦に近づき、苦に依り、苦に執着し、"
        "『これは私のもの、これは私、これは私の我である』と見る者——"
        "自ら苦を究竟し、苦を離れられるであろうか。"
        "……あなたもまた、このように苦に執着しているのではないか。"
    ),
    "MN35-P06": (
        "Dummukhaが『薩遮迦の逃げ道は折られた』と言うと、"
        "薩遮迦は言う——『私はあなたと語っていない。瞿曇尊者と語っている』と。"
        "（論争は相手を辱めるためではなく、我見を破るため。）"
    ),
    "MN35-P07": (
        "私の弟子は、過去·未来·現在、内·外、麤·細、劣·勝、遠·近——"
        "一切の色を、正慧をもって『これは私のものではない。これは私ではない。"
        "これは私の我ではない』と見る。……受·想·行·識についても、また同様である。"
        "（五蘊の一つを観察し、執着を手放す。）"
    ),
    "MN35-P08": (
        "一切の色……一切の識を、『我所に非ず·我に非ず·我我所に非ず』と見る——"
        "このように見て、執着なく解脱する。"
        "（就寝前、「私·私のもの」を想した瞬間を一つ認め、手放す。）"
    ),
    "MN35-P09": (
        "世尊は薩遮迦に説く——"
        "色·受·想·行·識は無常·無我である。"
        "王は領内に自在でも、蘊が我ならば自在であるはず——しかるに自在ではない。"
    ),
    "MN35-P10": (
        "受は無常か。……無常ならば苦か。……"
        "無常·苦·変壊の法を、『これは私のもの……』と見るに相応しいか——"
        "「いいえ。」（楽受も無常。執着すれば苦に近づく。）"
    ),
    "MN35-P11": (
        "苦に近づき執着し、『これは私の我である』と見る者は、苦を究竟し得ない。"
        "（苦受も無常。「我が苦」と取れば、苦が増す。）"
    ),
}

OBSERVE = {
    "MN35-P01": (
        "五蘊は無常·無我——朝、五蘊に我なしを一つ意識する。"
        "朝、今日「五蘊に我なし」を一つ意識する。"
    ),
    "MN35-P02": (
        "無常·苦·変壊——『我所·我·我我所』に非ず。体調·感情を蘊と見る。"
        "今日、体調·感情を「我」ではなく「蘊」と一瞬見る。"
    ),
    "MN35-P03": (
        "受に自在なし。苦·楽·不苦不楽として見る。"
        "今日、感じた受を「苦·楽·不苦不楽」の一つとして見る。"
    ),
    "MN35-P04": (
        "蘊＝我と主張しても自在はない——「我ある」という確信を問う。"
        "今日、「我ある」という確信を一度問う。"
    ),
    "MN35-P05": (
        "我見で苦に執着すれば苦は究竟しない——苦を我見の結果と見る。"
        "今日の苦を「我見の結果」と一度見る。"
    ),
    "MN35-P06": (
        "論争は我見を破るため。相手を破るためではない。"
        "今日、議論で「相手を破る」より「我見を破る」を意識する。"
    ),
    "MN35-P07": (
        "一切蘊を『我所に非ず』と見て執着を手放す。"
        "今日、五蘊の一つを観察し、執着を手放す。"
    ),
    "MN35-P08": (
        "夜、「私·私のもの」を想した瞬間を認め手放す。"
        "就寝前、今日「私・私のもの」を想した瞬間を一つ認め、手放す。"
    ),
    "MN35-P09": (
        "薩遮迦小経——自在論証と無常·苦·非我。"
        "今日、五蘊に「我なし」を一つ思い出す。"
    ),
    "MN35-P10": (
        "楽受も無常·苦·変壊——執着すれば苦に近づく。"
        "快い受を「楽受·無常」と一度見る。"
    ),
    "MN35-P11": (
        "苦受も無常。「我が苦」と取れば苦が増す。"
        "苦い受を「苦受·無常」と見て、「私の苦」と取らない。"
    ),
}

PRACTICE = {
    "MN35-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "朝、五蘊無我に触れて一つ意識する",
        "section": "五蘊·無我の教え",
        "category": "view",
    },
    "MN35-P02": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "体調·感情への我の掴みを蘊と見る",
        "section": "我所·我·我我所に非ず",
        "category": "view",
    },
    "MN35-P03": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "受を苦·楽·捨の一つとして見る",
        "section": "受に自在なし",
        "category": "mindfulness",
    },
    "MN35-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "「我ある」への欲しがり·確信を一度問う",
        "section": "自在の問い",
        "category": "view",
    },
    "MN35-P05": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦を我見の結果として見る",
        "section": "苦への執着",
        "category": "view",
    },
    "MN35-P06": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正見"],
        "reason": "相手攻撃を離れ、我見を破る語へ",
        "section": "論争の目的",
        "category": "speech",
    },
    "MN35-P07": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正精進"],
        "reason": "五蘊への掴みを観察し手放す",
        "section": "一切蘊を正慧に見る",
        "category": "view",
    },
    "MN35-P08": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "夜、我所の想いを認め手放す",
        "section": "夜の無我",
        "category": "view",
    },
    "MN35-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "五蘊我なしの教えに触れ思い出す",
        "section": "導·薩遮迦",
        "category": "mindfulness",
    },
    "MN35-P10": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "楽受を無常として見る",
        "section": "楽受·無常",
        "category": "mindfulness",
    },
    "MN35-P11": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦受を無常と見、「我が苦」と取らない",
        "section": "苦受·我所を取らず",
        "category": "view",
    },
}

CHINESE = {
    "MN35-P01": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-anicca",
        "text": "『……無常、苦、空、非我。』」薩遮尼揵子聞此語，心不喜……。",
        "satLocus": "大正蔵 T2.35b 薩遮",
        "note": "阿湿波誓の無常·苦·空·非我。",
    },
    "MN35-P02": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-not-mine",
        "text": "（無常·苦ならば我所·我·我我所に相応せず——パーリと同型の問い。）",
        "satLocus": "大正蔵 T2.36 薩遮",
        "note": "非我所·非我。",
    },
    "MN35-P03": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-feeling",
        "text": "汝言……受……是我人……。（自在を問い、受についても答を迫る。）",
        "satLocus": "大正蔵 T2.35c–36a 薩遮",
        "note": "受是我——自在なし。",
    },
    "MN35-P04": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-self",
        "text": "如是色是我人，善惡從生；受、想、行、識是我人，善惡從生。……佛告……：「汝言色是我人……」",
        "satLocus": "大正蔵 T2.35c–36a 薩遮",
        "note": "色是我人——世尊が問い返す。",
    },
    "MN35-P05": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-dukkha",
        "text": "（苦に執着し我所と見れば苦を究竟し得ない——パーリの問い。漢も論破の流れで対応。）",
        "satLocus": "大正蔵 T2.36 薩遮",
        "note": "我見·苦の執着。",
    },
    "MN35-P06": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-debate",
        "text": "（離車との応酬·論議の場面。要点は師への問いであり他者攻撃ではない。）",
        "satLocus": "大正蔵 T2.35b–c 薩遮",
        "note": "論議の場——我見を破る。",
    },
    "MN35-P07": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-disciple",
        "text": "（弟子は一切色等を正慧に非我所·非我と見る——パーリ詳説。漢も観法で対応。）",
        "satLocus": "大正蔵 T2.36–37 薩遮",
        "note": "正慧に非我。",
    },
    "MN35-P08": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-release",
        "text": "（非我所と見て執着なく——解脱の道。パーリ: not mine… freed。）",
        "satLocus": "大正蔵 T2.36–37 薩遮",
        "note": "夜の手放しの根拠。",
    },
    "MN35-P09": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-vajira",
        "text": "時，有金剛力鬼神持金剛杵……：「世尊再三問，汝何故不答？」……薩遮……默然。",
        "satLocus": "大正蔵 T2.36a 薩遮",
        "note": "三度問い·金剛神——自在論証の転換。",
    },
    "MN35-P10": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-sukha",
        "text": "無常、苦、空、非我。……（受·楽についても無常·苦の見。）",
        "satLocus": "大正蔵 T2.35b 薩遮",
        "note": "楽も無常·苦·非我。",
    },
    "MN35-P11": {
        "status": "mapped",
        "pin": "雑阿含110・薩遮（T99）",
        "t26": "SA110-dukkha-vedana",
        "text": "無常、苦、空、非我。……（苦受を我所と取れば増す——パーリの苦執着。）",
        "satLocus": "大正蔵 T2.35b·36 薩遮",
        "note": "苦受·我所を取らず。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部35経と雑阿含110薩遮の内容対応（EA37.10も類縁）。對照表: 法雨道場。",
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
    old_path = DATA / "majjhima" / "mn035.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN35-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 35",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・薩遮迦との小経／パーリMN35）",
                    "locus": f"中部・薩遮迦との小経（MN35）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 薩遮迦小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第35経・薩遮迦小経（薩遮迦との小経）"
    SHORT = "薩遮迦小経（薩遮迦との小経）"
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
            "id": "contact", "weekday": 1, "categoryId": "view", "nidanaLabel": "接触",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "五蘊無我の教えに触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の無我の一歩を変える",
            "toNext": "触のあと、受の分類が見える",
            "todayObserve": OBSERVE["MN35-P01"],
            "todayAction": actions["MN35-P01"],
            "when": ["五蘊我なしを意識した", "教えを思い出した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN35-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN35-P09"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "受を苦·楽·捨·無常として見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、苦·楽の受が立つ",
            "toNext": "受に乗ると「我ある」への欲しがりへ",
            "todayObserve": OBSERVE["MN35-P03"],
            "todayAction": actions["MN35-P03"],
            "when": ["受を分類した", "楽受を無常と見た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN35-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN35-P10"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "「我ある」への確信·欲しがりを問う",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、我への欲しがりが立つ",
            "toNext": "止めないと蘊への掴みへ",
            "todayObserve": OBSERVE["MN35-P04"],
            "todayAction": actions["MN35-P04"],
            "when": ["我ある確信を問うた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN35-P04"][:40] + "…",
            "secondaryObserve": "色に自在なし",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "蘊への我の掴みを観察し手放す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、我所の掴みが手前",
            "toNext": "掴むと我見の苦が見える",
            "todayObserve": OBSERVE["MN35-P02"],
            "todayAction": actions["MN35-P02"],
            "when": ["蘊と見た", "執着を手放した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN35-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN35-P07"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "苦を我見の結果と見、「我が苦」と取らない",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、我見の苦が見える",
            "toNext": "見れば、論争の目的を正し離す",
            "todayObserve": OBSERVE["MN35-P05"],
            "todayAction": actions["MN35-P05"],
            "when": ["我見の結果と見た", "我が苦と取らなかった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN35-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN35-P11"],
        },
        {
            "id": "release", "weekday": 6, "categoryId": "speech", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正語", "正見"], "pathFactorIds": ["speech", "view"],
            "pathLabel": "相手攻撃を離れ、我見を破る語へ",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、論争の目的を正し離す",
            "toNext": "離せば、夜の我所の見直しへ",
            "todayObserve": OBSERVE["MN35-P06"],
            "todayAction": actions["MN35-P06"],
            "when": ["我見を破るを意識した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN35-P06"][:40] + "…",
            "secondaryObserve": "相手を破るに非ず",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "「私·私のもの」を想した瞬間を認め手放す",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの無我の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN35-P08"],
            "todayAction": actions["MN35-P08"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN35-P08"][:40] + "…",
            "secondaryObserve": "非我所と見る",
        },
    ]

    out = {
        "chapter": 35,
        "sutta": 35,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：薩遮迦との小経）",
        "suttas": ["MN 35 薩遮迦小経（薩遮迦との小経）"],
        "source": {
            "primary": "パーリ・中部第35経（薩遮迦小経／薩遮迦との小経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN35（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT雑阿含110薩遮（T99；EA37.10も類縁）。"
                "薩遮迦の五蘊＝我を、自在の問いと無常·苦·非我で破る。"
                "苦に執着し我所と見れば苦を究竟し得ない。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・薩遮迦との小経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 雑阿含・薩遮（T2.35a）",
                    "url": SAT_URL,
                    "note": "色是我人·自在·金剛神·非我。對照表: 法雨道場（SA110）",
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
            "focusNodeId": "clinging",
            "focusReason": "薩遮迦小経は五蘊を我·我所と掴む見を、自在の問いと無常·苦·非我で破るのが主題。既定の焦点は掴む。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn035.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 35:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(35, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN35-P{i:02d}" for i, p in enumerate(pairs, 1))
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
