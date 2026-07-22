#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn022.json (蛇喩経／蛇の喩えの経) to match MN1–21 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0763b01"
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
    "MN22-P01": (
        "そのように、わたしは、世尊によって説示された法（教え）を了知する。"
        "すなわち、およそ、これらの、世尊によって説かれた、障りとなる諸々の法（性質）は、"
        "それらは、受用している者の障りとなるに十分ならず」と。"
        "（鷹匠の過去あるアリッタ比丘の妄見。）"
    ),
    "MN22-P02": (
        "比丘たちよ、ここに、一部の愚人たちは、法（教え）を……遍く学得します。"
        "彼らは、その法（教え）を遍く学得して、それらの法（教え）の義（意味）を、智慧によって近しく注視しません。"
        "……彼らは、まさしく、そして、〔他者への〕論詰という福利あることから、"
        "さらに、『かくのごとく〔云々〕』〔と批判する他者の〕論の解消という福利あることから、法（教え）を遍く学得します。"
        "……それは、たとえば、また、……〔蛇を〕あるいは、蜷局において、あるいは、尾において、掴みます。"
        "……彼は、それを因縁として、あるいは、死に遭遇するでしょうし、あるいは、死ぬほどの苦しみに〔遭遇するでしょう〕。"
        "それは、何を因とするのですか。比丘たちよ、蛇が悪しく掴まれたからです。"
    ),
    "MN22-P03": (
        "比丘たちよ、また、ここに、一部の良家の子息たちは、法（教え）を……遍く学得します。"
        "彼らは、その法（教え）を遍く学得して、それらの法（教え）の義（意味）を、智慧によって近しく注視します。"
        "……彼らは、……〔他者への〕論詰という福利あることから、ではなく……法（教え）を遍く学得します。"
        "……〔蛇を〕山羊足の棒によって……頭において、善く掴まれたものとして掴みます。"
        "……彼は、それを因縁として、あるいは、死に遭遇することも、あるいは、死ぬほどの苦しみに〔遭遇することも〕、まさしく、ありません。"
        "それは、何を因とするのですか。比丘たちよ、蛇が善く掴まれたからです。"
    ),
    "MN22-P04": (
        "諸々の欲望〔の対象〕は、世尊によって、悦楽少なきもの、苦痛多きもの、葛藤多きもの、"
        "ここにおいて、より一層の危険がある、と説かれました。"
        "……骨の鎖の喩え……肉片の喩え……草の松明の喩え……火坑の喩え……夢の喩え……"
        "蛇の頭の喩えあるもの、苦痛多きもの、葛藤多きもの、ここにおいて、より一層の危険がある、と説かれました。"
    ),
    "MN22-P05": (
        "比丘たちよ、超脱を義（目的）として、筏の喩えの法（教え）を、あなたたちに説示しましょう"
        "──掴み取ることを義（目的）として、ではなく。"
        "……比丘たちよ、まさしく、このように、まさに、超脱を義（目的）として、筏の喩えの法（教え）が、"
        "わたしによって説示されました──掴み取ることを義（目的）として、ではなく。"
    ),
    "MN22-P06": (
        "比丘たちよ、あなたたちに説示された筏の喩えの法（教え）を了知しているなら、"
        "あなたたちによって、諸々の法（教え）もまた捨棄されるべきです。"
        "ましてや、諸々の法（教え）ならざるものは〔言うまでもありません〕。"
    ),
    "MN22-P07": (
        "色形（色）を、『これは、わたしのものである。これは、わたしとして存在する。"
        "これは、わたしの自己である』と等しく随観します。"
        "感受〔作用〕（受）を……表象〔作用〕（想）を……諸々の形成〔作用〕（行）を……"
        "識知〔作用〕（識）を、『これは、わたしのものである。これは、わたしとして存在する。"
        "これは、わたしの自己である』と等しく随観します。"
        "（六つの見解の拠点——無聞の凡夫の随観。）"
    ),
    "MN22-P08": (
        "比丘たちよ、それゆえに、ここに、それが、あなたたちのものでないなら、それを捨棄しなさい。"
        "それは、捨棄されたなら、あなたたちにとって、長夜にわたり、利益のために〔成り〕、安楽のために成るでしょう。"
        "……色形は、あなたたちのものではありません。それを捨棄しなさい。"
        "……感受〔作用〕は……表象〔作用〕は……諸々の形成〔作用〕は……識知〔作用〕は、"
        "あなたたちのものではありません。それを捨棄しなさい。"
    ),
    "MN22-P09": (
        "比丘たちよ、そして、わたしは、過去において、さらに、今現在も、"
        "まさしく、そして、苦しみを報知し、さらに、苦しみの止滅を〔報知します〕。"
        "（『虚無論者の沙門ゴータマは……非生存を報知する』という誹謗への返答。）"
    ),
    "MN22-P10": (
        "愚人よ、そこで、また、しかしながら、あなたは、自己みずから悪しく把握したものによって、"
        "まさしく、そして、わたしたちを誹謗し、かつまた、自己を掘り崩し、"
        "さらに、多くの功徳ならざるものを生み出します。"
        "愚人よ、まさに、それは、あなたにとって、長夜にわたり、利益ならざるもののために〔成り〕、苦痛のために成るでしょう。"
        "（アリッタへの訶責——妄見で法を曲げた結果。）"
    ),
    "MN22-P11": (
        "比丘たちよ、このように見ながら、有聞の聖なる弟子は、色形にたいし厭離し、"
        "感受〔作用〕にたいし厭離し……識知〔作用〕にたいし厭離します。"
        "厭離しながら、離貪します。離貪あることから、解脱します。"
        "……この者は、『比丘として、かくのごとくもまた、……柱を引き抜いた者……束縛を離れた者』と説かれます。"
    ),
    "MN22-P12": (
        "比丘たちよ、それゆえに、ここに、それが、あなたたちのものでないなら、それを捨棄しなさい。"
        "それは、捨棄されたなら、あなたたちにとって、長夜にわたり、利益のために〔成り〕、安楽のために成るでしょう。"
        "……色形は、あなたたちのものではありません。……識知〔作用〕は、あなたたちのものではありません。"
        "それを捨棄しなさい。"
    ),
}

OBSERVE = {
    "MN22-P01": (
        "アリッタの妄見——障りとなる法を受用しても障りにならない、と極端に了知する——"
        "朝、教えを極端に解釈していないか一度問う。"
    ),
    "MN22-P02": (
        "悪く掴む蛇喩——尾·蜷局で掴み咬まれ死苦。論詰·論破の福利で法を学得し、義を慧で注視しない——"
        "今日、法を論争の材料として掴んでいないか一度問う。"
    ),
    "MN22-P03": (
        "善く掴む蛇喩——山羊足の棒で頭を正しく掴む。義を慧で注視し、論詰のためではなく学得する——"
        "今日学んだ一節について、意味を慧で一度考察する。"
    ),
    "MN22-P04": (
        "欲の諸喩——骨鎖·肉片·松明·火坑·夢·蛇の頭。悦楽少なく苦痛·葛藤多く、より一層の危険——"
        "快楽の裏に「蛇の頭の過害」を一瞬思い出す。"
    ),
    "MN22-P05": (
        "筏の喩え——超脱を義として説示され、掴み取ることを義としてではない——"
        "今日、教えを語るとき、相手が執着しないよう注意する。"
    ),
    "MN22-P06": (
        "筏を了知するなら、諸々の法もまた捨棄されるべき——ましてや非法は言うまでもない——"
        "「私の正しい理解」の執着する手を、一度緩める。"
    ),
    "MN22-P07": (
        "六見解拠点——色·受·想·行·識を「わたしのもの·わたし·自己」と随観する凡夫——"
        "朝、今日執着しやすい対象を一つ挙げ、「私·私所」を観察する。"
    ),
    "MN22-P08": (
        "ものでないなら捨棄せよ——色·受·想·行·識はあなたたちのものではない。捨棄すれば長夜の利益·安楽——"
        "今日、体調や感情を「私」ではなく「蘊の集まり」と一瞬見る。"
    ),
    "MN22-P09": (
        "過去においても今現在も——苦しみを報知し、苦しみの止滅を報知する。断滅論ではない——"
        "今日、確信の根拠が「正しい理解」か一度問う。"
    ),
    "MN22-P10": (
        "悪しく把握した妄見——世尊を誹謗し、自己を掘り崩し、多くの功徳ならざるものを生む——"
        "今日、教えを自分の都合に曲げていないか問う。"
    ),
    "MN22-P11": (
        "厭離→離貪→解脱——柱を引き抜いた者·束縛を離れた者。自己否定ではなく執着の手放し——"
        "今日、自分を責めるのではなく、執着だけを手放す。"
    ),
    "MN22-P12": (
        "夜の捨棄——ものでない色·受·想·行·識を捨棄すれば長夜の利益·安楽——"
        "就寝前、今日の執着を「執着する所なし」と一度手放す。"
    ),
}

PRACTICE = {
    "MN22-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "朝、教えとの接触で極端解釈の妄見が触れていないか問う",
        "section": "アリッタの妄見",
        "category": "view",
    },
    "MN22-P02": {
        "nidanaId": "clinging",
        "pathFactors": ["正思惟", "正見"],
        "reason": "論詰の福利で法を悪く掴む蛇喩の掴みを見る",
        "section": "悪く掴む蛇喩",
        "category": "intention",
    },
    "MN22-P03": {
        "nidanaId": "release",
        "pathFactors": ["正念", "正見"],
        "reason": "義を慧で注視し、頭で善く掴むように法を正しく掴む",
        "section": "善く掴む蛇喩",
        "category": "mindfulness",
    },
    "MN22-P04": {
        "nidanaId": "suffering",
        "pathFactors": ["正思惟", "正見"],
        "reason": "欲の蛇の頭の過害を見て、少楽多苦の危険を知る",
        "section": "欲の諸喩",
        "category": "intention",
    },
    "MN22-P05": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正思惟"],
        "reason": "筏は超脱のため——語るときも掴み取る執着を生ませない",
        "section": "筏喩·超脱",
        "category": "speech",
    },
    "MN22-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正思惟"],
        "reason": "法すら捨棄——「私の正しい理解」の手を緩める",
        "section": "筏喩·捨棄",
        "category": "view",
    },
    "MN22-P07": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "執着しやすい対象への「私·私所」の受を朝に観察する",
        "section": "六見解拠点",
        "category": "mindfulness",
    },
    "MN22-P08": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正念"],
        "reason": "体調·感情への「私」の欲しがりを蘊の集まりとして見る",
        "section": "捨棄·五蘊",
        "category": "view",
    },
    "MN22-P09": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "苦と苦の止滅だけを報知する根拠に、確信を照らす",
        "section": "苦と止滅の報知",
        "category": "view",
    },
    "MN22-P10": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正見"],
        "reason": "都合に曲げた把握が誹謗と自己掘削を生む流れを見る",
        "section": "悪しく把握",
        "category": "intention",
    },
    "MN22-P11": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正見"],
        "reason": "自己責めではなく、厭離·離貪で執着だけを手放す",
        "section": "厭離·解脱",
        "category": "effort",
    },
    "MN22-P12": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜、今日の執着を「ものでない」として一度捨棄する",
        "section": "夜の捨棄",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN22-P01": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-arittha",
        "text": "爾時阿梨吒比丘……生如是惡見。我知世尊如是說法。行欲者無障礙。",
        "satLocus": "大正蔵 T1.763b 阿梨吒経",
        "note": "行欲者無障礙＝障りとならない妄見。",
    },
    "MN22-P02": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-snake-wrong",
        "text": (
            "或有癡人顛倒受解義及文也。……彼諍知此義，不受解脫知此義。"
            "……譬若如人欲得捉蛇……見極大蛇，便前以手捉其腰中。"
            "蛇迴舉頭，或蜇手足及餘支節。……但受極苦唐自疲勞。"
            "所以者何。以不善解取蛇法故。"
        ),
        "satLocus": "大正蔵 T1.764a–b 阿梨吒経",
        "note": "捉其腰中＝尾·蜷局の悪掴み。諍知＝論詰の福利。",
    },
    "MN22-P03": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-snake-right",
        "text": (
            "或有族姓子不顛倒善受解義及文。……彼不諍知此義，唯受解脫知此義。"
            "……譬若如人欲得捉蛇……手執鐵杖……先以鐵杖押彼蛇頂手捉其頭。"
            "彼蛇雖反尾迴或纏手足及餘支節，然不能蜇。……以不顛倒受解法故。"
        ),
        "satLocus": "大正蔵 T1.764b 阿梨吒経",
        "note": "鐵杖押頂＝山羊足の棒で頭を正しく掴む。",
    },
    "MN22-P04": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-kama",
        "text": (
            "欲有障礙。世尊說欲有障礙也。"
            "欲如骨鎖……欲如肉臠……欲如把炬……欲如火坑……欲如毒蛇……"
            "欲如夢……欲如假借……欲如樹果。"
        ),
        "satLocus": "大正蔵 T1.763c–764a 阿梨吒経",
        "note": "欲如毒蛇＝パーリの蛇の頭の喩えに対応。",
    },
    "MN22-P05": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-raft-purpose",
        "text": "我為汝等長夜說筏喻法。欲令棄捨不欲令受故。",
        "satLocus": "大正蔵 T1.764b 阿梨吒経",
        "note": "欲令棄捨不欲令受＝超脱のため·掴み取るためではない。",
    },
    "MN22-P06": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-raft-abandon",
        "text": (
            "如是我為汝等長夜說筏喻法。欲令棄捨不欲令受。"
            "若汝等知我長夜說筏喻法者。當以捨是法。況非法耶。"
        ),
        "satLocus": "大正蔵 T1.764c 阿梨吒経",
        "note": "捨是法況非法＝法もまた捨棄、ましてや非法。",
    },
    "MN22-P07": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-six-views",
        "text": (
            "復次有六見處。……比丘者所有色……彼一切非我有。我非彼有亦非是神。"
            "如是慧觀知其如真。"
        ),
        "satLocus": "大正蔵 T1.764c 阿梨吒経",
        "note": "六見處——非我有の正観（凡夫の逆は「我·我所」）。",
    },
    "MN22-P08": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-not-mine",
        "text": (
            "比丘者所有色，過去未來現在……彼一切非我有，我非彼有，亦非是神，"
            "如是慧觀，知其如真。所有覺、所有想……亦非是神。"
        ),
        "satLocus": "大正蔵 T1.764c 阿梨吒経",
        "note": "非我有＝ものでない五蘊の捨棄に対応。",
    },
    "MN22-P09": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-not-uccheda",
        "text": (
            "諸沙門梵志誣謗我，虛妄言不真實……彼實有衆生施設斷滅壞。"
            "若此中無我不説。彼如來於現法中説無憂。"
        ),
        "satLocus": "大正蔵 T1.766a 阿梨吒経",
        "note": "断滅の誹謗への否定。パーリは「過去·今も苦と苦の止滅を報知」。",
    },
    "MN22-P10": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-wrong-grasp",
        "text": (
            "然此阿梨吒愚癡之人。顛倒受解義及文也。"
            "彼因自顛倒受解故。誣謗於我。為自傷害。有犯有罪……而得大罪。"
        ),
        "satLocus": "大正蔵 T1.764a 阿梨吒経",
        "note": "顛倒受解＝都合に曲げた把握。",
    },
    "MN22-P11": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-abandon-asmi",
        "text": (
            "彼或如來，或如來弟子，滅一切自身故說法，"
            "捨離一切漏一切我我所作，滅慢使故說法。"
        ),
        "satLocus": "大正蔵 T1.765a 阿梨吒経",
        "note": "捨離一切我我所作＝執着の手放し（自己否定ではない）。",
    },
    "MN22-P12": {
        "status": "mapped",
        "pin": "中阿含200・阿梨吒経（T26）",
        "t26": "T26-200-night-anatta",
        "text": (
            "比丘者所有色……彼一切非我有。我非彼有。亦非是神。"
            "如是慧觀知其如真。"
        ),
        "satLocus": "大正蔵 T1.764c / T1.765c 阿梨吒経",
        "note": "非我有の慧観を夜の手放しに対応。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部22経と中阿含200阿梨吒経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn022.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 13):
        pid = f"MN22-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 22",
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
                    "locus": f"中部・蛇の喩えの経（MN22）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 蛇喩経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第22経・蛇喩経（蛇の喩えの経）"
    SHORT = "蛇喩経（蛇の喩えの経）"
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
            "pathLabel": "朝、教えとの接触で極端解釈が触れていないか問う",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の教えの接触を変える",
            "toNext": "触のあと、私·私所の受が見える",
            "todayObserve": OBSERVE["MN22-P01"],
            "todayAction": actions["MN22-P01"],
            "when": ["教えに触れた", "極端に解釈しそう"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN22-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN22-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "執着しやすい対象への「私·私所」の受を観察する",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、わたしのものという受が立つ",
            "toNext": "受に乗ると都合への欲しがりへ",
            "todayObserve": OBSERVE["MN22-P07"],
            "todayAction": actions["MN22-P07"],
            "when": ["執着しやすい対象に触れた", "私·私所が出た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN22-P07"][:40] + "…",
            "secondaryObserve": "六見處",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "「私」への欲しがりと都合に曲げる把握を見る",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、私·都合への欲しがりが立つ",
            "toNext": "止めないと法の悪掴みへ",
            "todayObserve": OBSERVE["MN22-P08"],
            "todayAction": actions["MN22-P08"],
            "when": ["体調や感情に執着した", "都合に曲げそう"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN22-P08"][:40] + "…",
            "secondaryObserve": OBSERVE["MN22-P10"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "法を悪く掴まず、筏のごとく「私の理解」も緩める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、論詰·正しさの掴みが手前",
            "toNext": "誤掴みは蛇に噛まれるように苦になる",
            "todayObserve": OBSERVE["MN22-P02"],
            "todayAction": actions["MN22-P02"],
            "when": ["論争の材料にしたくなった", "正しい理解に執着した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN22-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN22-P06"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "intention", "nidanaLabel": "苦が太る",
            "pathFactors": ["正思惟", "正見"], "pathFactorIds": ["intention", "view"],
            "pathLabel": "欲の蛇の頭の過害を見て、少楽多苦の危険を知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、欲の過害が見える",
            "toNext": "見れば、正しく掴み·筏の離しへ",
            "todayObserve": OBSERVE["MN22-P04"],
            "todayAction": actions["MN22-P04"],
            "when": ["快楽に引かれた", "過害を思い出した"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN22-P04"][:40] + "…",
            "secondaryObserve": "欲如毒蛇",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "慧で正しく掴み、筏の超脱へ——執着だけを手放す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、善掴みと捨棄へ向き直る",
            "toNext": "離せば、夜の苦·止滅の見直しへ",
            "todayObserve": OBSERVE["MN22-P03"],
            "todayAction": actions["MN22-P03"],
            "when": ["慧で意味を見た", "執着を緩めた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN22-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN22-P05"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "苦と止滅の報知に照らして、今日の執着を捨棄する",
            "chapterHint": SHORT,
            "fromPrev": "一日の掴みは、朝からの妄見·執着の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN22-P09"],
            "todayAction": actions["MN22-P09"],
            "when": ["一日を閉じるとき", "執着を手放した夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN22-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN22-P12"],
        },
    ]

    out = {
        "chapter": 22,
        "sutta": 22,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：蛇の喩えの経）",
        "suttas": ["MN 22 蛇喩経（蛇の喩えの経）"],
        "source": {
            "primary": "パーリ・中部第22経（蛇喩経／蛇の喩えの経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含200阿梨吒経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・蛇の喩えの経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・阿梨吒経（T1.763b）",
                    "url": SAT_URL,
                    "note": "阿梨吒·蛇喩·筏喩。對照表: 法雨道場",
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
            "focusReason": "蛇の喩えの経は法の誤把捉と筏の掴みが主題。既定の焦点は掴む。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn022.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 22:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(22, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 12
    assert all(p["id"] == f"MN22-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/12; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
