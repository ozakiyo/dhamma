#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn023.json (蟻垤経／蟻塚の経) to match MN1–22 source alignment."""
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
# 對照表: No.95蟻喻経・雜阿含1079等。本文対応は雜阿含1079が近い。
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0282a01"
SAT_T95_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0095_%2C01%2C0918a01"
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
    "MN23-P01": (
        "比丘よ、『蟻塚』とは、まさに、これは、四つの大いなる元素（四大種：地・水・火・風）からなり、"
        "母と父を発生とし、飯と粥の蓄積にして、無常と捻転と圧搾と破壊と砕破の法（性質）ある、"
        "この身体の同義語です。"
    ),
    "MN23-P02": (
        "比丘よ、『屠殺場』とは、まさに、これは、五つの欲望の属性（五妙欲）の同義語です。"
        "眼によって識知されるべき諸々の色形（色）で、好ましく愛らしく意に適い……"
        "身によって識知されるべき諸々の感触（触・所触）で……貪るべきものの、〔同義語です〕。"
        "『屠殺場を引き揚げよ』〔とは〕、五つの欲望の属性を捨棄せよ。"
        "『思慮ある者よ、刃を取って掘り崩せ』とは、これが、この〔言葉〕の義（意味）となります。"
    ),
    "MN23-P03": (
        "比丘よ、『膨張した〔蛙〕』とは、まさに、これは、忿激と葛藤の同義語です。"
        "『膨張した〔蛙〕を引き揚げよ』〔とは〕、忿激と葛藤を捨棄せよ。……"
        "比丘よ、『肉片』とは、まさに、これは、愉悦と貪欲の同義語です。"
        "『肉片を引き揚げよ』〔とは〕、愉悦と貪欲を捨棄せよ。……"
        "比丘よ、『閂』とは、まさに、これは、無明の同義語です。"
        "『閂を引き揚げよ』〔とは〕、無明を捨棄せよ。"
    ),
    "MN23-P04": (
        "比丘よ、『刃』とは、まさに、これは、聖なる智慧の同義語です。"
        "比丘よ、『掘り崩すこと』とは、まさに、これは、精進勉励の同義語です。"
        "……『思慮ある者よ、刃を取って掘り崩せ』とは、これが、この〔言葉〕の義（意味）となります。"
    ),
    "MN23-P05": (
        "比丘よ、『閂』とは、まさに、これは、無明の同義語です。『閂を引き揚げよ』〔とは〕、無明を捨棄せよ。……"
        "比丘よ、『龍』とは、まさに、これは、煩悩が滅尽した比丘の同義語です。"
        "『龍は、ほうっておけ。龍を、打ってはならない。龍に、礼拝を為せ』とは、これが、この〔言葉〕の義（意味）となります。"
    ),
    "MN23-P06": (
        "婆羅門は、このように言いました。『思慮ある者よ、刃を取って掘り崩せ』と。"
        "思慮ある者は、刃を取って掘り崩しながら、閂を見ました。……膨張した〔蛙〕を……"
        "二様の道を……器を……亀を……屠殺場を……肉片を……龍を見ました。"
        "（次々に引き揚げよ——掘り崩しと捨棄の系列。）"
    ),
    "MN23-P07": (
        "比丘よ、『蟻塚』とは、まさに、これは……この身体の同義語です。"
        "比丘よ、すなわち、まさに、昼に、生業に励んで、夜に、刻々に思考し、刻々に想念するなら、"
        "これは、夜に発煙することです。"
        "比丘よ、すなわち、まさに、夜に、刻々に思考し、刻々に想念し、昼に、身体によって、言葉によって、"
        "意によって、生業に従事するなら、これは、昼に炎上することです。"
    ),
    "MN23-P08": (
        "比丘よ、すなわち、まさに、昼に、生業に励んで、夜に、刻々に思考し、刻々に想念するなら、"
        "これは、夜に発煙することです。"
        "……『屠殺場を引き揚げよ』〔とは〕、五つの欲望の属性を捨棄せよ。"
        "……『肉片を引き揚げよ』〔とは〕、愉悦と貪欲を捨棄せよ。"
    ),
    "MN23-P09": (
        "尊き方よ、いったい、まさに、何が、蟻塚であり、何が、夜に発煙することであり、"
        "何が、昼に炎上することであり……何が、龍なのですか」と。"
        "（クマーラ・カッサパが天神の問いを世尊に尋ね、説き明かしを受ける。）"
    ),
    "MN23-P10": (
        "比丘よ、比丘よ、この蟻塚は、夜に発煙し、昼に炎上します。"
        "……比丘よ、まさに、あなたは、近づいて行って、世尊に、これらの問いを尋ねるべきです。"
        "そして、すなわち、世尊が、あなたに説き明かすとおり、そのとおりに、それを保持するべきです。"
        "（外の謎は、内の法——身体·煩悩·精進·智慧——の同義語。）"
    ),
    "MN23-P11": (
        "比丘よ、『蟻塚』とは……この身体の同義語です。"
        "……『器』とは……五つの〔修行の〕妨害（五蓋）の同義語です。……"
        "『亀』とは……五つの〔心身を構成する〕執取の範疇（五取蘊）の同義語です。……"
        "『屠殺場』とは……五つの欲望の属性（五妙欲）の同義語です。……"
        "『刃』とは……聖なる智慧……『掘り崩すこと』とは……精進勉励の同義語です。"
    ),
}

OBSERVE = {
    "MN23-P01": (
        "蟻塚——四大・父母・飯粥の蓄積で、無常・破壊の法ある身体の同義語——"
        "朝、今日「蟻塚の譬喩」を一つ思い出す。"
    ),
    "MN23-P02": (
        "屠殺場——五妙欲（眼·耳·鼻·舌·身の好ましい対象）。引き揚げよ＝捨棄せよ——"
        "今日、六入のうち一つ（眼·耳等）を護る。"
    ),
    "MN23-P03": (
        "膨張した蛙＝忿激と葛藤、肉片＝愉悦と貪欲、閂＝無明。それぞれ引き揚げよ——"
        "今日、欲·瞋·痴のうち一つを「子牛の如き染」と見る。"
    ),
    "MN23-P04": (
        "刃＝聖なる智慧、掘り崩すこと＝精進勉励。思慮ある者よ、刃を取って掘り崩せ——"
        "今日、八正道のうち一つを「道の如く」歩む。"
    ),
    "MN23-P05": (
        "閂＝無明を捨棄せよ。龍＝煩悩滅尽の比丘——打たず礼拝せよ（漏尽）——"
        "今日、三漏のうち一つを特定し、対治する。"
    ),
    "MN23-P06": (
        "掘り崩しながら閂·蛙·二道·器·亀·屠殺場·肉片を次々に引き揚げ、龍に至る——"
        "今日、染を一つ「除く」練習をする。"
    ),
    "MN23-P07": (
        "身体は蟻塚。昼の生業→夜の思考＝発煙、夜の想念→昼の身語意＝炎上——"
        "今日、身体を「蟻垤の如く」一度見る。"
    ),
    "MN23-P08": (
        "夜の発煙——刻々の思考·想念。五妙欲と愉悦·貪欲を引き揚げよ——"
        "就寝前、今日「六入·染」に触れた瞬間を一つ認め、明日護る。"
    ),
    "MN23-P09": (
        "クマーラ・カッサパが天神の謎を世尊に問い、各同義語の説き明かしを受ける——"
        "今日学んだ譬喩を、意味を考えて一度語る。"
    ),
    "MN23-P10": (
        "天神の外の謎（蟻塚·発煙·炎上……龍）は、世尊により内の法の同義語として説き明かされる——"
        "今日、外の出来事を「譬喩」として一度見る。"
    ),
    "MN23-P11": (
        "蟻塚＝身体、器＝五蓋、亀＝五取蘊、屠殺場＝五妙欲、刃＝智慧、掘り崩し＝精進——"
        "今日、蟻垤の譬喩を一つ（身体·六入·染·道）思い出す。"
    ),
}

PRACTICE = {
    "MN23-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、身体という蟻塚への接触を譬喩で思い出す",
        "section": "蟻塚＝身体",
        "category": "mindfulness",
    },
    "MN23-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "五妙欲（屠殺場）への欲しがりを門で護る",
        "section": "屠殺場＝五妙欲",
        "category": "intention",
    },
    "MN23-P03": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正見"],
        "reason": "忿·欲·無明の掴みを蛙·肉片·閂として引き揚げる",
        "section": "蛙·肉片·閂",
        "category": "intention",
    },
    "MN23-P04": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正見"],
        "reason": "智慧の刃と精進で掘り崩し、道の一歩を進める",
        "section": "刃＝智慧·掘り崩し＝精進",
        "category": "effort",
    },
    "MN23-P05": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正精進"],
        "reason": "無明の閂と漏尽の龍を見て、漏の対治を知る",
        "section": "閂＝無明·龍＝漏尽",
        "category": "view",
    },
    "MN23-P06": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "次々に引き揚げ、染を一つ除く掘り崩しを練習する",
        "section": "掘り崩しの系列",
        "category": "effort",
    },
    "MN23-P07": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "身体を蟻塚として見、発煙·炎上の流れを一度観察する",
        "section": "発煙と炎上",
        "category": "mindfulness",
    },
    "MN23-P08": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正思惟"],
        "reason": "夜、発煙の想念と六入·染に触れた瞬間を認め、明日護る",
        "section": "夜の発煙·護門",
        "category": "mindfulness",
    },
    "MN23-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正念"],
        "reason": "学んだ譬喩を意味を考えて一度語る（問いと説き明かし）",
        "section": "問いと説き明かし",
        "category": "speech",
    },
    "MN23-P10": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "外の出来事を内の法の譬喩として一度受ける",
        "section": "外の謎·内の法",
        "category": "view",
    },
    "MN23-P11": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "蟻塚の譬喩のどれか一つを思い出し、掘り崩しへつなぐ",
        "section": "譬喩の想起",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN23-P01": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）／佛說蟻喻経（T95）",
        "t26": "T99-1079-body",
        "text": "丘塚者，謂眾生身——麤四大色，父母遺體，摶食、衣服、覆蓋……皆是變壞磨滅之法。",
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "丘塚＝蟻塚。對照表はT95蟻喻経・SA1079等。",
    },
    "MN23-P02": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）",
        "t26": "T99-1079-kama",
        "text": "屠殺者，謂五欲功德。",
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "屠殺＝パーリの屠殺場（五妙欲）。眼等の門を護る実践に対応。",
    },
    "MN23-P03": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）",
        "t26": "T99-1079-kilesa",
        "text": "氍氀者，謂忿恨。肉段者，謂慳愱。楞耆者，謂無明。",
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "忿·慳·無明。パーリは蛙＝忿激、肉片＝愉悦と貪欲、閂＝無明（対応差あり）。",
    },
    "MN23-P04": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）",
        "t26": "T99-1079-sword",
        "text": "發掘者，謂精勤方便。智士者，謂多聞聖弟子。刀劍者，謂智慧刀劍。",
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "刀劍＝聖慧、發掘＝精進（パーリの刃·掘り崩し）。",
    },
    "MN23-P05": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）",
        "t26": "T99-1079-naga",
        "text": "楞耆者，謂無明。……大龍者，謂漏盡羅漢。",
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "無明の捨と漏尽（龍）。パーリは閂＝無明、龍＝煩悩滅尽の比丘。",
    },
    "MN23-P06": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）／佛說蟻喻経（T95）",
        "t26": "T99-1079-dig",
        "text": (
            "大龜者，謂五蓋。氍氀者，謂忿恨。肉段者，謂慳愱。"
            "屠殺者，謂五欲功德。楞耆者，謂無明。二道，謂疑惑。門扇者，謂我慢。大龍者，謂漏盡羅漢。"
        ),
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "次々の捨棄系列。パーリは閂·蛙·二道·器·亀·屠殺場·肉片·龍。",
    },
    "MN23-P07": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）",
        "t26": "T99-1079-smoke",
        "text": (
            "丘塚者，謂眾生身……夜起煙者，謂有人於夜時起，隨覺、隨觀。"
            "晝行其教，身業、口業。"
        ),
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "夜起煙·晝行＝パーリの夜の発煙·昼の炎上。",
    },
    "MN23-P08": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）",
        "t26": "T99-1079-night",
        "text": "夜起煙者，謂有人於夜時起，隨覺、隨觀。……屠殺者，謂五欲功德。",
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "夜の尋伺と五欲の護。",
    },
    "MN23-P09": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）／佛說蟻喻経（T95）",
        "t26": "T99-1079-ask",
        "text": (
            "如是，比丘！若大師為聲聞所作……於汝已作，汝等當作所作……"
            "思惟禪思，不起放逸，莫令後悔——是則為我隨順之教。"
        ),
        "satLocus": "大正蔵 T2.282b 雜阿含1079",
        "note": "説示を受けて保持·実践する（パーリはカッサパの問いと説き明かし）。",
    },
    "MN23-P10": {
        "status": "mapped",
        "pin": "佛說蟻喻経（T95）",
        "t26": "T95-ant-riddle",
        "text": (
            "其蟻聚者，即是一切眾生五蘊聚身。夜中出煙者，即是眾生起諸尋伺。"
            "晝日火然者，即是眾生隨所尋伺起身語業。……龍者，即是諸阿羅漢。"
        ),
        "satLocus": "大正蔵 T1.918c 蟻喻経",
        "note": "外の相を内の法として説く対応。",
    },
    "MN23-P11": {
        "status": "mapped",
        "pin": "雜阿含1079（T99）",
        "t26": "T99-1079-summary",
        "text": (
            "丘塚者，謂眾生身……刀劍者，謂智慧刀劍。大龜者，謂五蓋……"
            "屠殺者，謂五欲功德……大龍者，謂漏盡羅漢。"
        ),
        "satLocus": "大正蔵 T2.282a 雜阿含1079",
        "note": "身体·蓋·欲·智慧·精進の譬喩まとめ。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部23経と雜阿含1079／蟻喻経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn023.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN23-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 23",
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
                    "locus": f"中部・蟻塚の経（MN23）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 蟻垤経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第23経・蟻垤経（蟻塚の経）"
    SHORT = "蟻垤経（蟻塚の経）"
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
            "pathLabel": "朝、身体という蟻塚への接触を譬喩で思い出す",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の身体への接触を変える",
            "toNext": "触のあと、発煙·炎上の受が見える",
            "todayObserve": OBSERVE["MN23-P01"],
            "todayAction": actions["MN23-P01"],
            "when": ["朝に身体に気づいた", "蟻塚の譬喩を思い出した"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN23-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN23-P09"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "身体を蟻塚として見、外の出来事を内の法として受ける",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、発煙·炎上の流れの受が立つ",
            "toNext": "受に乗ると五妙欲の欲しがりへ",
            "todayObserve": OBSERVE["MN23-P07"],
            "todayAction": actions["MN23-P07"],
            "when": ["身体を蟻塚と見た", "外を譬喩として見た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN23-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN23-P10"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "屠殺場＝五妙欲への欲しがりを門で護る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、好ましい色·声などへの欲しがりが立つ",
            "toNext": "止めないと忿·欲·無明の掴みへ",
            "todayObserve": OBSERVE["MN23-P02"],
            "todayAction": actions["MN23-P02"],
            "when": ["眼·耳などに引かれた", "門を護った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN23-P02"][:40] + "…",
            "secondaryObserve": "五欲功德",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "intention", "nidanaLabel": "掴む",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "忿·欲·無明の掴みを蛙·肉片·閂として引き揚げる",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、忿·貪欲·無明の掴みが手前",
            "toNext": "掴むと漏の苦が見える",
            "todayObserve": OBSERVE["MN23-P03"],
            "todayAction": actions["MN23-P03"],
            "when": ["忿が出た", "貪欲·無明に掴まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN23-P03"][:40] + "…",
            "secondaryObserve": "引き揚げよ",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "無明の閂と漏尽の龍を見て、漏の対治を知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、無明·漏の患が見える",
            "toNext": "見れば、刃と精進の掘り崩しへ",
            "todayObserve": OBSERVE["MN23-P05"],
            "todayAction": actions["MN23-P05"],
            "when": ["無明に気づいた", "漏を対治した"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN23-P05"][:40] + "…",
            "secondaryObserve": "漏盡羅漢",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "智慧の刃で掘り崩し、染を一つ引き揚げる",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、精進と智慧で掘り崩す",
            "toNext": "離せば、夜の発煙の見直しへ",
            "todayObserve": OBSERVE["MN23-P04"],
            "todayAction": actions["MN23-P04"],
            "when": ["刃を取って掘った", "染を一つ除いた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN23-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN23-P06"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "夜の発煙を認め、蟻塚の譬喩を一つ思い出す",
            "chapterHint": SHORT,
            "fromPrev": "一日の身語意は、朝からの掘り崩しの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN23-P08"],
            "todayAction": actions["MN23-P08"],
            "when": ["一日を閉じるとき", "譬喩を思い出した夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN23-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN23-P11"],
        },
    ]

    out = {
        "chapter": 23,
        "sutta": 23,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：蟻塚の経）",
        "suttas": ["MN 23 蟻垤経（蟻塚の経）"],
        "source": {
            "primary": "パーリ・中部第23経（蟻垤経／蟻塚の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT雜阿含1079（T99）を主とし、"
                "對照表の佛說蟻喻経（T95）も参照。旧スタブの夢·公牛等は経典にないため差し替え。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・蟻塚の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 雜阿含1079（T2.282a）／蟻喻経（T1.918）",
                    "url": SAT_URL,
                    "note": f"丘塚·夜煙·晝火·龍。蟻喻経: {SAT_T95_URL}。對照表: 法雨道場",
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
            "focusReason": "蟻塚の経は智慧の刃で掘り崩し、煩悩を次々に引き揚げるのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn023.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 23:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(23, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN23-P{i:02d}" for i, p in enumerate(pairs, 1))
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
