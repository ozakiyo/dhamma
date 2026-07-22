#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch23.json (象品) to match ch1–ch22 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-23"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0570"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap23/"
)

QUOTES = {
    320: "戦場において、弓から放たれた矢を〔忍受する〕象のように、わたしは、〔他者からの〕責め咎めを忍受するであろう。まさに、劣戒なるかな──〔世の〕多くの人々は。",
    321: "調御された〔象〕を、〔人々は〕戦場へと導く。調御された〔象〕に、王は乗る。〔自己が〕調御された者は、人間たちのなかの最勝の者──彼は、〔他者からの〕責め咎めを忍受する。",
    322: "優れているのは、調御された騾馬たちであり、そして、善き生まれのシンダヴァたち（シンドゥ産の良馬）であり、さらに、クンジャラの大いなる象たちである。それよりも優れているのは、自己が調御された者である。",
    323: "まさに、これらの乗物では、〔いまだ〕赴かざる方角（涅槃）に赴くことはできない──すなわち、善く調御された自己〔という乗物〕で、調御された者が調御によって赴くようには。",
    324: "「財の番人」という名のクンジャラ〔象〕がいる。辛辣なる破壊者で、防護し難く、捕縛されたなら、餌を食べない。クンジャラ〔象〕は、象の林を思念する。",
    325: "すなわち、惰眠の者として〔世に〕有るとき、さらに、大飯食いの者として〔世に有るとき〕、眠りこけてはごろ寝をする者となる。餌で養われた大豚のように、愚か者は、繰り返し、〔母の〕胎に近しく至る。",
    326: "かつて、この心は、〔気ままに〕歩みさすらう者として歩んできた──求めるところから、欲するところへと、楽しみあるままに。わたしは、今日、それ（心）を、根源から制御するであろう──鉤をもつ捕捉者（象使い）が、狂象を〔制御する〕ように。",
    327: "〔あなたたちは、気づきを〕怠らないこと（不放逸）に喜びある者たちと成れ、自らの心を守れ、難所から自己を引き抜け──汚泥にはまったクンジャラ〔象〕が、〔自らを引き抜く〕ように。",
    328: "それで、もし、賢明なる道友を得るなら、共に歩む善き住者たる慧者を〔得るなら〕、一切の危難を征服して、わが意を得た者となり、気づきある者として、彼とともに、歩むがよい。",
    329: "もし、賢明なる道友を得ないなら、共に歩む善き住者たる慧者を〔得ないなら〕、征圧した国土を捨棄して〔出家する〕王のように、マータンガの林のなかの象のように、独り、歩むがよい。",
    330: "独りある者の歩みのほうが、より勝っている。愚者のうちに、道友たること（真の友情）は存在しない。そして、諸々の悪しきことを為さず、〔俗事に〕思い入れ少なく、マータンガの林のなかの象のように、独り、歩むがよい。",
    331: "義（問題）が生じたとき、道友たちがいることは、安楽である。すなわち、いかなるものによっても〔足ることを知り〕、満足〔の思い〕あることは、安楽である。生命の消滅あるとき、〔善き〕功徳あることは、安楽である。一切の苦痛を捨棄することは、安楽である。",
    332: "世において、母を敬うことは、安楽である。さらに、父を敬うことは、安楽である。世において、沙門の資質あることは、安楽である。さらに、梵（婆羅門）の資質あることは、安楽である。",
    333: "すなわち、老いてなお、戒あることは、安楽である。確立した信あることは、安楽である。智慧を獲得することは、安楽である。諸々の悪を為さないことは、安楽である。",
}

OBSERVE = {
    320: "象が戦場に於て、弓より放たれし矢を〔堪え忍ぶが〕如く、我は誹謗を堪え忍ばん。 多くの人は破戒者なればなり。",
    321: "〔人は〕調御せられたる〔象〕を戦場に導き、王は調御せられたる〔象〕に乗る。 誹謗を堪え忍び調御せられたる人は、人中の最勝者なり。",
    322: "騾の調御せられたるは良し、気高き信度馬も良し、大象もまた良し。 自己を調御せる人は更に良し。",
    323: "これらの牽獣によりては未到の境（涅槃）に至ることなからん、調御せられたる人が、よく調御せられたる自己を調御せられたる〔牽獣〕として至るが如くに。",
    324: "ダナパーラカと名づくる象は、〔発情してこめかみより〕苦汁を分泌し、抑制し難く、縛せられて一片の〔餌〕をも食わず。 〔この〕象は象の林を念う。",
    325: "懶惰にして大食し、惰眠を貪りて輾転として臥し、穀類に飽満せる大豚の如くならば、〔かかる〕愚者は再々胞胎に入る。",
    326: "この心かつては望む所に従い、欲に随い楽に随いて徘徊せり。 今は我全くこれを制御せん、あたかも鉤を持てる〔象師の、発情して苦汁を〕流せる象を〔制御する〕如くに。",
    327: "汝ら不放逸を楽しめ、自己の心を護れ。 自己を難処（煩悩）より救出せよ、あたかも泥中に陥れる象の如くに。",
    328: "もし思慮に富み、正しく行い、賢明なる同行の伴侶を得ば、一切の危難を征服し、熟慮して欣然彼と共に行くべし。",
    329: "もし思慮に富み、正しく行い、賢明なる同行の伴侶を得ざれば、独り行くべし、あたかも征服せられたる国土を捨てし王の如く、林中に於ける象の如くに。",
    330: "独り行くこそ勝れ、愚者は断じて伴侶となすべからず。 独り行くべし、悪事を為すべからず、少欲なることあたかも林中に於ける象の如くに。",
    331: "事の起こりし時に友は楽しく、満足はいかなる場合にも楽し。 生命の尽くる時に善業は楽しく、一切の苦を捨つるは楽し。",
    332: "世に母を敬うは楽しく、父を敬うもまた楽し。 世に〔真の〕沙門たることは楽しく、〔真の〕婆羅門たることもまた楽し。",
    333: "老に至るまで戒を持するは楽しく、安立せる信仰は楽し。 智慧を得るは楽しく、悪をなさざるは楽し。",
}

PIN31 = "象喻品（T210 第31品）"

CHINESE = {
    320: {"status": "mapped", "pin": PIN31, "t210": "T210-31-001",
          "text": "我如象鬪，不恐中箭，常以誠信，度無戒人。", "satLocus": "大正蔵 T4.570b 象喻品第1頌"},
    321: {"status": "mapped", "pin": PIN31, "t210": "T210-31-002",
          "text": "譬象調正，可中王乘，調為尊人，乃受誠信。", "satLocus": "大正蔵 T4.570b 象喻品第2頌"},
    322: {"status": "mapped", "pin": PIN31, "t210": "T210-31-003",
          "text": "雖為常調，如彼新馳，亦最善象，不如自調。", "satLocus": "大正蔵 T4.570b 象喻品第3頌"},
    323: {"status": "mapped", "pin": PIN31, "t210": "T210-31-004",
          "text": "彼不能適，人所不至，唯自調者，能致調方。", "satLocus": "大正蔵 T4.570b 象喻品第4頌"},
    324: {"status": "mapped", "pin": PIN31, "t210": "T210-31-005",
          "text": "如象名財守，猛害難禁制，繫絆不與食，而猶暴逸象。", "satLocus": "大正蔵 T4.570b 象喻品第5頌"},
    325: {"status": "mapped", "pin": PIN31, "t210": "T210-31-006",
          "text": "沒在惡行者，恒以貪自繫，其象不知厭，故數入胞胎。", "satLocus": "大正蔵 T4.570b 象喻品第6頌"},
    326: {"status": "mapped", "pin": PIN31, "t210": "T210-31-007",
          "text": "本意為純行，及常行所安，悉捨降伏結，如鉤制象調。", "satLocus": "大正蔵 T4.570b 象喻品第7頌"},
    327: {"status": "mapped", "pin": PIN31, "t210": "T210-31-008",
          "text": "樂道不放逸，能常自護心，是為拔身苦，如象出于塪。", "satLocus": "大正蔵 T4.570b 象喻品第8頌"},
    328: {"status": "mapped", "pin": PIN31, "t210": "T210-31-009",
          "text": "若得賢能伴，俱行行善悍，能伏諸所聞，至到不失意。", "satLocus": "大正蔵 T4.570b 象喻品第9頌"},
    329: {"status": "mapped", "pin": PIN31, "t210": "T210-31-010",
          "text": "不得賢能伴，俱行行惡悍，廣斷王邑里，寧獨不為惡。", "satLocus": "大正蔵 T4.570b 象喻品第10頌"},
    330: {"status": "mapped", "pin": PIN31, "t210": "T210-31-011",
          "text": "寧獨行為善，不與愚為侶，獨而不為惡，如象驚自護。", "satLocus": "大正蔵 T4.570b 象喻品第11頌"},
    331: {"status": "mapped", "pin": PIN31, "t210": "T210-31-012",
          "text": "生而有利安，伴軟和為安，命盡為福安，眾惡不犯安。", "satLocus": "大正蔵 T4.570b 象喻品第12頌"},
    332: {"status": "mapped", "pin": PIN31, "t210": "T210-31-013",
          "text": "人家有母樂，有父斯亦樂，世有沙門樂，天下有道樂。", "satLocus": "大正蔵 T4.570b 象喻品第13頌"},
    333: {"status": "mapped", "pin": PIN31, "t210": "T210-31-014",
          "text": "持戒終老安，信正所正善，智慧最安身，不犯惡最安。", "satLocus": "大正蔵 T4.570b 象喻品第14頌"},
}

VERSE_PRACTICE = {
    320: {"nidanaId": "suffering", "pathFactors": ["正念", "正見"], "reason": "誹謗の苦を、戦場の象のように堪え忍ぶ"},
    321: {"nidanaId": "feeling", "pathFactors": ["正念", "正思惟"], "reason": "調御して誹謗の受を堪え忍ぶ者が最勝"},
    322: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "乗物より自己調御が最勝と知る接触"},
    323: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "調御された自己で未到の境（涅槃）へ赴く"},
    324: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "束縛の中でも象林を念う──本来の方向への欲しがり"},
    325: {"nidanaId": "craving", "pathFactors": ["正命", "正念"], "reason": "懶惰・大食・惰眠への欲しがりは輪廻を招く"},
    326: {"nidanaId": "clinging", "pathFactors": ["正念", "正定"], "reason": "気ままに徘徊する心を根源から制御する"},
    327: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "不放逸で心を護り、泥中から自己を引き抜く"},
    328: {"nidanaId": "contact", "pathFactors": ["正念", "正語"], "reason": "賢明な道友との接触を得て共に歩く"},
    329: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "善友なきときは独り林の象の如く歩く"},
    330: {"nidanaId": "clinging", "pathFactors": ["正念", "正語"], "reason": "愚者を伴侶と掴まず、独り少欲に歩く"},
    331: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "友・満足・善業・苦の捨棄という安楽を見直す"},
    332: {"nidanaId": "feeling", "pathFactors": ["正念", "正業"], "reason": "父母・沙門・婆羅門を敬う安楽を受ける"},
    333: {"nidanaId": "review", "pathFactors": ["正業", "正念"], "reason": "老いても戒・信・智・不悪という安楽を見直す"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP23-P01", 320),
    ("DP23-P02", 321),
    ("DP23-P03", 322),
    ("DP23-P04", 323),
    ("DP23-P05", 324),
    ("DP23-P06", 325),
    ("DP23-P07", 326),
    ("DP23-P08", 327),
    ("DP23-P09", 328),
    ("DP23-P10", 329),
    ("DP23-P11", 330), ("DP23-P12", 330),
    ("DP23-P13", 331),
    ("DP23-P14", 332),
    ("DP23-P15", 333),
]


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    c.setdefault(
        "note",
        "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
    )
    return c


def main():
    old = json.loads((DATA / "ch23.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 象の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第２３章・象品 第{verse}偈（#ch02-23）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第23章・象品（象の章）"
    SHORT = "象品（象の章）"
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
            "pathLabel": "自己調御と善友に触れ、一日の軸を定める",
            "chapterHint": SHORT,
            "fromPrev": "前夜の戒と信の見直しが、今朝の調御になる",
            "toNext": "接触のあと、誹謗や敬いの受が立ち上がる",
            "todayObserve": OBSERVE[322],
            "todayAction": actions["DP23-P03"],
            "when": ["朝の始まり", "善友に会う"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[322][:40] + "…",
            "secondaryObserve": "賢明なる同行の伴侶を得ば、欣然彼と共に行くべし",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "誹謗の受を調御して受け、敬いの安楽も受け取る",
            "chapterHint": SHORT,
            "fromPrev": "調御に触れたあと、誹謗や敬いの受が来る",
            "toNext": "受けた不快を、惰眠や気ままへの欲しがりへ落とさない",
            "todayObserve": OBSERVE[321],
            "todayAction": actions["DP23-P02"],
            "when": ["批判を受けた", "敬意を表す"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[321][:40] + "…",
            "secondaryObserve": "世に母を敬うは楽しく、父を敬うもまた楽し",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正命"], "pathFactorIds": ["mindfulness", "livelihood"],
            "pathLabel": "惰眠・大食と束縛中の逸れを緩め、本来の方向を見る",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、惰眠や逸れへの欲しがりへ",
            "toNext": "止めないと気ままな心の掴みへ進む",
            "todayObserve": OBSERVE[325],
            "todayAction": actions["DP23-P06"],
            "when": ["飲食睡眠を整えたい", "束縛の中で方向を確かめる"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[325][:40] + "…",
            "secondaryObserve": "縛せられても、象は象の林を念う",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "気ままな心と愚者との掴みを手放し、制御する",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、気まま・悪友として掴む手前",
            "toNext": "掴むと誹謗に耐えきれず輪廻の苦が太る",
            "todayObserve": OBSERVE[326],
            "todayAction": actions["DP23-P07"],
            "when": ["心が徘徊する", "愚者の流れに乗りそう"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[326][:40] + "…",
            "secondaryObserve": "愚者は断じて伴侶となすべからず",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "mindfulness", "nidanaLabel": "苦が太る",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "誹謗の矢を、象のように苦として受け止める",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、誹謗と破戒の苦が熟す",
            "toNext": "見れば、不放逸と自己調御へ向き直る",
            "todayObserve": OBSERVE[320],
            "todayAction": actions["DP23-P01"],
            "when": ["悪口を受けた", "反論したくなった"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[320][:40] + "…",
            "secondaryObserve": "多くの人は破戒者なればなり",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "不放逸で泥から抜け、調御された自己で離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、心を護り独り／共に歩く実践へ",
            "toNext": "離すと、安楽の夜の見直しへつながる",
            "todayObserve": OBSERVE[327],
            "todayAction": actions["DP23-P08"],
            "when": ["怠惰に流されそう", "独りで正しい選択をする"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[327][:40] + "…",
            "secondaryObserve": "調御せられたる自己で未到の境に至る",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "action", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "友・敬い・戒・信という安楽を、静かに見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、調御していたかの跡",
            "toNext": "見直しが、翌朝の自己調御になる",
            "todayObserve": OBSERVE[331] + " " + OBSERVE[333],
            "todayAction": actions["DP23-P13"],
            "when": ["一日を閉じるとき", "老いても後悔しない行いを考える"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[331][:40] + "…",
            "secondaryObserve": "老に至るまで戒を持するは楽しく、悪をなさざるは楽し",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 23,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第23章（象品／象の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210象喻品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・象の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第２３章・象品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・象喻品（T4.570b）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "象品は誹謗の受を調御して忍受する実践が中心。既定の焦点は受ける。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch23.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch23.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 24):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch23", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 15
    assert all(p["id"] == f"DP23-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(320, 334))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    assert set(by_nidana) == valid
    print("OK")


if __name__ == "__main__":
    main()
