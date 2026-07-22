#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn018.json (蜜丸経／蜜団子の経) to match MN1–17 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0603b11"
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
    "MN18-P01": (
        "友よ、すなわち、説く者としてあるなら……世において、誰とであれ口論して止住することがないように、"
        "また、そして……諸々の欲望〔の対象〕による束縛を離れた者として〔世に〕住んでいる、その婆羅門に……"
        "諸々の表象（想）が悪しき習いとなることがないように、友よ、まさに、わたしは、このように説く者であり、このように告げ知らせる者です。"
    ),
    "MN18-P02": (
        "比丘よ、それを因縁として、人に、虚構（戯論）の表象と名称が慣行となるとして、"
        "もし、ここにおいて、愉悦するべきものが〔存在せず〕、迎合するべきものが〔存在せず〕、固執するべきものが存在しないなら、"
        "まさしく、これは、諸々の貪り〔の思い〕の悪習の終極であり……諸々の棒を取ることや刃を取ることや紛争や口論や論争……の終極です。"
        "……世尊は、この〔言葉〕を言って……坐から立ち上がって、精舎に入りました。"
    ),
    "MN18-P03": (
        "比丘たちよ、マハー・カッチャーナは、賢者です。比丘たちよ、マハー・カッチャーナは、大いなる智慧ある者です。"
        "比丘たちよ、もし、また、あなたたちが、わたしに、この義（意味）を質問するなら、わたしもまた、それを、まさしく、このように説き明かすでしょう。"
        "すなわち、マハー・カッチャーナによって説き明かされた、そのとおりに。"
    ),
    "MN18-P04": (
        "友よ、かつまた、眼を縁として、かつまた、諸々の色形を〔縁として〕、眼の識知〔作用〕が生起します。"
        "三つのものの接合は、接触です。接触という縁あることから、感受があります。"
        "それを感受するなら、それを表象します。それを表象するなら、それを思考します。"
        "それを思考するなら、それを虚構します。それを虚構するなら、それを因縁として、人に、虚構の表象と名称が慣行となります。"
    ),
    "MN18-P05": (
        "それを虚構するなら、それを因縁として、人に、虚構の表象と名称が慣行となります──"
        "過去と未来と現在の眼によって識知されるべき諸々の色形において。"
        "……意によって識知されるべき諸々の法（意の対象）において。"
    ),
    "MN18-P06": (
        "それを因縁として、人に、虚構の表象と名称が慣行となるとして、"
        "もし、ここにおいて、愉悦するべきものが〔存在せず〕、迎合するべきものが〔存在せず〕、固執するべきものが存在しないなら、"
        "……諸々の思量の悪習の終極であり……ここにおいて、これらの悪しき善ならざる法（性質）は、完全に残りなく止滅します。"
    ),
    "MN18-P07": (
        "友よ、かつまた、眼を縁として……耳を縁として……鼻を縁として……舌を縁として……身を縁として……"
        "意を縁として、かつまた、諸々の法（意の対象）を〔縁として〕、意の識知〔作用〕が生起します。"
        "三つのものの接合は、接触です。……それを虚構するなら……虚構の表象と名称が慣行となります。"
    ),
    "MN18-P08": (
        "尊き方よ、それは、たとえば、また、飢えと力の衰えに打ち負かされた人が、蜜団子に到達するなら、"
        "彼は、〔それを〕味わう、そのたびごとに、雑物なしの善き味を、まさしく、得るように、"
        "……心の才覚に恵まれた比丘は、この法（教え）の教相の義（意味）を、智慧によって近しく注視する、そのたびごとに、"
        "わが意を得ることを、まさしく、得るでしょうし、心の浄信を、まさしく、得るでしょう。"
    ),
    "MN18-P09": (
        "アーナンダよ、それゆえに、ここに、あなたは、この法（教え）の教相を、まさしく、『蜜団子の教相』と、それを保持しなさい。"
    ),
    "MN18-P10": (
        "友よ、すなわち、説く者としてあるなら……世において、誰とであれ口論して止住することがないように……。"
        "……愉悦するべきものが〔存在せず〕、迎合するべきものが〔存在せず〕、固執するべきものが存在しないなら、"
        "……諸々の棒を取ることや刃を取ることや紛争や口論や論争や争議や中傷や虚偽を説くことの終極です。"
    ),
    "MN18-P11": (
        "友よ、それは、たとえば、また、硬材を義（目的）として硬材を探し求める人が、硬材を遍く探し求めるために歩みながら、"
        "〔そこに〕立っている硬材ある大木の、まさしく、根を超え行って、幹を超え行って、枝葉において硬材を遍く探し求めるべきと思い考えるようなものです。"
        "このように、これと同様に、尊者たちは、教師を超え行って、わたしに、この義（意味）の質問をなすものと考えるべきです。"
    ),
    "MN18-P12": (
        "接触という縁あることから、感受があります。それを感受するなら、それを表象します。"
        "それを表象するなら、それを思考します。それを思考するなら、それを虚構します。"
        "それを虚構するなら、それを因縁として、人に、虚構の表象と名称が慣行となります。"
    ),
    "MN18-P13": (
        "もし、ここにおいて、愉悦するべきものが〔存在せず〕、迎合するべきものが〔存在せず〕、固執するべきものが存在しないなら、"
        "……諸々の紛争や口論や論争……の終極です。"
        "ここにおいて、これらの悪しき善ならざる法（性質）は、完全に残りなく止滅します。"
        "アーナンダよ……この法（教え）の教相を、まさしく、『蜜団子の教相』と、それを保持しなさい。"
    ),
}

OBSERVE = {
    "MN18-P01": (
        "口論せず、欲の束縛を離れ、表象が悪しき習いとならない——これが説く者の宗。"
        "対立の根にある「愛するもの」を一つ見る。"
    ),
    "MN18-P02": (
        "世尊は略説のまま精舎へ——愉悦・迎合・固執がなければ貪瞋見疑慢の終極。"
        "争いの根を急いで結論づけず、縁起を辿る。"
    ),
    "MN18-P03": (
        "マハー・カッチャーナの詳説は世尊が同じく説く義——"
        "深い法を聞くとき、師の言葉を自分の解釈で急いで置き換えない。"
    ),
    "MN18-P04": (
        "眼·色→識→触→受→想→思→虚構→虚構の表象と名称の慣行——"
        "不快が来たらこの流れを一つ辿る。"
    ),
    "MN18-P05": (
        "虚構すれば、過去·現在·未来の色·法に虚構の表象と名称が慣行となる——"
        "「私·私所」の想が広がっていないか問う。"
    ),
    "MN18-P06": (
        "愉悦・迎合・固執がなければ、思量の悪習も止滅する——"
        "自己像を固定する言葉（ラベル）を一度外す。"
    ),
    "MN18-P07": (
        "六処すべてで同じ連鎖——触から虚構の慣行へ——"
        "一つの感覚入力への反応を観察する。"
    ),
    "MN18-P08": (
        "蜜団子を味わうたび善き味を得る如く——この教相を注視するたび歓喜と浄信を得る。"
        "一節を読み返し、歓喜と清安を保つ。"
    ),
    "MN18-P09": (
        "この法門を『蜜団子の教相』と保持しなさい——"
        "争いが来たらそう名づけ、触·受に戻る。"
    ),
    "MN18-P10": (
        "口論して止住せず、固執なければ紛争・虚偽の終極——"
        "議論で「正しさ」を証明したい欲を一度手放す。"
    ),
    "MN18-P11": (
        "硬材ある大木の根·幹を超え枝葉に探す如く——教師を超えて問うな。"
        "教えるとき、縁起の幹（触→受）から始める。"
    ),
    "MN18-P12": (
        "触→受→想→思→虚構の連鎖を見れば、争いの燃料が弱まる——"
        "夜、今日の争いの「触→虚構」を一つ手放す。"
    ),
    "MN18-P13": (
        "愉悦・迎合・固執を離れば悪法は止滅する——蜜団子の教相として保持する。"
        "夜、言葉·争い·取著を一つ振り返り、明日手放す。"
    ),
}

PRACTICE = {
    "MN18-P01": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正思惟"],
        "reason": "対立の根にある愛着を見て口論の燃料を弱める",
        "section": "ダンダパーニ·宗",
        "category": "view",
    },
    "MN18-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "略説の受を急いで結論せず、固執の有無を見る",
        "section": "略説·終極",
        "category": "view",
    },
    "MN18-P03": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "師の義を保持し、急な自己解釈で置き換えない",
        "section": "マハーカッチャーナ",
        "category": "mindfulness",
    },
    "MN18-P04": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "触→受→想→思→虚構の接触連鎖を辿る",
        "section": "触→虚構",
        "category": "mindfulness",
    },
    "MN18-P05": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "三世に広がる虚構の表象の掴みを見る",
        "section": "虚構の慣行",
        "category": "view",
    },
    "MN18-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正語"],
        "reason": "固執するラベルを外し、思量の掴みを緩める",
        "section": "愉悦·固執",
        "category": "intention",
    },
    "MN18-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正定"],
        "reason": "六処の一入力で触の連鎖を観察する",
        "section": "六処",
        "category": "mindfulness",
    },
    "MN18-P08": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正念"],
        "reason": "教相を味わい歓喜·浄信で心を離す",
        "section": "蜜団子·味",
        "category": "concentration",
    },
    "MN18-P09": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "争いを蜜団子の縁起として名づけ苦の連鎖を切る",
        "section": "蜜団子の教相",
        "category": "view",
    },
    "MN18-P10": {
        "nidanaId": "craving",
        "pathFactors": ["正語", "正思惟"],
        "reason": "正しさを証明したい欲しがりを手放し口論しない",
        "section": "口論なき",
        "category": "speech",
    },
    "MN18-P11": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正語"],
        "reason": "教えるとき根·幹（縁起）から始め枝葉に逸れない",
        "section": "硬材の喩",
        "category": "view",
    },
    "MN18-P12": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正見"],
        "reason": "夜に触→虚構の連鎖を一つ手放す",
        "section": "夜·虚構",
        "category": "mindfulness",
    },
    "MN18-P13": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "言葉·争い·取著を振り返り、固執なき方向を保持する",
        "section": "止滅·保持",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN18-P01": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-dandapani",
        "text": "沙門瞿曇！以何為宗本？說何等法？……若一切世間……使不鬪諍，修習離欲清淨梵志，捨離諂曲，除悔，不著有、非有，亦無想，是我宗本。",
        "satLocus": "大正蔵 T1.603b 蜜丸経",
        "note": "執杖釈の問いと不鬪諍の宗。",
    },
    "MN18-P02": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-brief",
        "text": "若人所因念，出家學道，思想修習，及過去、未來、今現在法，不愛、不樂、不著、不住，是說苦邊。……鬪諍……及無量惡不善之法，是說苦邊。佛說如是，即從坐起，入室燕坐。",
        "satLocus": "大正蔵 T1.603c 蜜丸経",
        "note": "略説ののち入室＝精舎へ。",
    },
    "MN18-P03": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-kaccana",
        "text": "善哉！善哉！我弟子中有眼、有智、有法、有義。……如迦旃延比丘所說，汝等應當如是受持。",
        "satLocus": "大正蔵 T1.604c 蜜丸経",
        "note": "大迦旃延の詳説を世尊が印可。",
    },
    "MN18-P04": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-phassa",
        "text": "緣眼及色，生眼識，三事共會，便有更觸，緣更觸便有所覺，若所覺便想，若所想便思，若所思便念，若所念便分別。",
        "satLocus": "大正蔵 T1.604b 蜜丸経",
        "note": "更触→覚→想→思→念→分別＝触→虚構。",
    },
    "MN18-P05": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-papanca",
        "text": "思想修習，此中過去、未來、今現在法，不愛、不樂、不著、不住，是說苦邊。",
        "satLocus": "大正蔵 T1.604b 蜜丸経",
        "note": "三世法への不著＝虚構の慣行の対治。",
    },
    "MN18-P06": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-anabhinandita",
        "text": "不愛、不樂、不著、不住，是說苦邊。……慢使……鬪諍……是說苦邊。",
        "satLocus": "大正蔵 T1.603c–604b 蜜丸経",
        "note": "不愛不樂不著不住＝愉悦・固執なき。",
    },
    "MN18-P07": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-salayatana",
        "text": "如是耳、鼻、舌、身緣意及法，生意識，三事共會，便有更觸……若所念便分別。",
        "satLocus": "大正蔵 T1.604b 蜜丸経",
        "note": "六処すべてに同じ連鎖。",
    },
    "MN18-P08": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-taste",
        "text": "猶如有人因行無事處、山林樹間，忽得蜜丸，隨彼所食而得其味，如是族姓子於我此正法、律，隨彼所觀而得其味。",
        "satLocus": "大正蔵 T1.604c 蜜丸経",
        "note": "蜜丸の味＝観ごとの味。",
    },
    "MN18-P09": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-name",
        "text": "阿難！此法名為蜜丸喻，汝當受持。……汝等受此蜜丸喻法，當諷誦讀。",
        "satLocus": "大正蔵 T1.604c–605a 蜜丸経",
        "note": "蜜丸喻の名。",
    },
    "MN18-P10": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-no-quarrel",
        "text": "使不鬪諍……是我宗本。……鬪諍、憎嫉、諛諂、欺誑、妄言、兩舌及無量惡不善之法，是說苦邊。",
        "satLocus": "大正蔵 T1.603b–c 蜜丸経",
        "note": "不鬪諍と鬪諍の苦辺。",
    },
    "MN18-P11": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-tree",
        "text": "猶如有人欲得求實……持斧入林，彼見大樹成根、莖、節、枝、葉、華、實，彼人不觸根、莖、節、實，但觸枝、葉。……世尊現在，捨來就我而問此義。",
        "satLocus": "大正蔵 T1.604a 蜜丸経",
        "note": "根茎を捨て枝葉に求む喩。",
    },
    "MN18-P12": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-chain-night",
        "text": "緣更觸便有所覺，若所覺便想，若所想便思，若所思便念，若所念便分別。",
        "satLocus": "大正蔵 T1.604b 蜜丸経",
        "note": "連鎖の夜の見直し。",
    },
    "MN18-P13": {
        "status": "mapped",
        "pin": "中阿含115・蜜丸経（T26）",
        "t26": "T26-115-summary",
        "text": "不愛、不樂、不著、不住，是說苦邊。……此法名為蜜丸喻，汝當受持。……梵行之本，趣通趣覺，趣於涅槃。",
        "satLocus": "大正蔵 T1.603c–605a 蜜丸経",
        "note": "苦辺の止と蜜丸喻の保持。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部18経と中阿含115蜜丸経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn018.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 14):
        pid = f"MN18-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 18",
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
                    "locus": f"中部・蜜団子の経（MN18）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 蜜丸経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第18経・蜜丸経（蜜団子の経）"
    SHORT = "蜜丸経（蜜団子の経）"
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
            "pathLabel": "触→受→想→思→虚構の連鎖を六処で辿る",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の感覚の接触を変える",
            "toNext": "触のあと、略説の受と対立の受が見える",
            "todayObserve": OBSERVE["MN18-P04"],
            "todayAction": actions["MN18-P04"],
            "when": ["音·画面に触れた", "言葉が触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN18-P04"][:40] + "…",
            "secondaryObserve": OBSERVE["MN18-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "略説の受を急いで結論せず、固執の有無を見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、愉悦·迎合の受が立つ",
            "toNext": "受に乗ると愛着と正しさの欲しがりへ",
            "todayObserve": OBSERVE["MN18-P02"],
            "todayAction": actions["MN18-P02"],
            "when": ["急いで結論したくなった", "略説に触れた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN18-P02"][:40] + "…",
            "secondaryObserve": "不愛不樂不著",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "対立の愛着と正しさへの欲しがりを手放す",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、愛するもの·正しさの欲しがりが立つ",
            "toNext": "止めないと虚構のラベルの掴みへ",
            "todayObserve": OBSERVE["MN18-P01"],
            "todayAction": actions["MN18-P01"],
            "when": ["対立で愛着を見た", "正しさを証明したくなった"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN18-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN18-P10"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "虚構の表象と自己ラベルの掴みを外す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、三世への虚構の掴みが手前",
            "toNext": "掴むと争いの苦が見える",
            "todayObserve": OBSERVE["MN18-P05"],
            "todayAction": actions["MN18-P05"],
            "when": ["私·私所の想が広がった", "ラベルに固執した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN18-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN18-P06"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "争いを蜜団子の縁起として名づけ、苦の連鎖を切る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、口論·論争の患が見える",
            "toNext": "見れば、味わいと手放しへ向き直る",
            "todayObserve": OBSERVE["MN18-P09"],
            "todayAction": actions["MN18-P09"],
            "when": ["争いが来た", "触·受に戻った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN18-P09"][:40] + "…",
            "secondaryObserve": "鬪諍是說苦邊",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "concentration", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "教相を味わい、触→虚構の連鎖を一つ手放す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、蜜団子の味と手放しへ",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN18-P08"],
            "todayAction": actions["MN18-P08"],
            "when": ["教相を味わった", "虚構を手放した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN18-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN18-P12"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "師の義と縁起の幹を保持し、争い·取著を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の虚構は、朝からの触の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN18-P13"],
            "todayAction": actions["MN18-P13"],
            "when": ["一日を閉じるとき", "教え·学びを振り返る"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN18-P13"][:40] + "…",
            "secondaryObserve": OBSERVE["MN18-P11"],
        },
    ]

    out = {
        "chapter": 18,
        "sutta": 18,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：蜜団子の経）",
        "suttas": ["MN 18 蜜丸経（蜜団子の経）"],
        "source": {
            "primary": "パーリ・中部第18経（蜜丸経／蜜団子の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含115蜜丸経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・蜜団子の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・蜜丸経（T1.603b）",
                    "url": SAT_URL,
                    "note": "執杖釈·大迦旃延·蜜丸喻。對照表: 法雨道場",
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
            "focusNodeId": "contact",
            "focusReason": "蜜団子の経は触→受→想→思→虚構の連鎖を見て口論と悪法の終極へ向かうのが主題。既定の焦点は接触。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn018.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 18:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(18, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 13
    assert all(p["id"] == f"MN18-P{i:02d}" for i, p in enumerate(pairs, 1))
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
