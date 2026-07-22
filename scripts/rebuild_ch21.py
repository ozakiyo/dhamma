#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch21.json (雑品) to match ch1–ch20 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-21"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0569"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap21/"
)

QUOTES = {
    290: "もし、少量なる安楽を完全に捨て去ることから、広大なる安楽を見ることになるなら、慧者は、少量なる安楽を捨て去るであろう──広大なる安楽を〔常に〕正しく見ている者として。",
    291: "他者に苦痛を与えることで、自己の安楽を求める、怨み〔の思い〕と持ちつ持たれつの者──彼は、怨み〔の思い〕から完全に解き放たれない。",
    292: "まさに、その、為すべきことが捨てられ、いっぽうで、為すべきではないことが為されるなら、傲慢で〔気づきを〕怠る彼らの、諸々の煩悩は増え行く。",
    293: "しかしながら、彼らに、常に、身体の在り方についての気づき（身至念：時々刻々の身体の状態についての気づき）があり、善く努め励むところとなるなら、彼らは、〔もはや〕為すべきではないことに慣れ親しまず、諸々の為すべきことを常に為す者たちとなる。気づきと正知の者たちの、諸々の煩悩は〔自ずと〕滅却に至る。",
    294: "母（渇愛）と父（「わたしは存在する」という思量）を打ち砕いて、そして、二者の士族の王（常住論と断滅論）を〔打ち砕いて〕、国土（認識作用と認識対象）を従者（喜びと貪り）と共に打ち砕いて、煩悶なき婆羅門は行く。",
    295: "母（渇愛）と父（「わたしは存在する」という思量）を打ち砕いて、そして、二者の聞経者（婆羅門）の王（常住論と断滅論）を〔打ち砕いて〕、第五のものたる虎（疑惑の思い）を打ち砕いて、煩悶なき婆羅門は行く。",
    296: "ゴータマの弟子たちは、善く目覚めた〔状態〕に、常に目覚めている。彼らには、そして、昼に、さらに、夜に、常に、覚者（仏：ブッダ）の在り方についての気づきがある。",
    297: "ゴータマの弟子たちは、善く目覚めた〔状態〕に、常に目覚めている。彼らには、そして、昼に、さらに、夜に、常に、法（法：ダンマ）の在り方についての気づきがある。",
    298: "ゴータマの弟子たちは、善く目覚めた〔状態〕に、常に目覚めている。彼らには、そして、昼に、さらに、夜に、常に、僧団（僧：サンガ）の在り方についての気づきがある。",
    299: "ゴータマの弟子たちは、善く目覚めた〔状態〕に、常に目覚めている。彼らには、そして、昼に、さらに、夜に、常に、身体の在り方についての気づきがある。",
    300: "ゴータマの弟子たちは、善く目覚めた〔状態〕に、常に目覚めている。彼らには、そして、昼に、さらに、夜に、不害〔の実践〕に喜びの意がある。",
    301: "ゴータマの弟子たちは、善く目覚めた〔状態〕に、常に目覚めている。彼らには、そして、昼に、さらに、夜に、修行〔の実践〕に喜びの意がある。",
    302: "出家は〔為し〕難く、〔出家の生活は〕喜び難きもの。在家〔の生活〕は居住し難く、苦しきもの。同輩との共住は苦しく、苦しみに出会うのが旅行く者（遊行者）。それゆえに、かつまた、旅行く者として存さず、かつまた、苦しみに出会う者として存さぬもの。",
    303: "信ある者となり、戒を成就した者となり、〔有する〕威徳によって財物を授与された者は、〔彼が〕親しくする、その〔地域〕その地域で、まさしく、そこかしこで、供養される者となる。",
    304: "正しくある者たちは、遠くにあるも知れわたる──ヒマヴァント（ヒマラヤ）の山嶺のように。正しからざる者たちは、この場にあるも見られない──あたかも、夜に放たれた諸々の矢のように。",
    305: "独り坐し、独り臥し、独り、休みなく歩み、独り、自己を調御しながら、林の外れで喜びある者として、〔世に〕存するであろう。",
}

OBSERVE = {
    290: "もし小楽を捨つるによりて、大楽を見得るとせば、賢者は大楽を見つつ、小楽を捨つべし。",
    291: "他人に苦を与えて自己の楽を望む。 かかる者は怨憎の繋縛に捉われて、怨憎より脱することなし。",
    292: "為すべきことを等閑にし、為すべからざることを為し、傲慢にして放逸なる者には煩悩増長す。",
    293: "常に身を念じ、為すべからざることを為さず、為すべきことを為してたゆまず、憶念あり思慮ある人には、煩悩終息す。",
    294: "母（愛欲）と父（我慢）とを殺し、刹帝利族の二王（断見・常見）を〔殺し〕、王国（十二処）とその従臣（喜貪）とを殺して、婆羅門は苦患なく行く。",
    295: "母と父とを殺し、婆羅門族の二王（断見・常見）を〔殺し〕、虎〔将〕を第五とするもの（五蓋、虎＝疑蓋）を殺して、婆羅門は苦患なく行く。",
    296: "瞿曇の弟子は常によく覚醒し、昼も夜も常に仏を念ず。",
    297: "瞿曇の弟子は常によく覚醒し、昼も夜も常に法を念ず。",
    298: "瞿曇の弟子は常によく覚醒し、昼も夜も常に僧を念ず。",
    299: "瞿曇の弟子は常によく覚醒し、昼も夜も常に身を念ず。",
    300: "瞿曇の弟子は常によく覚醒し、昼も夜も不殺生を念ず。",
    301: "瞿曇の弟子は常によく覚醒し、昼も夜も静慮によりて心楽しむ。",
    302: "出家の生活は難くして楽しみ難し。 在家の生活も難くして苦なり。 同輩と共に住むは苦なり。 〔輪廻の〕遍歴者は苦に陥る。 故に遍歴者たるべからず。 然らば苦に陥ることなからん。",
    303: "信あり、戒を具し、誉と財とを得たる者は、いかなる所に赴くも、至る所に於て尊敬せらる。",
    304: "遠方にあるとも善人は、輝くことヒマラヤ山の如く、近隣にあるとも不善者は、見えざること夜陰に放たれし矢の如し。",
    305: "独り臥し、独り行きて倦まず、独り自己を調御して林中に楽しむものたるべし。",
}

PIN29 = "廣衍品（T210 第29品）"
PIN02 = "教學品（T210 第2品）"

CHINESE = {
    290: {"status": "mapped", "pin": PIN29, "t210": "T210-29-001",
          "text": "施安雖小，其報彌大，慧從小施，受見景福。", "satLocus": "大正蔵 T4.569c 廣衍品第1頌"},
    291: {"status": "mapped", "pin": PIN29, "t210": "T210-29-002",
          "text": "施勞於人，而欲望祐，殃咎歸身，自遘廣怨。", "satLocus": "大正蔵 T4.569c 廣衍品第2頌"},
    292: {"status": "mapped", "pin": PIN29, "t210": "T210-29-003",
          "text": "已為多事，非事亦造，伎樂放逸，惡習日增。", "satLocus": "大正蔵 T4.569c 廣衍品第3頌"},
    293: {"status": "mapped", "pin": PIN29, "t210": "T210-29-004",
          "text": "精進惟行，習是捨非，修身自覺，是為正習。", "satLocus": "大正蔵 T4.569c 廣衍品第4頌"},
    294: {"status": "mapped", "pin": PIN02, "t210": "T210-02-012",
          "text": "學先斷母，率君二臣，廢諸營從，是上道人。", "satLocus": "大正蔵 T4.559c 教學品第12頌",
          "note": "パーリ雑品294はT210廣衍品ではなく教學品に対応（蘇錦坤對照表）。"},
    295: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ雑品295はT210に対応なし（蘇錦坤對照表）。"},
    296: {"status": "mapped", "pin": PIN29, "t210": "T210-29-008",
          "text": "為佛弟子，常寤自覺，晝夜念佛，惟法思眾。", "satLocus": "大正蔵 T4.569c 廣衍品第8頌",
          "note": "T210では仏・法・僧を一頌に併記。パーリ296は仏念に対応（蘇錦坤對照表）。"},
    297: {"status": "mapped", "pin": PIN29, "t210": "T210-29-008",
          "text": "為佛弟子，常寤自覺，晝夜念佛，惟法思眾。", "satLocus": "大正蔵 T4.569c 廣衍品第8頌",
          "note": "T210では仏・法・僧を一頌に併記。パーリ297は法念に対応（蘇錦坤對照表）。"},
    298: {"status": "mapped", "pin": PIN29, "t210": "T210-29-008",
          "text": "為佛弟子，常寤自覺，晝夜念佛，惟法思眾。", "satLocus": "大正蔵 T4.569c 廣衍品第8頌",
          "note": "T210では仏・法・僧を一頌に併記。パーリ298は僧念に対応（蘇錦坤對照表）。"},
    299: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ雑品299はT210に対応なし（蘇錦坤對照表）。"},
    300: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ雑品300はT210に対応なし（蘇錦坤對照表）。"},
    301: {"status": "mapped", "pin": PIN29, "t210": "T210-29-009",
          "text": "為佛弟子，常寤自覺，日暮思禪，樂觀一心。", "satLocus": "大正蔵 T4.569c 廣衍品第9頌"},
    302: {"status": "mapped", "pin": PIN29, "t210": "T210-29-011",
          "text": "學難捨罪難，居在家亦難，會止同利難，難難無過有。", "satLocus": "大正蔵 T4.569c 廣衍品第11頌"},
    303: {"status": "mapped", "pin": PIN29, "t210": "T210-29-013",
          "text": "有信則戒成，從戒多致寶，亦從得諧偶，在所見供養。", "satLocus": "大正蔵 T4.570a 廣衍品第13頌"},
    304: {"status": "mapped", "pin": PIN29, "t210": "T210-29-007",
          "text": "近道名顯，如高山雪，遠道闇昧，如夜發箭。", "satLocus": "大正蔵 T4.569c 廣衍品第7頌"},
    305: {"status": "mapped", "pin": PIN29, "t210": "T210-29-014",
          "text": "一坐一處臥，一行無放恣，守一以正身，心樂居樹間。", "satLocus": "大正蔵 T4.570a 廣衍品第14頌"},
}

VERSE_PRACTICE = {
    290: {"nidanaId": "craving", "pathFactors": ["正思惟", "正念"], "reason": "小楽への欲しがりを捨て、大楽を見る"},
    291: {"nidanaId": "clinging", "pathFactors": ["正業", "正念"], "reason": "他者を苦しめて自己の楽を掴む者は怨憎から解けない"},
    292: {"nidanaId": "suffering", "pathFactors": ["正精進", "正念"], "reason": "為すべきを捨て放逸すれば煩悩が増長する"},
    293: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "身念と為すべき実践で煩悩が終息する"},
    294: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "渇愛・我慢・常見断見を打ち砕き苦患なく行く"},
    295: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "渇愛・我慢・五蓋を打ち砕き苦患なく行く"},
    296: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "昼も夜も仏を念じて覚醒する"},
    297: {"nidanaId": "feeling", "pathFactors": ["正念", "正見"], "reason": "昼も夜も法を念じて覚醒する"},
    298: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "昼も夜も僧を念じて覚醒する"},
    299: {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "昼も夜も身を念じて覚醒する"},
    300: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "昼も夜も不殺生・不害を念じて離す"},
    301: {"nidanaId": "review", "pathFactors": ["正定", "正念"], "reason": "静慮により心楽しむ──日暮の見直し"},
    302: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "出家・在家・共住・遍歴のいずれも苦の性質を持つ"},
    303: {"nidanaId": "release", "pathFactors": ["正命", "正念"], "reason": "信と戒を具せば至る所で尊敬される"},
    304: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "善人は遠方でも輝き、不善は近くても見えない"},
    305: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "独り自己を調御し、林中に楽しむ"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP21-P01", 290), ("DP21-P02", 290),
    ("DP21-P03", 291),
    ("DP21-P04", 292),
    ("DP21-P05", 293),
    ("DP21-P06", 294),
    ("DP21-P07", 295),
    ("DP21-P08", 296),
    ("DP21-P09", 297),
    ("DP21-P10", 298),
    ("DP21-P11", 299),
    ("DP21-P12", 300),
    ("DP21-P13", 301),
    ("DP21-P14", 302),
    ("DP21-P15", 303),
    ("DP21-P16", 304),
    ("DP21-P17", 303),
    ("DP21-P18", 305),
]


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
        )
    return c


def main():
    old = json.loads((DATA / "ch21.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        pairs.append({
            "id": pid,
            "category": LABEL_TO_ID[factors[0]],
            "verse": verse,
            "observe": OBSERVE[verse],
            "action": actions[pid],
            "quote": QUOTES[verse],
            "nidanaId": vp["nidanaId"],
            "pathFactors": factors,
            "pathReason": vp["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー",
                    "locus": f"小部・ダンマパダ 雑駁なるものの章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第２１章・雑品 第{verse}偈（#ch02-21）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第21章・雑品（雑駁なるものの章）"
    SHORT = "雑品（雑駁なるものの章）"
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
            "pathLabel": "仏・僧・善人の光に触れ、覚醒して一日を始める",
            "chapterHint": SHORT,
            "fromPrev": "前夜の独り調御が、今朝の念仏・念僧になる",
            "toNext": "接触のあと、法と身の受が立ち上がる",
            "todayObserve": OBSERVE[296],
            "todayAction": actions["DP21-P08"],
            "when": ["朝の始まり", "善友を思い出す"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[296][:40] + "…",
            "secondaryObserve": "遠方にあるとも善人はヒマラヤの如く輝く",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "法と身の受を昼も夜も念じて受け取る",
            "chapterHint": SHORT,
            "fromPrev": "念に触れたあと、法と身体の受が来る",
            "toNext": "受けた快を、小楽への欲しがりへ落とさない",
            "todayObserve": OBSERVE[297] + " " + OBSERVE[299],
            "todayAction": actions["DP21-P11"],
            "when": ["身体を意識する", "法に触れた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[299][:40] + "…",
            "secondaryObserve": "昼も夜も常に法を念ず",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "小楽への欲しがりを見極め、大楽のために捨てる",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、目先の小楽への欲しがりへ",
            "toNext": "止めないと他者を苦しめる掴みへ進む",
            "todayObserve": OBSERVE[290],
            "todayAction": actions["DP21-P01"],
            "when": ["衝動が来た", "小楽か大楽か迷う"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[290][:40] + "…",
            "secondaryObserve": "賢者は大楽を見つつ、小楽を捨つべし",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "action", "nidanaLabel": "掴む",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "他者を苦しめて自己の楽を掴まず、怨憎を解く",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、他者への害として掴む手前",
            "toNext": "掴むと煩悩と遍歴の苦が太る",
            "todayObserve": OBSERVE[291],
            "todayAction": actions["DP21-P03"],
            "when": ["自分の利で相手が不快になる", "恨みを握っている"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[291][:40] + "…",
            "secondaryObserve": "怨憎の繋縛に捉われて、怨憎より脱することなし",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "放逸と遍歴が、煩悩と苦を太らせると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、煩悩増長と生活の苦が熟す",
            "toNext": "見れば、身念と不害の実践へ向き直る",
            "todayObserve": OBSERVE[292] + " " + OBSERVE[302],
            "todayAction": actions["DP21-P14"],
            "when": ["為すべきを後回しにした", "生活の難しさを感じた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[302][:40] + "…",
            "secondaryObserve": "傲慢にして放逸なる者には煩悩増長す",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "mindfulness", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正念", "正精進"], "pathFactorIds": ["mindfulness", "effort"],
            "pathLabel": "身念・不害・信戒で渇愛と我慢を打ち砕き離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、為すべきことと離欲へ向き直る",
            "toNext": "離すと、静慮と独り調御の見直しへつながる",
            "todayObserve": OBSERVE[293],
            "todayAction": actions["DP21-P05"],
            "when": ["身を観察する", "欲と慢心を手放す"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[293][:40] + "…",
            "secondaryObserve": "信あり戒を具せば、至る所に於て尊敬せらる",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "concentration", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "静慮と独り調御で、一日の念を閉じる",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、覚醒していたかの跡",
            "toNext": "見直しが、翌朝の念仏・念僧になる",
            "todayObserve": OBSERVE[301] + " " + OBSERVE[305],
            "todayAction": actions["DP21-P13"],
            "when": ["一日を閉じるとき", "一人の時間がある"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[301][:40] + "…",
            "secondaryObserve": "独り自己を調御して林中に楽しむものたるべし",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 21,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第21章（雑品／雑駁なるものの章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210廣衍品ほか）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・雑駁なるものの章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第２１章・雑品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・廣衍品（T4.569c）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "feeling",
            "focusReason": "雑品は法念・身念など受としての念が中心。既定の焦点は受ける。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch21.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch21.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 22):
        d = json.loads((DATA / f"ch{ch_id}.json").read_text(encoding="utf-8"))
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
            entries[pid].append({
                "collectionId": "dhammapada",
                "collectionName": "ダンマパダ",
                "chapterId": ch_id,
                "shortTitle": d["shortTitle"],
                "title": d["title"],
                "pairCount": len(ids),
                "pairIds": ids,
            })

    psi = {"version": 1, "scope": "dhammapada-ch1-ch21", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 18
    assert all(p["id"] == f"DP21-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(290, 306))
    assert all(p["alignment"]["chinese"]["status"] in ("mapped", "unmapped") for p in pairs)
    unmapped_ids = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] == "unmapped"]
    assert unmapped_ids == ["DP21-P07", "DP21-P11", "DP21-P12"], unmapped_ids
    assert set(by_nidana) == valid
    print("OK")


if __name__ == "__main__":
    main()
