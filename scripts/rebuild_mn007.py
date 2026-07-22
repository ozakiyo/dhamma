#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn007.json (布喩経／衣装の経) to match MN1–6 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0575"
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
    "MN7-P01": (
        "比丘たちよ、それは、たとえば、また、汚染され垢にまみれた衣装があるとします。"
        "〔まさに〕その、この〔衣装〕を、染色師が……染料の類のなかに設置するなら、"
        "まさしく、悪しく染められた色艶のものとして存するでしょうし、……完全なる清浄ならざる色艶のものとして存するでしょう。"
        "比丘たちよ、まさしく、このように、まさに、心が汚染されているとき、悪しき境遇が待っています。"
    ),
    "MN7-P02": (
        "比丘たちよ、それは、たとえば、また、完全なる清浄にして完全なる清白の衣装があるとします。"
        "〔まさに〕その、この〔衣装〕を、染色師が……染料の類のなかに設置するなら、"
        "まさしく、善く染められた色艶のものとして存するでしょうし、……完全なる清浄の色艶のものとして存するでしょう。"
        "比丘たちよ、まさしく、このように、まさに、心が汚染されていないとき、善き境遇（善趣）が待っています。"
    ),
    "MN7-P03": (
        "比丘たちよ、では、どのようなものが、心の、付随する〔心の〕汚れ（随煩悩）なのですか。"
        "強欲〔の思い〕と正義ならざる貪り〔の思い〕は……憎悪……忿激……怨恨……嫉妬……物惜……思量……高慢……驕慢……放逸は、"
        "心の、付随する〔心の〕汚れです。"
    ),
    "MN7-P04": (
        "彼は、覚者にたいする確固たる浄信を具備した者として〔世に〕有ります。……"
        "法（教え）にたいする確固たる浄信を具備した者として〔世に〕有ります。……"
        "僧団にたいする確固たる浄信を具備した者として〔世に〕有ります。"
    ),
    "MN7-P05": (
        "彼は、『覚者にたいする確固たる浄信を具備した者として、〔わたしは〕存している』と、"
        "義（意味）の信受を得、法（教え）の信受を得、法（真理）を伴った歓喜を得ます。"
        "歓喜した者には、喜悦が生じます。喜悦の意ある者には、身体が静息します。"
        "静息した身体ある者は、安楽を感受します。安楽ある者には、心が定められます。"
    ),
    "MN7-P06": (
        "また、まさに、すなわち、限界まで、彼の、〔付随する心の汚れは〕捨てられたものと成り、吐き捨てられたものと〔成り〕、"
        "解き放たれたものと〔成り〕、捨棄されたものと〔成り〕、放棄されたものと〔成ります〕。"
    ),
    "MN7-P07": (
        "比丘たちよ、それで、まさに、その比丘が、このような戒ある者であり、このような法（教え）ある者であり、このような智慧ある者であるなら、"
        "たとえ、もし、黒米を選り分けた諸々の米の飯と幾多の汁と幾多の香味ある〔行乞の〕施食を受けるとして、"
        "彼にとって、それは、まさしく、障りと成りません。"
    ),
    "MN7-P08": (
        "彼は、慈愛〔の思い〕（慈）を共具した心で、一つの方角を充満して、〔世に〕住みます。……"
        "一切すべての世を、広大で莫大で無量にして怨念〔の思い〕なく憎悪〔の思い〕なく慈愛〔の思い〕を共具した心で充満して、〔世に〕住みます。"
        "慈悲〔の思い〕（悲）を……歓喜〔の思い〕（喜）を……放捨〔の思い〕（捨）を共具した心で……充満して、〔世に〕住みます。"
    ),
    "MN7-P09": (
        "彼は、『これが存在する』『下劣なるものが存在する』『精妙なるものが存在する』"
        "『この表象を具したものには、より上なる出離が存在する』と覚知します。"
        "彼が、このように知っていると、このように見ていると、欲望の煩悩からもまた、心は解脱し、……無明の煩悩からもまた、心は解脱します。"
        "比丘たちよ、この者は、『比丘として、内なる沐浴によって沐浴した者である』〔と〕説かれます。"
    ),
    "MN7-P10": (
        "〔そこで、詩偈に言う〕「バーフカー〔川〕に、そして、アディカッカー〔川〕に、ガヤー〔川〕に、……"
        "愚者が、たとえ、常に飛び込むも、黒き行為は清まらない。"
        "スンダリカー〔川〕が、何を為すというのだろう……怨みある者を、罪障を作った者を、悪しき行為あるその人を、まさに、清めない。"
    ),
    "MN7-P11": (
        "まさに、清浄の者には、常に春がある。清浄の者には、常に斎戒（布薩）がある。"
        "清浄の者にして清らかな行為ある者には、常に掟が成就する。"
        "婆羅門よ、まさしく、ここに、沐浴せよ。一切の生類たちにたいし、平安なることを為せ。"
        "それで、もし、〔あなたが〕虚偽を話さないなら、……命あるものを害さないなら、……与えられていないものを取らないなら、……"
        "ガヤー〔川〕に赴いて、何を為すというのだろう。"
    ),
    "MN7-P12": (
        "〔まさに〕この、わたしは、帰依所として、貴君ゴータマのもとに赴きます──そして、法（教え）のもとに、さらに、比丘の僧団のもとに。"
        "わたしが、貴君ゴータマの現前において、出家を得られますように──〔戒の〕成就を得られますように。"
        "……独り、〔静所に〕隠棲し、〔気づきを〕怠らず、熱情ある者となり、自己を精励する者として〔世に〕住んでいると、……"
    ),
    "MN7-P13": (
        "比丘たちよ、まさしく、このように、まさに、心が汚染されているとき、悪しき境遇が待っています。"
        "……心が汚染されていないとき、善き境遇が待っています。"
        "……内なる沐浴によって沐浴した者である〔と〕説かれます。"
    ),
}

OBSERVE = {
    "MN7-P01": (
        "垢にまみれた衣装は、どんな染料でも美しく染まらない。"
        "心が汚染されているとき、悪しき境遇が待つ。"
    ),
    "MN7-P02": (
        "清浄な衣装は、青・黄・赤・深紅にも美しく染まる。"
        "心が汚染されていないとき、善き境遇が待つ。"
    ),
    "MN7-P03": (
        "心の随煩悩——強欲・不正貪・憎悪・忿恨・嫉妬・慳・慢・放逸など。"
        "それを名づけて見出す。"
    ),
    "MN7-P04": (
        "随煩悩を捨てた者は、仏・法・僧への確固たる浄信を具備する。"
    ),
    "MN7-P05": (
        "浄信から義の信受・法の信受・法を伴った歓喜が生じ、"
        "喜悦→身体の静息→安楽→心が定まる。"
    ),
    "MN7-P06": (
        "随煩悩は、捨てられ、吐き捨てられ、解き放たれ、捨棄され、放棄される。"
    ),
    "MN7-P07": (
        "戒・法・慧ある者には、上質の施食を受けても障りとならない。"
        "垢衣が清水で清まるように、金が炉で清まるように。"
    ),
    "MN7-P08": (
        "慈・悲・喜・捨の心で、一切の方角・一切の世を、"
        "怨念なく憎悪なく充満して住む。"
    ),
    "MN7-P09": (
        "下劣・精妙・出離を覚知し、三漏から心が解脱する。"
        "これが『内なる沐浴』である。"
    ),
    "MN7-P10": (
        "聖河に飛び込んでも、愚者の黒き行為は清まらない。"
        "外の沐浴は、怨み・罪障を清めない。"
    ),
    "MN7-P11": (
        "清浄の者には常に布薩があり、清らかな行為がある。"
        "ここに沐浴せよ——不妄・不殺・不盗・信・不慳。"
    ),
    "MN7-P12": (
        "スンダリカ婆羅門は法を聞いて三宝に帰依し、出家・具足戒を得、"
        "精励して住んだ。"
    ),
    "MN7-P13": (
        "一日の地図——心の汚れを名づけ、捨て、信・慈で内浴し、外の儀式に頼らない。"
    ),
}

PRACTICE = {
    "MN7-P01": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "汚染心は悪趣を待つ——垢衣の譬喩",
        "section": "垢衣",
        "category": "view",
    },
    "MN7-P02": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "清浄心は善趣を待つ——浄衣の譬喩",
        "section": "浄衣",
        "category": "view",
    },
    "MN7-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "随煩悩（強欲・憎悪等）を名づける",
        "section": "随煩悩",
        "category": "intention",
    },
    "MN7-P04": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "捨てたあと仏法僧への浄信を具備する",
        "section": "三宝信",
        "category": "view",
    },
    "MN7-P05": {
        "nidanaId": "feeling",
        "pathFactors": ["正定", "正念"],
        "reason": "歓喜→軽安→楽→定の内面の次第",
        "section": "歓喜·定",
        "category": "concentration",
    },
    "MN7-P06": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正思惟"],
        "reason": "随煩悩を捨て吐き出し放棄する",
        "section": "捨棄",
        "category": "effort",
    },
    "MN7-P07": {
        "nidanaId": "contact",
        "pathFactors": ["正命", "正念"],
        "reason": "戒法慧あれば四事の接触も障りにならない",
        "section": "戒法慧",
        "category": "livelihood",
    },
    "MN7-P08": {
        "nidanaId": "release",
        "pathFactors": ["正思惟", "正念"],
        "reason": "四無量心で世を充満する",
        "section": "四無量",
        "category": "intention",
    },
    "MN7-P09": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正定"],
        "reason": "三漏解脱——内なる沐浴",
        "section": "内浴·漏尽",
        "category": "view",
    },
    "MN7-P10": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正思惟"],
        "reason": "外の聖河沐浴への執着は黒業を清めない",
        "section": "外浴·非",
        "category": "view",
    },
    "MN7-P11": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正業"],
        "reason": "ここに沐浴——不妄・不殺・不盗・信",
        "section": "清浄行",
        "category": "speech",
    },
    "MN7-P12": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正見"],
        "reason": "聞いて帰依し精励する——結語",
        "section": "帰依·出家",
        "category": "mindfulness",
    },
    "MN7-P13": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正精進"],
        "reason": "一日の段階を振り返り明日の一歩を決める",
        "section": "総括",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN7-P01": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-dirty",
        "text": "若有二十一穢汚於心者。必至惡處生地獄中。……猶垢膩衣持與染家。……然此汚衣故有穢色。",
        "satLocus": "大正蔵 T1.575c 水淨梵志経",
        "note": "垢膩衣＝パーリの垢衣。心穢→悪処。",
    },
    "MN7-P02": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-clean",
        "text": "若有二十一穢不汚心者。必至善處生於天上。……猶如白淨波羅奈衣持與染家。……然此白淨波羅奈衣本已淨而復淨。",
        "satLocus": "大正蔵 T1.575c–576a 水淨梵志経",
        "note": "白淨衣＝パーリの浄衣。不汚心→善処。",
    },
    "MN7-P03": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-defilements",
        "text": "云何二十一穢。邪見心穢……貪心穢恚心穢……慳心穢嫉心穢……慢心穢……放逸心穢。",
        "satLocus": "大正蔵 T1.575c 水淨梵志経",
        "note": "漢訳は二十一穢（パーリ十六随煩悩に対応・拡張）。",
    },
    "MN7-P04": {
        "status": "unmapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": None,
        "text": None,
        "satLocus": "大正蔵 T1.575c–576b",
        "note": "パーリの仏法僧への確固たる浄信の段は、増一／中阿含のこの経で明示せず。",
    },
    "MN7-P05": {
        "status": "unmapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": None,
        "text": None,
        "satLocus": "大正蔵 T1.575c–576b",
        "note": "パーリの歓喜→軽安→楽→定の次第は、この漢訳経に対応段落なし。",
    },
    "MN7-P06": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-abandon",
        "text": "若知邪見是心穢者知已便斷。……若知放逸是心穢者知已便斷。",
        "satLocus": "大正蔵 T1.576a 水淨梵志経",
        "note": "知已便断＝見出して捨棄。",
    },
    "MN7-P07": {
        "status": "unmapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": None,
        "text": None,
        "satLocus": "大正蔵 T1.575c–576b",
        "note": "パーリの戒法慧あれば美食も障りなしの譬喩は、この漢訳経に対応段落なし。",
    },
    "MN7-P08": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-brahma",
        "text": "彼心與慈倶遍滿十方成就遊。……如是悲喜心與捨倶。無結無怨無恚無諍。極廣甚大無量善修。遍滿一切世間成就遊。",
        "satLocus": "大正蔵 T1.576a 水淨梵志経",
        "note": "慈悲喜捨＝四無量。",
    },
    "MN7-P09": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-inner",
        "text": "梵志。是謂洗浴内心非浴外身。",
        "satLocus": "大正蔵 T1.576a 水淨梵志経",
        "note": "洗浴内心＝パーリの内なる沐浴。漏尽の詳説は漢訳で圧縮。",
    },
    "MN7-P10": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-river",
        "text": "爾時世尊爲彼梵志而説頌曰……是愚常遊戲 不能淨黒業……人作不善業 清水何所益",
        "satLocus": "大正蔵 T1.576a–b 水淨梵志経",
        "note": "多水河に入っても黒業は浄まらない。",
    },
    "MN7-P11": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-conduct",
        "text": "淨者無垢穢 淨者常説戒……若汝不殺生 常不與不取 眞諦不妄語 常正念正知……淨洗以善法 何須弊惡水",
        "satLocus": "大正蔵 T1.576b 水淨梵志経",
        "note": "善法で浄洗——外水に頼らない。",
    },
    "MN7-P12": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-convert",
        "text": "梵志聞佛教 心中大歡喜 即時禮佛足 歸命佛法衆……受我爲優婆塞。從今日始終身自歸乃至命盡。",
        "satLocus": "大正蔵 T1.576b 水淨梵志経",
        "note": "漢訳は優婆塞帰依（パーリは出家・阿羅漢）。内容対応。",
    },
    "MN7-P13": {
        "status": "mapped",
        "pin": "中阿含93・水淨梵志経（T26）",
        "t26": "T26-093-close",
        "text": "佛説如是。好首水淨梵志。及諸比丘聞佛所説。歡喜奉行",
        "satLocus": "大正蔵 T1.576b 水淨梵志経",
        "note": "結語・歓喜奉行。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部7経と中阿含93水淨梵志経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn007.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 14):
        pid = f"MN7-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 7",
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
                    "locus": f"中部・衣装の経（MN7）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 布喩経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第7経・布喩経（衣装の経）"
    SHORT = "布喩経（衣装の経）"
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
            "id": "contact", "weekday": 1, "categoryId": "livelihood", "nidanaLabel": "接触",
            "pathFactors": ["正命", "正念"], "pathFactorIds": ["livelihood", "mindfulness"],
            "pathLabel": "四事の接触も、戒法慧あれば障りにならない",
            "chapterHint": SHORT,
            "fromPrev": "前夜の見直しが、今朝の受け方になる",
            "toNext": "接触のあと、快不快の受が来る",
            "todayObserve": OBSERVE["MN7-P07"],
            "todayAction": actions["MN7-P07"],
            "when": ["食事の前", "道具を受けた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN7-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN7-P02"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "concentration", "nidanaLabel": "受ける",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "歓喜→軽安→楽→定の受の次第を保つ",
            "chapterHint": SHORT,
            "fromPrev": "浄信のあと、歓喜の受が立ち上がる",
            "toNext": "受に乗らず定へ向かう",
            "todayObserve": OBSERVE["MN7-P05"],
            "todayAction": actions["MN7-P05"],
            "when": ["善い行いのあと", "心が明るくなった"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN7-P05"][:40] + "…",
            "secondaryObserve": "歓喜を一呼吸保つ",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "強欲・憎悪などの随煩悩を名づける",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、強欲や憎悪が立ち上がる",
            "toNext": "止めないと外の儀式などへの掴みへ",
            "todayObserve": OBSERVE["MN7-P03"],
            "todayAction": actions["MN7-P03"],
            "when": ["欲や怒りが出た", "慢心が立った"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN7-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN7-P06"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正思惟"], "pathFactorIds": ["view", "intention"],
            "pathLabel": "外の聖河沐浴への執着を掴まず離す",
            "chapterHint": SHORT,
            "fromPrev": "汚れを外で洗おうと掴む手前",
            "toNext": "掴むと黒業は清まらず苦が残る",
            "todayObserve": OBSERVE["MN7-P10"],
            "todayAction": actions["MN7-P10"],
            "when": ["形だけの清めに頼った", "外の儀式を優先した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN7-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN7-P11"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "汚染心は悪趣を待つ——垢衣の帰結を見る",
            "chapterHint": SHORT,
            "fromPrev": "汚れを残した結果として、悪しき境遇が見える",
            "toNext": "見れば、洗い捨て内浴へ向き直る",
            "todayObserve": OBSERVE["MN7-P01"],
            "todayAction": actions["MN7-P01"],
            "when": ["心が濁って重い", "染みが取れない"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN7-P01"][:40] + "…",
            "secondaryObserve": "垢衣は美しく染まらない",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "汚れを捨て、慈で充満し、内浴で解脱する",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、浄衣・捨棄・四無量・内浴へ",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN7-P06"],
            "todayAction": actions["MN7-P06"],
            "when": ["染みを一つ捨てた", "慈心を向けた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN7-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN7-P09"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "今日の汚れと内浴を振り返り、明日の一歩を決める",
            "chapterHint": SHORT,
            "fromPrev": "一日の染みと捨ては、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN7-P13"],
            "todayAction": actions["MN7-P13"],
            "when": ["一日を閉じるとき", "聞法できた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN7-P13"][:40] + "…",
            "secondaryObserve": OBSERVE["MN7-P04"],
        },
    ]

    out = {
        "chapter": 7,
        "sutta": 7,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 根本法門品（アラナ：衣装の経）",
        "suttas": ["MN 7 布喩経（衣装の経）"],
        "source": {
            "primary": "パーリ・中部第7経（布喩経／衣装の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含93水淨梵志経（T26）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・衣装の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・水淨梵志経（T1.575c）",
                    "url": SAT_URL,
                    "note": "漢訳は一部圧縮。對照表: 法雨道場",
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
            "focusReason": "布喩経は心の汚れを捨て内なる沐浴で清めるのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn007.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 7:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(7, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 13
    assert all(p["id"] == f"MN7-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] != "mapped"]
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/13; unmapped {unmapped}; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
