#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn026.json (聖求経／聖求の経) to match MN1–25 source alignment.

Note: Arana mid-cache ends at MN25; quotes follow Arana-style Japanese from the
Pāli of MN26 (Ariyapariyesanā / Pāsarāsi), cross-checked with 中阿含204羅摩経.
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0775c01"
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
    "MN26-P01": (
        "比丘たちよ、二つの探求があります。聖なる探求と、聖ならざる探求です。"
    ),
    "MN26-P02": (
        "比丘たちよ、聖ならざる探求とは、何ですか。"
        "比丘たちよ、ここに、或る者が、自ら生の法を有しながら、生の法を探し求めます。"
        "自ら老の法を有しながら、老の法を……病……死……憂……穢汚の法を探し求めます。"
        "……妻子・奴婢・山羊・鶏・象牛馬・金銀——それらに縛られ、狂い、執着して、"
        "自ら生の法を有しながら生の法を探し求める——これが、聖ならざる探求です。"
    ),
    "MN26-P03": (
        "比丘たちよ、聖なる探求とは、何ですか。"
        "比丘たちよ、ここに、或る者が、自ら生の法を有しながら、生の法における災患を知り、"
        "生なき、無上の安穏なる涅槃を探し求めます。"
        "自ら老……病……死……憂……穢汚の法を有しながら、その災患を知り、"
        "老なき……穢汚なき、無上の安穏なる涅槃を探し求めます。"
        "比丘たちよ、これが、聖なる探求です。"
    ),
    "MN26-P04": (
        "そこで、わたしに、このような〔思いが〕有りました。"
        "『この法は、厭離に導かず、離貪に導かず、滅尽に導かず、寂静に導かず、"
        "勝智に導かず、正覚に導かず、涅槃に導かない。"
        "それは、ただ、無所有処への再生に至るまでのものである』と。"
        "……『……それは、ただ、非想非非想処への再生に至るまでのものである』と。"
        "この法が不充分であると了知して、わたしは不満を抱き、去りました。"
        "（アーラーラ・カーラーマ／ウッダカ・ラーマプッタのもとでの最上の定。）"
    ),
    "MN26-P05": (
        "比丘たちよ、五つの欲望の属性があります。……色・声・香・味・触……。"
        "……災患を見、出要を了知して受ける者——罠の山に捕らわれぬ鹿のごとく……。"
        "……諸々の欲望から離れて……第一の瞑想を成就して住む者は、"
        "『悪魔を盲者に作り為した……パーピマントの見なきところに至り』と説かれます。"
        "（漢訳羅摩経では、五比丘への教示に二邊を捨て八正道を取る段もあり。）"
    ),
    "MN26-P06": (
        "そこで、わたしに、このような〔思いが〕有りました。"
        "『わたしによって証得された、この法は、深遠で、見難く、了知し難く、"
        "寂静で、勝れ、思惟の領分を超え、微妙で、賢者の知るべきものである。"
        "しかしながら、人々は執着を好み、執着を愛し、執着を楽しむ。"
        "……縁起……一切の行の止滅……渇愛の滅尽……涅槃は、彼らにとって見難い。"
        "もし、わたしが法を説くなら、他者たちがわたしを了知しないかもしれず、"
        "それはわたしにとって疲弊と悩苦と成るであろう』と。"
    ),
    "MN26-P07": (
        "そこで、サハンパティ梵天は……わたしの前に現れ……こう言いました。"
        "『尊き方よ、世尊は、法を説いてください。善逝は、法を説いてください。"
        "眼に塵の少なき有情たちがいます。彼らは、法を聞かずに衰退します。"
        "法を了知する者たちがあるでしょう』と。"
        "……『不死の門は、開かれました。耳ある者たちは、信を発してください』と。"
    ),
    "MN26-P08": (
        "そこで、わたしに、このような〔思いが〕有りました。"
        "『五人の比丘たちは、わたしにとって多くを為した。"
        "わたしが精励していたとき、彼らはわたしを世話した。"
        "それなら、さあ、わたしは、まず彼らに法を説示しよう』と。"
        "……わたしは、五人の比丘たちを説得することができました。"
    ),
    "MN26-P09": (
        "比丘たちよ、五つの欲望の属性があります。"
        "眼によって識知されるべき諸々の色形……身によって識知されるべき諸々の感触……。"
        "……それらに縛られ、狂い、執着し、災患を見ず、出要を了知せずして受ける者は、"
        "不幸に落ち、滅び、魔の思うままの所にある、と了知されるべきです。"
        "……たとえば、また、林野の鹿が、罠の山に捕らえられて横たわっているとします……。"
    ),
    "MN26-P10": (
        "まさに、このように教え示され、教え諭されながら、五人の比丘たちは、"
        "自ら生の法を有しながら、生の法における災患を知り、"
        "生なき、無上の安穏なる涅槃を探し求め——そして、それを得ました。……"
        "……わたしに、知見が生じました。"
        "『わたしの解脱は、不動である。これは、最後の生である。いまや、再生は無い』と。"
    ),
    "MN26-P11": (
        "（漢訳・羅摩経）五比丘！當知有二邊行，諸為道者所不當學："
        "一曰著欲樂下賤業，凡人所行；二曰自煩自苦，非賢聖求法，無義相應。"
        "五比丘！捨此二邊，有取中道……謂八正道，正見乃至正定。"
        "（パーリ聖求経は同段で五欲·罠山·禅定を説く。非聖求の快楽執着と、"
        "定のみで足りると見る偏りを、二邊の実践に対応させる。）"
    ),
    "MN26-P12": (
        "自ら生の法を有しながら、生の法における災患を知り、"
        "生なき、無上の安穏なる涅槃を探し求める。……老……病……死……憂……穢汚……。"
        "（漢訳では漏尽の知見として苦·集·滅·道を如実に知る段もあり。）"
    ),
    "MN26-P13": (
        "比丘たちよ、二つの探求があります。聖なる探求と、聖ならざる探求です。"
        "……聖なる探求とは……災患を知り、無上の安穏なる涅槃を探し求めることです。"
    ),
}

OBSERVE = {
    "MN26-P01": (
        "探求は二つ——聖ならざる求（生老病死等の法を追う）と、聖なる求（災患を知り涅槃を求む）——"
        "朝、今日の「欲しい」がこの岸の快楽か、彼岸の安らぎか一度問う。"
    ),
    "MN26-P02": (
        "非聖求——自ら生·老·病·死·憂·穢汚の法を有しながら、妻子·財貨など同じ法を求め、縛られ狂い執着する——"
        "今日、快楽の裏に「いつか終わる」を一瞬思い出す。"
    ),
    "MN26-P03": (
        "聖求——生等の災患を知り、生なき無上の安穏なる涅槃を探し求める——"
        "一つの苦について「害い（害）」を静かに認める。"
    ),
    "MN26-P04": (
        "二師の定——無所有処·非想非非想処。厭離·離貪·涅槃に導かず不充分と知り去る——"
        "今日、過度な私慢と油断のどちらに偏っていないか確認する。"
    ),
    "MN26-P05": (
        "五欲の罠山から逃れ、魔の見なき処（初禅等）へ。漢訳は二邊を捨て八正道を取る——"
        "今日、八正道のうち一つを意識して歩む。"
    ),
    "MN26-P06": (
        "証得の法は深遠·見難い。人々は執着を好み、縁起と涅槃は見難い——急いで証明しようとしない——"
        "今日、深い法を急いで証明しようとする衝動を一度止める。"
    ),
    "MN26-P07": (
        "サハンパティ梵天の勧請——眼に塵の少なき有情あり、法を聞かずして衰退する。不死の門を開け——"
        "今日、相手の準備が整うまで、言葉を一度控える。"
    ),
    "MN26-P08": (
        "五比丘への初教——精励のときの世話に報い、まず彼らに法を説く。学ぶ姿勢で聞く——"
        "今日、誰かから学ぶ姿勢を一つ執着する。"
    ),
    "MN26-P09": (
        "五欲——縛られ狂い執着し、災患を見ず出要を知らねば魔の思うまま。罠の山に捕らわれた鹿——"
        "今日強く「欲しい」と感じた対象の愛を、一度緩める。"
    ),
    "MN26-P10": (
        "五比丘も聖求を体得——解脱は不動、これ最後の生、再生は無い——"
        "今日、執着が弱まった瞬間を「解脱の知」と認める。"
    ),
    "MN26-P11": (
        "二邊（漢訳）——欲楽への耽溺と自苦。非聖求の快楽逃避と「定で足りる」固執のどちらにも偏らない——"
        "今日、快楽への逃避と苦行への固執のどちらかに偏っていないか問う。"
    ),
    "MN26-P12": (
        "聖求の見分け——今日の苦を生·老·病·死·憂·穢汚のどれか／災患と逃れ（涅槃）で見る。"
        "漢訳は苦·集·滅·道の如実知もあり——"
        "今日の苦一つを、四諦の四句のどれに当てはまるか静かに見分ける。"
    ),
    "MN26-P13": (
        "夜、二つの探求を振り返る——今日、非聖求に流れたか、聖求（災患を知り涅槃へ）を修したか——"
        "就寝前、今日四諦·縁起のうちどれを修したか一つ振り返り、明日も続ける。"
    ),
}

PRACTICE = {
    "MN26-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、今日の欲しさが聖求か非聖求か問う",
        "section": "二種の探求",
        "category": "mindfulness",
    },
    "MN26-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正見"],
        "reason": "生老等と同じ法への欲しがりを非聖求として見る",
        "section": "聖ならざる探求",
        "category": "intention",
    },
    "MN26-P03": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正思惟"],
        "reason": "災患を認め、無上の安穏なる涅槃へ向き直る",
        "section": "聖なる探求",
        "category": "view",
    },
    "MN26-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正精進"],
        "reason": "最上の定への私慢·油断を離し、涅槃に導くかを問う",
        "section": "二師の定",
        "category": "view",
    },
    "MN26-P05": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "八正道の一歩で罠山から逃れ、魔の見なき処へ",
        "section": "罠山·出要",
        "category": "effort",
    },
    "MN26-P06": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "深法を急いで証明したい受を一度止める",
        "section": "深法·執着を好む世",
        "category": "mindfulness",
    },
    "MN26-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正思惟"],
        "reason": "相手の準備が整うまで語を控え、塵の少なき耳を待つ",
        "section": "梵天勧請",
        "category": "speech",
    },
    "MN26-P08": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正語"],
        "reason": "学ぶ姿勢で法に触れ、初教を受ける",
        "section": "五比丘への初教",
        "category": "mindfulness",
    },
    "MN26-P09": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "五欲への欲しがりを罠山として緩める",
        "section": "五欲·罠山",
        "category": "intention",
    },
    "MN26-P10": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正念"],
        "reason": "執着が弱まった瞬間を不動の解脱の知として認める",
        "section": "解脱の知見",
        "category": "view",
    },
    "MN26-P11": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正精進"],
        "reason": "快楽逃避と自苦の二邊の苦を見て中道へ",
        "section": "二邊（漢訳対応）",
        "category": "view",
    },
    "MN26-P12": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "今日の苦を聖求の見分け（災患·逃れ）／四諦で照らす",
        "section": "災患と四諦",
        "category": "view",
    },
    "MN26-P13": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "夜、二種の探求と修した法を一つ振り返る",
        "section": "夜の聖求",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN26-P01": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-two",
        "text": "有二種求，一曰聖求，二曰非聖求。",
        "satLocus": "大正蔵 T1.776a 羅摩経",
        "note": "二種求＝聖求·非聖求。",
    },
    "MN26-P02": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-anariya",
        "text": (
            "云何非聖求？……兒子、兄弟……象馬、牛羊、奴婢、錢財……"
            "眾生於中觸染貪著，憍慠受入，不見災患，不見出要，而取用之。……是謂非聖求。"
        ),
        "satLocus": "大正蔵 T1.776a 羅摩経",
        "note": "非聖求——病老死等の法を求める。",
    },
    "MN26-P03": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-ariya",
        "text": (
            "云何聖求耶？……我今寧可求無病無上安隱涅槃，求無老、無死……無穢污法無上安隱涅槃。"
        ),
        "satLocus": "大正蔵 T1.776a 羅摩経",
        "note": "聖求——無病等の無上安隱涅槃。",
    },
    "MN26-P04": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-teachers",
        "text": (
            "此法不趣智，不趣覺，不趣涅槃，我今寧可捨此法，更求無病無上安隱涅槃……。"
            "（阿羅羅伽羅摩·欝陀羅羅摩子。）"
        ),
        "satLocus": "大正蔵 T1.776b–777a 羅摩経",
        "note": "不趣涅槃＝パーリの厭離等に導かず。",
    },
    "MN26-P05": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-path",
        "text": (
            "捨此二邊，有取中道……謂八正道，正見乃至正定，是謂為八。"
            "……有五欲功德……見災患，見出要，而取用之。"
        ),
        "satLocus": "大正蔵 T1.777c–778b 羅摩経",
        "note": "漢訳は八正道と五欲出要。パーリは罠山·禅定を詳説。",
    },
    "MN26-P06": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-deep",
        "text": (
            "（パーリ詳説：法は深遠·見難く、人々は執着を好む。"
            "漢訳は成道後すぐ五比丘を選ぶ流れが主で、梵天勧請段は薄い／欠く場合あり。）"
        ),
        "satLocus": "大正蔵 T1.777a 羅摩経（対照）",
        "note": "深法·執着を好む世はパーリ中心。對照表で羅摩経対応。",
    },
    "MN26-P07": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-teach",
        "text": (
            "我至波羅［木＊奈］，擊妙甘露鼓，轉無上法輪，世所未曾轉。"
            "（パーリ：梵天勧請「願世尊說法……眼塵少者……」。）"
        ),
        "satLocus": "大正蔵 T1.777b 羅摩経",
        "note": "説法の決意。パーリの梵天勧請に対応する実践（相手の準備）。",
    },
    "MN26-P08": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-five",
        "text": (
            "昔五比丘為我執勞，多所饒益……我今寧可為五比丘先說法耶？"
            "……五比丘！我如來、無所著、正盡覺，汝等莫稱我本姓字……。"
        ),
        "satLocus": "大正蔵 T1.777b–c 羅摩経",
        "note": "五比丘への初教。",
    },
    "MN26-P09": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-kama",
        "text": (
            "有五欲功德可愛、可樂……眼知色，耳知聲……身知觸。"
            "……不見災患，不見出要，而取用之。當知彼隨弊魔……為魔羂所纏。"
            "猶如野鹿，為纏所纏……。"
        ),
        "satLocus": "大正蔵 T1.778a 羅摩経",
        "note": "五欲·魔羂＝パーリの五欲·罠山。",
    },
    "MN26-P10": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-vimutti",
        "text": (
            "生知生見，定道品法，生已盡，梵行已立，所作已辦，不更受有，知如真。"
            "……是說無病無上安隱涅槃……。"
        ),
        "satLocus": "大正蔵 T1.777c / T1.778c 羅摩経",
        "note": "解脱の知見＝不動·最後の生。",
    },
    "MN26-P11": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-extremes",
        "text": (
            "當知有二邊行，諸為道者所不當學：一曰著欲樂下賤業，凡人所行；"
            "二曰自煩自苦，非賢聖求法，無義相應。捨此二邊，有取中道……。"
        ),
        "satLocus": "大正蔵 T1.777c 羅摩経",
        "note": "二邊は漢訳に明示。パーリMN26は同段で五欲·罠を説く。",
    },
    "MN26-P12": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-sacca",
        "text": (
            "彼知此苦如真，知此苦習、知此苦滅、知此苦滅道如真。"
            "知此漏如真……解脫已便知解脫……。"
        ),
        "satLocus": "大正蔵 T1.778b 羅摩経",
        "note": "四諦·漏の如実知（漢訳）。パーリは聖求の災患·涅槃の見分け。",
    },
    "MN26-P13": {
        "status": "mapped",
        "pin": "中阿含204・羅摩経（T26）",
        "t26": "T26-204-close",
        "text": "有二種求，一曰聖求，二曰非聖求。……是說無病無上安隱涅槃……。",
        "satLocus": "大正蔵 T1.776a / T1.778c 羅摩経",
        "note": "二種求と涅槃の総括。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部26経と中阿含204羅摩経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn026.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 14):
        pid = f"MN26-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 26",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・聖求の経／パーリMN26）",
                    "locus": f"中部・聖求の経（MN26）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 聖求経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第26経・聖求経（聖求の経）"
    SHORT = "聖求経（聖求の経）"
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
            "pathFactors": ["正念", "正語"], "pathFactorIds": ["mindfulness", "speech"],
            "pathLabel": "朝、聖求か非聖求か問い、学ぶ姿勢で法に触れる",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の欲しさの接触を変える",
            "toNext": "触のあと、証明したい受や学ぶ受が見える",
            "todayObserve": OBSERVE["MN26-P01"],
            "todayAction": actions["MN26-P01"],
            "when": ["朝に欲しさを問うた", "学ぶ姿勢で聞いた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN26-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN26-P07"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "深法を急いで証明したい受を止め、学ぶ姿勢で受ける",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、理解したい·証明したい受が立つ",
            "toNext": "受に乗ると非聖の欲しがりへ",
            "todayObserve": OBSERVE["MN26-P06"],
            "todayAction": actions["MN26-P06"],
            "when": ["急いで証明したくなった", "学ぶ姿勢で受けた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN26-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN26-P08"],
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "非聖求と五欲の欲しがりを罠として緩める",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、生老と同じ法・五欲への欲しがりが立つ",
            "toNext": "止めないと定·私慢の掴みへ",
            "todayObserve": OBSERVE["MN26-P02"],
            "todayAction": actions["MN26-P02"],
            "when": ["快楽を追った", "五欲に引かれた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN26-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN26-P09"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "最上の定への私慢·油断を離し、涅槃に導くかを問う",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、「これで足りる」掴みが手前",
            "toNext": "掴むと二邊の苦が見える",
            "todayObserve": OBSERVE["MN26-P04"],
            "todayAction": actions["MN26-P04"],
            "when": ["私慢が出た", "定で足りると掴んだ"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN26-P04"][:40] + "…",
            "secondaryObserve": "不趣涅槃",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "快楽逃避と自苦の二邊の苦を見て中道へ",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、二邊の患が見える",
            "toNext": "見れば、聖求と出要の離しへ",
            "todayObserve": OBSERVE["MN26-P11"],
            "todayAction": actions["MN26-P11"],
            "when": ["快楽に逃げた", "自苦に偏った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN26-P11"][:40] + "…",
            "secondaryObserve": "二邊行",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "災患を知り涅槃を求め、罠山から逃れ解脱の知へ",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、聖求と八正道の一歩へ",
            "toNext": "離せば、夜の四諦·縁起の見直しへ",
            "todayObserve": OBSERVE["MN26-P03"],
            "todayAction": actions["MN26-P03"],
            "when": ["害いを認めた", "執着が弱まった"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN26-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN26-P10"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "今日の苦を聖求·四諦で見分け、二種の探求を振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の欲しさは、朝からの探求の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN26-P12"],
            "todayAction": actions["MN26-P12"],
            "when": ["一日を閉じるとき", "四諦を振り返った夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN26-P12"][:40] + "…",
            "secondaryObserve": OBSERVE["MN26-P13"],
        },
    ]

    out = {
        "chapter": 26,
        "sutta": 26,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：聖求の経／Pāsarāsi）",
        "suttas": ["MN 26 聖求経（聖求の経）"],
        "source": {
            "primary": "パーリ・中部第26経（聖求経／聖求の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN26（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含204羅摩経（T26）。"
                "パーリは聖求·二師·梵天勧請·五欲·罠山·禅定が中心。"
                "漢訳は五比丘教示に二邊·八正道·四諦を含む（段差はnoteで明示）。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・聖求の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（聖求／わな山）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・羅摩経（T1.775c）",
                    "url": SAT_URL,
                    "note": "聖求·非聖求·阿羅羅·欝陀羅·五比丘·五欲。對照表: 法雨道場",
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
            "focusReason": "聖求経は災患を知り無上の安穏なる涅槃を探し求めるのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn026.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 26:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(26, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 13
    assert all(p["id"] == f"MN26-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/13; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
