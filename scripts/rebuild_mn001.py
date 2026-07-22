#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn001.json (根本法門経) to match dhammapada source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0596"
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

# 経典の言葉＝アラナ精舎（根元の教相の経）
QUOTES = {
    "MN1-P01": (
        "比丘たちよ、一切の諸法（事象）の根元の教相を、あなたたちに説示しましょう。"
        "それを聞きなさい。善くしっかりと、意を為しなさい。〔では〕語ります"
    ),
    "MN1-P02": (
        "比丘たちよ、ここに、無聞の凡夫が、聖者たちと会見しない者であり、"
        "聖者たちの法（教え）を熟知しない者であり、聖者たちの法（教え）において教導されず、"
        "正なる人士たちと会見しない者であり、正なる人士たちの法（教え）を熟知しない者であり、"
        "正なる人士たちの法（教え）において教導されず"
    ),
    "MN1-P03": (
        "地を地として表象します。地を地として表象して〔そののち〕、地のことを思い考えます。"
        "地について思い考え、地として思い考え、地を『わたしのものである』と思い考え、地に愉悦します。"
        "それは、何を因とするのですか。『彼には、〔いまだ〕遍知されていないものがあるから』と、〔わたしは〕説きます。"
    ),
    "MN1-P04": (
        "見られたものを見られたものとして表象します。見られたものを見られたものとして表象して〔そののち〕、"
        "見られたもののことを思い考えます。見られたものについて思い考え、見られたものとして思い考え、"
        "見られたものを『わたしのものである』と思い考え、見られたものに愉悦します。"
    ),
    "MN1-P05": (
        "すなわち、また、その比丘が、〔いまだ〕学びある者（有学）であり、〔いまだ〕意図に至り得ていない者であり、"
        "束縛からの平安（軛安穏）という無上なるものを切望しながら〔世に〕住むなら、彼もまた、地を地として証知します。"
        "地を地として証知して〔そののち〕、地のことを思い考えてはなりません。……地に愉悦してはなりません。"
        "それは、何を因とするのですか。『彼には、〔それが〕遍知されるべきであるから』と、〔わたしは〕説きます。"
    ),
    "MN1-P06": (
        "すなわち、また、その比丘が、阿羅漢であり、煩悩（漏）の滅尽者であり、〔梵行の〕完成者であり、"
        "為すべきことを為した者であり、〔生の〕重荷を置いた者であり、正しい了知による解脱者であるなら、"
        "彼もまた、地を地として証知します。……地に愉悦しません。"
        "それは、何を因とするのですか。『彼には、〔それが〕遍知されたから』と、〔わたしは〕説きます。"
    ),
    "MN1-P07": (
        "『愉悦は、苦しみの根元である』と、かくのごとく見出して、『生存から生がある』『生類には老と死がある』と〔知るからです〕。"
        "比丘たちよ、それゆえに、ここに、『如来は。全てにわたり、諸々の渇愛（愛）の、滅尽あることから、"
        "離貪あることから、止滅あることから、施捨あることから、放棄あることから、無上なる正等覚を現正覚したのだ』と、〔わたしは〕説きます。"
    ),
    "MN1-P08": (
        "彼もまた、地を地として証知します。地を地として証知して〔そののち〕、"
        "地のことを思い考えてはなりません。……地に愉悦してはなりません。"
        "それは、何を因とするのですか。『彼には、〔それが〕遍知されるべきであるから』と、〔わたしは〕説きます。"
    ),
    "MN1-P09": (
        "涅槃を涅槃として表象します。涅槃を涅槃として表象して〔そののち〕、涅槃のことを思い考えます。"
        "涅槃について思い考え、涅槃として思い考え、涅槃を『わたしのものである』と思い考え、涅槃に愉悦します。"
        "それは、何を因とするのですか。『彼には、〔いまだ〕遍知されていないものがあるから』と、〔わたしは〕説きます。"
    ),
    "MN1-P10": "それを聞きなさい。善くしっかりと、意を為しなさい。〔では〕語ります",
    "MN1-P11": (
        "世尊は、この〔言葉〕を言いました。"
        "それらの比丘たちは、世尊の語ったことを大いに喜ばなかった（愉悦しなかった）、ということです。"
    ),
}

# 現代語訳＝南伝大蔵経系の読みやすい現代語（true-buddhismが南伝を公開）
OBSERVE = {
    "MN1-P01": (
        "比丘たちよ、わたしはあなたたちに、一切の法の根本法門を説く。"
        "よく聞き、よく心に留めよ。今、説こう。"
    ),
    "MN1-P02": (
        "教えを十分に聞いていない凡夫は、聖者を認めず、聖なる法を熟知せず、"
        "聖なる法を導きとせず、正なる人を認めず、正なる法を熟知せず、正なる法を導きとしない。"
    ),
    "MN1-P03": (
        "凡夫は地を地と想い、地を『わたしのものだ』と考え、地を喜ぶ。"
        "なぜなら、まだ遍く知っていないからである。"
    ),
    "MN1-P04": (
        "見られたもの・聞かれたものも同じである。"
        "『これはわたしのものだ』と取って喜べば、遍知されていないまま苦が続く。"
    ),
    "MN1-P05": (
        "学びの途上にある比丘（有学）は、地を地として正しく知るが、"
        "『わたしのものだ』と考えてはならず、地を喜んではならない。"
        "なぜなら、まだ遍く知るべきだからである。"
    ),
    "MN1-P06": (
        "阿羅漢は地を地として正しく知り、考えず、『わたしのものだ』とせず、喜ばない。"
        "なぜなら、すでに遍く知ったからである。"
    ),
    "MN1-P07": (
        "如来は、喜びが苦の根本であることを知り、有から生があり、生類に老死があることを知る。"
        "ゆえに一切の渇愛を滅尽し、離貪・止滅・捨棄によって無上の正等覚を現正覚した。"
    ),
    "MN1-P08": (
        "正見とは対象を否定することではない。"
        "地を地として正しく知り、逆さまに取らず、喜びに乗らないことである。"
    ),
    "MN1-P09": (
        "涅槃まで『わたしの涅槃だ』と想い、涅槃を喜べば、解脱さえ概念の執着になる。"
        "遍知されていないからである。"
    ),
    "MN1-P10": "よく聞き、心にしっかりと留めよ。今、説く。",
    "MN1-P11": (
        "世尊がこう説かれたとき、比丘たちは大いに喜ばなかった。"
        "根本法門は、対象への愉悦を根として見抜く深い教えである。"
    ),
}

PRACTICE = {
    "MN1-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "一切法の根本法門を聞く入口",
        "section": "導",
        "category": "mindfulness",
    },
    "MN1-P02": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "無聞の凡夫として教えに触れない構造",
        "section": "凡夫",
        "category": "view",
    },
    "MN1-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "地を『わたしのもの』として喜ぶ欲しがり",
        "section": "凡夫·地",
        "category": "intention",
    },
    "MN1-P04": {
        "nidanaId": "clinging",
        "pathFactors": ["正念", "正見"],
        "reason": "見聞を『わたしのもの』として掴む",
        "section": "凡夫·見聞",
        "category": "mindfulness",
    },
    "MN1-P05": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "有学として想せず喜ばず遍知へ向かう",
        "section": "有学",
        "category": "effort",
    },
    "MN1-P06": {
        "nidanaId": "release",
        "pathFactors": ["正定", "正念"],
        "reason": "阿羅漢は遍知ゆえに喜ばない",
        "section": "阿羅漢",
        "category": "concentration",
    },
    "MN1-P07": {
        "nidanaId": "suffering",
        "pathFactors": ["正見"],
        "reason": "愉悦が苦の根元であると見る",
        "section": "如来",
        "category": "view",
    },
    "MN1-P08": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "正しく知るとは逆さまに取らないこと",
        "section": "有学·正知",
        "category": "view",
    },
    "MN1-P09": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "涅槃概念への欲しがり・愉悦",
        "section": "凡夫·涅槃",
        "category": "intention",
    },
    "MN1-P10": {
        "nidanaId": "contact",
        "pathFactors": ["正念"],
        "reason": "善く意を為して聞く",
        "section": "導·聴聞",
        "category": "mindfulness",
    },
    "MN1-P11": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "愉悦に乗らず、根本を夜に見直す",
        "section": "結語",
        "category": "view",
    },
}

# 漢訳＝中阿含106想経（T26）。構成は短縮対応のため、対応弱い箇所は unmapped。
CHINESE = {
    "MN1-P01": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-open",
        "text": "我聞如是。一時佛遊舍衞國在勝林給孤獨園。爾時世尊告諸比丘。",
        "satLocus": "大正蔵 T1.596b 想経第十",
        "note": "対応経は中阿含106想経（及び別訳・楽想経T56）。導入は舎衛／祇園で、パーリ（ウッカッター）と場は異なる。",
    },
    "MN1-P02": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-puthujjana",
        "text": "若有沙門梵志於地有地想。地即是神。地是神所。神是地所。彼計地即是神已便不知地。",
        "satLocus": "大正蔵 T1.596b 想経",
        "note": "漢訳は『凡夫の無聞』を詳述せず、地想＝神と計る誤りとして対応する。",
    },
    "MN1-P03": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-pathavi",
        "text": "若有沙門梵志於地有地想。地即是神。地是神所。神是地所。彼計地即是神已便不知地。如是水火風……",
        "satLocus": "大正蔵 T1.596b 想経",
        "note": "地を地と想い神と計る＝パーリの『わたしのもの／愉悦』に近い執取の漢訳表現。",
    },
    "MN1-P04": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-dittha",
        "text": "一別若干見聞識知得觀意所念意所思。從此世至彼世。從彼世至此世。彼於一切有一切想。",
        "satLocus": "大正蔵 T1.596b–c 想経",
        "note": "見聞識知への想と一切想が、パーリの見聞等への愉悦に対応。",
    },
    "MN1-P05": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-sekha",
        "text": "若有沙門梵志於地則知地。地非是神地非神所神非地所。彼不計地即是神已。彼便知地。",
        "satLocus": "大正蔵 T1.596b–c 想経",
        "note": "正しく知り神と計らない＝有学の『想せず喜ばず』に近い。漢訳は有学／阿羅漢の段階分けが短い。",
    },
    "MN1-P06": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-arahant",
        "text": "彼於一切則知一切。一切非是神一切非神所神非一切所。彼不計一切即是神已。彼便知一切。",
        "satLocus": "大正蔵 T1.596c 想経",
        "note": "遍知して神と計らない。パーリの阿羅漢段（貪瞋痴の滅尽による不愉悦）は漢訳で圧縮。",
    },
    "MN1-P07": {
        "status": "unmapped",
        "pin": "中阿含106・想経（T26）",
        "note": (
            "想経には『愉悦は苦の根元／渇愛滅尽による正覚』の如来段が明示されない。"
            "対応は経全体（想を離れ正しく知る）に留め、本ペアは unmapped。"
        ),
    },
    "MN1-P08": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-yathabhuta",
        "text": "我於地則知地。地非是神地非神所神非地所。我不計地即是神已。我便知地。",
        "satLocus": "大正蔵 T1.596c 想経",
        "note": "正しく知る＝神と計らない知。",
    },
    "MN1-P09": {
        "status": "unmapped",
        "pin": "中阿含106・想経（T26）",
        "note": "想経は涅槃への愉悦を独立に説かない（一切想に含む可能性はあるが、直接対応なし）。",
    },
    "MN1-P10": {
        "status": "mapped",
        "pin": "中阿含106・想経（T26）",
        "t26": "T26-106-listen",
        "text": "爾時世尊告諸比丘。",
        "satLocus": "大正蔵 T1.596b 想経",
        "note": "聴聞の導入。パーリの『善く意を為せ』に相当する文言は漢訳で短い。",
    },
    "MN1-P11": {
        "status": "unmapped",
        "pin": "中阿含106・想経（T26）",
        "note": (
            "パーリ結語は比丘が喜ばなかった。想経結語は『歡喜奉行』で逆。"
            "対応なしとして unmapped。"
        ),
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部1経と中阿含106想経の内容対応（對照表: 法雨道場／蘇錦坤系）。場・段階分けはずれる場合あり。",
        )
    return c


def main():
    old_path = DATA / "majjhima" / "mn001.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES)

    pairs = []
    for i in range(1, 12):
        pid = f"MN1-P{i:02d}"
        pr = PRACTICE[pid]
        factors = pr["pathFactors"]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 1",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": factors,
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー",
                    "locus": f"中部・根元の教相の経（MN1）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 根本法門経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第1経・根本法門経（根元の教相の経）"
    SHORT = "根本法門経（根元の教相の経）"
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
            "pathLabel": "根本法門を聞き、凡夫の無聞に触れる",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の聴聞の土台になる",
            "toNext": "接触のあと、対象への想と受が立ち上がる",
            "todayObserve": OBSERVE["MN1-P01"],
            "todayAction": actions["MN1-P01"],
            "when": ["教えを読むとき", "確信の根拠を問うとき"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN1-P01"][:48] + "…",
            "secondaryObserve": OBSERVE["MN1-P02"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念"], "pathFactorIds": ["mindfulness"],
            "pathLabel": "想と受だけを見て、愉悦の手前で留まる",
            "chapterHint": SHORT,
            "fromPrev": "対象に触れたあと、快・想が立つ",
            "toNext": "止めないと『わたしのもの』への欲しがりへ",
            "todayObserve": "地を地と想う瞬間、快・不快・考えだけを見る。",
            "todayAction": actions["MN1-P03"],
            "when": ["身体・場所に触れた", "情報に触れた"],
            "sources": by_nidana.get("feeling", []) or ["MN1-P03"],
            "leadQuote": QUOTES["MN1-P03"][:40] + "…",
            "secondaryObserve": "想だけを見て、所有の物語に乗せない",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "『わたしのもの』として喜ぶ欲しがりを見抜く",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、地から涅槃まで愉悦へ流れる",
            "toNext": "喜べば掴み、苦が太る",
            "todayObserve": OBSERVE["MN1-P03"],
            "todayAction": actions["MN1-P03"],
            "when": ["欲が出た", "正しさに酔った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN1-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN1-P09"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "見聞の正しさを掴まず、乗せない",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、見聞・所有として掴む手前",
            "toNext": "掴むと苦と老死の流れが見える",
            "todayObserve": OBSERVE["MN1-P04"],
            "todayAction": actions["MN1-P04"],
            "when": ["見た・聞いた情報に乗る前", "これは私だと感じた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN1-P04"][:40] + "…",
            "secondaryObserve": "見聞を『わたしの正しさ』にしない",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見"], "pathFactorIds": ["view"],
            "pathLabel": "愉悦が苦の根元だと見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、有・生・老死が熟す",
            "toNext": "見れば、喜ばず遍知する実践へ向き直る",
            "todayObserve": OBSERVE["MN1-P07"],
            "todayAction": actions["MN1-P07"],
            "when": ["快のあとに重さが出た", "執着の結果を見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN1-P07"][:40] + "…",
            "secondaryObserve": "有より生、生より老死",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "想せず喜ばず、遍知へ戻る",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、有学・阿羅漢の不愉悦へ向き直る",
            "toNext": "離すと、正しく知る夜の見直しへつながる",
            "todayObserve": OBSERVE["MN1-P05"],
            "todayAction": actions["MN1-P05"],
            "when": ["まだ執着があると感じた", "喜ばない知に触れた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN1-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN1-P06"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "どこで喜びに乗ったかを見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の想・愉悦は朝からの流れの跡",
            "toNext": "見直しが、翌朝の根本法門の聴聞になる",
            "todayObserve": OBSERVE["MN1-P08"] + " " + OBSERVE["MN1-P11"],
            "todayAction": actions["MN1-P11"],
            "when": ["一日を閉じるとき", "教えが重く感じた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN1-P11"][:40] + "…",
            "secondaryObserve": OBSERVE["MN1-P08"],
        },
    ]

    out = {
        "chapter": 1,
        "sutta": 1,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：根元の教相の章）",
        "suttas": ["MN 1 根本法門経（根元の教相の経）"],
        "source": {
            "primary": "パーリ・中部第1経（根本法門経／根元の教相の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含106想経（T26）を段落対応でマッピング"
                "（対応なしは明示）。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・根元の教相の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・想経（T1.596b）",
                    "url": SAT_URL,
                    "note": "漢訳対応は段落ごとに異なる。對照表: 法雨道場",
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
            "focusReason": "根本法門経は執着・愉悦の構造が主題。既定の焦点は欲しがる。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn001.json", len(pairs))

    # majjhima index titles
    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 1:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    # path-scene-index: keep dhammapada, add/replace majjhima mn1
    psi_path = DATA / "path-scene-index.json"
    psi = json.loads(psi_path.read_text(encoding="utf-8"))
    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    by_path = defaultdict(list)
    for p in pairs:
        for lab in p["pathFactors"]:
            by_path[LABEL_TO_ID[lab]].append(p["id"])
        by_path[p["category"]].append(p["id"])

    for pid in PATH_ORDER:
        ids = sorted(set(by_path[pid]), key=lambda x: int(x.split("-P")[1]))
        entries = psi["entries"].setdefault(pid, [])
        entries = [
            e for e in entries
            if not (e.get("collectionId") == "majjhima" and e.get("chapterId") == 1)
        ]
        if ids:
            entries.append({
                "collectionId": "majjhima",
                "collectionName": "中部",
                "chapterId": 1,
                "shortTitle": SHORT,
                "title": TITLE,
                "pairCount": len(ids),
                "pairIds": ids,
            })
        psi["entries"][pid] = entries

    psi["scope"] = "dhammapada-ch1-ch26+majjhima-mn1"
    psi_path.write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN1-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    assert all(p["alignment"]["chinese"]["status"] in ("mapped", "unmapped") for p in pairs)
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] == "unmapped"]
    assert unmapped == ["MN1-P07", "MN1-P09", "MN1-P11"], unmapped
    print("OK unmapped", unmapped)


if __name__ == "__main__":
    main()
