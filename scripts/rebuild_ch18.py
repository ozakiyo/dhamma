#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch18.json (垢穢品) to match ch1–ch17 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-18"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0568"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap18/"
)

QUOTES = {
    235: "今や、枯葉のような者として、〔あなたは〕存する。そして、夜魔（閻魔）の使者たちもまた、あなたを待ち構えている。そして、〔あなたは〕旅路の門に立つ。そして、あなたには、〔旅の〕路銀さえも見出されない。",
    236: "〔まさに〕その〔あなた〕は、自己の洲（依り所）を作れ。すみやかに努めよ。賢者と成れ。〔世俗の〕垢を取り払った〔あなた〕は、穢れなき者となり、天の聖なる境地に近づくであろう。",
    237: "そして、今や、衰失に導かれた者として、〔あなたは〕存する。夜魔の現前に進み行く者として、〔あなたは〕存する。途中、あなたに、住居は存在しない。そして、あなたには、〔旅の〕路銀さえも見出されない。",
    238: "〔まさに〕その〔あなた〕は、自己の洲（依り所）を作れ。すみやかに努めよ。賢者と成れ。〔世俗の〕垢を取り払った〔あなた〕は、穢れなき者となり、ふたたび、生と老に近づくことはないであろう。",
    239: "思慮ある者は、順次に、瞬間瞬間に、少しずつ、鍛冶屋が銀の〔垢を取り除く〕ように、自己の垢を取り払うがよい。",
    240: "鉄から現起した垢（錆）が、それ（鉄）から出起して、まさしく、それ〔自身〕を喰い尽くすように、このように、諸々の自らの行為（業）は、罪行者を、悪しき境遇（悪趣）に導く。",
    241: "不誦という垢あるのが、諸々の呪文である。不精という垢あるのが、諸々の家屋である。色艶には、怠惰という垢がある。〔心身を〕守っている者には、放逸という垢がある。",
    242: "婦女には、悪しき行ない（不品行）という垢がある。〔施物を〕施している者には、物惜という垢がある。まさに、諸々の悪しき法（性質）という垢がある──この世において、さらに、他〔の世〕において。",
    243: "その垢よりも、さらにひどい垢として、無明という最高の垢がある。比丘たちよ、この垢を捨棄して、無垢の者たちと成れ。",
    244: "生き易きは、恥〔の思い〕がなく、烏の厚かましさがある、厚顔で、傲岸で、尊大で、〔心が〕汚染された者による、生である。",
    245: "しかしながら、生き難きは、恥〔の思い〕があり、常に清らかさを探し求め、陰鬱ならず、尊大ならず、清浄の生き方がある、〔常に真実を〕見ている者による、〔生である〕。",
    246: "彼が、命あるものを殺すなら、さらに、虚偽の論を語るなら、世において与えられていないものを取るなら、さらに、他者の妻のもとに赴くなら──",
    247: "さらに、その人が、穀物酒や果実酒などの飲み物に〔自らを〕束縛するなら、この者は、まさしく、ここに、〔この〕世において、自己の根元を掘り崩す。",
    248: "君よ、男よ、このように知りなさい。〔これらの五者の〕自制なき者たちは、悪しき法（性質）の者たちである。貪り〔の思い〕が、そして、法（正義）ならざる〔生き方〕が、あなたを、長きにわたり、苦しみへと追いやってはならない。",
    249: "人は、まさに、信あるままに、浄信するままに、〔布施を〕施す。そこにおいて、彼（布施を受ける者）が、他者たちの飲み物と食料に〔心を〕惑わす者と成るなら（他者と自己の施物を比較して、心を動かすなら）、彼は、昼であろうが、夜であろうが、禅定（定・三昧）に到達しない。",
    250: "しかしながら、彼の、この〔汚点〕が断絶され、根元から殲滅され、完破されたなら、彼は、まさに、昼であろうが、夜であろうが、禅定に到達する。",
    251: "貪欲（貪）に等しい火は、存在しない。憤怒（瞋）に等しい捕捉者は、存在しない。迷妄（痴）に等しい網は、存在しない。渇愛に等しい川は、存在しない。",
    252: "他者たちの罪過は見易く、いっぽうで、自己の〔罪過は〕見難い。まさに、彼は、他者たちの諸々の罪過を、あたかも、籾殻のように、〔誇大に〕暴き立て、いっぽうで、自己の〔罪過は〕覆い隠す──狡猾な賭博師が、〔悪しき〕賽の目を〔隠す〕ように。",
    253: "他者の罪過を随観し、常に譴責の表象（想：概念・心象）ある者──彼の、諸々の煩悩は増え行き、彼は、煩悩の滅尽から遠く離れている。",
    254: "まさしく、虚空に、足跡は存在せず、外に、沙門は存在しない。戯論（空想）に歓楽あるのが、〔世の〕人々である。戯論なきは、如来たちである。",
    255: "まさしく、虚空に、足跡は存在せず、外に、沙門は存在しない。諸々の形成〔作用〕（諸行：形成されたもの・現象世界）は、常久のものとして存在しない。覚者たちに、〔心の〕動揺は存在しない。",
}

OBSERVE = {
    235: "汝は今や枯葉の如く、閻魔の使者また汝に近づけり。 汝は死出の門に立つ。 されど汝に旅路の糧なし。",
    236: "汝自ら自己の依所を造れ、速やかに精勤せよ、賢者たれ。 〔心の〕垢穢（くえ）を払い、罪過なくば、汝は天の聖地に至らん。",
    237: "汝は今や齢既に傾き、閻魔の元に近づけり。 途上に汝の住所なく、また旅路の糧もなし。",
    238: "汝自ら自己の依所を造れ、速やかに精勤せよ、賢者たれ。 〔心の〕垢穢を払い、罪過なくば、汝は再び生と老とに近づかざるべし。",
    239: "賢慮ある者は、漸次に、少量ずつ、刹那刹那に、自己の垢穢を払うべし、あたかも鍛工が銀の〔鉱垢を除くが〕如く。",
    240: "鉄より生じたる垢穢（錆）が、鉄より生じて鉄を蝕むが如く、自己の業は悪業者を悪趣に導く。",
    241: "読誦（どくじゅ）せざるは聖典の垢穢、修復せざるは家屋の垢穢、懈怠（けたい）は美の垢穢、放逸は番士の垢穢なり。",
    242: "不義は婦人の垢穢、吝嗇は施与者の垢穢、実に悪法（悪行）はこの世に於てもかの世に於ても垢穢なり。",
    243: "これらの諸垢穢より更に甚だしき垢穢は無明にして、〔こは〕最大の垢穢なり。 比丘らよ、この垢穢を捨てて無垢となれ。",
    244: "慚愧心（ざんぎしん）なく、厚顔・暴戻・大胆・傲慢にして、罪に汚れたる人の生活は安易なり。",
    245: "慚愧心あり、常に清浄を求め、執着なく、謙遜にして、清浄の生活を営み、識見ある人の生活は困難なり。",
    246: "生あるものを殺し、妄語を語り、この世に於て与えられざるを取り、他人の妻を犯し、",
    247: "スラー酒・メーラヤ酒に沈湎する人は、この世に於て自己の根底を掘るものなり。",
    248: "人よ、是の如く知れ、節制なき者は邪悪なりと。 貪欲と非法とをして永く汝を苦に陥らしむることなかれ。",
    249: "人は実に信ずる所に従い、好む所に従いて施与す。 他人の得たる飲食に対し、不満を抱く者は、昼も夜も三昧に入るを得ず。",
    250: "かかる〔心を〕断ち、根元より絶滅する者は、昼も夜も実に三昧に入ることを得。",
    251: "貪欲に等しき火なく、瞋恚（しんに）に等しき捕捉者なく、愚痴に等しき羅網なく、愛欲に等しき河流なし。",
    252: "他人の過失は見易く、自己の〔過失〕は見難し。 他人の過失は籾殻の如く散布し、自己の〔過失〕は、これを隠匿すること、狡猾なる賭博者のカリ（最悪の骰子（さい）数）に於けるが如し。",
    253: "他人の過失を詮索し、常に怒り易き人の煩悩は増長す。 彼は煩悩の滅尽を去ること遠し。",
    254: "虚空に道なく、外道に沙門なし。 衆生は虚妄を喜び、如来には虚妄なし。",
    255: "虚空に道なく、外道に沙門なし。 万象は常住ならず、諸仏に擾乱（じょうらん）なし。",
}

CHINESE = {
    235: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ垢の章235はT210に対応なし（蘇錦坤對照表）。"},
    236: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ垢の章236はT210に対応なし（蘇錦坤對照表）。"},
    237: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-001",
          "text": "生無善行，死墮惡道，往疾無間，到無資用。", "satLocus": "大正蔵 T4.568b 塵垢品第1頌"},
    238: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-002",
          "text": "當求智慧，以然意錠，去垢勿污，可離苦形。", "satLocus": "大正蔵 T4.568b 塵垢品第2頌"},
    239: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-003",
          "text": "慧人以漸，安徐精進，洗除心垢，如工鍊金。", "satLocus": "大正蔵 T4.568b 塵垢品第3頌"},
    240: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-004",
          "text": "惡生於心，還自壞形，如鐵生垢，反食其身。", "satLocus": "大正蔵 T4.568b 塵垢品第4頌"},
    241: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-005",
          "text": "不誦為言垢，不勤為家垢，不嚴為色垢，放逸為事垢。", "satLocus": "大正蔵 T4.568b 塵垢品第5頌"},
    242: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-006",
          "text": "慳為惠施垢，不善為行垢，今世亦後世，惡法為常垢。", "satLocus": "大正蔵 T4.568b 塵垢品第6頌"},
    243: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-007",
          "text": "垢中之垢，莫甚於癡，學當捨惡，比丘無垢。", "satLocus": "大正蔵 T4.568b 塵垢品第7頌"},
    244: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-008",
          "text": "苟生無恥，如鳥長喙，強顏耐辱，名曰穢生。", "satLocus": "大正蔵 T4.568b 塵垢品第8頌"},
    245: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-009",
          "text": "廉恥雖苦，義取清白，避辱不妄，名曰潔生。", "satLocus": "大正蔵 T4.568c 塵垢品第9頌"},
    246: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-010",
          "text": "愚人好殺，言無誠實，不與而取，好犯人婦。", "satLocus": "大正蔵 T4.568c 塵垢品第10頌"},
    247: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-011",
          "text": "逞心犯戒，迷惑於酒，斯人世世，自掘身本。", "satLocus": "大正蔵 T4.568c 塵垢品第11頌"},
    248: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-012",
          "text": "人如覺是，不當念惡，愚近非法，久自燒沒。", "satLocus": "大正蔵 T4.568c 塵垢品第12頌"},
    249: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-013",
          "text": "若信布施，欲揚名譽，會人虛飾，非入淨定。", "satLocus": "大正蔵 T4.568c 塵垢品第13頌"},
    250: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-014",
          "text": "一切斷欲，截意根原，晝夜守一，必入定意。", "satLocus": "大正蔵 T4.568c 塵垢品第14頌"},
    251: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-017",
          "text": "火莫熱於婬，捷莫疾於怒，網莫密於癡，愛流駛乎河。", "satLocus": "大正蔵 T4.568c 塵垢品第17頌"},
    252: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ垢の章252はT210に対応なし（蘇錦坤對照表）。"},
    253: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ垢の章253はT210に対応なし（蘇錦坤對照表）。"},
    254: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-018",
          "text": "虛空無轍迹，沙門無外意，眾人盡樂惡，唯佛淨無穢。", "satLocus": "大正蔵 T4.568c 塵垢品第18頌"},
    255: {"status": "mapped", "pin": "塵垢品（T210 第26品）", "t210": "T210-26-019",
          "text": "空無轍迹，沙門無外意，世間皆無常，佛無我所有。", "satLocus": "大正蔵 T4.568c 塵垢品第19頌"},
}

VERSE_PRACTICE = {
    235: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "枯葉の如く死出の門に立つ、旅路の糧を積め"},
    236: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "自己の依所を造り、垢穢を払え"},
    237: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "齢は既に傾き、途上に住所も糧もない"},
    238: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "垢穢を払えば、再び生と老に近づかない"},
    239: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "漸次に少量ずつ、垢穢を払う"},
    240: {"nidanaId": "clinging", "pathFactors": ["正見", "正念"], "reason": "自己の悪業は錆の如く自己を蝕む"},
    241: {"nidanaId": "contact", "pathFactors": ["正念", "正精進"], "reason": "不誦・怠惰・放逸はそれぞれの垢"},
    242: {"nidanaId": "craving", "pathFactors": ["正念", "正業"], "reason": "不義・吝嗇・悪法はこの世にもかの世にも垢"},
    243: {"nidanaId": "craving", "pathFactors": ["正見", "正念"], "reason": "無明は最大の垢穢"},
    244: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "慚愧なき傲慢な生活は安易に見える"},
    245: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "慚愧・清浄・謙遜の生活は困難だが価値がある"},
    246: {"nidanaId": "clinging", "pathFactors": ["正業", "正念"], "reason": "殺生・妄語・偸盗・邪淫は自己の根を掘る"},
    247: {"nidanaId": "clinging", "pathFactors": ["正念", "正命"], "reason": "酒に沈湎する者は自己の根底を掘る"},
    248: {"nidanaId": "craving", "pathFactors": ["正念", "正業"], "reason": "貪欲と非法をして永く苦に陥らしむな"},
    249: {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "他人の得た食への不満は三昧を妨げる"},
    250: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "嫉妬を断てば、昼も夜も三昧に入る"},
    251: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "貪欲の火・瞋恚・愚痴・愛欲の河流"},
    252: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "他人の過失は見易く、自己の過失は見難い"},
    253: {"nidanaId": "clinging", "pathFactors": ["正念", "正見"], "reason": "他人の過失を詮索すれば煩悩が増長する"},
    254: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "衆生は虚妄を喜び、如来には虚妄なし"},
    255: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "万象は常住ならず、諸仏に擾乱なし"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP18-P01", 235),
    ("DP18-P02", 236),
    ("DP18-P03", 237),
    ("DP18-P04", 238),
    ("DP18-P05", 239), ("DP18-P06", 239),
    ("DP18-P07", 240), ("DP18-P08", 240),
    ("DP18-P09", 241), ("DP18-P10", 241),
    ("DP18-P11", 242),
    ("DP18-P12", 243),
    ("DP18-P13", 244),
    ("DP18-P14", 245),
    ("DP18-P15", 246),  # 246–247
    ("DP18-P16", 248),
    ("DP18-P17", 249),
    ("DP18-P18", 250),
    ("DP18-P19", 251),
    ("DP18-P20", 252),
    ("DP18-P21", 253),
    ("DP18-P22", 254),
    ("DP18-P23", 255),
    ("DP18-P24", 254),
]

COMBINED = {
    246: (246, 247),
}


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


def chinese_for_pair(verse, parts=None):
    if parts:
        for v in parts:
            if CHINESE[v]["status"] == "mapped":
                zh = chinese_block(v)
                if v != verse:
                    zh["note"] = (
                        f"併記偈のうち第{v}偈の漢訳対応を表示。"
                        + (CHINESE[verse].get("note") or "")
                    ).strip()
                return zh
    return chinese_block(verse)


def main():
    old = json.loads((DATA / "ch18.json").read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}

    pairs = []
    for pid, verse in PAIR_META:
        vp = VERSE_PRACTICE[verse]
        factors = vp["pathFactors"]
        if verse in COMBINED:
            parts = COMBINED[verse]
            observe = " ".join(OBSERVE[v] for v in parts)
            quote = " ".join(QUOTES[v] for v in parts)
            a, b = parts[0], parts[-1]
            pali_locus = f"小部・ダンマパダ 垢の章 第{a}-{b}偈"
            modern_locus = f"第１８章・垢穢品 第{a}-{b}偈（#ch02-18）"
            zh = chinese_for_pair(verse, parts)
            verse_out = a
        else:
            observe = OBSERVE[verse]
            quote = QUOTES[verse]
            pali_locus = f"小部・ダンマパダ 垢の章 第{verse}偈"
            modern_locus = f"第１８章・垢穢品 第{verse}偈（#ch02-18）"
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

    TITLE = "ダンマパダ 第18章・垢穢品（垢の章）"
    SHORT = "垢穢品（垢の章）"
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
            "pathLabel": "死出の門と虚妄に触れ、旅路の糧と真実を選ぶ",
            "chapterHint": SHORT,
            "fromPrev": "前夜の無常の見直しが、今朝の精勤になる",
            "toNext": "接触のあと、嫉妬・不満の受が立ち上がる",
            "todayObserve": OBSERVE[235],
            "todayAction": actions["DP18-P01"],
            "when": ["朝の始まり", "虚妄に触れそう"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[235][:40] + "…",
            "secondaryObserve": "不誦・怠惰・放逸はそれぞれの垢",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "他人の得たものへの不満の受を、三昧を妨げる垢と知る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、比較・嫉妬の受が来る",
            "toNext": "受けた不満を、貪欲の欲しがりへ落とさない",
            "todayObserve": OBSERVE[249],
            "todayAction": actions["DP18-P17"],
            "when": ["誰かの成功に不満を感じた", "比べて苦しんだ"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[249][:40] + "…",
            "secondaryObserve": "不満を抱く者は、昼も夜も三昧に入れない",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "貪欲・無明の垢への欲しがりを緩める",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、貪欲と非法への欲しがりへ落ちる",
            "toNext": "止めないと悪業・詮索の掴みへ進む",
            "todayObserve": OBSERVE[251],
            "todayAction": actions["DP18-P19"],
            "when": ["欲が燃えた", "無知に安住しそう"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[251][:40] + "…",
            "secondaryObserve": "無明は最大の垢穢",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "action", "nidanaLabel": "掴む",
            "pathFactors": ["正業", "正念"], "pathFactorIds": ["action", "mindfulness"],
            "pathLabel": "悪業と他人の過失への掴みを断つ",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、悪習慣・詮索として掴む手前",
            "toNext": "掴むと錆の如く自己を蝕み、苦が太る",
            "todayObserve": OBSERVE[240],
            "todayAction": actions["DP18-P07"],
            "when": ["悪い習慣を止められない", "他人の過失を詮索した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[240][:40] + "…",
            "secondaryObserve": "自己の悪業は錆の如く自己を蝕む",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "糧なき旅路と、自己の過失を見ない苦を知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、老いと自己欺瞞の苦が熟す",
            "toNext": "見れば、垢穢を払う精勤へ向き直る",
            "todayObserve": OBSERVE[237],
            "todayAction": actions["DP18-P03"],
            "when": ["後回しが積もった", "自分の過失が見えない"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[237][:40] + "…",
            "secondaryObserve": "他人の過失は見易く、自己の過失は見難い",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "自己の依所を造り、漸次に垢穢を払って離す",
            "chapterHint": SHORT,
            "fromPrev": "垢への掴みが流れを加速させる",
            "toNext": "離すと、無常と不動の見直しへつながる",
            "todayObserve": OBSERVE[239],
            "todayAction": actions["DP18-P05"],
            "when": ["少しずつ改善したい", "垢を払いたい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[239][:40] + "…",
            "secondaryObserve": "自己の依所を造り、速やかに精勤せよ",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正定"], "pathFactorIds": ["mindfulness", "concentration"],
            "pathLabel": "万象は常住ならず、今日の垢を払えたか見直す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、垢か清浄かの跡",
            "toNext": "見直しが、翌朝の旅路の糧になる",
            "todayObserve": OBSERVE[255],
            "todayAction": actions["DP18-P23"],
            "when": ["一日を閉じるとき", "変化に動じた"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[255][:40] + "…",
            "secondaryObserve": "万象は常住ならず、諸仏に擾乱なし",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 18,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第18章（垢穢品／垢の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（主にT210塵垢品、一部未対応あり）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・垢の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第１８章・垢穢品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・塵垢品（T4.568b）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "垢穢品は漸次に心の垢を払い自己の依所を造ることが中心。既定の焦点は離す。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch18.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch18.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 19):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch18", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 24
    assert all(p["id"] == f"DP18-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(235, 256))
    assert all(p["alignment"]["chinese"]["status"] in ("mapped", "unmapped") for p in pairs)
    print("OK")


if __name__ == "__main__":
    main()
