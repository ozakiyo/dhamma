#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn020.json (考想息止経／思考の様相の経) to match MN1–19 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0588a05"
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
    "MN20-P01": (
        "比丘たちよ、卓越の心（瞑想）に専念する比丘によって、五つの形相が、〔その〕時〔その〕時に〔しかるべく〕意が為されるべきです。"
        "どのようなものが、五つのものなのですか。"
    ),
    "MN20-P02": (
        "（１）……その形相に意を為していると、諸々の悪しき善ならざる思考が──欲〔の思い〕を伴ったものもまた、憤怒を伴ったものもまた、迷妄を伴ったものもまた──生起するなら、"
        "……その形相から、善なるものを伴った他の形相に意が為されるべきです。"
        "……すなわち、諸々の悪しき善ならざる思考は……捨棄され……滅至します。"
        "……内に、心は、確立し、静止し、専一と成り、定められます。"
    ),
    "MN20-P03": (
        "（２）……その比丘によって、それらの思考の危険（患・過患）が近しく注視されるべきです。"
        "『かくのごとくもまた、わたしの諸々の思考は、善ならざるものである。"
        "かくのごとくもまた、わたしの諸々の思考は、財貨を有するもの（世俗のもの）である。"
        "かくのごとくもまた、わたしの諸々の思考は、苦痛の報い（異熟）あるものである』と。"
    ),
    "MN20-P04": (
        "（３）……その比丘によって、それらの思考の、思念なく意を為さないことが惹起されるべきです。"
        "彼が、それらの思考の、思念なく意を為さないことを惹起していると、"
        "すなわち、諸々の悪しき善ならざる思考は……捨棄され……滅至します。"
    ),
    "MN20-P05": (
        "（４）……その比丘によって、それらの思考の、思考を形成する働き（行）の様相に意が為されるべきです。"
        "……それは、たとえば、また、人が、急いで赴くとします。……『……ゆっくりと赴くのだ』……『……立つのだ』……『……坐るのだ』……『……横になるのだ』と。"
        "……振る舞いの道の粗雑なるもの粗雑なるものを回避して、振る舞いの道の繊細なるもの繊細なるものを営為します。"
    ),
    "MN20-P06": (
        "（５）……その比丘によって、歯のうえに歯を置いて、舌で上顎に触れて、"
        "心によって、心が、制御されるべきであり、圧迫されるべきであり、撃滅されるべきです。"
        "……力ある人が、より力の弱い人を……掴んで、制御し、圧迫し、撃滅するように……。"
    ),
    "MN20-P07": (
        "……それは、たとえば、また、能ある、あるいは、石工が、あるいは、石工の内弟子が、"
        "繊細な楔で、粗雑な楔を、打ち砕き、引き抜き、取り出すように……"
        "その形相から、善なるものを伴った他の形相に意が為されるべきです。"
        "（危険の注視→思念なく意を為さない→行の様相→心で心を制御——順に進む。）"
    ),
    "MN20-P08": (
        "……それは、たとえば、また、年少にして、若く、派手好きの、あるいは、女が、あるいは、男が、"
        "あるいは、蛇の死骸を、あるいは、犬の死骸を、あるいは、人間の死骸を、首に掛けられたなら、"
        "苦悩し、自責し、忌避するように……それらの思考の危険が近しく注視されるべきです。"
    ),
    "MN20-P09": (
        "……それは、たとえば、また、眼ある人が、眼の視野にやってきた諸々の色形を見ないことを欲する者として存するなら、"
        "彼は、あるいは、〔眼を〕閉じるであろうし、あるいは、他を顧みるであろうように……"
        "それらの思考の、思念なく意を為さないことが惹起されるべきです。"
    ),
    "MN20-P10": (
        "比丘たちよ、この者は、『比丘として、諸々の思考の教相の道における自在者であり、"
        "その思考を望むなら、その思考を思考するであろう。その思考を望まないなら、その思考を思考しないであろう。"
        "渇愛を断ち、束縛するものを還転させた。〔我想の〕思量の寂止あることから、正しく苦しみの終極を為した』〔と〕説かれます。"
    ),
    "MN20-P11": (
        "……それらの思考の、思念なく意を為さないことが惹起されるべきです。"
        "彼が、それらの思考の、思念なく意を為さないことを惹起していると、"
        "すなわち、諸々の悪しき善ならざる思考は……捨棄され……滅至します。"
        "……内に、心は、確立し、静止し、専一と成り、定められます。"
    ),
    "MN20-P12": (
        "……その形相から、善なるものを伴った他の形相に意が為されるべきです。"
        "彼が、その形相から、善なるものを伴った他の形相に意を為していると、"
        "すなわち、諸々の悪しき善ならざる思考は……捨棄され……滅至します。"
        "……内に、心は、確立し、静止し、専一と成り、定められます。"
    ),
}

OBSERVE = {
    "MN20-P01": (
        "卓越の心に専念する比丘は、五つの形相を時々意に為す——"
        "反芻が止まらないとき、まず別の善い対象に意識を移す。"
    ),
    "MN20-P02": (
        "第一——不善思考が起きたら、その形相から善を伴った他の形相に意を為す——"
        "反芻の対象と反対の善い縁想を一つ選び、意識を移す。"
    ),
    "MN20-P03": (
        "第二——思考の危険を注視する。不善・世俗・苦痛の報い——"
        "反芻の害を具体的に数えてみる。"
    ),
    "MN20-P04": (
        "第三——それらの思考に、思念なく意を為さない——"
        "一度「この反芻には応答しない」と決めて黙る。"
    ),
    "MN20-P05": (
        "第四——思考を形成する働きの様相に意を為す。急ぎ→徐行→立→坐→臥のように粗を細へ——"
        "「なぜこの思いが来たか」を静かに調べ、呼吸で鎮める。"
    ),
    "MN20-P06": (
        "第五——歯を合わせ舌を上顎に付け、心で心を制御し圧迫し撃滅する——"
        "反芻が激しいとき、身体を一度締め、呼吸で心を抑える。"
    ),
    "MN20-P07": (
        "五法は順に——繊細な楔で粗雑な楔を抜き取る石工の如く——"
        "善相→過害→念じない→行の様相→心で抑えるの順で試す。"
    ),
    "MN20-P08": (
        "過害を見る——首に死骸を掛けられた若者が厭い忌避する如く——"
        "反芻を「これ厭うべきもの」と見て、一歩距離を置く。"
    ),
    "MN20-P09": (
        "思念なく意を為さない——眼ある人が色を見たくなければ閉眼するか他を顧みる如く——"
        "小さな反芻を「見ない」と決め、最初の段階で対処する。"
    ),
    "MN20-P10": (
        "思考の教相の道における自在者——望む思考を思考し、望まない思考を思考しない——"
        "就寝前、反芻を五呼吸で手放し、善い縁想を一つ置く。"
    ),
    "MN20-P11": (
        "思念なく意を為さない——反芻を語って強めない——"
        "今日、反芻を他人に話して強めない。"
    ),
    "MN20-P12": (
        "善を伴った他の形相——あらかじめ用意しておく——"
        "反芻の代わりに使う善い縁想を一つ決め、メモしておく。"
    ),
}

PRACTICE = {
    "MN20-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正定"],
        "reason": "反芻に触れ、五形相の第一として善対象へ移す",
        "section": "五つの形相",
        "category": "mindfulness",
    },
    "MN20-P02": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正念"],
        "reason": "不善形相から善形相へ意を移し思考を捨棄する",
        "section": "第一·別相",
        "category": "intention",
    },
    "MN20-P03": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "思考の危険·苦報を注視し滅至させる",
        "section": "第二·過患",
        "category": "view",
    },
    "MN20-P04": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正定"],
        "reason": "思念なく意を為さず、応答しないで滅至させる",
        "section": "第三·不念",
        "category": "mindfulness",
    },
    "MN20-P05": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正思惟"],
        "reason": "思考形成の様相を調べ、粗を細へ鎮める",
        "section": "第四·行の様相",
        "category": "mindfulness",
    },
    "MN20-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正精進", "正定"],
        "reason": "最後手段として心で心を制御し圧迫する",
        "section": "第五·心で抑える",
        "category": "effort",
    },
    "MN20-P07": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "五法を順に試し、楔で楔を抜くように離す",
        "section": "楔の喩",
        "category": "effort",
    },
    "MN20-P08": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "厭い忌避の受で過害を見て距離を置く",
        "section": "死骸の喩",
        "category": "view",
    },
    "MN20-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正定"],
        "reason": "小さな反芻の接触で閉眼·他顧のように応じない",
        "section": "閉眼の喩",
        "category": "mindfulness",
    },
    "MN20-P10": {
        "nidanaId": "review",
        "pathFactors": ["正定", "正念"],
        "reason": "夜に自在を振り返り、望まない思考を手放す",
        "section": "思考の自在",
        "category": "concentration",
    },
    "MN20-P11": {
        "nidanaId": "craving",
        "pathFactors": ["正語", "正念"],
        "reason": "語って強める欲しがりを止め、不念で離す",
        "section": "語らず強めず",
        "category": "speech",
    },
    "MN20-P12": {
        "nidanaId": "feeling",
        "pathFactors": ["正思惟", "正念"],
        "reason": "善縁想を用意し、不善が来たときの置き換え先にする",
        "section": "善相の用意",
        "category": "intention",
    },
}

CHINESE = {
    "MN20-P01": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-intro",
        "text": "若比丘欲得增上心者，當以數數念於五相。數念五相已，生不善念，即便得滅，惡念滅已，心便常住，在內止息，一意得定。",
        "satLocus": "大正蔵 T1.588a 増上心経",
        "note": "數數念五相＝五つの形相。",
    },
    "MN20-P02": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-nimitta",
        "text": "念相善相應，若生不善念者，彼因此相復更念異相善相應，令不生惡不善之念。……猶木工師……則以利斧，斫治令直。",
        "satLocus": "大正蔵 T1.588a 増上心経",
        "note": "異相善相應＝善を伴った他の形相。漢は墨繩·利斧喩。",
    },
    "MN20-P03": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-adinava",
        "text": "彼觀此念惡有災患，此念不善，此念是惡，此念智者所惡，此念若滿具者，則不得通、不得覺道、不得涅槃。",
        "satLocus": "大正蔵 T1.588a–b 増上心経",
        "note": "觀惡有災患＝危険の注視。",
    },
    "MN20-P04": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-asati",
        "text": "彼比丘不應念此念，令生惡不善念故。彼不念此念，已生不善念，即便得滅。",
        "satLocus": "大正蔵 T1.588b 増上心経",
        "note": "不應念＝思念なく意を為さない。",
    },
    "MN20-P05": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-sankhara",
        "text": "彼比丘為此念，當以思行漸減其念……猶人行道，進路急速……徐徐行……住……坐……臥……漸漸息身麤行。",
        "satLocus": "大正蔵 T1.588b–c 増上心経",
        "note": "思行漸減＝行の様相。",
    },
    "MN20-P06": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-abhiniggaha",
        "text": "齒齒相著，舌逼上齶，以心修心，受持降伏……猶二力士捉一羸人，受持降伏。",
        "satLocus": "大正蔵 T1.588c 増上心経",
        "note": "以心修心受持降伏＝心で心を制御。",
    },
    "MN20-P07": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-sequence",
        "text": "當以數數念於五相。……第一相……第二相……第三相……第四相……第五相。",
        "satLocus": "大正蔵 T1.588a–c 増上心経",
        "note": "五相を順に數數念。パーリの楔喩は漢で木工墨繩。",
    },
    "MN20-P08": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-asubha",
        "text": "猶人年少……或以死蛇、死狗、死人……繫著彼頸，彼便惡穢，不喜不樂。如是……彼觀此念，惡有災患。",
        "satLocus": "大正蔵 T1.588a–b 増上心経",
        "note": "死蛇死狗死人繫頸＝死骸の喩。",
    },
    "MN20-P09": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-cakkhuma",
        "text": "猶有目人，色在光明，而不用見，彼或閉目，或身避去。……彼不念此念，已生不善念，即便得滅。",
        "satLocus": "大正蔵 T1.588b 増上心経",
        "note": "閉目·身避＝閉眼·他顧。",
    },
    "MN20-P10": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-vasavatti",
        "text": "便得自在，欲念則念，不念則不念。若比丘欲念則念，不欲念則不念者，是謂比丘隨意諸念，自在諸念跡。",
        "satLocus": "大正蔵 T1.589a 増上心経",
        "note": "自在諸念＝思考の教相の道における自在。",
    },
    "MN20-P11": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-no-reinforce",
        "text": "彼比丘不應念此念……彼不念此念，已生不善念，即便得滅，惡念滅已，心便常住，在內止息，一意得定。",
        "satLocus": "大正蔵 T1.588b 増上心経",
        "note": "不念＝語って強めない実践。",
    },
    "MN20-P12": {
        "status": "mapped",
        "pin": "中阿含101・増上心経（T26）",
        "t26": "T26-101-prepare",
        "text": "彼因此相復更念異相善相應，令不生惡不善之念。……心便常住，在內止息，一意得定。",
        "satLocus": "大正蔵 T1.588a 増上心経",
        "note": "異相善相應の用意。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部20経と中阿含101増上心経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn020.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 13):
        pid = f"MN20-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 20",
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
                    "locus": f"中部・思考の様相の経（MN20）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 考想息止経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第20経・考想息止経（思考の様相の経）"
    SHORT = "考想息止経（思考の様相の経）"
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
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "反芻に触れ、五形相の入口で善対象へ移す",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の反芻の接触を変える",
            "toNext": "触のあと、過害と厭いの受が見える",
            "todayObserve": OBSERVE["MN20-P01"],
            "todayAction": actions["MN20-P01"],
            "when": ["反芻が始まった", "善相を用意した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN20-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN20-P09"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "厭い忌避の受で過害を見て、善縁想の置き換え先を持つ",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、厭うべき受が立つ",
            "toNext": "受に乗ると語って強める欲しがりへ",
            "todayObserve": OBSERVE["MN20-P08"],
            "todayAction": actions["MN20-P08"],
            "when": ["厭いを見た", "善相をメモした"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN20-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN20-P12"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "speech", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正語", "正念"], "pathFactorIds": ["speech", "mindfulness"],
            "pathLabel": "語って強める欲しがりを止め、不念で離す",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、話して固めたい欲しがりが立つ",
            "toNext": "止めないと心で抑え込む掴みへ",
            "todayObserve": OBSERVE["MN20-P11"],
            "todayAction": actions["MN20-P11"],
            "when": ["反芻を話したくなった", "黙って離した"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN20-P11"][:40] + "…",
            "secondaryObserve": "不應念此念",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "effort", "nidanaLabel": "掴む",
            "pathFactors": ["正精進", "正定"], "pathFactorIds": ["effort", "concentration"],
            "pathLabel": "最後手段として心で心を制御し圧迫する",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、激しい反芻の掴みが手前",
            "toNext": "掴むと苦報の患が見える（または離しへ）",
            "todayObserve": OBSERVE["MN20-P06"],
            "todayAction": actions["MN20-P06"],
            "when": ["反芻が激しかった", "歯を合わせた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN20-P06"][:40] + "…",
            "secondaryObserve": "以心修心",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "思考の危険·苦報を注視し滅至させる",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、不善·苦報の患が見える",
            "toNext": "見れば、五法の順で離しへ向き直る",
            "todayObserve": OBSERVE["MN20-P03"],
            "todayAction": actions["MN20-P03"],
            "when": ["害を数えた", "苦報を見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN20-P03"][:40] + "…",
            "secondaryObserve": "惡有災患",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "善相·不念·五法の順で不善思考を捨棄する",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、楔で楔を抜くように離す",
            "toNext": "離せば、夜の自在の見直しへ",
            "todayObserve": OBSERVE["MN20-P02"],
            "todayAction": actions["MN20-P02"],
            "when": ["善相へ移った", "五法を順に試した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN20-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN20-P07"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "行の様相を調べ、思考の自在を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の反芻は、朝からの五形相の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN20-P10"],
            "todayAction": actions["MN20-P10"],
            "when": ["一日を閉じるとき", "行の様相を調べた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN20-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN20-P05"],
        },
    ]

    out = {
        "chapter": 20,
        "sutta": 20,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：思考の様相の経）",
        "suttas": ["MN 20 考想息止経（思考の様相の経）"],
        "source": {
            "primary": "パーリ・中部第20経（考想息止経／思考の様相の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含101増上心経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・思考の様相の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・増上心経（T1.588a）",
                    "url": SAT_URL,
                    "note": "五相對治。對照表: 法雨道場（想念止息經）",
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
            "focusReason": "思考の様相の経は五つの形相で不善思考を捨棄し心を内に確立するのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn020.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 20:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(20, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 12
    assert all(p["id"] == f"MN20-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/12; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
