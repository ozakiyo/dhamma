#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn019.json (双考経／二種の思考の経) to match MN1–18 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0589a12"
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
    "MN19-P01": (
        "比丘たちよ、正覚より、まさしく、過去において、〔いまだ〕現正覚していない、まさしく、菩薩として存しているわたしに、この〔思い〕が有りました。"
        "『それなら、さあ、わたしは、二種に為しては二種に為して、思考（尋）のうちに住むのだ』と。"
        "……欲望の思考……憎悪の思考……悩害の思考……これを、一つの部分と為し、"
        "……離欲の思考……憎悪なき思考……悩害なき思考……これを、第二の部分と為しました。"
    ),
    "MN19-P02": (
        "……欲望の思考が生起します。……憎悪の思考が生起します。……悩害の思考が生起します。"
        "……『そして、それは、まさに、自己にたいする加害〔の思い〕のためにもまた等しく転起し、"
        "他者にたいする加害〔の思い〕のためにもまた等しく転起し、両者にたいする加害〔の思い〕のためにもまた等しく転起し、"
        "智慧を止滅させるものであり、悩苦の徒党であり、涅槃ならざるものを等しく転起させるものである』〔と〕。"
    ),
    "MN19-P03": (
        "……『自己にたいする加害〔の思い〕のために等しく転起する』ともまた、わたしが深慮していると、〔欲望の思考は〕滅至します。"
        "……『他者にたいする……』……『両者にたいする……』……"
        "『智慧を止滅させるものであり、悩苦の徒党であり、涅槃ならざるものを等しく転起させるものである』ともまた、わたしが深慮していると、〔欲望の思考は〕滅至します。"
    ),
    "MN19-P04": (
        "……離欲の思考が生起します。……『そして、それは、まさに、まさしく、自己にたいする加害〔の思い〕のために等しく転起せず、"
        "他者にたいする加害〔の思い〕のために等しく転起せず、両者にたいする加害〔の思い〕のために等しく転起せず、"
        "智慧を増大させるものであり、悩苦ならざるものの徒党であり、涅槃を等しく転起させるものである』〔と〕。"
    ),
    "MN19-P05": (
        "比丘たちよ、もし、比丘が、離欲の思考を、多く、刻々に思考し、刻々に想念し、欲望の思考を捨棄したなら、"
        "離欲の思考を多く為したなら、彼の、その心は、離欲の思考に傾きます。"
        "……憎悪なき思考を……悩害なき思考を……多く為したなら、彼の、その心は、悩害なき思考に傾きます。"
    ),
    "MN19-P06": (
        "比丘たちよ、それで、まさに、わたしは、生起しては生起した欲望の思考を、まさしく、捨棄しながら、まさしく、除去しながら、まさしく、その終息を為しました。"
        "（憎悪の思考・悩害の思考についても同様に、捨棄し、除去し、終息を為しました。）"
    ),
    "MN19-P07": (
        "比丘たちよ、まさしく、このように、まさに、わたしは、諸々の善ならざる法（性質）の危険と卑賎と汚染を、"
        "諸々の善なる法（性質）の離欲と福利と浄化の側面を、見ました。"
    ),
    "MN19-P08": (
        "比丘たちよ、比丘が、多く、刻々に思考し、刻々に想念する、まさしく、そのたびごとに、そのとおり、そのとおりに、心の誘導が有ります。"
        "比丘たちよ、もし、比丘が、欲望の思考を、多く……離欲の思考を捨棄したなら……彼の、その心は、欲望の思考に傾きます。"
    ),
    "MN19-P09": (
        "しかしながら、また、まさに、わたしが、長々と、刻々に思考し、刻々に想念していると、身体は疲弊するであろう。"
        "身体が疲弊しているとき、心は乱されるであろう。心が乱されたとき、心は、禅定から遠く離れている』と。"
        "比丘たちよ、それで、まさに、わたしは、まさしく、内に、心を、確立させ、静止させ、専一に作り為し、定めます。"
        "それは、何を因とするのですか。『わたしの心が乱されてはいけない』と〔思うからです〕。"
    ),
    "MN19-P10": (
        "比丘たちよ、もし、比丘が、悩害なき思考を、多く、刻々に思考し、刻々に想念し、悩害の思考を捨棄したなら、"
        "悩害なき思考を多く為したなら、彼の、その心は、悩害なき思考に傾きます。"
        "……憎悪なき思考を多く為したなら、彼の、その心は、憎悪なき思考に傾きます。"
    ),
    "MN19-P11": (
        "比丘たちよ、『平安で、安穏で、喜悦に至るべき道』とは、まさに、これは、聖なる八つの支分ある道の同義語です。"
        "それは、すなわち、この、正しい見解であり、正しい思惟であり、正しい言葉であり、正しい行業であり、"
        "正しい生き方であり、正しい努力であり、正しい気づきであり、正しい禅定です。"
        "……『悪しき道』とは、まさに、これは、八つの支分ある誤った道の同義語です。"
    ),
    "MN19-P12": (
        "比丘たちよ、これらの木の根元があります。これらの空家があります。"
        "比丘たちよ、瞑想しなさい。〔気づきを〕怠ってはいけません。のちに後悔ある者たちと成ってはいけません。"
        "これは、あなたたちへの、わたしたちの教示です。"
    ),
    "MN19-P13": (
        "比丘たちよ、かくのごとく、まさに、わたしによって、平安で、安穏で、喜悦に至るべき道は開かれ、悪しき道は閉ざされ、"
        "〔囮の〕雄獣は取り去られ、〔囮の〕雌獣は放逐されました。"
        "……『それなら、さあ、わたしは、二種に為しては二種に為して、思考（尋）のうちに住むのだ』と。"
    ),
}

OBSERVE = {
    "MN19-P01": (
        "正覚以前——思考を二種に分けて住む。欲·瞋·害と離欲·無瞋·無害。"
        "朝、浮かんだ思いに「善/不善」のラベルを一つ付ける。"
    ),
    "MN19-P02": (
        "欲·瞋·害の思考は自他・両者の加害、智慧を止め、涅槃ならざるものを転起させる——"
        "悪意·嫉妬·怒りを行動に移す前に一度止める。"
    ),
    "MN19-P03": (
        "自害·他害·両者害、智慧止滅、悩苦の徒党と深慮すれば、不善の思考は滅至する——"
        "反芻の害を具体的に数えてみる。"
    ),
    "MN19-P04": (
        "離欲の思考は自他を害せず、智慧を増大し、涅槃を転起させる——"
        "最初に浮かんだ善い思いを一つ行動に移す。"
    ),
    "MN19-P05": (
        "離欲·無瞋·無害を多く想念すれば、心はその思考に傾く——"
        "善い思いを一つ選び、意図的に育てる。"
    ),
    "MN19-P06": (
        "生起した欲·瞋·害の思考を、捨棄し、除去し、終息を為す——"
        "反芻が来たら「善でない考え」と名づけ、呼吸三回で手放す。"
    ),
    "MN19-P07": (
        "不善法の危険·卑賎·汚染を見、善法の離欲·福利·浄化の側面を見る——"
        "反芻が来たら「これ過害·汚れ」と一瞬見て、善い考えに置き換える。"
    ),
    "MN19-P08": (
        "多く刻々に思考すれば、そのとおりに心が誘導される——欲思考を多くすれば欲に傾く。"
        "批判の思いが来たら「これ心を欲考えに傾ける」と認める。"
    ),
    "MN19-P09": (
        "長々と想念すれば身体が疲弊し、心が乱れ、禅定から遠ざかる——内に心を確立し静止し専一にする。"
        "反芻が続くとき、身体の疲れを感じたら呼吸で心を一度静める。"
    ),
    "MN19-P10": (
        "悩害なき·憎悪なき思考を多くすれば、心はそこに傾く——"
        "無害・不瞋の思いを一つ意識的に増やす。"
    ),
    "MN19-P11": (
        "平安·安穏·喜悦の道＝八支聖道。悪しき道＝八邪道——"
        "今日の行動一つを八正道のどれかと結びつける。"
    ),
    "MN19-P12": (
        "木の根元・空家で瞑想し、怠らず、のちに後悔ある者と成るな——"
        "夜、不善の考えを一つ認め、善い考えに置き換えて眠る。"
    ),
    "MN19-P13": (
        "平安の道は開かれ、悪しき道は閉ざされた——思考を二種に分けて住む。"
        "夜、反芻を一つ認め、善い考えまたは正しい見で手放して眠る。"
    ),
}

PRACTICE = {
    "MN19-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正思惟"],
        "reason": "朝、浮かんだ思考に触れ、善/不善を分ける",
        "section": "二種に分ける",
        "category": "intention",
    },
    "MN19-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "欲·瞋·害の思考の欲しがりを行動の前に止める",
        "section": "欲·瞋·害",
        "category": "intention",
    },
    "MN19-P03": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "自他の加害と涅槃ならざる転起を深慮し滅至させる",
        "section": "自他の害",
        "category": "view",
    },
    "MN19-P04": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正業"],
        "reason": "離欲の思考を行動に移し不善から離す",
        "section": "離欲·行動",
        "category": "intention",
    },
    "MN19-P05": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正精進"],
        "reason": "善い思考を多く想念し心を善に傾ける",
        "section": "善を育てる",
        "category": "intention",
    },
    "MN19-P06": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "生起した不善思考を捨棄·除去·終息する",
        "section": "捨棄·除去",
        "category": "effort",
    },
    "MN19-P07": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "不善の危険と善の福利の受を見て置き換える",
        "section": "危険·福利",
        "category": "view",
    },
    "MN19-P08": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正念"],
        "reason": "多く想念すれば心が傾く掴みを認める",
        "section": "心の誘導",
        "category": "intention",
    },
    "MN19-P09": {
        "nidanaId": "feeling",
        "pathFactors": ["正定", "正念"],
        "reason": "身疲·心乱の受を見て内に心を静止し専一にする",
        "section": "身疲·内定",
        "category": "concentration",
    },
    "MN19-P10": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正精進"],
        "reason": "無害·無瞋を増やし害の欲しがりを弱める",
        "section": "無害·無瞋",
        "category": "intention",
    },
    "MN19-P11": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正思惟"],
        "reason": "今日の行を八正道に結び、平安の道を開く",
        "section": "八正道",
        "category": "view",
    },
    "MN19-P12": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正定"],
        "reason": "夜に不善思考を善に置き換え、怠らず眠る",
        "section": "木下·空家",
        "category": "mindfulness",
    },
    "MN19-P13": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "二種の思考と平安の道を振り返り手放す",
        "section": "道を開く",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN19-P01": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-dvedha",
        "text": "我本未覺無上正盡覺時，作如是念：『我寧可別諸念作二分，欲念、恚念、害念作一分，無欲念、無恚念、無害念復作一分。』",
        "satLocus": "大正蔵 T1.589a 念経",
        "note": "別諸念作二分＝二種に分ける。",
    },
    "MN19-P02": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-akusala",
        "text": "生欲念，我即覺生欲念，自害、害他、二俱害，滅慧、多煩勞、不得涅槃。……復生恚念、害念……。",
        "satLocus": "大正蔵 T1.589a 念経",
        "note": "欲·恚·害念＝欲望·憎悪·悩害の思考。",
    },
    "MN19-P03": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-parinama",
        "text": "覺自害、害他、二俱害，滅慧、多煩勞、不得涅槃，便速滅。",
        "satLocus": "大正蔵 T1.589a 念経",
        "note": "覺→速滅＝深慮して滅至。",
    },
    "MN19-P04": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-nekkhamma",
        "text": "生無欲念，我即覺生無欲念，不自害、不害他，亦不俱害，修慧、不煩勞而得涅槃。……便速修習廣布。",
        "satLocus": "大正蔵 T1.589b 念経",
        "note": "無欲念＝離欲の思考。",
    },
    "MN19-P05": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-bahulikata",
        "text": "若比丘多念無欲念者，則捨欲念，以多念無欲念故，心便樂中。若比丘多念無恚念、無害念者……心便樂中。",
        "satLocus": "大正蔵 T1.589c 念経",
        "note": "多念→心便樂中＝傾く。",
    },
    "MN19-P06": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-pajahati",
        "text": "我生欲念，不受、斷、除、吐，生恚念、害念，不受、斷、除、吐。",
        "satLocus": "大正蔵 T1.589a–b 念経",
        "note": "不受斷除吐＝捨棄·除去·終息。",
    },
    "MN19-P07": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-adinava",
        "text": "所以者何？我見因此故，必生無量惡不善之法。……我亦如是……不受、斷、除、吐。",
        "satLocus": "大正蔵 T1.589b 念経",
        "note": "見必生惡不善＝危険·汚染を見る。",
    },
    "MN19-P08": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-nati",
        "text": "比丘者，隨所思、隨所念，心便樂中。若比丘多念欲念者，則捨無欲念，以多念欲念故，心便樂中。",
        "satLocus": "大正蔵 T1.589b 念経",
        "note": "心便樂中＝心の誘導·傾向。",
    },
    "MN19-P09": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-kayakilanta",
        "text": "多思念者，身定憙忘，則便損心，我寧可治內心，常住在內止息，一意得定，令不損心。",
        "satLocus": "大正蔵 T1.589b 念経",
        "note": "身損心→治內心止息一意得定。",
    },
    "MN19-P10": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-avyapada",
        "text": "若比丘多念無恚念、無害念者，則捨恚念、害念，以多念無恚念、無害念故，心便樂中。",
        "satLocus": "大正蔵 T1.589c 念経",
        "note": "無恚·無害念の多念。",
    },
    "MN19-P11": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-atthangika",
        "text": "開平正路，閉塞惡道者，是三善念：無欲念、無恚念、無害念也。……復更有道，謂八正道，正見乃至正定是為八。……復更有惡道，謂八邪道，邪見乃至邪定是為八。",
        "satLocus": "大正蔵 T1.590a 念経",
        "note": "八正道·八邪道。",
    },
    "MN19-P12": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-rukkhamula",
        "text": "汝等亦當復自作，至無事處山林樹下空安靜處，宴坐思惟，勿得放逸，勤加精進，無令後悔。此是我之教勅，是我訓誨。",
        "satLocus": "大正蔵 T1.590a 念経",
        "note": "樹下空安靜處·勿放逸·無令後悔。",
    },
    "MN19-P13": {
        "status": "mapped",
        "pin": "中阿含102・念経（T26）",
        "t26": "T26-102-summary",
        "text": "比丘！我為汝等開平正路，閉塞惡道，填平坑壍，除却守人。……我寧可別諸念作二分……。",
        "satLocus": "大正蔵 T1.589a–590a 念経",
        "note": "開正路·閉惡道＋二分の総括。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部19経と中阿含102念経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn019.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 14):
        pid = f"MN19-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 19",
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
                    "locus": f"中部・二種の思考の経（MN19）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 双考経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第19経・双考経（二種の思考の経）"
    SHORT = "双考経（二種の思考の経）"
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
            "id": "contact", "weekday": 1, "categoryId": "intention", "nidanaLabel": "接触",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "朝、浮かんだ思考に触れ、善/不善を分ける",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の思考の接触を変える",
            "toNext": "触のあと、欲·瞋·害の受と欲しがりが見える",
            "todayObserve": OBSERVE["MN19-P01"],
            "todayAction": actions["MN19-P01"],
            "when": ["思いが浮かんだ朝", "善/不善を分けた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN19-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN19-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "不善の危険と身疲の受を見て、善に置き換え内定する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、過害や疲れの受が立つ",
            "toNext": "受に乗ると欲·害の欲しがりへ",
            "todayObserve": OBSERVE["MN19-P07"],
            "todayAction": actions["MN19-P07"],
            "when": ["過害を見た", "身が疲れた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN19-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN19-P09"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "欲·瞋·害を止め、無害·無瞋を増やす",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、不善思考の欲しがりが立つ",
            "toNext": "止めないと多く想念する掴みへ",
            "todayObserve": OBSERVE["MN19-P02"],
            "todayAction": actions["MN19-P02"],
            "when": ["怒りが浮かんだ", "無害を増やした"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN19-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN19-P10"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "多く想念すれば心が傾く掴みを認める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、反芻の掴みが手前",
            "toNext": "掴むと自他の加害の苦が見える",
            "todayObserve": OBSERVE["MN19-P08"],
            "todayAction": actions["MN19-P08"],
            "when": ["批判を繰り返した", "心の傾きを認めた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN19-P08"][:40] + "…",
            "secondaryObserve": "心便樂中",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "自他の加害と涅槃ならざる転起を深慮し滅至させる",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、自他の害が見える",
            "toNext": "見れば、捨棄と善の育成へ向き直る",
            "todayObserve": OBSERVE["MN19-P03"],
            "todayAction": actions["MN19-P03"],
            "when": ["反芻の害を数えた", "深慮して滅した"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN19-P03"][:40] + "…",
            "secondaryObserve": "自害害他二俱害",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "intention", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正思惟", "正精進"], "pathFactorIds": ["intention", "effort"],
            "pathLabel": "不善を捨棄し、離欲·善思考を育て行動に移す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、手放しと善の育成へ",
            "toNext": "離せば、夜の八正道の見直しへ",
            "todayObserve": OBSERVE["MN19-P06"],
            "todayAction": actions["MN19-P06"],
            "when": ["不善を手放した", "善を育てた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN19-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN19-P05"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "八正道に結び、不善を善に置き換え振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の思考は、朝からの二種分けの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN19-P12"],
            "todayAction": actions["MN19-P12"],
            "when": ["一日を閉じるとき", "八正道に結んだ日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN19-P12"][:40] + "…",
            "secondaryObserve": OBSERVE["MN19-P11"],
        },
    ]

    out = {
        "chapter": 19,
        "sutta": 19,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：二種の思考の経）",
        "suttas": ["MN 19 双考経（二種の思考の経）"],
        "source": {
            "primary": "パーリ・中部第19経（双考経／二種の思考の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含102念経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・二種の思考の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・念経（T1.589a）",
                    "url": SAT_URL,
                    "note": "欲恚害念と無欲等。對照表: 法雨道場（雙想經）",
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
            "focusNodeId": "craving",
            "focusReason": "二種の思考の経は欲·瞋·害の思考と離欲·無瞋·無害を分け、不善の欲しがりを捨て善に傾けるのが主題。既定の焦点は欲しがる。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn019.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 19:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(19, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 13
    assert all(p["id"] == f"MN19-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/13; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
