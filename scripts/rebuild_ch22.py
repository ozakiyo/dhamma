#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch22.json (地獄品) to match ch1–ch21 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-22"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0570"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap22/"
)

QUOTES = {
    306: "事実ならざることを説く者は、地獄に近づく。あるいは、また、彼が、為して〔そののち〕、さらに、「〔わたしは〕為さない」〔と〕言うなら、〔彼もまた、地獄に近づく〕。両者ともどもに、彼らは、下劣な行為の人間たちとして、死してのち、他所（来世）において、等しき者たちと成る。",
    307: "黄褐色〔の衣〕（袈裟）を首にしながら、自制なく悪しき法（性質）の者たちが多くいる。悪しき者たちは、彼らは、〔自己の為した〕諸々の悪しき行為（悪業）によって、地獄に再生する。",
    308: "すなわち、もし、自制なき劣戒の者が、国人による〔行乞の〕食を受けるなら、熱せられた、火炎の如き鉄の玉を食べたほうが、より勝っている（悪業を作って地獄に落ちるよりはまだましである）。",
    309: "〔気づきを〕怠り、他者の妻に近しく慣れ親しむ人は、四つの状況を惹起する。〔すなわち〕善ならざる利得（悪しき報い）あること、欲するままに臥せないこと、第三に、非難〔を受けること〕、第四に、地獄〔に落ちること〕である。",
    310: "そして、〔男は〕善ならざる利得ある者となり、かつまた、〔女は〕悪しき境遇ある者となる。恐怖する〔男〕に、恐怖する〔女〕に、そして、歓楽はごく僅か。かつまた、王は、重き棒（罰）を課す。それゆえに、人は、他者の妻には慣れ親しまぬがよい。",
    311: "あたかも、誤って掴んだ茅〔の葉〕が、まさしく、手を傷つけるように、誤って偏執された沙門の資質は、〔沙門その人を〕地獄へと引きずり込む。",
    312: "それが何であれ、緩慢な行為であるなら、さらに、それが、汚染された掟であり、疑いある梵行（禁欲清浄行）であるなら、それは、大いなる果と成らない。",
    313: "もし、為すべきなら、これを為し、断固として、これに勤しむがよい。なぜなら、緩慢な遍歴遊行者は、より一層、塵を撒き散らすからである。",
    314: "悪行は、〔為すよりは〕為さずにいたほうが、より勝っている。〔為したその〕悪行が、のちに悩み苦しめる〔からである〕。そして、善行は、〔為さずにいるよりは〕為したほうが、より勝っている。それを為して悩み苦しまない〔からである〕。",
    315: "あたかも、辺境にある、内外共に保護された城市のように、このように、自己を保護するがよい。〔この〕瞬間が、あなたたちを過ぎ行くことがあってはならない（瞬時でさえも、虚しく過ごしてはならない）。なぜなら、〔この〕瞬間を〔虚しく〕過ごした者たちは、地獄に引き渡され、憂い悲しむからである。",
    316: "〔彼らは〕恥ずべきではないところで恥じ、恥ずべきところで恥じない──誤った見解（邪見）を受持しながら、〔迷いの〕有情たちは、悪しき境遇（悪趣）に赴く。",
    317: "恐怖なきところで恐怖を見る者たち、さらに、恐怖あるところで恐怖を見ない者たち──誤った見解を受持しながら、〔迷いの〕有情たちは、悪しき境遇に赴く。",
    318: "罪過なきものについて「罪過あり」と思い、さらに、罪過あるものについて「罪過なし」と見る者たち──誤った見解を受持しながら、〔迷いの〕有情たちは、悪しき境遇に赴く。",
    319: "しかしながら、罪過あるものを「罪過あり」と知って、さらに、罪過なきものを「罪過なし」と〔見る者たち〕──正しい見解（正見）を受持しながら、〔迷いなき〕有情たちは、善き境遇（善趣）に赴く。",
}

OBSERVE = {
    306: "不実を語る者は地獄に堕す。 或いはまた〔自ら〕為して、我為さずと言う者も〔地獄に堕す〕。 これら両種の悪業者は、死後他世（地獄）に於て同等なり。",
    307: "袈裟を頸に纒うも、悪を行い節制なき者多し。 かかる悪人はその悪業によりて地獄に堕す。",
    308: "破戒・無節制にして、国民の施食を受くるよりは、むしろ火炎の如く灼熱せる鉄丸を食うこそ勝れ。",
    309: "放逸にして他人の妻を犯す人は、〔次の〕四事に達す。 罪業を得ること、安臥せざること、第三に誹謗、第四に地獄。",
    310: "〔彼は〕罪業を得、また悪趣〔に堕す〕。 かつ怯えたる〔男〕と怯えたる〔女〕との淫楽は少なし。 王もまた〔これに〕酷しき刀杖を加う。 されば人は他人の妻を犯すべからず。",
    311: "掴みそこねし茅草の手を切る如く、修行を誤れる沙門道は人を地獄に導く。",
    312: "懈怠の行為、汚れたる戒行、逡巡せる梵行、かかるものに大果なし。",
    313: "もし為すべくんばこれを為し、断固としてこれを遂行すべし。 懈怠の遊行者は更に多くの欲塵を散ずるのみ。",
    314: "悪業は為さざるこそ勝れ、後に至りて悪業は人を苦しむ。 善業は為すこそ勝れ、そを為して苦しむことなし。",
    315: "辺境の城を内外共に護るが如く、自己を護るべし。 一刹那も〔ゆるがせに〕過ぎ去らしむることなかれ。 刹那をゆるがせにせる者は、地獄に至りて憂患を受く。",
    316: "恥ずべからざるを恥じ、恥ずべきを恥じず、邪見を抱ける衆生は悪趣に至る。",
    317: "怖るべからざることに恐怖を見、怖るべきことに恐怖を見ず、邪見を抱ける衆生は悪趣に至る。",
    318: "罪なきことを罪ありと思い、罪あることを罪なしと見る、邪見を抱ける衆生は悪趣に至る。",
    319: "罪ある所に罪ありと知り、また罪なき所に罪なしと〔知る〕、正見を抱ける衆生は善趣に至る。",
}

PIN30 = "地獄品（T210 第30品）"

CHINESE = {
    306: {"status": "mapped", "pin": PIN30, "t210": "T210-30-001",
          "text": "妄語地獄近，作之言不作，二罪後俱受，是行自牽往。", "satLocus": "大正蔵 T4.570a 地獄品第1頌"},
    307: {"status": "mapped", "pin": PIN30, "t210": "T210-30-002",
          "text": "法衣在其身，為惡不自禁，苟沒惡行者，終則墮地獄。", "satLocus": "大正蔵 T4.570a 地獄品第2頌"},
    308: {"status": "mapped", "pin": PIN30, "t210": "T210-30-003",
          "text": "無戒受供養，理豈不自損？死噉燒鐵丸，然熱劇火炭。", "satLocus": "大正蔵 T4.570a 地獄品第3頌"},
    309: {"status": "mapped", "pin": PIN30, "t210": "T210-30-004",
          "text": "放逸有四事：好犯他人婦，臥險非福利，毀三淫泆四。", "satLocus": "大正蔵 T4.570a 地獄品第4頌"},
    310: {"status": "mapped", "pin": PIN30, "t210": "T210-30-005",
          "text": "不福利墮惡，畏惡畏樂寡，王法重罰加，身死入地獄。", "satLocus": "大正蔵 T4.570a 地獄品第5頌"},
    311: {"status": "mapped", "pin": PIN30, "t210": "T210-30-006",
          "text": "譬如拔菅草，執緩則傷手，學戒不禁制，獄錄乃自賊。", "satLocus": "大正蔵 T4.570a 地獄品第6頌"},
    312: {"status": "mapped", "pin": PIN30, "t210": "T210-30-007",
          "text": "人行為慢惰，不能除眾勞，梵行有玷缺，終不受大福。", "satLocus": "大正蔵 T4.570a 地獄品第7頌"},
    313: {"status": "mapped", "pin": PIN30, "t210": "T210-30-008",
          "text": "常行所當行，自持必令強，遠離諸外道，莫習為塵垢。", "satLocus": "大正蔵 T4.570a 地獄品第8頌"},
    314: {"status": "mapped", "pin": PIN30, "t210": "T210-30-009",
          "text": "為所不當為，然後致欝毒，行善常吉順，所適無悔恡。", "satLocus": "大正蔵 T4.570a 地獄品第9頌"},
    315: {"status": "mapped", "pin": PIN30, "t210": "T210-30-012",
          "text": "如備邊城，中外牢固，自守其心，非法不生，行缺致憂，令墮地獄。", "satLocus": "大正蔵 T4.570a 地獄品第12頌"},
    316: {"status": "mapped", "pin": PIN30, "t210": "T210-30-013",
          "text": "可羞不羞，非羞反羞，生為邪見，死墮地獄。", "satLocus": "大正蔵 T4.570a 地獄品第13頌"},
    317: {"status": "mapped", "pin": PIN30, "t210": "T210-30-014",
          "text": "可畏不畏，非畏反畏，信向邪見，死墮地獄。", "satLocus": "大正蔵 T4.570a 地獄品第14頌"},
    318: {"status": "mapped", "pin": PIN30, "t210": "T210-30-015",
          "text": "可避不避，可就不就，翫習邪見，死墮地獄。", "satLocus": "大正蔵 T4.570a 地獄品第15頌"},
    319: {"status": "mapped", "pin": PIN30, "t210": "T210-30-016",
          "text": "可近則近，可遠則遠，恒守正見，死墮善道。", "satLocus": "大正蔵 T4.570a 地獄品第16頌"},
}

VERSE_PRACTICE = {
    306: {"nidanaId": "clinging", "pathFactors": ["正語", "正念"], "reason": "妄語・隠蔽は地獄へ近づく掴み"},
    307: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "袈裟という外形に触れても、悪行あれば地獄へ"},
    308: {"nidanaId": "clinging", "pathFactors": ["正命", "正念"], "reason": "無戒で施食を掴むより鉄丸を食うほうが勝る"},
    309: {"nidanaId": "craving", "pathFactors": ["正思惟", "正念"], "reason": "他人の領域への欲しがりは四つの悪果を招く"},
    310: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "罪業・悪趣・恐怖・罰──淫楽は少なく苦が多い"},
    311: {"nidanaId": "clinging", "pathFactors": ["正念", "正業"], "reason": "誤った修行の掴みは地獄へ引きずり込む"},
    312: {"nidanaId": "craving", "pathFactors": ["正精進", "正念"], "reason": "懈怠・汚れた戒・逡巡に大果なし"},
    313: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "為すべきを断固として遂行し、塵を散らさぬ"},
    314: {"nidanaId": "review", "pathFactors": ["正業", "正念"], "reason": "悪業は為さず、善業は為す──後の苦を防ぐ"},
    315: {"nidanaId": "contact", "pathFactors": ["正念", "正定"], "reason": "内外を護り、一刹那もゆるがせにしない"},
    316: {"nidanaId": "feeling", "pathFactors": ["正見", "正念"], "reason": "恥じの受が歪めば邪見となり悪趣へ"},
    317: {"nidanaId": "feeling", "pathFactors": ["正見", "正念"], "reason": "恐怖の受が歪めば邪見となり悪趣へ"},
    318: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "罪の見誤りは邪見となり悪趣の苦を招く"},
    319: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "罪あるを罪ありと知り、正見で善趣へ離す"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP22-P01", 306),
    ("DP22-P02", 307),
    ("DP22-P03", 308),
    ("DP22-P04", 309), ("DP22-P05", 309),
    ("DP22-P06", 310),
    ("DP22-P07", 311),
    ("DP22-P08", 312),
    ("DP22-P09", 313),
    ("DP22-P10", 314),
    ("DP22-P11", 315),
    ("DP22-P12", 316),
    ("DP22-P13", 317),
    ("DP22-P14", 318),
    ("DP22-P15", 319),
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
    old = json.loads((DATA / "ch22.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 地獄の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第２２章・地獄品 第{verse}偈（#ch02-22）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第22章・地獄品（地獄の章）"
    SHORT = "地獄品（地獄の章）"
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
            "pathLabel": "外形に触れず、内外を護って一日を始める",
            "chapterHint": SHORT,
            "fromPrev": "前夜の正見の見直しが、今朝の自己護持になる",
            "toNext": "接触のあと、恥じ・恐怖の受が立ち上がる",
            "todayObserve": OBSERVE[315],
            "todayAction": actions["DP22-P11"],
            "when": ["朝の始まり", "見た目で安心しそう"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[315][:40] + "…",
            "secondaryObserve": "袈裟を纒うも、悪を行い節制なき者は地獄に堕す",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "恥じと恐怖の受を正見で受け取り、歪めない",
            "chapterHint": SHORT,
            "fromPrev": "護りのあと、恥じ・恐怖の受が来る",
            "toNext": "歪んだ受を、境界侵犯の欲しがりへ落とさない",
            "todayObserve": OBSERVE[316] + " " + OBSERVE[317],
            "todayAction": actions["DP22-P12"],
            "when": ["羞恥心が揺れた", "恐れを感じた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[316][:40] + "…",
            "secondaryObserve": "怖るべからざるに恐怖を見、怖るべきに恐怖を見ずば悪趣へ",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "他者の領域への欲しがりと懈怠を緩める",
            "chapterHint": SHORT,
            "fromPrev": "受が歪むと、侵犯や中途半端への欲しがりへ",
            "toNext": "止めないと妄語・無戒の掴みへ進む",
            "todayObserve": OBSERVE[309],
            "todayAction": actions["DP22-P04"],
            "when": ["一線を越えそう", "怠けて手を抜きたくなった"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[309][:40] + "…",
            "secondaryObserve": "懈怠・汚れた戒・逡巡に大果なし",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "speech", "nidanaLabel": "掴む",
            "pathFactors": ["正語", "正念"], "pathFactorIds": ["speech", "mindfulness"],
            "pathLabel": "妄語・無戒・誤った修行を掴まず、誠実に立つ",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、隠蔽・無戒・誤修として掴む手前",
            "toNext": "掴むと罪業と地獄の苦が太る",
            "todayObserve": OBSERVE[306],
            "todayAction": actions["DP22-P01"],
            "when": ["言い訳しそう", "信頼に値しない受け取り"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[306][:40] + "…",
            "secondaryObserve": "修行を誤れる沙門道は人を地獄に導く",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "侵犯と邪見の掴みが、悪趣の苦になると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、罪業・罰・悪趣の苦が熟す",
            "toNext": "見れば、断固とした行いと正見へ向き直る",
            "todayObserve": OBSERVE[310],
            "todayAction": actions["DP22-P06"],
            "when": ["欲の先の苦を想像する", "罪の見誤りに気づいた"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[310][:40] + "…",
            "secondaryObserve": "罪なきを罪あり、罪あるを罪なしと見れば悪趣へ",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "為すべきを断固として為し、正見で離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、懈怠を捨て正見へ向き直る",
            "toNext": "離すと、善悪の夜の見直しへつながる",
            "todayObserve": OBSERVE[313],
            "todayAction": actions["DP22-P09"],
            "when": ["決めたことをやり切る", "正見で分ける"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[313][:40] + "…",
            "secondaryObserve": "罪ある所に罪ありと知り、正見を抱ける衆生は善趣に至る",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "action", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "悪業を為さず善業を為したかを、公平に見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、地獄か善趣かの跡",
            "toNext": "見直しが、翌朝の自己護持になる",
            "todayObserve": OBSERVE[314] + " " + OBSERVE[319],
            "todayAction": actions["DP22-P10"],
            "when": ["一日を閉じるとき", "後悔と継続を分ける"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[314][:40] + "…",
            "secondaryObserve": "悪業は為さざるこそ勝れ、善業は為すこそ勝れ",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 22,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第22章（地獄品／地獄の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210地獄品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・地獄の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第２２章・地獄品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・地獄品（T4.570a）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "地獄品は妄語・無戒・誤修など掴みが地獄へ近づく中心。既定の焦点は掴む。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch22.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch22.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 23):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch22", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 15
    assert all(p["id"] == f"DP22-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(306, 320))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    assert set(by_nidana) == valid
    print("OK")


if __name__ == "__main__":
    main()
