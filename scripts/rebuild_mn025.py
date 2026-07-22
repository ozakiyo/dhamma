#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn025.json (撒餌経／撒餌の経) to match MN1–24 source alignment."""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0026_%2C01%2C0718c01"
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
    "MN25-P01": (
        "比丘たちよ、猟師は、獣類たちに、撒餌を、このように撒きます。"
        "『獣類たちは、わたしが撒いたこの撒餌に深入りして耽溺し、諸々の食料を食べるであろう。"
        "……放逸の者たちとして存しながら、〔猟師の〕欲するままに為される者たちと成るであろう──この撒餌において』と。"
        "……『撒餌』とは、まさに、これは、五つの欲望の属性（五妙欲：色・声・香・味・触）の同義語です。"
        "『猟師』とは、まさに、これは、悪魔パーピマントの同義語です。"
    ),
    "MN25-P02": (
        "比丘たちよ、『撒餌』とは、まさに、これは、五つの欲望の属性（五妙欲：色・声・香・味・触）の同義語です。"
        "……眼によって識知されるべき諸々の色形（色）で、好ましく愛らしく意に適い、愛しい形態にして欲望を伴った貪るべきもの……。"
        "（第一の群——深入りして耽溺し、驕慢·放逸し、猟師の欲するままに為される。）"
    ),
    "MN25-P03": (
        "比丘たちよ、『撒餌』とは……五つの欲望の属性……耳によって識知されるべき諸々の音声（声）で……貪るべきもの……。"
        "……第一の沙門や婆羅門たちは、悪魔が撒いたこの撒餌に……深入りして耽溺し……放逸の者たちとして存しながら、"
        "〔悪魔の〕欲するままに為される者たちと成りました。"
    ),
    "MN25-P04": (
        "比丘たちよ、『撒餌』とは……五つの欲望の属性……鼻によって識知されるべき諸々の臭気（香）で……"
        "舌によって識知されるべき諸々の味感（味）で……身によって識知されるべき諸々の感触（触・所触）で……貪るべきもの……。"
    ),
    "MN25-P05": (
        "……第二の沙門や婆羅門たちは……『それなら、さあ、わたしたちは、全てにわたり、撒餌の食料から、世の財貨から、離間するのだ』と。"
        "……夏の最後の月となり……身体は……極度の痩せ細りに……活力と精進は、遍く衰退しました。"
        "……まさしく、その、悪魔が撒いたこの撒餌に……戻りました。……深入りして耽溺し……〔悪魔の〕欲するままに為される者たちと成りました。"
        "（極端な離間だけでは解き放たれない——味·財貨の餌に戻る。）"
    ),
    "MN25-P06": (
        "……第三の沙門や婆羅門たちは……悪魔が撒いたこの撒餌に……近しく依拠して、棲処を営みました。"
        "……深入りせずして耽溺することなく、諸々の食料を食べ……驕慢を惹起しませんでした。……放逸を惹起しませんでした。"
        "しかしながら、また、まさに、このような見解ある者たちと成りました。"
        "『世〔界〕は、常久である』ともまた……『如来は、死後に……』ともまた。"
        "……第三の……ものもまた、悪魔の神通の威力から完全に完全に解き放たれませんでした。"
    ),
    "MN25-P07": (
        "しかしながら、また、まさに、このような見解ある者たちと成りました。"
        "『世〔界〕は、常久である』ともまた、『世〔界〕は、常久ではない』ともまた……"
        "『如来は、死後に、まさしく、有ることもなく、有ることがないこともない』ともまた。"
        "比丘たちよ、まさに、このように、それらの第三の沙門や婆羅門たちもまた、"
        "悪魔の神通の威力から完全に完全に解き放たれませんでした。"
        "（見解·議論への執着もまた、魔の網に囲まれる巣。）"
    ),
    "MN25-P08": (
        "……第四の沙門や婆羅門たちは……『それなら、さあ、わたしたちは、すなわち、そして、悪魔の、さらに、悪魔の衆の、"
        "赴かない所で、そこで、棲処を営むのだ。……深入りせずして耽溺することなく……驕慢を惹起しないのだ……"
        "〔悪魔の〕欲するままに為される者たちと成らないのだ』と。"
        "……第四の沙門や婆羅門たちは、悪魔の神通の威力から完全に完全に解き放たれました。"
    ),
    "MN25-P09": (
        "……第一の……ものは……深入りして耽溺し……驕慢を惹起し……放逸を惹起し……"
        "〔悪魔の〕欲するままに為される者たちと成りました……悪魔の神通の威力から完全に完全に解き放たれませんでした。"
        "……それは、たとえば、また、それらの第一の獣類たちのように……。"
    ),
    "MN25-P10": (
        "比丘たちよ、では、どのように、そして、悪魔の、さらに、悪魔の衆の、赴かない所があるのですか。"
        "比丘たちよ、ここに、比丘が……第一の瞑想（初禅）を成就して〔世に〕住みます。"
        "……『比丘として、悪魔を盲者に作り為した──悪魔の眼を跡形なく打倒して、パーピマントの見なきところに至り』〔と〕説かれます。"
        "……表象と感覚の止滅（想受滅）を成就して……諸々の煩悩は、完全に滅尽したものと成ります。"
        "……『……パーピマントの見なきところに至り、世における執着を超えた者となり』〔と〕説かれます。"
    ),
    "MN25-P11": (
        "比丘たちよ、『撒餌』とは……五つの欲望の属性……『猟師』とは……悪魔パーピマント……"
        "『獣類たち』とは……沙門や婆羅門たち……。"
        "……第四の……ものは、悪魔の神通の威力から完全に完全に解き放たれました。"
        "……悪魔の……赴かない所で……棲処を営む。"
    ),
}

OBSERVE = {
    "MN25-P01": (
        "撒餌＝五妙欲、猟師＝悪魔。深入りして耽溺→驕慢→放逸→魔の欲するまま——"
        "朝、今日「魔の餌」に触れないよう一つ決める。"
    ),
    "MN25-P02": (
        "五妙欲の色——好ましい色形への深入りは第一群の堕ち方——"
        "今日、見た色に「餌」と一瞬見て、触れない。"
    ),
    "MN25-P03": (
        "五妙欲の声——好ましい音声への耽溺もまた魔の撒餌——"
        "今日、聞いた声に「餌」と一瞬見て、触れない。"
    ),
    "MN25-P04": (
        "五妙欲の香·味·触——鼻·舌·身の好ましい対象も撒餌——"
        "今日、覚えた香·味·触に「餌」と一瞬見て、触れない。"
    ),
    "MN25-P05": (
        "第二群——極端に離間しても痩せ細り、活力が衰退し餌に戻る。食事は修行の助けとして正しく用いる——"
        "食事を「餌のためでなく、清らかな修行の助けのため」と確認する。"
    ),
    "MN25-P06": (
        "第三群——餌の近くで耽溺せず食べるが、見解の網に囲まれて解き放たれない。触の対象にも深入りしない——"
        "今日、触の対象に「餌」と一瞬見て、触れない。"
    ),
    "MN25-P07": (
        "第三群の見解——世界の常·無常、如来の死後などへの執着も魔の巣。経典に「法の餌」という六欲はない——"
        "今日、知った法に「執着·餌」と一瞬見て、触れない。"
    ),
    "MN25-P08": (
        "第四群——悪魔の赴かない所に棲処を営み、深入りせず、驕慢·放逸せず、完全に解き放たれる——"
        "今日、一つの「餌」に触れず、避ける。"
    ),
    "MN25-P09": (
        "第一群——深入り·耽溺·驕慢·放逸の結果、魔の欲するまま。苦は餌に触れた流れ——"
        "今日の苦を「餌に触れた結果」と一度見る。"
    ),
    "MN25-P10": (
        "悪魔の赴かない所——初禅〜想受滅。夜、餌に触れた瞬間を認め、見なきところへ向かう——"
        "就寝前、今日「餌に触れた」瞬間を一つ認め、明日触れない。"
    ),
    "MN25-P11": (
        "猟師＝悪魔パーピマント、撒餌＝五妙欲。外を責めるより、内の欲·執着としての魔の領域を観る——"
        "今日、外の誘惑より内の「魔（欲·執着）」を観る。"
    ),
}

PRACTICE = {
    "MN25-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正思惟"],
        "reason": "朝、魔の撒餌（五妙欲）に触れないよう一つ決める",
        "section": "撒餌＝五妙欲",
        "category": "mindfulness",
    },
    "MN25-P02": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "好ましい色を餌と見て欲しがりに乗らない",
        "section": "色の撒餌",
        "category": "intention",
    },
    "MN25-P03": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正念"],
        "reason": "好ましい声を餌と見て欲しがりに乗らない",
        "section": "声の撒餌",
        "category": "intention",
    },
    "MN25-P04": {
        "nidanaId": "feeling",
        "pathFactors": ["正念", "正思惟"],
        "reason": "香·味·触の受を餌と見て深入りしない",
        "section": "香·味·触の撒餌",
        "category": "mindfulness",
    },
    "MN25-P05": {
        "nidanaId": "craving",
        "pathFactors": ["正命", "正念"],
        "reason": "食事を餌の耽溺ではなく修行の助けとして用いる",
        "section": "第二群·味と財貨",
        "category": "livelihood",
    },
    "MN25-P06": {
        "nidanaId": "clinging",
        "pathFactors": ["正念", "正思惟"],
        "reason": "触の対象への掴みを餌と見て離す",
        "section": "第三群·近住",
        "category": "mindfulness",
    },
    "MN25-P07": {
        "nidanaId": "clinging",
        "pathFactors": ["正見", "正思惟"],
        "reason": "見解·法への執着も魔の網として掴みを緩める",
        "section": "第三群·見解",
        "category": "view",
    },
    "MN25-P08": {
        "nidanaId": "release",
        "pathFactors": ["正精進", "正念"],
        "reason": "第四群のように餌に触れず、魔の赴かない所へ離す",
        "section": "第四群·解き放ち",
        "category": "effort",
    },
    "MN25-P09": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "苦を深入り·耽溺の結果として見る",
        "section": "第一群·苦",
        "category": "view",
    },
    "MN25-P10": {
        "nidanaId": "review",
        "pathFactors": ["正念", "正定"],
        "reason": "夜、餌に触れた瞬間を認め、魔の見なきところを思い出す",
        "section": "魔の赴かない所",
        "category": "mindfulness",
    },
    "MN25-P11": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "外の誘惑より内の欲·執着としての魔を観る",
        "section": "猟師＝悪魔",
        "category": "view",
    },
}

CHINESE = {
    "MN25-P01": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-bait",
        "text": (
            "獵師食者，當知五欲功德，眼知色、耳知聲、鼻知香、舌知味、身知觸。"
            "獵師者，當知是惡魔王也。獵師眷屬者，當知是魔王眷屬也。群鹿者，當知是沙門、梵志也。"
        ),
        "satLocus": "大正蔵 T1.719a 獵師経",
        "note": "獵師食＝撒餌＝五欲功德。",
    },
    "MN25-P02": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-rupa",
        "text": "獵師食者，當知五欲功德，眼知色……。第一沙門、梵志近食魔王食……便憍恣放逸……不脫魔王境界。",
        "satLocus": "大正蔵 T1.719a 獵師経",
        "note": "眼知色＝色の撒餌。",
    },
    "MN25-P03": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-sadda",
        "text": "耳知聲……。第一沙門、梵志近食魔王食，世間信施食，彼近食已，便憍恣放逸……。",
        "satLocus": "大正蔵 T1.719a 獵師経",
        "note": "耳知聲＝声の撒餌。",
    },
    "MN25-P04": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-gandha",
        "text": "鼻知香、舌知味、身知觸。獵師食者，當知是五欲功德也。",
        "satLocus": "大正蔵 T1.719a 獵師経",
        "note": "香·味·触＝五欲の残部。",
    },
    "MN25-P05": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-second",
        "text": (
            "第二沙門、梵志……捨獵師食，離於恐怖，依無事處……彼春後月諸草水盡，身體極羸，氣力衰退……"
            "便隨魔王、魔王眷屬……亦不脫魔王境界。"
        ),
        "satLocus": "大正蔵 T1.719a–b 獵師経",
        "note": "第二群——極端離間の後に戻る。",
    },
    "MN25-P06": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-third",
        "text": (
            "第三群鹿……依住不遠，住不遠已，不近食獵師食，不近食已，便不憍恣放逸……"
            "（而猟師以棒網囲之，得其巣穴——仍不脱。）"
        ),
        "satLocus": "大正蔵 T1.719b–c 獵師経",
        "note": "第三群——近くで耽溺せずも網に囲まれる。",
    },
    "MN25-P07": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-views",
        "text": (
            "第三沙門、梵志……不近食已，便不憍恣放逸……然彼猶有見……"
            "（パーリ：常久·無常等の見解。漢訳も第三はなお魔境を脱せず。）"
        ),
        "satLocus": "大正蔵 T1.719b–c 獵師経",
        "note": "旧「法の餌」は経典にない。見解の執着に対応。",
    },
    "MN25-P08": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-fourth",
        "text": (
            "第四沙門、梵志……依住於魔王、魔王眷屬所不至之處……不近食……不憍恣放逸……"
            "便不隨魔王、魔王眷屬……已脫魔王境界。"
        ),
        "satLocus": "大正蔵 T1.719c–720a 獵師経",
        "note": "第四群——魔の不至処。",
    },
    "MN25-P09": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-first-dukkha",
        "text": "第一沙門、梵志近食魔王食……便憍恣放逸，放逸已，便隨魔王、魔王眷屬，如是……不脫魔王境界。",
        "satLocus": "大正蔵 T1.719a 獵師経",
        "note": "近食→憍恣放逸＝餌に触れた結果。",
    },
    "MN25-P10": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-jhana",
        "text": (
            "云何魔王、魔王眷屬所不至之處？……入初禪……乃至……想知滅定……"
            "令魔盲無眼，至無見處。"
        ),
        "satLocus": "大正蔵 T1.720a–b 獵師経",
        "note": "四禅·無色·滅尽＝魔の不至処（漢訳は四無量等も列す場合あり）。",
    },
    "MN25-P11": {
        "status": "mapped",
        "pin": "中阿含178・獵師経（T26）",
        "t26": "T26-178-mara",
        "text": "獵師者，當知是惡魔王也。……獵師食者，當知是五欲功德也。",
        "satLocus": "大正蔵 T1.719a 獵師経",
        "note": "魔＝五欲の猟師。内の欲·執着として観る実践に対応。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部25経と中阿含178獵師経の内容対応（對照表: 法雨道場）。",
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
    old_path = DATA / "majjhima" / "mn025.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN25-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 25",
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
                    "locus": f"中部・撒餌の経（MN25）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 撒餌経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第25経・撒餌経（撒餌の経）"
    SHORT = "撒餌経（撒餌の経）"
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
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "朝、魔の撒餌（五妙欲）に触れないよう一つ決める",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の餌への接触を変える",
            "toNext": "触のあと、好ましい受が見える",
            "todayObserve": OBSERVE["MN25-P01"],
            "todayAction": actions["MN25-P01"],
            "when": ["朝に餌を決めた", "五妙欲に触れた"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN25-P01"][:40] + "…",
            "secondaryObserve": "五欲功德",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "香·味·触の受を餌と見て深入りしない",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、好ましい香·味·触の受が立つ",
            "toNext": "受に乗ると色·声·味への欲しがりへ",
            "todayObserve": OBSERVE["MN25-P04"],
            "todayAction": actions["MN25-P04"],
            "when": ["香·味·触を覚えた", "餌と見た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN25-P04"][:40] + "…",
            "secondaryObserve": "身知觸",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正念"], "pathFactorIds": ["intention", "mindfulness"],
            "pathLabel": "色·声·味への欲しがりを撒餌と見て乗らない",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、もっと欲しいが立つ",
            "toNext": "止めないと触·見解の掴みへ",
            "todayObserve": OBSERVE["MN25-P02"],
            "todayAction": actions["MN25-P02"],
            "when": ["色·声に引かれた", "食事を餌と混同しそう"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN25-P02"][:40] + "…",
            "secondaryObserve": OBSERVE["MN25-P03"],
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "view", "nidanaLabel": "掴む",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "触と見解への掴みを魔の網として緩める",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、触·法見の掴みが手前",
            "toNext": "掴むと放逸·苦が見える",
            "todayObserve": OBSERVE["MN25-P06"],
            "todayAction": actions["MN25-P06"],
            "when": ["触に掴まった", "見解に執着した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN25-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN25-P07"],
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "苦を深入り·耽溺·放逸の結果として見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、魔の欲するままの患が見える",
            "toNext": "見れば、第四群の離しへ",
            "todayObserve": OBSERVE["MN25-P09"],
            "todayAction": actions["MN25-P09"],
            "when": ["苦が残った", "餌に触れたと見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN25-P09"][:40] + "…",
            "secondaryObserve": "不脫魔王境界",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正定"], "pathFactorIds": ["effort", "concentration"],
            "pathLabel": "第四群のように餌に触れず、魔の赴かない所へ離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、深入りせず解き放つ",
            "toNext": "離せば、夜の餌の見直しへ",
            "todayObserve": OBSERVE["MN25-P08"],
            "todayAction": actions["MN25-P08"],
            "when": ["餌を避けた", "定に向かった"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN25-P08"][:40] + "…",
            "secondaryObserve": "魔王所不至之處",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "mindfulness", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "餌に触れた瞬間を認め、内の魔（欲·執着）を観る",
            "chapterHint": SHORT,
            "fromPrev": "一日の欲は、朝からの撒餌の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN25-P10"],
            "todayAction": actions["MN25-P10"],
            "when": ["一日を閉じるとき", "内の魔を観た夜"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN25-P10"][:40] + "…",
            "secondaryObserve": OBSERVE["MN25-P11"],
        },
    ]

    out = {
        "chapter": 25,
        "sutta": 25,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 譬喩法品（アラナ：撒餌の経）",
        "suttas": ["MN 25 撒餌経（撒餌の経）"],
        "source": {
            "primary": "パーリ・中部第25経（撒餌経／撒餌の経）観察ペア単位対応",
            "note": (
                "経典の言葉＝アラナ精舎和訳、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT中阿含178獵師経（T26）を段落対応でマッピング。"
                "撒餌は五妙欲（色·声·香·味·触）。旧スタブの「法の餌」は経典にないため、第三群の見解執着に対応。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・撒餌の経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 中阿含・獵師経（T1.718c）",
                    "url": SAT_URL,
                    "note": "獵師·五欲·四群鹿·魔王不至処。對照表: 法雨道場",
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
            "focusReason": "撒餌の経は五妙欲という魔の餌への深入り·耽溺が主題。既定の焦点は欲しがる。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn025.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 25:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(25, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN25-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    print(f"OK chinese mapped {mapped}/11; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
