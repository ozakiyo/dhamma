#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn012.json (師子吼大経／大いなる獅子吼の経) to match MN1–11 source alignment."""
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
# 中阿含なし。單経 No.757 身毛喜豎経（對照表）
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0757_%2C17%2C0591"
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
    "MN12-P01": (
        "サーリプッタよ、また、まさに、十のものがあります。これらの、如来にとって、如来の力となるものです。"
        "それらの力を具備した如来は、雄牛たる境位を明言し、諸々の衆のなかで獅子吼を吼え叫び、梵の輪（不滅の真理）を転起させます。"
    ),
    "MN12-P02": (
        "サーリプッタよ、ここに、如来は、そして、状況あること（道理あること）を状況あることとして、"
        "さらに、状況なきこと（道理なきこと）を状況なきこととして、事実のとおりに覚知します。"
        "……過去と未来と現在の諸々の行為の……報いを……覚知します。"
        "……一切所に至る〔実践の〕道を……覚知します。"
        "……諸々の煩悩の滅尽あることから、……〔観察の〕智慧による解脱を、まさしく、所見の法（現世）において、自ら、証知して、実証して、成就して、〔世に〕住みます。"
    ),
    "MN12-P03": (
        "サーリプッタよ、四つのものがあります。これらの、如来のものたる離怖〔のあり方〕（無畏）です。"
        "それらの離怖を具備した如来は、雄牛たる境位を明言し、諸々の衆のなかで獅子吼を吼え叫び、梵の輪を転起させます。"
        "……平安に至り得た者として、恐怖なき〔境地〕に至り得た者として、離怖に至り得た者として、〔世に〕住みます。"
    ),
    "MN12-P04": (
        "リッチャヴィ〔族〕の子息のスナッカッタが……このような言葉を語ります。"
        "『沙門ゴータマに、人間の法（性質）を超える、十全にして聖なる知見という殊勝〔の境地〕は存在しない。"
        "沙門ゴータマは、考慮によって撃打されたものとして、法（教え）を説示する……』と。"
        "サーリプッタよ、まさに、この者は、愚人のスナッカッタは、忿激する者です。……忿激ゆえに、彼のこの言葉は語られました。"
    ),
    "MN12-P05": (
        "サーリプッタよ、まさに、愚人のスナッカッタは、『栄誉ならざることを、〔わたしは〕語るのだ』と〔思いつつ〕、まさしく、如来の栄誉を語ります。"
        "……なぜなら、これは、如来の栄誉であるからです。……『……正しく苦しみの滅尽への出脱となる』と。"
    ),
    "MN12-P06": (
        "サーリプッタよ、四つのものがあります。まさに、これらの胎です。"
        "卵生の胎であり、胎生の胎であり、湿生の胎であり、化生の胎です。"
    ),
    "MN12-P07": (
        "『また、まさに、その義（目的）のために、あなたによって、法（教え）が説示されたなら、"
        "それは、それを為す者のために、正しく苦しみの滅尽への出脱とならず』と、……叱責するであろう、という、この形相を、〔わたしは〕等しく随観しません。"
        "……平安に至り得た者として、恐怖なき〔境地〕に至り得た者として、離怖に至り得た者として、〔世に〕住みます。"
    ),
    "MN12-P08": (
        "一方に坐った、まさに、尊者サーリプッタは、世尊に、こう言いました。"
        "『尊き方よ、リッチャヴィ〔族〕の子息のスナッカッタが、この法（教え）と律から立ち去ったすぐあと、"
        "彼は、ヴェーサーリーの衆のなかで、このような言葉を語ります……』と。"
        "サーリプッタよ、まさに、この者は、愚人のスナッカッタは、忿激する者です。……"
        "サーリプッタよ、また、まさに、十のものがあります。これらの、如来にとって、如来の力となるものです。"
    ),
    "MN12-P09": (
        "尊者ナーガサマーラは、世尊に、こう言いました。"
        "『尊き方よ、……この法（教え）の教相を聞いて、わたしの諸々の身の毛がよだったからです。"
        "……どのような名前が、この法（教え）の教相にありますか』と。"
        "『ナーガサマーラよ、……この法（教え）の教相を、まさしく、「諸々の身の毛のよだちの教相」と、それを保持しなさい』と。"
    ),
    "MN12-P10": (
        "それらの力を具備した如来は、雄牛たる境位を明言し、諸々の衆のなかで獅子吼を吼え叫び、梵の輪を転起させます。"
        "……善く説示された法は、それを為す者のために、正しく苦しみの滅尽への出脱となる。"
    ),
    "MN12-P11": (
        "人間を超越した清浄の天眼によって、有情たちが、死滅しつつあるのを、再生しつつあるのを、見ます。"
        "……〔為した〕行為のとおり〔報いに〕近しく赴く者たちとして、有情たちを覚知します。"
        "……悪しき行ないを具備し……誤った見解ある者たち……地獄に、再生したのだ。"
        "……善き行ないを具備し……正しい見解ある者たち……天上の世に、再生したのだ。"
    ),
}

OBSERVE = {
    "MN12-P01": (
        "大獅子吼は形式の誇示ではない——如来十力を具備し、衆中で梵輪を転ずること。"
    ),
    "MN12-P02": (
        "如来十力——処非処・業異熟・一切道・諸界・信解・諸根・禅解脱・宿命・天眼・漏尽智を如実に知る。"
    ),
    "MN12-P03": (
        "四無畏——正覚・漏尽・障道法・苦滅道について、誰にも法をもって叱責されぬ離怖に住む。"
    ),
    "MN12-P04": (
        "善星（スナッカッタ）は忿激ゆえに『殊勝の知見なし』と謗る——"
        "有無の極端な決めつけは、法の見極めではない。"
    ),
    "MN12-P05": (
        "栄誉を落とそうとして語っても、苦滅への出脱を認める言葉は如来の栄誉となる。"
        "証明・誹謗の衝動を戲論と名づける。"
    ),
    "MN12-P06": (
        "四胎——卵生・胎生・湿生・化生。"
        "今日の執着が、有への掴みのどの場にあるかを特定する。"
    ),
    "MN12-P07": (
        "法が苦滅の出脱とならぬ、という非難の形相を随観せず、離怖・無掛慮に住む。"
    ),
    "MN12-P08": (
        "舎利弗が衆中の謗りを報告し、仏は忿激せず十力・無畏を説く——"
        "反論の前に、相手（聞き手）の利益を考える。"
    ),
    "MN12-P09": (
        "身の毛のよだちの教相——聞法の感動を保持し、今日取ったものを明日手放す。"
    ),
    "MN12-P10": (
        "獅子吼と梵輪——善く説かれた法は、行う者に苦滅への出脱をもたらす。"
        "一節を声に出して読み返す。"
    ),
    "MN12-P11": (
        "天眼は業に随う再生を見る——悪行・邪見は悪趣、善行・正見は善趣。"
        "執着が来たら触→受→愛→取の流れを辿る。"
    ),
}

PRACTICE = {
    "MN12-P01": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "修行を形式ではなく十力・果に結びつける",
        "section": "十力·獅子吼",
        "category": "view",
    },
    "MN12-P02": {
        "nidanaId": "contact",
        "pathFactors": ["正見", "正念"],
        "reason": "確信の根拠を如来の如実力知に置く",
        "section": "如来十力",
        "category": "view",
    },
    "MN12-P03": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正思惟"],
        "reason": "四無畏の離怖に学び、見解の掴みを手放す",
        "section": "四無畏",
        "category": "view",
    },
    "MN12-P04": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "忿激の有無決めつけが苦を太らせると見る",
        "section": "善星·謗",
        "category": "view",
    },
    "MN12-P05": {
        "nidanaId": "craving",
        "pathFactors": ["正見", "正念"],
        "reason": "証明・誹謗したい衝動を戲論の欲しがりと名づける",
        "section": "忿激·戲論",
        "category": "view",
    },
    "MN12-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正念"],
        "reason": "今日の執着を四胎＝有への掴みとして特定する",
        "section": "四胎",
        "category": "view",
    },
    "MN12-P07": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正定"],
        "reason": "非難の形相に掛慮せず離怖に住む",
        "section": "離怖·出脱",
        "category": "concentration",
    },
    "MN12-P08": {
        "nidanaId": "release",
        "pathFactors": ["正語", "正思惟"],
        "reason": "反論の前に聞き手の利益を考えてから話す",
        "section": "舎利弗·説示",
        "category": "speech",
    },
    "MN12-P09": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正精進"],
        "reason": "身毛喜豎の教相を反芻し、取ったものを手放す",
        "section": "身毛よだち",
        "category": "mindfulness",
    },
    "MN12-P10": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "梵輪の一節を読み、苦滅への出脱を確かめる",
        "section": "梵輪",
        "category": "view",
    },
    "MN12-P11": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正見"],
        "reason": "業に随う苦楽の受から愛・取の流れを辿る",
        "section": "天眼·業趣",
        "category": "mindfulness",
    },
}

CHINESE = {
    "MN12-P01": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-sihanada",
        "text": "所有如來應供正等正覺。成就四無所畏而悉能知聖所行處。於大衆中。作師子吼。轉大梵輪。",
        "satLocus": "大正蔵 T17.591c– 身毛喜豎経",
        "note": "師子吼・轉梵輪。中阿含には対応経なし（對照表）。",
    },
    "MN12-P02": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-dasabala",
        "text": "於處非處以自智力。悉如實知。……一切所行。所至之道。悉以正智。如實了知……於諸有情。差別諸根。……天眼過於人眼。能觀世間一切有情生滅好醜。",
        "satLocus": "大正蔵 T17.592–593 身毛喜豎経",
        "note": "如來智力＝パーリ十力の核。",
    },
    "MN12-P03": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-vesarajja",
        "text": "成就四無所畏……一者……證一切智……我得安樂。無恐無畏……二者……諸漏已盡……三者……貪欲是障道法……四者……説正道法。而能出要。盡苦邊際。",
        "satLocus": "大正蔵 T17.593 身毛喜豎経",
        "note": "四無所畏＝四離怖。",
    },
    "MN12-P04": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-sunakkhatta",
        "text": "善星。捨離佛法。……謗佛法僧。而作是言。沙門瞿曇。尚無人中最上之法。況聖知見最勝所證。",
        "satLocus": "大正蔵 T17.591c 身毛喜豎経",
        "note": "善星＝スナッカッタ。殊勝知見の否定。",
    },
    "MN12-P05": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-abbhakkhana",
        "text": "以不信故。乃發是言。而爲誹謗。由彼心言及彼所見。相續謗故。速墮地獄。",
        "satLocus": "大正蔵 T17.592a 身毛喜豎経",
        "note": "不信・誹謗の相續＝戲論の害。",
    },
    "MN12-P06": {
        "status": "unmapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": None,
        "text": None,
        "satLocus": "大正蔵 T17.591c– 身毛喜豎経（卷上中心）",
        "note": "パーリ四胎は、取得した漢訳卷上・卷中断片に明示なし。増壹等の並行を参照可。",
    },
    "MN12-P07": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-abhaya",
        "text": "四者如來……説正道法。而能出要。盡苦邊際。……我得安樂無恐無畏。如實了知聖所行處。作師子吼。轉大梵輪。",
        "satLocus": "大正蔵 T17.593 身毛喜豎経",
        "note": "出要盡苦・無恐無畏＝第四無畏と離怖。",
    },
    "MN12-P08": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-sariputta",
        "text": "爾時尊者舍利子。於其食時著衣持鉢。入毘舍離大城。……聞彼城中善星長者子……謗佛法僧。",
        "satLocus": "大正蔵 T17.591c 身毛喜豎経",
        "note": "舍利子が衆中の謗りを聞き仏に報ずる枠。",
    },
    "MN12-P09": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-lomahamsa",
        "text": "佛説身毛喜豎經",
        "satLocus": "大正蔵 T17.591c 身毛喜豎経",
        "note": "経題そのものがパーリ「身の毛のよだちの教相」に対応。結部の命名場面は巻末側。",
    },
    "MN12-P10": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-brahma-cakka",
        "text": "於大衆中。作師子吼。轉大梵輪。餘諸沙門婆羅門。若魔若梵。悉不能轉。",
        "satLocus": "大正蔵 T17.593 身毛喜豎経",
        "note": "師子吼・轉大梵輪。",
    },
    "MN12-P11": {
        "status": "mapped",
        "pin": "佛説身毛喜豎経（T757）",
        "t26": "T757-dibba-cakkhu",
        "text": "天眼過於人眼。能觀世間一切有情生滅好醜。若貴若賤。隨業所受。……造不善業……墮在惡趣。生地獄中。……造衆善業……生於善趣天界之中。",
        "satLocus": "大正蔵 T17.592c–593a 身毛喜豎経",
        "note": "天眼・随業＝第九力に近接。縁起の触受愛取はパーリ側で補う。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部12経と單経身毛喜豎経（T757）の内容対応（對照表: 法雨道場）。中阿含には非収録。",
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
    old_path = DATA / "majjhima" / "mn012.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN12-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 12",
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
                    "locus": f"中部・大いなる獅子吼の経（MN12）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 師子吼大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第12経・師子吼大経（大いなる獅子吼の経）"
    SHORT = "師子吼大経（大いなる獅子吼の経）"
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
            "pathLabel": "衆中の言葉に触れ、如来の如実力知を根拠にする",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の謗りへの接触を変える",
            "toNext": "接触のあと、快・不快の受が立つ",
            "todayObserve": OBSERVE["MN12-P02"],
            "todayAction": actions["MN12-P02"],
            "when": ["謗りを聞いた", "確信を問われた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN12-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN12-P01"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "業に随う苦楽の受から愛・取の流れを辿る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、苦楽の受が立つ",
            "toNext": "受に乗ると忿激・戲論へ",
            "todayObserve": OBSERVE["MN12-P11"],
            "todayAction": actions["MN12-P11"],
            "when": ["苦楽を強く感じた", "業の報いを思った"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN12-P11"][:40] + "…",
            "secondaryObserve": "触→受→愛→取",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "view", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "証明・誹謗したい衝動を戲論の欲しがりと名づける",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、忿激の欲しがりが立つ",
            "toNext": "止めないと有への掴みへ",
            "todayObserve": OBSERVE["MN12-P05"],
            "todayAction": actions["MN12-P05"],
            "when": ["証明したくなった", "謗りたくなった"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN12-P05"][:40] + "…",
            "secondaryObserve": OBSERVE["MN12-P04"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "四胎＝有への掴みとして今日の執着を特定する",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、有への掴みが手前",
            "toNext": "掴むと謗りの苦が見える",
            "todayObserve": OBSERVE["MN12-P06"],
            "todayAction": actions["MN12-P06"],
            "when": ["有に固着した", "形式に掴まった"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN12-P06"][:40] + "…",
            "secondaryObserve": "卵生・胎生・湿生・化生",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "忿激の有無決めつけが苦を太らせると見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、謗りと悪趣の苦が見える",
            "toNext": "見れば、離怖の実践へ向き直る",
            "todayObserve": OBSERVE["MN12-P04"],
            "todayAction": actions["MN12-P04"],
            "when": ["極端に寄った", "忿激で語った"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN12-P04"][:40] + "…",
            "secondaryObserve": "速堕地獄の縁",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正定"], "pathFactorIds": ["view", "concentration"],
            "pathLabel": "四無畏の離怖に住み、非難に掛慮しない",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、離怖の一歩を踏む",
            "toNext": "離せば、夜の見直しへつながる",
            "todayObserve": OBSERVE["MN12-P07"],
            "todayAction": actions["MN12-P07"],
            "when": ["掛慮を一つ手放した", "無畏に戻った"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN12-P07"][:40] + "…",
            "secondaryObserve": OBSERVE["MN12-P03"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "身毛喜豎と梵輪を振り返り、明日の根拠を正す",
            "chapterHint": SHORT,
            "fromPrev": "一日の確信は、朝からの流れの跡",
            "toNext": "見直しが、翌朝の接触の根拠になる",
            "todayObserve": OBSERVE["MN12-P09"],
            "todayAction": actions["MN12-P09"],
            "when": ["一日を閉じるとき", "謗りに揺れた日"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN12-P09"][:40] + "…",
            "secondaryObserve": OBSERVE["MN12-P10"],
        },
    ]

    out = {
        "chapter": 12,
        "sutta": 12,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 師子吼品（アラナ：大いなる獅子吼の経）",
        "suttas": ["MN 12 師子吼大経（大いなる獅子吼の経）"],
        "source": {
            "primary": "パーリ・中部第12経（師子吼大経／大いなる獅子吼の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT佛説身毛喜豎経（T757；中阿含非収録）を段落対応でマッピング。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・大いなる獅子吼の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 佛説身毛喜豎経（T17.591c）",
                    "url": SAT_URL,
                    "note": "中阿含非収録。對照表: 法雨道場（増壹・雑阿含等も並行）",
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
            "focusReason": "師子吼大経は如来十力・四無畏に基づく離怖の獅子吼が主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn012.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 12:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(12, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN12-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    unmapped = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] != "mapped"]
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11 unmapped={unmapped}; nidanas", sorted(by_nidana))


if __name__ == "__main__":
    main()
