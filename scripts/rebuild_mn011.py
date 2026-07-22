#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn011.json (師子吼小経／小なる獅子吼の経) to match MN1–10 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0590"
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
    "MN11-P01": (
        "比丘たちよ、『まさしく、ここに、沙門があり、ここに、第二の沙門があり、ここに、第三の沙門があり、ここに、第四の沙門がある。"
        "他の沙門たちによる諸々の異論は、空無なるもの』と、比丘たちよ、このように、このことを、〔あなたたちは〕正しく獅子吼として吼え叫びなさい。"
    ),
    "MN11-P02": (
        "友よ、まさに、わたしたちには、教師にたいする浄信が存在し、法（教え）にたいする浄信が存在し、"
        "諸戒における円満成就を為す者たることが存在します。"
        "また、まさに、法（教え）を共にする者たちは、愛しく意に適う者たちです──まさしく、そして、在家者たちも、さらに、出家者たちも。"
    ),
    "MN11-P03": (
        "『友よ、目的は一つです。目的は多々にありません』と。"
        "『友よ、その目的は、貪欲を離れた者のためにあります。……憤怒を離れた者のためにあります。……迷妄を離れた者のためにあります。"
        "……渇愛を離れた者のためにあります。……執取を離れた者のためにあります。"
        "……知ある者のためにあります。……共感せず反感しない者のためにあります。"
        "……虚構なきものを喜びとし虚構なきものを喜ぶ者のためにあります』と。"
    ),
    "MN11-P04": (
        "比丘たちよ、これらの二つの見解があります。そして、生存の見解（有見）であり、さらに、非生存の見解（非有見）です。"
        "……生存の見解に固着した者たちであるなら、彼らは、非生存の見解に反感ある者たちです。"
        "……非生存の見解に固着した者たちであるなら、彼らは、生存の見解に反感ある者たちです。"
    ),
    "MN11-P05": (
        "これらの二つの見解の、そして、集起を、さらに、滅至を、そして、悦楽を、かつまた、危険を、さらに、出離を、事実のとおりに覚知しないなら、"
        "彼らは、……虚構を喜びとし虚構を喜ぶ者たちであり、……苦しみから完全に解き放たれない、と、〔わたしは〕説きます。"
    ),
    "MN11-P06": (
        "比丘たちよ、四つのものがあります。これらの執取です。"
        "欲望への執取であり、見解への執取であり、戒や掟への執取であり、自己の論への執取です。"
    ),
    "MN11-P07": (
        "これらの四つの執取は、渇愛を因縁とし、渇愛を集起とします。"
        "渇愛は、感受を因縁とし……。感受は、接触を因縁とし……。"
        "接触は、六つの〔認識の〕場所を因縁とし……〔以下、名色・識・諸行・無明に至る〕。"
    ),
    "MN11-P08": (
        "すなわち、まさに、比丘の、無明が捨棄されたものと成り、明知が生起したものと〔成ることから〕、"
        "彼は、……欲望への執取に執取せず、見解への執取に執取せず、戒や掟への執取に執取せず、自己の論への執取に執取しません。"
        "〔何も〕執取せずにいる者は、〔何も〕思い悩みません。……各自それぞれに、完全なる涅槃に到達します。"
    ),
    "MN11-P09": (
        "これらの二つの見解の……出離を、事実のとおりに覚知しないなら、"
        "彼らは、……共感し反感する者たちであり、彼らは、虚構を喜びとし虚構を喜ぶ者たちであり、"
        "彼らは、生から、老から、死から……完全に解き放たれません。"
        "『〔彼らは〕苦しみから完全に解き放たれない』と、〔わたしは〕説きます。"
    ),
    "MN11-P10": (
        "『友よ、その目的は、共感せず反感しない者のためにあります。"
        "その目的は、共感し反感する者のためにあるのではありません』と。"
        "『友よ、その目的は、虚構なきものを喜びとし虚構なきものを喜ぶ者のためにあります』と。"
    ),
    "MN11-P11": (
        "善く告げ知らされ、善く説き知らされ、出脱〔の教え〕であり、寂止のために等しく転起するものであり、"
        "正等覚者によって知らされたものである、法（教え）と律においては、"
        "教師にたいする浄信は……正しい至達あるものと告げ知らされ、……法を共にする者たちにおける愛しく意に適うことは……告げ知らされます。"
    ),
    "MN11-P12": (
        "一切の執取の遍知を説く者たちと明言している、或る沙門や婆羅門たちが存在します。"
        "彼らは、欲望への執取の遍知を報知するも、見解への執取の遍知を報知せず、戒や掟への執取の遍知を報知せず、自己の論への執取の遍知を報知しません。"
        "……阿羅漢にして正等覚者たる如来は、……欲望への執取の遍知を報知し、見解への……戒や掟への……自己の論への執取の遍知を報知します。"
    ),
}

OBSERVE = {
    "MN11-P01": (
        "正しく獅子吼せよ——ここに四沙門（四果）があり、他の異論は空無である。"
    ),
    "MN11-P02": (
        "四法——師への浄信・法への浄信・戒の円満・法を共にする者への愛敬。"
        "外道もこれを称するが、差は一切の執取の遍知にある。"
    ),
    "MN11-P03": (
        "目的は一つ——貪・瞋・痴・渇愛・執取を離れ、知あり、反感なく、虚構なきを喜ぶ者のため。"
    ),
    "MN11-P04": (
        "有見と非有見——一方に固着すれば他方に反感し、諍いが起きる。"
    ),
    "MN11-P05": (
        "二見の集・滅・味・患・出離を知らねば、虚構（戯論）を喜び、苦から解き放たれない。"
    ),
    "MN11-P06": (
        "四取——欲取・見取・戒禁取・我語取。"
    ),
    "MN11-P07": (
        "四取は渇愛を因縁とし、渇愛は受、受は触……無明に至る。"
        "執着が来たら触→受→愛→取を辿る。"
    ),
    "MN11-P08": (
        "無明を捨て明知が生じれば四取に執取せず、思い悩まない者は各自涅槃に至る。"
    ),
    "MN11-P09": (
        "二見を如実に知らぬ者は、反感と虚構を喜び、生老死の苦から解き放たれない。"
    ),
    "MN11-P10": (
        "究極の目的は、共感・反感なく、虚構なきを喜ぶ者のため——争う論者のためではない。"
    ),
    "MN11-P11": (
        "善く説かれた出脱・寂止の法と律においてのみ、四法の浄信は正しい至達となる。"
    ),
    "MN11-P12": (
        "欲取だけ知り我語取を知らぬ「一切の執取の遍知」は円満ではない。"
        "如来は四取すべてを正しく報知する。"
    ),
}

PRACTICE = {
    "MN11-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正見"],
        "reason": "異論との接触で、果に基づく獅子吼を立てる",
        "section": "獅子吼",
        "category": "speech",
    },
    "MN11-P02": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正業"],
        "reason": "四法を認めつつ、執取の遍知で差を見る",
        "section": "四法",
        "category": "view",
    },
    "MN11-P03": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正思惟"],
        "reason": "目標を執取の減る方向に置く",
        "section": "一究竟",
        "category": "view",
    },
    "MN11-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "有見・非有見の両極端に固着しない",
        "section": "二見",
        "category": "view",
    },
    "MN11-P05": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正念"],
        "reason": "見解を証明したい衝動を戯論の欲しがりと見る",
        "section": "二見·戯論",
        "category": "view",
    },
    "MN11-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "今日の執着を四取のどれかと特定する",
        "section": "四取",
        "category": "view",
    },
    "MN11-P07": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "受から渇愛・執取へ流れる縁起を辿る",
        "section": "縁起",
        "category": "mindfulness",
    },
    "MN11-P08": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "無明を捨て四取に執取せず涅槃へ",
        "section": "明知·涅槃",
        "category": "view",
    },
    "MN11-P09": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "諍いと戯論が苦から解き放たれないと見る",
        "section": "苦·不脱",
        "category": "view",
    },
    "MN11-P10": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正思惟"],
        "reason": "反感なく、相手の利益を考えてから話す",
        "section": "無憎無諍",
        "category": "speech",
    },
    "MN11-P11": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "善説の法と律を振り返り、明日も反芻する",
        "section": "正法律",
        "category": "view",
    },
    "MN11-P12": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正精進"],
        "reason": "好みの取だけ知って終わっていないか確かめる",
        "section": "一切取遍知",
        "category": "view",
    },
}

CHINESE = {
    "MN11-P01": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-roar",
        "text": "此有第一沙門第二第三第四沙門。此外更無沙門梵志。異道一切空無沙門梵志。汝等隨在衆中作如是正師子吼。",
        "satLocus": "大正蔵 T1.590c 師子吼経",
        "note": "正師子吼＝四沙門の宣言。",
    },
    "MN11-P02": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-four",
        "text": "我等信尊師信法信戒徳具足。愛敬同道恭恪奉事。……我等亦信尊師……有何勝有何意有何差別耶。",
        "satLocus": "大正蔵 T1.590c 師子吼経",
        "note": "四法と異学との差別の問い。",
    },
    "MN11-P03": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-ekanta",
        "text": "有一究竟無衆多究竟。……無欲者得究竟是……無恚……無癡……無愛無受……有慧説慧……無憎無諍者得究竟是。",
        "satLocus": "大正蔵 T1.590c–591a 師子吼経",
        "note": "一究竟＝離貪等の者のため。",
    },
    "MN11-P04": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-two-views",
        "text": "若有沙門梵志依無量見彼一切依猗二見。有見及無見也。若依有見者。彼便著有見……憎諍無見若依無見者……憎諍有見。",
        "satLocus": "大正蔵 T1.591a 師子吼経",
        "note": "有見・無見＝有見・非有見。",
    },
    "MN11-P05": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-papanca",
        "text": "不知因不知習不知滅不知盡。不知味不知患。不知出要如眞者。彼一切有欲恚有癡有愛有受無慧非説慧有憎有諍。",
        "satLocus": "大正蔵 T1.591a 師子吼経",
        "note": "味患出要を知らぬ＝戯論・諍い。",
    },
    "MN11-P06": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-upadana",
        "text": "施設斷欲受。不施設斷戒受見受我受。……施設斷欲受戒受見受我受",
        "satLocus": "大正蔵 T1.591a–b 師子吼経",
        "note": "漢訳「四受」＝パーリ四取。",
    },
    "MN11-P07": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-nidana",
        "text": "此四受何因何習從何而生以何爲本。此四受因無明習無明從無明生以無明爲本。",
        "satLocus": "大正蔵 T1.591b 師子吼経",
        "note": "漢訳は四取の本を無明に圧縮。パーリは渇愛←受←触の連鎖を詳説。",
    },
    "MN11-P08": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-nibbana",
        "text": "若有比丘無明已盡明已生者。彼便從是不復更受欲受戒受見受我受。彼不受已則不恐怖……必般涅槃。生已盡梵行已立。",
        "satLocus": "大正蔵 T1.591b 師子吼経",
        "note": "無明尽・明生→不受四取→涅槃。",
    },
    "MN11-P09": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-dukkha",
        "text": "有憎有諍。彼則不離生老病死亦不能脱愁慼啼哭憂苦懊惱不得苦邊。",
        "satLocus": "大正蔵 T1.591a 師子吼経",
        "note": "憎諍＝苦からの不脱。",
    },
    "MN11-P10": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-no-quarrel",
        "text": "無憎無諍者得究竟是。非有憎有諍者得究竟是。",
        "satLocus": "大正蔵 T1.591a 師子吼経",
        "note": "無憎無諍＝究極の条件。",
    },
    "MN11-P11": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-saddhamma",
        "text": "如是正法律若信尊師者是正是第一。若信法者是正是第一。若戒徳具足者是正是第一。若愛敬同道恭恪奉事者是正是第一。",
        "satLocus": "大正蔵 T1.591b 師子吼経",
        "note": "正法律における四法の第一。",
    },
    "MN11-P12": {
        "status": "mapped",
        "pin": "中阿含103・師子吼経（T26）",
        "t26": "T26-103-incomplete",
        "text": "施設斷欲受。不施設斷戒受見受我受。……如來……於現法中施設斷一切受。施設斷欲受戒受見受我受",
        "satLocus": "大正蔵 T1.591a–b 師子吼経",
        "note": "部分的断受≠一切受の断。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部11経と中阿含103師子吼経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn011.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 13):
        pid = f"MN11-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 11",
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
                    "locus": f"中部・小なる獅子吼の経（MN11）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 師子吼小経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第11経・師子吼小経（小なる獅子吼の経）"
    SHORT = "師子吼小経（小なる獅子吼の経）"
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
            "id": "contact", "weekday": 1, "categoryId": "speech", "nidanaLabel": "接触",
            "pathFactors": ["正語", "正見"], "pathFactorIds": ["speech", "view"],
            "pathLabel": "異論との接触で、果に基づく獅子吼を立てる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の対論の接触を変える",
            "toNext": "接触のあと、見解の受が立つ",
            "todayObserve": OBSERVE["MN11-P01"],
            "todayAction": actions["MN11-P01"],
            "when": ["異論に触れた", "教団の差を問われた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN11-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN11-P02"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "受から渇愛・執取へ流れる縁起を辿る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、受が立ち上がる",
            "toNext": "受に乗ると渇愛・戯論へ",
            "todayObserve": OBSERVE["MN11-P07"],
            "todayAction": actions["MN11-P07"],
            "when": ["見解に快・不快を感じた", "執着の流れを辿った"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN11-P07"][:40] + "…",
            "secondaryObserve": "受→渇愛→四取",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "見解を証明したい衝動を戯論の欲しがりと見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、虚構を喜ぶ欲しがりが立つ",
            "toNext": "止めないと二見への掴みへ",
            "todayObserve": OBSERVE["MN11-P05"],
            "todayAction": actions["MN11-P05"],
            "when": ["証明したくなった", "空論が止まらない"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN11-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN11-P09"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "四取と二見への固着を特定し緩める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、有見・四取が掴む手前",
            "toNext": "掴むと諍いの苦が見える",
            "todayObserve": OBSERVE["MN11-P06"],
            "todayAction": actions["MN11-P06"],
            "when": ["見解に固着した", "戒や自己論に掴まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN11-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN11-P04"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "諍いと戯論が苦から解き放たれないと見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、生老死の苦が見える",
            "toNext": "見れば、執取を離れる方向へ向き直る",
            "todayObserve": OBSERVE["MN11-P09"],
            "todayAction": actions["MN11-P09"],
            "when": ["人と諍った", "空論で重くなった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN11-P09"][:40] + "…",
            "secondaryObserve": "苦しみから完全に解き放たれない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "無明を捨て四取に執取せず、反感なく離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、一究竟の実践へ戻る",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN11-P08"],
            "todayAction": actions["MN11-P08"],
            "when": ["執取を一つ手放した", "反感なく話した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN11-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN11-P03"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "正法律と四法を振り返り、明日の獅子吼に結ぶ",
            "chapterHint": SHORT,
            "fromPrev": "一日の対論は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の獅子吼になる",
            "todayObserve": OBSERVE["MN11-P11"],
            "todayAction": actions["MN11-P11"],
            "when": ["一日を閉じるとき", "見解で争った日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN11-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN11-P02"],
        },
    ]

    out = {
        "chapter": 11,
        "sutta": 11,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：小なる獅子吼の経）",
        "suttas": ["MN 11 師子吼小経（小なる獅子吼の経）"],
        "source": {
            "primary": "パーリ・中部第11経（師子吼小経／小なる獅子吼の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含103師子吼経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・小なる獅子吼の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・師子吼経（T1.590c）",
                    "url": SAT_URL,
                    "note": "漢訳は正師子吼・四受。對照表: 法雨道場",
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
            "focusReason": "師子吼小経は一切の執取（四取）の遍知が主題。既定の焦点は掴む。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn011.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 11:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(11, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 12
    assert all(p["id"] == f"MN11-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/12; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
