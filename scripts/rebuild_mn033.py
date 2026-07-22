#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild majjhima/mn033.json (牧牛者大経／牧牛者の大経) to match MN1–32 source alignment.

実経: 牧牛十一法——色·相·蛆（不善尋）·瘡（根門）·煙（説法）·渡し場（請問）·
満足（法喜）·道（八正道）·牧場（四念処）·搾り尽くさず（受用の節度）·長老への慈。
旧スタブは DN19 マハーゴービンダ（梵天·無常）の混入。actions は保持し実文へ橋渡し。
"""
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
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0342c01"
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
    "MN33-P01": (
        "比丘たちよ、十一の支を具した牧牛者は、牛群を護り増やすことができない……。"
        "同様に、十一の法を具した比丘は、この法·律において増長·広大·円熟を得られない。"
        "（旧実践語の「梵天界も無常」は別経の混入。"
        "本経の朝の一歩は、十一法——まず色を知る——を一度思い出すことに置く。）"
    ),
    "MN33-P02": (
        "比丘は、いかに色を知るか。"
        "一切の色は、四大、および四大所造であると、如実に知る——"
        "このように色を知る。"
        "（快い経験·成功も色·有為——無常として一度見る。）"
    ),
    "MN33-P03": (
        "比丘は、いかに道を知るか。"
        "聖なる八支道を、如実に知る——"
        "このように道を知る。"
        "（これが牧場の「道」——真の法として八正道の一つを歩む。）"
    ),
    "MN33-P04": (
        "比丘は、いかに蛆を除くか。"
        "欲尋·瞋尋·害尋が生じても、それを忍ばず、捨て、除き、滅する——"
        "このように蛆を除く。"
        "（天界·楽への願いも欲尋の一環——解脱かと問う。）"
    ),
    "MN33-P05": (
        "十一の法を具した比丘は、この法·律において増長·広大·円熟を得る。"
        "色を知り、相に巧み、蛆を除き、瘡を覆い、煙を上げ、渡し場を知り、"
        "満足を知り、道を知り、牧場に巧み、乳を搾り尽くさず、長老に慈を行う。"
        "（施·戒·定を修しつつ、この十一法で解脱·円熟を目指す。）"
    ),
    "MN33-P06": (
        "一切の色は、四大、および四大所造であると、如実に知る。"
        "……愚者は業によって相づけられ、智者は業によって相づけられる。"
        "（今日の楽·苦も有為——無常として一度見る。）"
    ),
    "MN33-P07": (
        "愚者は業によって相づけられ、智者は業によって相づけられる——"
        "このように相に巧みである。"
        "（就寝前、「常」と錯覚した瞬間を一つ認め、有為·無常として見る。）"
    ),
    "MN33-P08": (
        "愚者は業によって相づけられ、智者は業によって相づけられる。"
        "（過去の成功·失敗も業の相——十一法増長の教訓として見る。）"
    ),
    "MN33-P09": (
        "比丘は、いかに煙を上げるか。"
        "自ら学び憶持したとおりに、法を他者に詳しく説く——"
        "このように煙を上げる。"
        "道とは、聖なる八支道である。"
        "（天界·楽より、八正道·解脱の法を語る。）"
    ),
    "MN33-P10": (
        "十一の法を具した比丘は、法·律において増長·広大·円熟を得る——"
        "色·相·蛆·瘡·煙·渡し場·満足·道·牧場·節度·長老への慈。"
        "道とは八正道、牧場とは四念処である。"
    ),
    "MN33-P11": (
        "十一の法を具すれば、この法·律において増長·広大·円熟を得る。"
        "……乳を搾り尽くさず（受用に節度あり）、"
        "長老·僧伽の父たる者に、身口意の慈を行う。"
        "（帰依の対象は有漏の楽ではなく、法·律の円熟·解脱かと問う。）"
    ),
}

OBSERVE = {
    "MN33-P01": (
        "牧牛十一法——欠ければ法·律に増長できない。"
        "（旧「梵天無常」はDN19混入。今朝は十一法の一つを無常·有為の視点で思い出す。）"
        "朝、今日「梵天界も無常」と一度思い出す。"
    ),
    "MN33-P02": (
        "色を知る——一切色は四大·四大造。快い経験も色として無常。"
        "今日、快い経験·成功を「無常」と一度見る。"
    ),
    "MN33-P03": (
        "道を知る——聖八正道。真の法として一支を歩む。"
        "今日、八正道のうち一つを「真の法」として歩む。"
    ),
    "MN33-P04": (
        "蛆を除く——欲·瞋·害尋を忍ばず滅する。天界願いも欲尋かと問う。"
        "今日、願いが「天界·楽」で「解脱」でないか問う。"
    ),
    "MN33-P05": (
        "十一法で法·律に円熟——施·戒·定もこの増長の中で解脱を目指す。"
        "今日、施·戒·禅を修しつつ、解脱を目指す。"
    ),
    "MN33-P06": (
        "色·相——楽も苦も有為。無常として一度見る。"
        "今日の楽·苦を「無常」と一度見る。"
    ),
    "MN33-P07": (
        "相に巧み——業が愚·智を相づける。夜、「常」の錯覚を一つ認め無常を見る。"
        "就寝前、今日「常」と錯覚した瞬間を一つ認め、無常を見る。"
    ),
    "MN33-P08": (
        "過去の成功·失敗は業の相——十一法増長の教訓。"
        "今日、過去の成功·失敗を「無常の教訓」として見る。"
    ),
    "MN33-P09": (
        "煙を上げる——学んだ法を説く。道＝八正道を語る。"
        "今日、天界·楽より八正道·解脱を語る。"
    ),
    "MN33-P10": (
        "牧牛者大経の教え——十一法·八正道·四念処。"
        "今日、牧牛者大経の教え（無常·八正道）を一つ思い出す。"
    ),
    "MN33-P11": (
        "法·律の円熟·解脱が帰依。受用の節度と長老への慈。"
        "今日、帰依の対象が「解脱」か一度問う。"
    ),
}

PRACTICE = {
    "MN33-P01": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "朝、十一法·有為無常に触れて一度思い出す",
        "section": "十一法·導入",
        "category": "mindfulness",
    },
    "MN33-P02": {
        "nidanaId": "feeling",
        "pathFactors": ["正見", "正念"],
        "reason": "快い受を色·無常として見る",
        "section": "色を知る",
        "category": "view",
    },
    "MN33-P03": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正精進"],
        "reason": "八正道の一支を真の法として歩み離す",
        "section": "道を知る",
        "category": "view",
    },
    "MN33-P04": {
        "nidanaId": "craving",
        "pathFactors": ["正思惟", "正精進"],
        "reason": "欲尋·天界願いを蛆として除くか問う",
        "section": "蛆を除く",
        "category": "intention",
    },
    "MN33-P05": {
        "nidanaId": "clinging",
        "pathFactors": ["正精進", "正見"],
        "reason": "下位の成果に掴まず、十一法で解脱·円熟を目指す",
        "section": "十一法で円熟",
        "category": "effort",
    },
    "MN33-P06": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正念"],
        "reason": "楽·苦を有為·無常として苦の視点で見る",
        "section": "色·楽苦",
        "category": "view",
    },
    "MN33-P07": {
        "nidanaId": "review",
        "pathFactors": ["正見", "正念"],
        "reason": "夜、「常」の錯覚を認め無常を見る",
        "section": "夜·相に巧み",
        "category": "view",
    },
    "MN33-P08": {
        "nidanaId": "suffering",
        "pathFactors": ["正見", "正思惟"],
        "reason": "過去の成敗を業の相·教訓として見る",
        "section": "業の相",
        "category": "view",
    },
    "MN33-P09": {
        "nidanaId": "contact",
        "pathFactors": ["正語", "正見"],
        "reason": "法に触れ、八正道·解脱を語る（煙）",
        "section": "煙を上げる",
        "category": "speech",
    },
    "MN33-P10": {
        "nidanaId": "contact",
        "pathFactors": ["正念", "正見"],
        "reason": "十一法·八正道の教えに触れ一つ思い出す",
        "section": "導·十一法を憶う",
        "category": "mindfulness",
    },
    "MN33-P11": {
        "nidanaId": "release",
        "pathFactors": ["正見", "正命"],
        "reason": "有漏の楽への帰依を離れ、解脱·円熟か問う",
        "section": "円熟·節度·慈",
        "category": "view",
    },
}

CHINESE = {
    "MN33-P01": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-eleven",
        "text": "比丘成就十一法者，不能自安，亦不安他。何等為十一？謂不知色、不知相……。",
        "satLocus": "大正蔵 T2.342c 牧牛者",
        "note": "十一法欠ければ自他を安んじられない。中阿含無相当（EA49.1等も類縁）。",
    },
    "MN33-P02": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-form",
        "text": "云何不知色？諸所有色，彼一切四大，及四大造，是名為色不如實知。",
        "satLocus": "大正蔵 T2.342c 牧牛者",
        "note": "色＝四大·四大造。",
    },
    "MN33-P03": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-path",
        "text": "云何不知正道？八正道及聖法、律是名為道，彼不如實知，是名不知道。",
        "satLocus": "大正蔵 T2.343a 牧牛者",
        "note": "正道＝八正道。",
    },
    "MN33-P04": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-eggs",
        "text": "云何名不知去蟲？所起欲覺能安，不離、不覺、不滅，所起瞋恚、害覺能安……是名不去蟲。",
        "satLocus": "大正蔵 T2.342c–343a 牧牛者",
        "note": "去蟲＝欲·瞋·害覚を滅する（パーリの蛆）。",
    },
    "MN33-P05": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-growth",
        "text": "（十一法を成就すれば自他を安んじ、法·律に増長する——逆の十一法の対。）",
        "satLocus": "大正蔵 T2.342c–343a 牧牛者",
        "note": "十一法成就＝増長。",
    },
    "MN33-P06": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-anicca",
        "text": "諸所有色，彼一切四大，及四大造……。事業是過相，事業是慧相。",
        "satLocus": "大正蔵 T2.342c 牧牛者",
        "note": "色·業相——楽苦を有為として見る根拠。",
    },
    "MN33-P07": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-lakkhaṇa",
        "text": "云何不知相？事業是過相，事業是慧相，是不如實知，是名不知相。",
        "satLocus": "大正蔵 T2.342c 牧牛者",
        "note": "相＝業による過·慧の相。",
    },
    "MN33-P08": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-kamma",
        "text": "事業是過相，事業是慧相。",
        "satLocus": "大正蔵 T2.342c 牧牛者",
        "note": "過去の成敗＝業の相の教訓。",
    },
    "MN33-P09": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-smoke",
        "text": "云何不起烟？如所聞，如所受法，不能為人分別顯示，是名不起烟。……八正道及聖法、律是名為道。",
        "satLocus": "大正蔵 T2.343a 牧牛者",
        "note": "起烟＝所聞法を分別顯示。",
    },
    "MN33-P10": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-recall",
        "text": "何等為十一？謂不知色、不知相……不知正路……不知放牧處……。放牧處謂四念處。",
        "satLocus": "大正蔵 T2.342c–343a 牧牛者",
        "note": "十一法·八正道·四念処。",
    },
    "MN33-P11": {
        "status": "mapped",
        "pin": "雑阿含1249・牧牛者（T99）",
        "t26": "SA1249-maturity",
        "text": "彼比丘受者不知限量，是名盡搾其乳。……不善料理能領群者。",
        "satLocus": "大正蔵 T2.343a 牧牛者",
        "note": "節度·領群——円熟·解脱への帰依と対応。",
    },
}


def chinese_block(pid):
    c = dict(CHINESE[pid])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault(
            "note",
            "パーリ中部33経の対応は雑阿含1249牧牛者（EA49.1等も類縁）。對照表: 法雨道場。",
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
    old_path = DATA / "majjhima" / "mn033.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    actions = {p["id"]: p["action"] for p in old["pairs"]}
    assert set(actions) == set(QUOTES), (set(actions) ^ set(QUOTES))

    pairs = []
    for i in range(1, 12):
        pid = f"MN33-P{i:02d}"
        pr = PRACTICE[pid]
        pairs.append({
            "id": pid,
            "category": pr["category"],
            "ref": "MN 33",
            "section": pr["section"],
            "observe": OBSERVE[pid],
            "action": actions[pid],
            "quote": QUOTES[pid],
            "nidanaId": pr["nidanaId"],
            "pathFactors": pr["pathFactors"],
            "pathReason": pr["reason"],
            "alignment": {
                "pali": {
                    "source": "アラナ精舎 経典ライブラリー（中部・牧牛者の大経／パーリMN33）",
                    "locus": f"中部・牧牛者の大経（MN33）·{pr['section']}",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": "第９巻 中部経典一 · 牧牛者大経（南伝公開目次）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(pid),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "中部 第33経・牧牛者大経（牧牛者の大経）"
    SHORT = "牧牛者大経（牧牛者の大経）"
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
            "pathFactors": ["正念", "正語"], "pathFactorIds": ["mindfulness", "speech"],
            "pathLabel": "十一法·八正道に触れ、法を語る",
            "chapterHint": SHORT,
            "fromPrev": "見直しが、今朝の十一法の一歩を変える",
            "toNext": "触のあと、快い受が見える",
            "todayObserve": OBSERVE["MN33-P01"],
            "todayAction": actions["MN33-P01"],
            "when": ["十一法を思い出した", "法を語った"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES["MN33-P01"][:40] + "…",
            "secondaryObserve": OBSERVE["MN33-P10"],
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "view", "nidanaLabel": "受ける",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "快い受を色·無常として見る",
            "chapterHint": SHORT,
            "fromPrev": "接触のあと、快·成功の受が立つ",
            "toNext": "受に乗ると欲尋·天界の欲しがりへ",
            "todayObserve": OBSERVE["MN33-P02"],
            "todayAction": actions["MN33-P02"],
            "when": ["快を無常と見た"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES["MN33-P02"][:40] + "…",
            "secondaryObserve": "色＝四大",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "intention", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正思惟", "正精進"], "pathFactorIds": ["intention", "effort"],
            "pathLabel": "欲尋·天界願いを蛆として除く",
            "chapterHint": SHORT,
            "fromPrev": "受のあと、欲·天界の欲しがりが立つ",
            "toNext": "止めないと下位成果への掴みへ",
            "todayObserve": OBSERVE["MN33-P04"],
            "todayAction": actions["MN33-P04"],
            "when": ["願いを問うた", "欲尋を除いた"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES["MN33-P04"][:40] + "…",
            "secondaryObserve": "去蟲",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "effort", "nidanaLabel": "掴む",
            "pathFactors": ["正精進", "正見"], "pathFactorIds": ["effort", "view"],
            "pathLabel": "下位の成果に掴まず、十一法で円熟を目指す",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりのあと、施戒禅だけの掴みが手前",
            "toNext": "掴むと楽苦の苦が見える",
            "todayObserve": OBSERVE["MN33-P05"],
            "todayAction": actions["MN33-P05"],
            "when": ["解脱を目指して修した"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES["MN33-P05"][:40] + "…",
            "secondaryObserve": "十一法で円熟",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "楽·苦·過去の成敗を有為·業の相として見る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、楽苦の患が見える",
            "toNext": "見れば、八正道·解脱へ離す",
            "todayObserve": OBSERVE["MN33-P06"],
            "todayAction": actions["MN33-P06"],
            "when": ["楽苦を無常と見た", "過去を教訓と見た"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES["MN33-P06"][:40] + "…",
            "secondaryObserve": OBSERVE["MN33-P08"],
        },
        {
            "id": "release", "weekday": 6, "categoryId": "view", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正見", "正精進"], "pathFactorIds": ["view", "effort"],
            "pathLabel": "八正道を歩み、有漏の帰依を離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、真の法として道を歩む",
            "toNext": "離せば、夜の無常の見直しへ",
            "todayObserve": OBSERVE["MN33-P03"],
            "todayAction": actions["MN33-P03"],
            "when": ["八正道の一支を歩んだ", "帰依を問うた"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES["MN33-P03"][:40] + "…",
            "secondaryObserve": OBSERVE["MN33-P11"],
        },
        {
            "id": "review", "weekday": 0, "categoryId": "view", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "「常」の錯覚を認め、業の相·無常を見る",
            "chapterHint": SHORT,
            "fromPrev": "一日の離しは、朝からの十一法の跡",
            "toNext": "見直しが、翌朝の接触の土台になる",
            "todayObserve": OBSERVE["MN33-P07"],
            "todayAction": actions["MN33-P07"],
            "when": ["一日を閉じるとき"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES["MN33-P07"][:40] + "…",
            "secondaryObserve": "事業是相",
        },
    ]

    out = {
        "chapter": 33,
        "sutta": 33,
        "title": TITLE,
        "shortTitle": SHORT,
        "mapNote": "根本五十経篇 · 双大品（アラナ：牧牛者の大経）",
        "suttas": ["MN 33 牧牛者大経（牧牛者の大経）"],
        "source": {
            "primary": "パーリ・中部第33経（牧牛者大経／牧牛者の大経）観察ペア単位対応",
            "note": (
                "経典の言葉＝パーリMN33（アラナ精舎系和訳表記）、現代語訳＝南伝大蔵経系の読みやすい現代語表記"
                "（true-buddhismが南伝大蔵経を公開）、対応漢訳＝SAT雑阿含1249牧牛者（T99；EA49.1等も類縁）。"
                "牧牛十一法で法·律に増長する。旧スタブのマハーゴービンダ·梵天説はDN19の混入であり本経ではない。"
            ),
            "verifyLinks": {
                "pali": {
                    "label": "アラナ精舎（中部・牧牛者の大経）",
                    "url": ARANA_URL,
                    "note": "パーリ和訳出典（キャッシュ外の場合はパーリ忠実なアラナ調和訳）",
                },
                "modern": {
                    "label": "true-buddhism（南伝大蔵経・第9巻中部経典一）",
                    "url": TB_URL,
                    "note": "南伝大蔵経系の現代語表記（中部は巻目次で公開）",
                },
                "chinese": {
                    "label": "SAT 雑阿含・牧牛者（T2.342c）",
                    "url": SAT_URL,
                    "note": "十一法·四大·去蟲·八正道·四念処。對照表: 法雨道場（SA1249）",
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
            "focusReason": "牧牛者大経は蛆（不善尋）を除き、八正道を歩み、十一法で法·律に円熟するのが主題。既定の焦点は離す。表示は現在のペアの縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
    }

    old_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote mn033.json", len(pairs))

    idx_path = DATA / "majjhima" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    for ch in idx["chapters"]:
        if ch["id"] == 33:
            ch["title"] = TITLE
            ch["shortTitle"] = SHORT
            ch["mapNote"] = out["mapNote"]
            ch["pairCount"] = len(pairs)
            break
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated majjhima/index.json")

    scope = rebuild_path_scene_for_mn(33, SHORT, TITLE, pairs)
    print("path-scene-index", scope)

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 11
    assert all(p["id"] == f"MN33-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert all(p["action"] == actions[p["id"]] for p in pairs)
    for p in pairs:
        for lab in p["pathFactors"]:
            assert lab in LABEL_TO_ID, (p["id"], lab)
    mapped = sum(1 for p in pairs if p["alignment"]["chinese"]["status"] == "mapped")
    missing = valid - set(by_nidana)
    assert not missing, missing
    # effort is eightfold id - used as focusNodeId; valid nidanas don't include effort
    print(f"OK chinese mapped {mapped}/11; nidanas", dict(sorted((k, v) for k, v in by_nidana.items())))


if __name__ == "__main__":
    main()
