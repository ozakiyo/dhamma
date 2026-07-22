#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch9.json (悪品) to match ch1–ch8 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-09"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0565"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap09/"
)

QUOTES = {
    116: "善きことにおいて急ぐように。悪から、心を防護するように。なぜなら、善を遅く為している者の意は、悪において喜ぶからである。",
    117: "もし、人が、悪を為すなら、繰り返し、その〔悪〕を為さないように。その〔悪〕にたいし、欲〔の思い〕を為さないように。悪を積み重ねることは、苦痛である。",
    118: "もし、人が、善を為すなら、繰り返し、その〔善〕を為すように。その〔善〕にたいし、欲〔の思い〕を為すように。善を積み重ねることは、安楽である。",
    119: "〔自己の為した〕悪しき〔行為〕が煮られない、それまでのあいだ、悪しき者もまた、幸いを見る。しかしながら、〔自己の為した〕悪しき〔行為〕が煮られる、そのとき、そこで、悪しき者は、諸々の悪（不幸）を見る。",
    120: "〔自己の為した〕幸いなる〔行為〕が煮られない、それまでのあいだ、幸いなる者（善人）もまた、悪（不幸）を見る。しかしながら、〔自己の為した〕幸いなる〔行為〕が煮られる、そのとき、そこで、幸いなる者は、諸々の幸いを見る。",
    121: "「それは、わたしに帰ってこないであろう」〔と〕、〔自己の為す〕悪しき〔行為〕を軽く考えてはならない。水瓶でさえも、水滴の落下で満ち溢れる。たとえ、少しずつでも、〔行為を〕蓄積しながら、愚者は、悪〔の報い〕に満ち溢れる。",
    122: "「それは、わたしに帰ってこないであろう」〔と〕、〔自己の為す〕善き〔行為〕を軽く考えてはならない。水瓶でさえも、水滴の落下で満ち溢れる。たとえ、少しずつでも、〔行為を〕蓄積しながら、慧者は、善〔の報い〕に満ち溢れる。",
    123: "〔人員〕少なき隊商にして、〔かつまた〕大財ある商人が、〔危険に満ちた〕恐怖の道を〔避ける〕ように──〔長く〕生きることを欲する者が、毒を〔避ける〕ように──諸々の悪を遍く避けるがよい。",
    124: "もし、手に傷が存在しないなら、手で毒を運ぶことができる。傷なき者に、毒が従い行くことはない。〔悪を〕為さずにいる者に、悪は存在しない。",
    125: "彼が、汚れなき人を汚すなら、清浄で穢れなき人を〔穢すなら〕（怒りなき者に怒り、悪意なき者に悪意を抱くなら）、まさしく、その愚者に、悪は戻り来る──風に逆らって投げられた細かい塵が、〔投げた者自身に戻り来る〕ように。",
    126: "或る者たちは、〔母の〕胎に生起する。悪しき行為（悪業）ある者たちは、地獄に〔落ちる〕。善き境遇（善趣）の者たちは、天上に行く。煩悩なき者たちは、完全なる涅槃に到達する。",
    127: "空中に〔見出され〕ず、海中に〔見出され〕ず、山々の〔岩の〕裂け目に入っても〔見出され〕ない──そこにおいて止住する者が、〔自己の為した〕悪しき行為から解き放たれる、その〔場所〕は、地上における〔どの〕地域も、見出されない。",
    128: "空中に〔見出され〕ず、海中に〔見出され〕ず、山々の〔岩の〕裂け目に入っても〔見出され〕ない──そこにおいて止住する者を、死魔が打ち負かすことなき、その〔場所〕は、地上における〔どの〕地域も、見出されない。",
}

OBSERVE = {
    116: "善に急ぐべし、心を悪より遠ざくべし。 善をなすに懈怠（けたい）する者は、その心悪を喜ぶ。",
    117: "たとい人悪をなすも、重ねてこれをなすべからず、これを喜ぶべからず。 悪の積集（しゃくじゅう）は苦なり。",
    118: "もし人善をなさば、重ねてこれをなすべし、これを喜ぶべし。 善の積集（しゃくじゅう）は楽なり。",
    119: "悪人といえども、悪の未だ熟せざる間は、福善を見る。 然れども悪の熟するや、その時悪人は苦悪を見る。",
    120: "善人といえども、善の未だ熟せざる間は、苦悪を見る。 然れども善の熟するや、その時善人は福善を見る。",
    121: "「そは我に報い来らざるべし」とて、悪を軽視すべからず。 点滴の落下によりて水瓶も満たさる。 微々として積みつつも愚者は悪に満たさる。",
    122: "「そは我に報い来らざるべし」とて、善を軽視すべからず。 点滴の落下によりて水瓶も満たさる。 微々として積みつつも賢者は善に満たさる。",
    123: "伴侶少なく財貨多き商人の、危なき道を〔避くる〕如く、寿を願う者の毒を〔避くる〕如く、悪業を避くべし。",
    124: "手に傷なければ、手にて毒を捕らうも可なり。 毒は傷なき者には入らず。 悪をなさざる者に悪はなし。",
    125: "邪念なき人を害し、清浄にして罪穢なき人を〔害せば〕、悪はかえってその愚者に及ぶ。 あたかも風に逆らって散らされし微塵の如く。",
    126: "ある者は〔人〕胎に宿り、悪業を造れる者は地獄に〔墜ち〕、正しき者は天界に昇り、煩悩を滅尽せる者は涅槃に入る。",
    127: "虚空に於ても、海中に於ても、山間の洞窟に入りても、そこに留まりて悪業より免れ得べき処は、世界になし。",
    128: "虚空に於ても、海中に於ても、山間の洞窟に入りても、そこに留まりて死の力の及ばざる処は世界になし。",
}

CHINESE = {
    116: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-001",
          "text": "見善不從，反隨惡心，求福不正，反樂邪婬。", "satLocus": "大正蔵 T4.565c 惡行品第1頌"},
    117: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-003",
          "text": "凶人行虐，沈漸數數，快欲為人，罪報自然。", "satLocus": "大正蔵 T4.565c 惡行品第3頌"},
    118: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-004",
          "text": "吉人行德，相隨積增，甘心為之，福應自然。", "satLocus": "大正蔵 T4.565c 惡行品第4頌"},
    119: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-005",
          "text": "妖孽見福，其惡未熟，至其惡熟，自受罪虐。", "satLocus": "大正蔵 T4.565c 惡行品第5頌"},
    120: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-006",
          "text": "貞祥見禍，其善未熟，至其善熟，必受其福。", "satLocus": "大正蔵 T4.565c 惡行品第6頌"},
    121: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-009",
          "text": "莫輕小惡，以為無殃，水滴雖微，漸盈大器，凡罪充滿，從小積成。", "satLocus": "大正蔵 T4.565c 惡行品第9頌"},
    122: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-010",
          "text": "莫輕小善，以為無福，水滴雖微，漸盈大器，凡福充滿，從纖纖積。", "satLocus": "大正蔵 T4.566a 惡行品第10頌"},
    123: {"status": "mapped", "pin": "愛欲品（T210 第32品）", "t210": "T210-32-027",
          "text": "伴少而貨多，商人怵惕懼，嗜欲賊害命，故慧不貪欲。", "satLocus": "大正蔵 T4.569b 愛欲品第27頌",
          "note": "パーリ悪の章123はT210惡行品ではなく愛欲品に対応（蘇錦坤對照表）。"},
    124: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-016",
          "text": "如毒摩瘡，船入洄澓，惡行流衍，靡不傷尅。", "satLocus": "大正蔵 T4.566a 惡行品第16頌"},
    125: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-017",
          "text": "加惡誣罔人，清白猶不污，愚殃反自及，如塵逆風坌。", "satLocus": "大正蔵 T4.566a 惡行品第17頌"},
    126: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-020",
          "text": "有識墮胞胎，惡者入地獄，行善上昇天，無為得泥洹。", "satLocus": "大正蔵 T4.566a 惡行品第20頌"},
    127: {"status": "mapped", "pin": "惡行品（T210 第17品）", "t210": "T210-17-021",
          "text": "非空非海中，非隱山石間，莫能於此處，避免宿惡殃。", "satLocus": "大正蔵 T4.566a 惡行品第21頌"},
    128: {"status": "mapped", "pin": "無常品（T210 第1品）", "t210": "T210-01-019",
          "text": "非空非海中、非入山石間，無有地方所，脫之不受死。", "satLocus": "大正蔵 T4.559a 無常品第19頌",
          "note": "パーリ悪の章128はT210惡行品ではなく無常品に対応（蘇錦坤對照表）。"},
}

VERSE_PRACTICE = {
    116: {"nidanaId": "contact", "pathFactors": ["正精進", "正念"], "reason": "善に急ぎ、悪から心を護る"},
    117: {"nidanaId": "craving", "pathFactors": ["正業", "正念"], "reason": "悪を繰り返さず、積集は苦と知る"},
    118: {"nidanaId": "release", "pathFactors": ["正業", "正精進"], "reason": "善を繰り返し、積集は楽と知る"},
    119: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "悪が熟せぬ間は福に見え、熟すれば苦を見る"},
    120: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "善が熟せぬ間は苦に見え、熟すれば福を見る"},
    121: {"nidanaId": "clinging", "pathFactors": ["正見", "正念"], "reason": "小悪を軽視するな、点滴が水瓶を満たす"},
    122: {"nidanaId": "contact", "pathFactors": ["正業", "正念"], "reason": "小善を軽視するな、点滴が水瓶を満たす"},
    123: {"nidanaId": "craving", "pathFactors": ["正思惟", "正念"], "reason": "商人と毒を避ける者の如く、悪を避ける"},
    124: {"nidanaId": "feeling", "pathFactors": ["正念", "正業"], "reason": "傷なき手に毒は入らず、悪をなさぬ者に悪はない"},
    125: {"nidanaId": "clinging", "pathFactors": ["正語", "正念"], "reason": "清浄な人を害せば、悪は風に逆らう塵の如く戻る"},
    126: {"nidanaId": "review", "pathFactors": ["正見", "正念"], "reason": "業により胎・地獄・天・涅槃へと分かれる"},
    127: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "悪業から逃れられる処は地上にない"},
    128: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "死魔の及ばぬ処は地上にない"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP9-P01", 116), ("DP9-P02", 116),
    ("DP9-P03", 117), ("DP9-P04", 117),
    ("DP9-P05", 118), ("DP9-P06", 118),
    ("DP9-P07", 119), ("DP9-P08", 119),  # 119–120 combined
    ("DP9-P09", 121), ("DP9-P10", 121),
    ("DP9-P11", 122), ("DP9-P12", 122),
    ("DP9-P13", 123), ("DP9-P14", 123),
    ("DP9-P15", 124),
    ("DP9-P16", 125), ("DP9-P17", 125),
    ("DP9-P18", 126),
    ("DP9-P19", 127), ("DP9-P20", 127),  # 127–128 combined
]

COMBINED = {
    119: (119, 120),
    127: (127, 128),
}


def chinese_block(verse: int) -> dict:
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    c.setdefault(
        "note",
        "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。",
    )
    return c


def main() -> None:
    old = json.loads((DATA / "ch9.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        if verse in COMBINED:
            a, b = COMBINED[verse]
            observe = OBSERVE[a] + " " + OBSERVE[b]
            quote = QUOTES[a] + " " + QUOTES[b]
            pali_locus = f"小部・ダンマパダ 悪の章 第{a}-{b}偈"
            modern_locus = f"第９章・悪品 第{a}-{b}偈（#ch02-09）"
            zh = chinese_block(a)
            verse_out = a
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 悪の章 第{verse}偈"
            modern_locus = f"第９章・悪品 第{verse}偈（#ch02-09）"
            zh = chinese_block(verse)
            verse_out = verse

        pairs.append({
            "id": pid,
            "category": LABEL_TO_ID[factors[0]],
            "verse": verse_out,
            "observe": observe,
            "action": actions[pid],
            "quote": quote,
            "nidanaId": vp["nidanaId"],
            "pathFactors": factors,
            "pathReason": vp["reason"],
            "alignment": {
                "pali": {"source": "アラナ精舎 経典ライブラリー", "locus": pali_locus, "url": ARANA_URL},
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": modern_locus,
                    "url": TB_URL,
                },
                "chinese": zh,
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第9章・悪品（悪の章）"
    SHORT = "悪品（悪の章）"
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
            "id": "contact", "weekday": 1, "categoryId": "effort", "nidanaLabel": "接触",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "触れた瞬間に善へ急ぎ、悪から護る",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見方が、今朝の接触の土台になる",
            "toNext": "善を遅らせると、意は悪を喜ぶ",
            "todayObserve": OBSERVE[116],
            "todayAction": actions["DP9-P01"],
            "when": ["善いことを後回しにしたくなった", "朝の始まり"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[116][:40] + "…",
            "secondaryObserve": "小善も点滴の如く積み、水瓶を満たす",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "傷なき心で毒を運ばぬよう、隙を塞ぐ",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、欲・怒りの受が立ち上がる",
            "toNext": "隙があれば、欲しがりと悪業へ落ちる",
            "todayObserve": OBSERVE[124],
            "todayAction": actions["DP9-P15"],
            "when": ["衝動が来た", "隙ができそう"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[124][:40] + "…",
            "secondaryObserve": "悪をなさぬ者に、悪は存在しない",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "action", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "悪への欲しがりを繰り返しから離す",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、悪を重ねる欲しがりへ落ちる",
            "toNext": "止めないと小悪の掴みへ進む",
            "todayObserve": OBSERVE[117],
            "todayAction": actions["DP9-P03"],
            "when": ["またやってしまった", "危険な場に近づいた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[117][:40] + "…",
            "secondaryObserve": "商人と毒を避ける者の如く、悪を避ける",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "小悪を軽視して掴むな",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、「これくらい」と掴む手前",
            "toNext": "掴むと点滴が集まり、悪に満ちる",
            "todayObserve": OBSERVE[121],
            "todayAction": actions["DP9-P09"],
            "when": ["小さな嘘", "これくらいと思った"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[121][:40] + "…",
            "secondaryObserve": "清浄な人を害せば、悪は自分に戻る",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "業が熟するとき苦悪が見えると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、今は見えていなくても苦が熟す",
            "toNext": "見れば、逃げ場がないと知り正しく向き合う",
            "todayObserve": OBSERVE[119],
            "todayAction": actions["DP9-P07"],
            "when": ["今うまくいっている", "逃れたい"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[119][:40] + "…",
            "secondaryObserve": "悪業から逃れられる処は、地上にない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "action", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正業", "正精進"], "pathFactorIds": ["action", "effort"],
            "pathLabel": "善を繰り返し積み、悪から離す",
            "chapterHint": SHORT,
            "fromPrev": "悪の積集が流れを加速させる",
            "toNext": "善の積集は安楽となり、心が澄む",
            "todayObserve": OBSERVE[118],
            "todayAction": actions["DP9-P05"],
            "when": ["善い行いを続けたい", "過ちを繰り返した"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[118][:40] + "…",
            "secondaryObserve": "善の積集は楽なり",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "今日の行いが行き先を作ると振り返る",
            "chapterHint": SHORT,
            "fromPrev": "一日の語り・行いは朝からの心の跡",
            "toNext": "見直しが、翌朝の善への急ぎになる",
            "todayObserve": OBSERVE[126],
            "todayAction": actions["DP9-P18"],
            "when": ["一日を閉じるとき", "小さな悪を確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[126][:40] + "…",
            "secondaryObserve": "業により胎・地獄・天・涅槃へと分かれる",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 9,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第9章（悪品／悪の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210惡行品、一部他品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・悪の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第９章・悪品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・惡行品（T4.565c）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "悪品は小悪の軽視と積集が中心。既定の焦点は掴む。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch9.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch9.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 10):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch9", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])
    for k, v in entries.items():
        print(k, [(e["chapterId"], e["pairCount"]) for e in v])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 20
    assert all(p["id"] == f"DP9-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(116, 129))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    print("OK")


if __name__ == "__main__":
    main()
