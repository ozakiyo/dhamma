#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch4.json (花品) to match ch1–ch3 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-04"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0563"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap04/"
)

QUOTES = {
    44: "誰が、この地を征圧するのだろう──そして、夜魔（閻魔）の世を、天を含むこの〔世〕を。誰が、見事に説示された法（真理）の句を〔摘み取るのだろう〕──巧みな智ある者が、〔真理の〕花を摘み取るように。",
    45: "学びある者（有学）が、〔この〕地を征圧するであろう──そして、夜魔の世を、天を含むこの〔世〕を。学びある者が、見事に説示された法（真理）の句を〔摘み取るであろう〕──巧みな智（善巧）ある者が、〔真理の〕花を摘み取るように。",
    46: "この身体を、泡沫の如きものと知って、陽炎の法（性質）あるものと、現に正覚している者は、悪魔の諸々の花の矢（迷いの生存）を断ち切って、死魔の王の見えざるところ（彼岸）に去り行くであろう。",
    47: "まさしく、まさに、花々を摘んでいる執着の意図ある人を、死魔は取って去り行く──眠りについた村を、大激流が〔流し去ってしまう〕ように。",
    48: "まさしく、まさに、花々を摘んでいる執着の意図ある人を、まさしく、諸々の欲望〔の対象〕に満足しない者を、死神は〔思いのままに〕支配を為す。",
    49: "たとえば、また、蜜蜂が、色艶と香りある花を損なうことなく、味（蜜）を取って移り行くように、このように、牟尼（沈黙の聖者）は、村を歩むがよい。",
    50: "他者たちの諸々の過ちではなく、他者たちの為したことや為さなかったことではなく、まさしく、自己の、諸々の為したことを、さらに、諸々の為さなかったことを、〔智慧の眼で〕注視するがよい。",
    51: "たとえば、また、好ましく、色艶ある花に、香り無きものがあるように、このように、見事に語られた言葉は、為さずにいる者には、果の無きものと成る。",
    52: "たとえば、また、好ましく、色艶ある花に、香り有るものがあるように、このように、見事に語られた言葉は、為している者には、果の有るものと成る。",
    53: "たとえば、また、山積みの花から、多くの花飾の連なりを作るように、このように、死すべき者（人間）として生まれたなら、多くの善きことを為すべきである。",
    54: "花の香りは、風に逆らって行くことがない。栴檀〔の香り〕も、あるいは、タガラ（伽羅）やマッリカー（ジャスミン）〔の香り〕も、〔風に逆らって行くことは〕ない。しかしながら、正しくある者たちの香りは、風に逆らって行く。正なる人士は、全ての方角に香り行く。",
    55: "栴檀、あるいは、また、タガラ、青蓮、さらに、ヴァッシキー（ジャスミン）──これらの香りある類のなかでは、戒の香りが、無上なるものである。",
    56: "すなわち、この、タガラと栴檀〔の香り〕であるが、この香りは、僅かばかりのもの。しかしながら、〔まさに〕その、戒ある者たちの香りは、最上のものであり、天〔の神々〕たちにおいて香りただよう。",
    57: "彼ら、戒を成就した者たちの〔道を〕──不放逸の住者たちの〔道を〕──正しい了知による解脱者たちの道を──悪魔は知らない。",
    58: "たとえば、塵芥の〔堆積する〕場となり、廃棄された大道において、そこにおいて、清らかな香りがあり、意が喜びとする、〔美しい〕蓮華が生じるように──",
    59: "このように、塵芥の生類（輪廻する有情）たちのなかにおいて、暗愚と成った〔迷える〕凡夫たちに、正等覚者（ブッダ）の弟子は、智慧によって輝きまさる。",
}

OBSERVE = {
    44: "誰かこの地界と閻魔界と天界とを征服する。 誰か妙説の法句を摘み集むること、熟練せる人の花を〔摘む〕如くする。",
    45: "仏教を修する者は、この地界と閻魔界と天界とを征服せん。 仏教を修する者は、妙説の法句を摘み集むること、熟練せる人の花を〔摘む〕如くせん。",
    46: "この身は泡沫に譬うべきを知り、幻影に等しきを悟る人は、魔王の花矢（誘惑）を破り、〔地獄の〕死王（閻魔）に見ゆることなけん。",
    47: "花（快楽）をのみ摘みて心貪着せる人を、死は捉え去る、あたかも眠れる村落を瀑流の〔漂蕩（ひょうとう）し去る〕如く。",
    48: "花をのみ摘みて心貪着し、愛欲に飽くことなき人を死は克服す。",
    49: "蜜蜂の、花と色と香りとを損なうことなく、甘味のみを取り去る如く、かく智者は村落に乞食すべし。",
    50: "他の非違を〔観る〕べからず、他の為せること、為さざりしことを〔観る〕べからず。 ただ自己の為せること（罪過）為さざりしこと（懈怠（けたい））を観るべし。",
    51: "愛すべく色麗しくとも芳香なき花の如く、実行なき人の語は、善く説かるるとも効果なし。",
    52: "愛すべく色麗しく芳香ある花の如く、実行する人の語は、善く説かれてしかも効果あり。",
    53: "堆積せる花より、多くの華鬘を造り得る如く、人と生まれては多くの善事をなすべし。",
    54: "花の香りは風に逆らいて進まず、栴檀（せんだん）・多伽羅（たがら）または茉莉花（まつりか）（香木の名）の〔香り〕も〔また然り〕。 されど善人の香りは風に逆らいても進み、正しき人は一切方に薫ず。",
    55: "栴檀または多伽羅・青蓮華はたまたヴァッシキー（香木の名）、これらの諸香の中、戒の香り最も勝れたり。",
    56: "多伽羅・栴檀に属するその香りは軽微なり。 されど持戒者の香りは最上にして諸天の間に薫ず。",
    57: "戒行を成就し、不放逸に住し、正智により解脱せる者には、魔王も近づくあたわず。",
    58: "大道に捨てられたる塵埃の堆積中に、芳香馥郁（ふくいく）として美しき蓮華の生ずる如く、",
    59: "この如く、塵埃にも等しき盲昧の凡夫中に、正等覚者の弟子は智慧を以て輝く。",
}

# T210 華香品（蘇錦坤對照表）— 44–59 いずれも対応あり
CHINESE = {
    44: {"status": "mapped", "t210": "T210-12-001", "text": "孰能擇地，捨監取天？誰說法句，如擇善華？", "satLocus": "大正蔵 T4.563c 華香品第1頌"},
    45: {"status": "mapped", "t210": "T210-12-002", "text": "學者擇地，捨監取天，善說法句，能採德華。", "satLocus": "大正蔵 T4.563c 華香品第2頌"},
    46: {"status": "mapped", "t210": "T210-12-004", "text": "見身如沫，幻法自然，斷魔華敷，不覩生死。", "satLocus": "大正蔵 T4.563c 華香品第4頌"},
    47: {"status": "mapped", "t210": "T210-12-005", "text": "身病則萎，若華零落；死命來至，如水湍驟。", "satLocus": "大正蔵 T4.563c 華香品第5頌"},
    48: {"status": "mapped", "t210": "T210-12-006", "text": "貪欲無厭，消散人念，邪致之財，為自侵欺。", "satLocus": "大正蔵 T4.563c 華香品第6頌"},
    49: {"status": "mapped", "t210": "T210-12-007", "text": "如蜂集華，不嬈色香，但取味去，仁入聚然。", "satLocus": "大正蔵 T4.563c 華香品第7頌"},
    50: {"status": "mapped", "t210": "T210-12-008", "text": "不務觀彼，作與不作，常自省身，知正不正。", "satLocus": "大正蔵 T4.563c 華香品第8頌"},
    51: {"status": "mapped", "t210": "T210-12-009", "text": "如可意華，色好無香，工語如是，不行無得。", "satLocus": "大正蔵 T4.563c 華香品第9頌"},
    52: {"status": "mapped", "t210": "T210-12-010", "text": "如可意華，色美且香，工語有行，必得其福。", "satLocus": "大正蔵 T4.564a 華香品第10頌"},
    53: {"status": "mapped", "t210": "T210-12-011", "text": "多作寶花，結步搖綺，廣積德者，所生轉好。", "satLocus": "大正蔵 T4.564a 華香品第11頌"},
    54: {"status": "mapped", "t210": "T210-12-012", "text": "奇草芳花，不逆風熏，近道敷開，德人遍香。", "satLocus": "大正蔵 T4.564a 華香品第12頌"},
    55: {"status": "mapped", "t210": "T210-12-013", "text": "旃檀多香，青蓮芳花，雖曰是真，不如戒香。", "satLocus": "大正蔵 T4.564a 華香品第13頌"},
    56: {"status": "mapped", "t210": "T210-12-014", "text": "華香氣微，不可謂真，持戒之香，到天殊勝。", "satLocus": "大正蔵 T4.564a 華香品第14頌"},
    57: {"status": "mapped", "t210": "T210-12-015", "text": "戒具成就，行無放逸，定意度脫，長離魔道。", "satLocus": "大正蔵 T4.564a 華香品第15頌"},
    58: {"status": "mapped", "t210": "T210-12-016", "text": "如作田溝，近于大道，中生蓮華，香潔可意。", "satLocus": "大正蔵 T4.564a 華香品第16頌"},
    59: {"status": "mapped", "t210": "T210-12-017", "text": "有生死然，凡夫處邊，慧者樂出，為佛弟子。", "satLocus": "大正蔵 T4.564a 華香品第17頌"},
}

VERSE_PRACTICE = {
    44: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "誰が法句を花のように摘み取るのかと問う"},
    45: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "有学が法句を摘み、世界を征圧する"},
    46: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "身を泡沫・陽炎と知り魔の花矢を断つ"},
    47: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "花を摘む執着の人を死魔が運び去る"},
    48: {"nidanaId": "craving", "pathFactors": ["正念", "正精進"], "reason": "欲に飽かぬ者を死神が支配する"},
    49: {"nidanaId": "contact", "pathFactors": ["正命", "正念"], "reason": "蜂のように場を損なわず味だけを取る"},
    50: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "他ではなく自己の為した・為さぬを観る"},
    51: {"nidanaId": "clinging", "pathFactors": ["正語", "正業"], "reason": "実行なき美語は香なき花のように実がない"},
    52: {"nidanaId": "clinging", "pathFactors": ["正語", "正業"], "reason": "実行ある美語は香りある花のように実がある"},
    53: {"nidanaId": "contact", "pathFactors": ["正業", "正精進"], "reason": "人と生まれたなら多くの善を為すべき"},
    54: {"nidanaId": "contact", "pathFactors": ["正業", "正念"], "reason": "善人の香りは風に逆らっても四方に薫る"},
    55: {"nidanaId": "contact", "pathFactors": ["正業", "正念"], "reason": "諸香の中で戒の香りが最上である"},
    56: {"nidanaId": "review", "pathFactors": ["正業", "正念"], "reason": "持戒者の香りは諸天の間に薫る"},
    57: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "戒・不放逸・正智の解脱者には魔も近づけない"},
    58: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "塵芥の大道にも清らかな蓮が生じる"},
    59: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "凡夫の中で覚者の弟子は智慧で輝く"},
}

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

# Keep pair IDs; assign primary verse (P01 covers 44–45 theme via v45 answer)
PAIR_META = [
    ("DP4-P01", 45),
    ("DP4-P02", 46),
    ("DP4-P03", 46),
    ("DP4-P04", 47),
    ("DP4-P05", 48),
    ("DP4-P06", 49),
    ("DP4-P07", 49),
    ("DP4-P08", 50),
    ("DP4-P09", 50),
    ("DP4-P10", 51),
    ("DP4-P11", 52),
    ("DP4-P12", 53),
    ("DP4-P13", 54),
    ("DP4-P14", 55),
    ("DP4-P15", 56),
    ("DP4-P16", 57),
    ("DP4-P17", 58),
    ("DP4-P18", 59),
]


def chinese_block(verse: int) -> dict:
    c = dict(CHINESE[verse])
    c["pin"] = "華香品（T210 第12品）"
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    c["note"] = "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号はパーリとずれる場合あり。"
    return c


def main() -> None:
    old = json.loads((DATA / "ch4.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        # P01: show both 44–45 modern/arana (question + answer) for continuity
        if pid == "DP4-P01":
            observe = OBSERVE[44] + " " + OBSERVE[45]
            quote = QUOTES[44] + " " + QUOTES[45]
            pali_locus = "小部・ダンマパダ 花の章 第44-45偈"
            modern_locus = "第４章・花品 第44-45偈（#ch02-04）"
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 花の章 第{verse}偈"
            modern_locus = f"第４章・花品 第{verse}偈（#ch02-04）"

        pairs.append(
            {
                "id": pid,
                "category": LABEL_TO_ID[factors[0]],
                "verse": verse,
                "observe": observe,
                "action": actions[pid],
                "quote": quote,
                "nidanaId": vp["nidanaId"],
                "pathFactors": factors,
                "pathReason": vp["reason"],
                "alignment": {
                    "pali": {
                        "source": "アラナ精舎 経典ライブラリー",
                        "locus": pali_locus,
                        "url": ARANA_URL,
                    },
                    "modern": {
                        "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                        "locus": modern_locus,
                        "url": TB_URL,
                    },
                    "chinese": chinese_block(verse),
                },
            }
        )

    # Ensure verse 44 chinese/path also reachable: add P01 chinese from 45 is OK;
    # also stamp versePracticeMap includes 44.
    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第4章・花品（花の章）"
    SHORT = "花品（花の章）"
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
            "id": "contact",
            "weekday": 1,
            "categoryId": "view",
            "nidanaLabel": "接触",
            "pathFactors": ["正見", "正念"],
            "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "触れた場で法句を花のように摘む",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見方が、今朝の接触の土台になる",
            "toNext": "止めないと、快・不快の受が立ち上がる",
            "todayObserve": OBSERVE[45],
            "todayAction": actions["DP4-P01"],
            "when": ["通知が来た", "学びの言葉に触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[45][:42] + "…",
            "secondaryObserve": "蜂のように場を損なわず、必要な味だけを取る",
        },
        {
            "id": "feeling",
            "weekday": 2,
            "categoryId": "mindfulness",
            "nidanaLabel": "受ける",
            "pathFactors": ["正念"],
            "pathFactorIds": ["mindfulness"],
            "pathLabel": "快の花に心が寄っていないか見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、快・不快の受が立ち上がる",
            "toNext": "止めないと欲しがりへ進む",
            "todayObserve": OBSERVE[47],
            "todayAction": actions["DP4-P04"],
            "when": ["気持ちよくなった", "つい手を伸ばした"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[47][:42] + "…",
            "secondaryObserve": "快楽を摘む手を止め、大切な一事へ戻る",
        },
        {
            "id": "craving",
            "weekday": 3,
            "categoryId": "intention",
            "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"],
            "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "花を摘む執着を手放す",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、もっと欲しいへ落ちる",
            "toNext": "止めないと掴みに進む",
            "todayObserve": OBSERVE[48],
            "todayAction": actions["DP4-P05"],
            "when": ["もっと欲しい", "飽きれない"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[48][:42] + "…",
            "secondaryObserve": "欲に飽かぬ心を、死神が支配する",
        },
        {
            "id": "clinging",
            "weekday": 4,
            "categoryId": "speech",
            "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正業"],
            "pathFactorIds": ["speech", "action"],
            "pathLabel": "言葉だけでなく実行で掴み直す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、語り・行いに乗る手前",
            "toNext": "実行なき美語は実を結ばない",
            "todayObserve": OBSERVE[51],
            "todayAction": actions["DP4-P10"],
            "when": ["立派なことを言った", "まだ動いていない"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[51][:42] + "…",
            "secondaryObserve": "実行ある言葉は、香りある花のように実がある",
        },
        {
            "id": "suffering",
            "weekday": 5,
            "categoryId": "view",
            "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"],
            "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "塵芥の中にも蓮が咲くと見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、心や関係が重くなる",
            "toNext": "見ないままだと凡夫のまま沈む",
            "todayObserve": OBSERVE[59],
            "todayAction": actions["DP4-P17"],
            "when": ["苦しい状況", "周囲が暗い"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[59][:42] + "…",
            "secondaryObserve": "泥の中から蓮が咲くように、智慧は輝く",
        },
        {
            "id": "release",
            "weekday": 6,
            "categoryId": "mindfulness",
            "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正定"],
            "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "魔の花矢を断ち、戒と正智で離す",
            "chapterHint": SHORT,
            "fromPrev": "執着と放逸が流れを加速させる",
            "toNext": "戒・不放逸・正智なら魔も近づけない",
            "todayObserve": OBSERVE[57],
            "todayAction": actions["DP4-P16"],
            "when": ["誘惑が強い", "気を抜きたくなった"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[57][:42] + "…",
            "secondaryObserve": "身を泡沫と知り、死王の見えぬところへ",
        },
        {
            "id": "review",
            "weekday": 0,
            "categoryId": "mindfulness",
            "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"],
            "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "他ではなく自己の行いを見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の語り・行いは朝からの心の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE[50],
            "todayAction": actions["DP4-P09"],
            "when": ["一日を閉じるとき", "誰かを批判した日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[50][:42] + "…",
            "secondaryObserve": "戒の香りは、諸天の間にも薫る",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 4,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第4章（花品／花の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210華香品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（ダンマパダ・花の章）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（第４章・花品）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記",
                },
                "chinese": {
                    "label": "SAT 法句経・華香品（T4.563c）",
                    "url": SAT_URL,
                    "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤",
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
                {"id": "view", "label": "正見"},
                {"id": "intention", "label": "正思惟"},
                {"id": "speech", "label": "正語"},
                {"id": "action", "label": "正業"},
                {"id": "livelihood", "label": "正命"},
                {"id": "effort", "label": "正精進"},
                {"id": "mindfulness", "label": "正念"},
                {"id": "concentration", "label": "正定"},
            ],
            "nodes": nodes,
            "focusNodeId": "contact",
            "focusReason": "花品は接触の場で法句を摘み取る比喩が中心。既定の焦点は接触。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch4.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote ch4.json", len(pairs))

    # Rebuild path-scene-index for ch1–ch4
    PATH_ORDER = [
        "view",
        "intention",
        "speech",
        "action",
        "livelihood",
        "effort",
        "mindfulness",
        "concentration",
    ]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id, fname in [(1, "ch1.json"), (2, "ch2.json"), (3, "ch3.json"), (4, "ch4.json")]:
        d = json.loads((DATA / fname).read_text(encoding="utf-8"))
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
            entries[pid].append(
                {
                    "collectionId": "dhammapada",
                    "collectionName": "ダンマパダ",
                    "chapterId": ch_id,
                    "shortTitle": d["shortTitle"],
                    "title": d["title"],
                    "pairCount": len(ids),
                    "pairIds": ids,
                }
            )

    psi = {
        "version": 1,
        "scope": "dhammapada-ch1-ch4",
        "entries": entries,
    }
    (DATA / "path-scene-index.json").write_text(
        json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("path-scene-index scope", psi["scope"])
    for k, v in entries.items():
        print(k, [(e["chapterId"], e["pairCount"]) for e in v])

    assert len(out["pairs"]) == 18
    assert all(p["id"] == f"DP4-P{i:02d}" for i, p in enumerate(out["pairs"], 1))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in out["pairs"])
    verses = sorted({p["verse"] for p in out["pairs"]})
    print("verses covered", verses)
    print("OK")


if __name__ == "__main__":
    main()
