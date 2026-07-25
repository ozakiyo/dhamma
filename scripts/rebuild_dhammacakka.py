#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build data/dhammacakka/ — 初転法輪 as a standalone collection (like Dhammapada).

Spine (SN 56.11 全文寄り):
  開経 → 二辺·中道 → 苦·集·滅·道 → 示·勧·証（各×四諦） → 正覚宣言 → 法輪転起
Origin track (初転のみ): 苦諦→集諦→滅諦→道諦
Path track: 八正道（道諦の中身）
Source: SN 56.11 / アラナ · true-buddhism · 雑阿含379（SAT）
Pair text: scripts/dhammacakka_chapters.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dhammacakka"
CHAPTERS_JSON = Path(__file__).with_name("dhammacakka_chapters.json")

ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E7%9B%B8%E5%BF%9C%E9%83%A8%E7%B5%8C%E5%85%B8"
)
TB_URL = "https://true-buddhism.com/sutra/palisanzo/"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0099_%2C02%2C0103c13"
MAP_URL = "https://dhammarain.github.io/canon/sutta/S-vs-SA-dhammarain.pdf"

CATEGORIES = [
    {"id": "dukkha", "name": "苦諦", "short": "苦", "weekday": 1, "order": 1},
    {"id": "samudaya", "name": "集諦", "short": "集", "weekday": 2, "order": 2},
    {"id": "nirodha", "name": "滅諦", "short": "滅", "weekday": 3, "order": 3},
    {"id": "magga", "name": "道諦", "short": "道", "weekday": 4, "order": 4},
]

# 初転法輪専用：縁起トラック＝四聖諦の流れ（触→受→欲…ではない）
ORIGIN_NODES = [
    {"id": "dukkha", "label": "苦諦"},
    {"id": "samudaya", "label": "集諦"},
    {"id": "nirodha", "label": "滅諦"},
    {"id": "magga", "label": "道諦"},
]

PATH_FACTORS_META = [
    {"id": "view", "label": "正見"}, {"id": "intention", "label": "正思惟"},
    {"id": "speech", "label": "正語"}, {"id": "action", "label": "正業"},
    {"id": "livelihood", "label": "正命"}, {"id": "effort", "label": "正精進"},
    {"id": "mindfulness", "label": "正念"}, {"id": "concentration", "label": "正定"},
]

LABEL_TO_ID = {m["label"]: m["id"] for m in PATH_FACTORS_META}
ALL_EIGHT = [m["label"] for m in PATH_FACTORS_META]

CHAPTERS = json.loads(CHAPTERS_JSON.read_text(encoding="utf-8"))

def source_block():
    return {
        "primary": "パーリ・相応部 SN 56.11（転法輪経／法輪転起経）観察ペア単位対応",
        "note": (
            "経典の言葉＝パーリSN56.11（アラナ精舎系和訳表記）、"
            "現代語訳＝南伝大蔵経系の読みやすい現代語表記（true-buddhismが南伝大蔵経を公開）、"
            "対応漢訳＝雑阿含379転法輪（T99）。"
            "初転法輪——開経·二辺·中道·四諦·示勧証（十二行相）·正覚宣言·法輪転起（SN56.11全文寄り）。"
            "縁起トラックは四聖諦（苦→集→滅→道）。八正道は道諦の中身。"
        ),
        "verifyLinks": {
            "pali": {
                "label": "アラナ精舎（相応部・転法輪／法輪転起）",
                "url": ARANA_URL,
                "note": "パーリ和訳出典",
            },
            "modern": {
                "label": "true-buddhism（南伝大蔵経・相応部）",
                "url": TB_URL,
                "note": "南伝大蔵経系の現代語表記",
            },
            "chinese": {
                "label": "SAT 雑阿含・転法輪（T2.103c）",
                "url": SAT_URL,
                "note": "對照: 雑阿含379（類縁T109等）",
            },
        },
        "chineseMapTable": MAP_URL,
    }


def alignment_for(pair):
    c = dict(pair["chinese"])
    c.setdefault("satUrl", SAT_URL)
    c["mapTableUrl"] = MAP_URL
    c.setdefault("t26", "")
    return {
        "pali": {
            "source": "アラナ精舎 経典ライブラリー（相応部・転法輪経／パーリSN56.11）",
            "locus": f"相応部・転法輪経（SN56.11）·{pair['section']}",
            "url": ARANA_URL,
        },
        "modern": {
            "source": "true-buddhism（南伝大蔵経系・現代語表記）",
            "locus": "相応部 · 諦相応 · 転法輪経（南伝公開目次）",
            "url": TB_URL,
        },
        "chinese": c,
    }


def pf_ids(labels):
    return [LABEL_TO_ID[l] for l in labels if l in LABEL_TO_ID]


def _first_for(pairs, nidana, field, default=""):
    for p in pairs:
        if p["nidanaId"] == nidana:
            return p[field]
    return default


def practice_nodes(pairs, short):
    """四諦ノード。pair.nidanaId と一致させる。"""
    by_nidana = {}
    for p in pairs:
        by_nidana.setdefault(p["nidanaId"], []).append(p["id"])
    lead = pairs[0]

    specs = [
        {
            "id": "dukkha",
            "weekday": 1,
            "categoryId": "dukkha",
            "nidanaLabel": "苦聖諦",
            "pathFactors": ["正見", "正念"],
            "pathLabel": "苦を苦として見る",
            "pathReason": "今日の苦を、苦聖諦の一側面として認める",
            "fromPrev": "道を修したあと、再び苦が見える",
            "toNext": "苦が見えれば、集（渇愛）へ問う",
            "when": ["苦を認めた"],
            "fallbackObserve": "苦を苦として一度認める",
            "fallbackAction": "今日の苦を一つ特定して観る",
        },
        {
            "id": "samudaya",
            "weekday": 2,
            "categoryId": "samudaya",
            "nidanaLabel": "苦集聖諦",
            "pathFactors": ["正思惟", "正念"],
            "pathLabel": "渇愛を集として名づける",
            "pathReason": "欲しがりを、苦の集起として見る",
            "fromPrev": "苦のあと、集（渇愛）が手前に立つ",
            "toNext": "集を見れば、滅（離欲）へ向かう",
            "when": ["渇愛を名づけた"],
            "fallbackObserve": "渇愛を集と見る",
            "fallbackAction": "今日の欲しがりを一つ名づける",
        },
        {
            "id": "nirodha",
            "weekday": 3,
            "categoryId": "nirodha",
            "nidanaLabel": "苦滅聖諦",
            "pathFactors": ["正見", "正念"],
            "pathLabel": "渇愛を離欲し、滅へ向かう",
            "pathReason": "掴みを手放す方向へ意図を戻す",
            "fromPrev": "集が見えれば、離欲へ戻る",
            "toNext": "離せば、道（八正道）を修する",
            "when": ["離欲した"],
            "fallbackObserve": "渇愛を離欲する",
            "fallbackAction": "小さな欲しがりを一つ手放す",
        },
        {
            "id": "magga",
            "weekday": 4,
            "categoryId": "magga",
            "nidanaLabel": "苦滅道跡聖諦",
            "pathFactors": ["正見", "正念"],
            "pathLabel": "八正道を道として修する",
            "pathReason": "中道＝八支聖道を、苦滅への道跡として歩む",
            "fromPrev": "滅の方向が見えれば、道を修する",
            "toNext": "道を修したあと、再び苦を見直す",
            "when": ["道を修した"],
            "fallbackObserve": "八正道の一支に触れる",
            "fallbackAction": "一支を今日の行為に結びつける",
        },
    ]

    nodes = []
    for spec in specs:
        nid = spec["id"]
        factors = spec["pathFactors"]
        # Prefer factors from a pair on this node when present
        pair_factors = _first_for(pairs, nid, "pathFactors", factors)
        if pair_factors:
            factors = pair_factors[:3] if len(pair_factors) > 3 and nid != "magga" else (
                pair_factors if len(pair_factors) <= 3 else ["正見", "正念"]
            )
            # For magga with all eight, keep 正見·正念 as node highlight default
            if len(pair_factors) > 3:
                factors = ["正見", "正念"]
        observe = _first_for(pairs, nid, "observe", spec["fallbackObserve"])
        action = _first_for(pairs, nid, "action", spec["fallbackAction"] or lead["action"])
        quote = _first_for(pairs, nid, "quote", lead["quote"])
        nodes.append({
            "id": nid,
            "weekday": spec["weekday"],
            "categoryId": spec["categoryId"],
            "nidanaLabel": spec["nidanaLabel"],
            "pathFactors": factors,
            "pathFactorIds": pf_ids(factors),
            "pathLabel": spec["pathLabel"],
            "pathReason": spec["pathReason"],
            "chapterHint": short,
            "fromPrev": spec["fromPrev"],
            "toNext": spec["toNext"],
            "todayObserve": observe,
            "todayAction": action,
            "when": spec["when"],
            "sources": by_nidana.get(nid, [lead["id"]] if nid == lead["nidanaId"] else []),
            "leadQuote": (quote[:48] + "…") if quote else "",
            "secondaryObserve": "",
        })
    return nodes


def write_chapter(ch):
    pairs_out = []
    for p in ch["pairs"]:
        pairs_out.append({
            "id": p["id"],
            "category": p["category"],
            "ref": "SN 56.11",
            "section": p["section"],
            "observe": p["observe"],
            "action": p["action"],
            "quote": p["quote"],
            "nidanaId": p["nidanaId"],
            "pathFactors": p["pathFactors"],
            "pathReason": p["pathReason"],
            "alignment": alignment_for(p),
        })

    out = {
        "chapter": ch["id"],
        "sutta": 11,
        "title": ch["title"],
        "shortTitle": ch["shortTitle"],
        "mapNote": ch["mapNote"],
        "suttas": ["SN 56.11 転法輪経（法輪転起経）"],
        "source": source_block(),
        "categories": CATEGORIES,
        "practicePath": {
            "model": "four-noble-truths",
            "chapterTitle": ch["title"],
            "shortTitle": ch["shortTitle"],
            "spineOrigin": "苦諦を見た→集諦（渇愛）を見た→滅諦へ離した→道諦を修した",
            "spinePath": "四諦を通しで見る。八正道は道諦（中道）の中身",
            "originNodes": ORIGIN_NODES,
            "pathFactors": PATH_FACTORS_META,
            "nodes": practice_nodes(ch["pairs"], ch["shortTitle"]),
            "focusNodeId": ch["focusNodeId"],
            "focusReason": ch["focusReason"],
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs_out,
    }
    path = DATA / ch["file"]
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(pairs_out)


def update_path_scene(all_pairs_by_chapter):
    """Register 道諦 pairs under eightfold scene index where pathFactors apply."""
    psi_path = ROOT / "data" / "path-scene-index.json"
    psi = json.loads(psi_path.read_text(encoding="utf-8"))
    # remove old dhammacakka entries
    for pid, entries in list(psi.get("entries", {}).items()):
        psi["entries"][pid] = [
            e for e in entries if e.get("collectionId") != "dhammacakka"
        ]

    from collections import defaultdict
    by_path = defaultdict(list)
    titles = {}
    for ch_id, (short, title, pairs) in all_pairs_by_chapter.items():
        titles[ch_id] = (short, title)
        for p in pairs:
            for lab in p["pathFactors"]:
                by_path[(LABEL_TO_ID[lab], ch_id)].append(p["id"])

    for (path_id, ch_id), ids in by_path.items():
        short, title = titles[ch_id]
        ids = sorted(set(ids), key=lambda x: int(x.split("-P")[1]))
        psi["entries"].setdefault(path_id, []).append({
            "collectionId": "dhammacakka",
            "collectionName": "初転法輪",
            "chapterId": ch_id,
            "shortTitle": short,
            "title": title,
            "pairCount": len(ids),
            "pairIds": ids,
        })

    scope = psi.get("scope", "")
    if "dhammacakka" not in scope:
        psi["scope"] = (scope + "+dhammacakka-ch1-ch11") if scope else "dhammacakka-ch1-ch11"
    elif "dhammacakka-ch1-ch7" in scope:
        psi["scope"] = scope.replace("dhammacakka-ch1-ch7", "dhammacakka-ch1-ch11")
    psi_path.write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    index_chapters = []
    total = 0
    all_pairs = {}
    for ch in CHAPTERS:
        n = write_chapter(ch)
        total += n
        index_chapters.append({
            "id": ch["id"],
            "file": ch["file"],
            "title": ch["title"],
            "shortTitle": ch["shortTitle"],
            "pairCount": n,
            "mapNote": ch["mapNote"],
        })
        all_pairs[ch["id"]] = (ch["shortTitle"], ch["title"], ch["pairs"])
        print("wrote", ch["file"], n)

    index = {
        "title": "初転法輪（SN 56.11・転法輪経）",
        "source": "パーリ相応部 SN 56.11／雑阿含379",
        "totalPairs": total,
        "chapters": index_chapters,
    }
    (DATA / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote index.json", total, "pairs", len(index_chapters), "chapters")
    update_path_scene(all_pairs)
    print("updated path-scene-index.json")


if __name__ == "__main__":
    main()
