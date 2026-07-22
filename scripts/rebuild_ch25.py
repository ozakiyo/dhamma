#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch25.json (比丘品) to match ch1–ch24 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-25"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0571"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap25/"
)

QUOTES = {
    360: "眼（視覚機能）によって統御することは、善きことである。耳（聴覚機能）によって統御することは、善きことである。鼻（嗅覚機能）によって統御することは、善きことである。舌（味覚機能）によって統御することは、善きことである。",
    361: "身体（身）によって統御することは、善きことである。言葉（口・語）によって統御することは、善きことである。意（意）によって統御することは、善きことである。一切所において統御することは、善きことである。一切所において統御された比丘は、一切の苦しみから解き放たれる。",
    362: "手によって自制され、足によって自制され、言葉によって自制された、最上の自制者──内に喜び、〔心が〕定められた者──〔常に〕満ち足りている、独りある者──彼を、〔賢者たちは〕「比丘」と言う。",
    363: "彼が、口によって自制された比丘として、明慧によって話し、〔心が〕高揚せず、義（道理）を〔明らかにし〕、かつまた、法（真理）を明らかにするなら、彼の語るところは、〔蜜のように〕甘美である。",
    364: "法（教え）を喜びとし、法（教え）を喜び、法（教え）を〔常に〕弁別し、法（教え）を〔常に〕随念している比丘は、正なる法（教え）から遍く衰退しない。",
    365: "自らの利得（行乞で得た施物）を軽んじないように。他者たち〔の利得〕を羨む者として歩まないように。他者たち〔の利得〕を羨んでいる比丘は、禅定（定・三昧）に到達しない。",
    366: "たとえ、もし、〔得られた〕利得が僅かであるも、比丘が、自らの利得を軽んじないなら、休むことなく〔励み〕清浄の生き方ある、その〔比丘〕を、まさに、天〔の神々〕たちは賞賛する。",
    367: "彼に、全てにあまねく、名前と色形（名色：心的作用と肉体）について、わがものと〔錯視〕されたもの（執着の対象）が存在しないなら、そして、〔彼は〕所有するものがないので、〔もはや〕憂い悲しまず、彼は、まさに、「比丘」と説かれる。",
    368: "すなわち、慈愛の住者たる比丘は、覚者の教えに浄信ある〔比丘〕は、寂静の境処に到達するであろう──形成〔作用〕（行：生の輪廻を施設し造作する働き）の寂止という安楽〔の境地〕に。",
    369: "比丘よ、この舟〔の水〕を汲み出せ。あなたが〔水を〕汲み出したなら、〔舟は〕軽やかに行くであろう。そして、貪欲を断ち切って、さらに、憤怒を〔断ち切って〕、そののち、〔あなたは〕涅槃に行くであろう。",
    370: "五つ〔の束縛するもの〕（人を欲界に束縛する五つの煩悩、有身見・疑・戒禁取・欲貪・瞋恚）を断つべきである。五つ〔の束縛するもの〕（修行者を色界と無色界に束縛する五つの煩悩、色貪・無色貪・慢・掉挙・無明）を捨棄するべきである。そして、五つ〔の機能〕（信根・精進根・念根・定根・慧根）をより以上に修めるべきである。五つの執着（貪・瞋・痴・慢・見）を超え行く比丘は、「激流を超え渡った者」と説かれる。",
    371: "比丘よ、瞑想せよ。〔気づきを〕怠ること（放逸）があってはならない。欲望の属性（妙欲）に、あなたの心を喜ばせることがあってはならない。怠る者となり、銅の玉を飲み込んではならない。〔欲の炎に〕焼かれながら、「これは、苦しみだ」と泣き叫んではならない。",
    372: "智慧なき者に、瞑想（禅・静慮：禅定の境地）は存在しない。瞑想なき者に、智慧は存在しない。彼において、かつまた、瞑想があり、かつまた、智慧があるなら、彼は、まさに、涅槃の現前にある。",
    373: "〔人のいない〕空家に入り、心が寂静となった比丘が、正しく法（事象）を観察していると、人間ならざる喜びが有る（世俗の喜びを超えた喜びが生起する）。",
    374: "〔五つの心身を構成する〕範疇（蘊）の生成と衰失を〔時々刻々に〕触知する、そのたびごとに、〔自己と世界をあるがままに〕識知している者たちの、〔まさに〕その、不死なる喜悦と歓喜を、〔彼は〕得る。",
    375: "そこで、このことは、ここに、智慧ある比丘にとって、最初〔に為すべきこと〕と成る──〔感官の〕機能（根）を守ることであり、〔足ることを知り〕満ち足りていることであり、そして、戒条（波羅提木叉：戒律条項）において統御することである。",
    376: "休むことなく〔励み〕清浄の生き方ある、善き朋友たちと親しくせよ。友愛の生活ある者として存し、〔正しい〕行ないに巧みな智ある者として存するなら、そののち、歓喜多き者となり、苦しみの終極を為すであろう。",
    377: "ヴァッシカー（ジャスミン）が、萎れた花々を解き放つ（落とす）ように、比丘たちよ、このように、そして、貪欲を、さらに、憤怒を、解き放つのだ。",
    378: "身体が寂静で、言葉が寂静で、〔心が〕善く定められた寂静なる者──世の財貨を吐き捨てた比丘は、「寂静者」と説かれる。",
    379: "自己によって自己を叱咤せよ。自己によって〔自己を〕反省せよ。比丘よ、〔まさに〕その〔あなた〕は、自己が守られた、気づきある者となり、安楽に住むであろう。",
    380: "まさに、自己は、自己の主（あるじ）。まさに、他の誰が、主として存するというのだろう。まさに、自己は、自己の赴く所。それゆえに、自己を自制せよ──商人が、賢馬を〔調御する〕ように。",
    381: "歓喜多き比丘は、覚者の教えに浄信ある〔比丘〕は、寂静の境処に到達するであろう──形成〔作用〕の寂止という安楽〔の境地〕に。",
    382: "彼が、まさに、青年でありながら、比丘として、覚者の教えに専念するなら、彼は、雲から解き放たれた月のように、この世を照らす。",
}

OBSERVE = {
    360: "眼を制するは善し。 耳を制するは善し。 鼻を制するは善し。 舌を制するは善し。",
    361: "身を制するは善し。 語を制するは善し。 意を制するは善し。 一切に於て制するは善し。 一切に於て制したる比丘は一切の苦より脱す。",
    362: "手を慎み、足を慎み、語を慎み、最もよく慎み、内心に喜び、三昧に住し、独居して満足する者、これを比丘と称す。",
    363: "口を慎み、語る所賢明に、寂静にして正理と正法とを明らかにする比丘は、その説く所甘美なり。",
    364: "法を楽園とし、法を楽しみ、法に随って思惟し、法を憶念する比丘は、正法より退堕することなし。",
    365: "自己の所得を軽んずべからず。 他を羨むべからず。 他を羨む比丘は三昧に入ることなし。",
    366: "たとい得る所少しといえども、比丘もし自己の所得を軽んぜざれば、諸天も実に、〔この〕生活清浄にして懈怠なき者を称讃す。",
    367: "名色に於て全く我執なく、かつ〔その〕非有の故に憂えざる者は、実に比丘と称せらる。",
    368: "慈悲に住し、仏陀の教えを信ずる比丘は、寂静にして諸行静止せる安楽境に至るべし。",
    369: "比丘よ、この舟〔の水〕（身中の邪念）を汲み出せ、〔水〕汲み出されなば、〔舟は〕汝の為に疾く進まん。 貪欲と瞋恚とを断たば汝は涅槃に至らん。",
    370: "五を断つべし、五を捨つべし、而してよく五を勤修すべし。 五著を超越せる比丘は、瀑流（煩悩）を渡れる者と称せらる。",
    371: "比丘よ、禅定を修せよ。 放逸なるなかれ。 汝の心を愛欲に迷い行かしむることなかれ。 放逸にして〔熱〕鉄丸を呑むなかれ。 焼かれつつ「こは苦なり」と叫ぶことなかれ。",
    372: "智慧なき者に禅定なく、禅定なき者に智慧なし。 禅定と智慧とを備えたる者は、実に涅槃に近づけるなり。",
    373: "空屋（閑寂処）に入りて心寂静に、正しく法を観ずる比丘は、人界になき楽を受く。",
    374: "人もし諸蘊の生滅を思念すれば、忽ち、不死（涅槃）を知得せし人の歓喜と悦楽とを獲得す。",
    375: "こは現世に於て、智慧ある比丘の最初に〔為すべきこと〕なり。 〔すなわち〕諸根を摂護し、満足し、戒律に従いて制御し、生活清浄にして倦むことなき良友と交われ。",
    376: "好誼を尽くすべし、善行を全うすべし。 これによりて悦楽多く、苦を滅尽するに至らん。",
    377: "ヴァッシカー草が萎みし花を振るい落とすが如く、比丘らよ、貪欲と瞋恚とを捨てよ。",
    378: "身を静め、語を静め、寂静にしてよく三昧に住し、世俗の快楽を捨棄せる比丘は、寂静者と称せらる。",
    379: "自ら自己を励まし、自ら自己を省察すべし。 自ら摂護し、正念を持せば、比丘よ、汝は安楽に住せん。",
    380: "実に自己は自己の主にして、自己は自己の依所なり。 故に自己を制御せよ、あたかも商賈の良馬を〔調御する〕如く。",
    381: "悦楽多く、仏陀の教えを信ずる比丘は、寂静にして諸行静止せる安楽境に至るべし。",
    382: "たとい年少なりといえども、仏陀の教えに精勤する比丘は、雲を離れし月の如くこの世を照らす。",
}

PIN34 = "沙門品（T210 第34品）"
NOTE = "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。"

CHINESE = {
    360: {"status": "mapped", "pin": PIN34, "t210": "T210-34-001",
          "text": "端目耳鼻口，身意常守正，比丘行如是，可以免眾苦。", "satLocus": "大正蔵 T4.571c 沙門品第1頌",
          "note": "T210では360–361を一頌に併記（蘇錦坤對照表）。"},
    361: {"status": "mapped", "pin": PIN34, "t210": "T210-34-001",
          "text": "端目耳鼻口，身意常守正，比丘行如是，可以免眾苦。", "satLocus": "大正蔵 T4.571c 沙門品第1頌",
          "note": "T210では360–361を一頌に併記（蘇錦坤對照表）。"},
    362: {"status": "mapped", "pin": PIN34, "t210": "T210-34-002",
          "text": "手足莫妄犯，節言慎所行，常內樂定意，守一行寂然。", "satLocus": "大正蔵 T4.571c 沙門品第2頌"},
    363: {"status": "mapped", "pin": PIN34, "t210": "T210-34-003",
          "text": "學當守口，寡言安徐，法義為定，言必柔軟。", "satLocus": "大正蔵 T4.571c 沙門品第3頌"},
    364: {"status": "mapped", "pin": PIN34, "t210": "T210-34-004",
          "text": "樂法欲法，思惟安法，比丘依法，正而不費。", "satLocus": "大正蔵 T4.571c 沙門品第4頌"},
    365: {"status": "mapped", "pin": PIN34, "t210": "T210-34-005",
          "text": "學無求利，無愛他行，比丘好他，不得定意。", "satLocus": "大正蔵 T4.571c 沙門品第5頌"},
    366: {"status": "mapped", "pin": PIN34, "t210": "T210-34-006",
          "text": "比丘少取，以得無積，天人所譽，生淨無穢。", "satLocus": "大正蔵 T4.571c 沙門品第6頌"},
    367: {"status": "mapped", "pin": PIN34, "t210": "T210-34-008",
          "text": "一切名色，非有莫惑，不近不憂，乃為比丘。", "satLocus": "大正蔵 T4.571c 沙門品第8頌"},
    368: {"status": "mapped", "pin": PIN34, "t210": "T210-34-007",
          "text": "比丘為慈，愛敬佛教，深入止觀，滅行乃安。", "satLocus": "大正蔵 T4.571c 沙門品第7頌"},
    369: {"status": "mapped", "pin": PIN34, "t210": "T210-34-009",
          "text": "比丘戽船，中虛則輕，除婬怒癡，是為泥洹。", "satLocus": "大正蔵 T4.571c 沙門品第9頌"},
    370: {"status": "mapped", "pin": PIN34, "t210": "T210-34-010",
          "text": "捨五斷五，思惟五根，能分別五，乃渡河淵。", "satLocus": "大正蔵 T4.571c 沙門品第10頌"},
    371: {"status": "mapped", "pin": PIN34, "t210": "T210-34-011",
          "text": "禪無放逸，莫為欲亂，不吞洋銅，自惱燋形。", "satLocus": "大正蔵 T4.572a 沙門品第11頌"},
    372: {"status": "mapped", "pin": PIN34, "t210": "T210-34-012",
          "text": "無禪不智，無智不禪，道從禪智，得至泥洹。", "satLocus": "大正蔵 T4.572a 沙門品第12頌"},
    373: {"status": "mapped", "pin": PIN34, "t210": "T210-34-013",
          "text": "當學入空，靜居止意，樂獨屏處，一心觀法。", "satLocus": "大正蔵 T4.572a 沙門品第13頌"},
    374: {"status": "mapped", "pin": PIN34, "t210": "T210-34-014",
          "text": "當制五陰，伏意如水，清淨和悅，為甘露味。", "satLocus": "大正蔵 T4.572a 沙門品第14頌"},
    375: {"status": "mapped", "pin": PIN34, "t210": "T210-34-015",
          "text": "不受所有，為慧比丘，攝根知足，戒律悉持。", "satLocus": "大正蔵 T4.572a 沙門品第15頌"},
    376: {"status": "mapped", "pin": PIN34, "t210": "T210-34-016",
          "text": "生當行淨，求善師友，智者成人，度苦致喜。", "satLocus": "大正蔵 T4.572a 沙門品第16頌"},
    377: {"status": "mapped", "pin": PIN34, "t210": "T210-34-017",
          "text": "如衛師華，熟知自墮，釋婬怒癡，生死自解。", "satLocus": "大正蔵 T4.572a 沙門品第17頌"},
    378: {"status": "mapped", "pin": PIN34, "t210": "T210-34-018",
          "text": "止身止言，心守玄默，比丘棄世，是為受寂。", "satLocus": "大正蔵 T4.572a 沙門品第18頌"},
    379: {"status": "mapped", "pin": PIN34, "t210": "T210-34-019",
          "text": "當自飾身，內與心爭，護身念諦，比丘惟安。", "satLocus": "大正蔵 T4.572a 沙門品第19頌"},
    380: {"status": "mapped", "pin": PIN34, "t210": "T210-34-020",
          "text": "我自為我，計無有我，故當損我，調乃為賢。", "satLocus": "大正蔵 T4.572a 沙門品第20頌"},
    381: {"status": "mapped", "pin": PIN34, "t210": "T210-34-021",
          "text": "喜在佛教，可以多喜，至到寂寞，行滅永安。", "satLocus": "大正蔵 T4.572a 沙門品第21頌"},
    382: {"status": "mapped", "pin": PIN34, "t210": "T210-34-022",
          "text": "儻有少行，應佛教誡，此照世間，如日無曀。", "satLocus": "大正蔵 T4.572a 沙門品第22頌"},
}

VERSE_PRACTICE = {
    360: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "眼耳鼻舌を制する接触から始める"},
    361: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "身語意を一切制すれば一切の苦より脱す"},
    362: {"nidanaId": "contact", "pathFactors": ["正念", "正定"], "reason": "自制・内心の喜び・独居満足が比丘との接触"},
    363: {"nidanaId": "feeling", "pathFactors": ["正語", "正念"], "reason": "慎みある語は甘美な受をもたらす"},
    364: {"nidanaId": "feeling", "pathFactors": ["正念", "正見"], "reason": "法を楽しみ憶念する受に住む"},
    365: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "他を羨む欲しがりは三昧に入れない"},
    366: {"nidanaId": "release", "pathFactors": ["正命", "正念"], "reason": "少くとも所得を軽んぜず清浄に離す"},
    367: {"nidanaId": "clinging", "pathFactors": ["正念", "正見"], "reason": "名色への我執という掴みを手放す"},
    368: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "慈悲と信で寂静の安楽境へ離す"},
    369: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "舟の水を汲み出し貪欲瞋恚を断つ"},
    370: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "五を断ち五を修し瀑流を渡る"},
    371: {"nidanaId": "craving", "pathFactors": ["正念", "正定"], "reason": "愛欲に迷い熱鉄丸を呑むな"},
    372: {"nidanaId": "contact", "pathFactors": ["正定", "正見"], "reason": "禅定と智慧の両輪に触れる"},
    373: {"nidanaId": "review", "pathFactors": ["正定", "正念"], "reason": "空屋で法を観じ、人界になき楽を見直す"},
    374: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "諸蘊の生滅を思念し不死の悦楽を見直す"},
    375: {"nidanaId": "contact", "pathFactors": ["正念", "正命"], "reason": "諸根・知足・戒という最初の接触"},
    376: {"nidanaId": "contact", "pathFactors": ["正念", "正語"], "reason": "良友・好誼・善行に触れて苦を滅尽す"},
    377: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "萎んだ花のように貪欲と瞋恚を振り落とす"},
    378: {"nidanaId": "feeling", "pathFactors": ["正念", "正定"], "reason": "身語心の寂静という受に住む"},
    379: {"nidanaId": "review", "pathFactors": ["正念", "正精進"], "reason": "自ら励まし省察し、安楽に住む"},
    380: {"nidanaId": "clinging", "pathFactors": ["正念", "正定"], "reason": "自己を主とし、良馬のように自制する"},
    381: {"nidanaId": "suffering", "pathFactors": ["正念", "正見"], "reason": "信の悦楽で諸行静止の安楽境へ──苦の終極"},
    382: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "精勤すれば雲を離れし月の如く世を照らす"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [(f"DP25-P{i:02d}", 359 + i) for i in range(1, 24)]


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault("note", NOTE)
    return c


def main():
    old = json.loads((DATA / "ch25.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 比丘の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第２５章・比丘品 第{verse}偈（#ch02-25）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第25章・比丘品（比丘の章）"
    SHORT = "比丘品（比丘の章）"
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
            "pathLabel": "諸根・戒・禅智・良友に触れ、比丘の一日を始める",
            "chapterHint": SHORT,
            "fromPrev": "前夜の省察が、今朝の諸根護持になる",
            "toNext": "接触のあと、法楽と語の受が立ち上がる",
            "todayObserve": OBSERVE[360],
            "todayAction": actions["DP25-P01"],
            "when": ["朝の始まり", "情報を制限する"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[360][:40] + "…",
            "secondaryObserve": "禅定と智慧とを備えたる者は、実に涅槃に近づけるなり",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "speech", "nidanaLabel": "受ける",
            "pathFactors": ["正語", "正念"], "pathFactorIds": ["speech", "mindfulness"],
            "pathLabel": "法楽と甘美な語、寂静の受を受け取る",
            "chapterHint": SHORT,
            "fromPrev": "護持に触れたあと、法と語の受が来る",
            "toNext": "受けた快を、羨みや愛欲への欲しがりへ落とさない",
            "todayObserve": OBSERVE[364],
            "todayAction": actions["DP25-P05"],
            "when": ["法を楽しむ", "言葉を発する前"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[364][:40] + "…",
            "secondaryObserve": "口を慎み、正理と正法とを明らかにする語は甘美なり",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "羨みと愛欲への欲しがりを緩め、禅定を守る",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、他への羨みや欲への欲しがりへ",
            "toNext": "止めないと我執・放逸の掴みへ進む",
            "todayObserve": OBSERVE[365],
            "todayAction": actions["DP25-P06"],
            "when": ["他と比較した", "誘惑が来た"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[365][:40] + "…",
            "secondaryObserve": "汝の心を愛欲に迷い行かしむることなかれ",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "名色への我執を掴まず、自己を主として自制する",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、我執・放逸として掴む手前",
            "toNext": "掴むと苦が太り、安楽境から遠ざかる",
            "todayObserve": OBSERVE[367],
            "todayAction": actions["DP25-P08"],
            "when": ["これは私のものだと思った", "自律を失いそう"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[367][:40] + "…",
            "secondaryObserve": "自己は自己の主なり。故に自己を制御せよ",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "mindfulness", "nidanaLabel": "苦が太る",
            "pathFactors": ["正念", "正見"], "pathFactorIds": ["mindfulness", "view"],
            "pathLabel": "信の悦楽で、諸行の苦を見据え安楽境へ向かう",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、放逸の苦が見える",
            "toNext": "見れば、制と慈悲の実践へ向き直る",
            "todayObserve": OBSERVE[381],
            "todayAction": actions["DP25-P22"],
            "when": ["苦境の中で足場を探す", "法を信ずる悦楽を思い起こす"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[381][:40] + "…",
            "secondaryObserve": "寂静にして諸行静止せる安楽境に至るべし",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "制し、汲み出し、五を断ち、花のように離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、舟の水を汲み出し離欲へ",
            "toNext": "離すと、空屋と諸蘊の夜の見直しへつながる",
            "todayObserve": OBSERVE[361],
            "todayAction": actions["DP25-P10"],
            "when": ["邪念を汲み出す", "貪欲と瞋恚を捨てる"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[361][:40] + "…",
            "secondaryObserve": "ヴァッシカー草が萎みし花を振るい落とすが如く、貪欲と瞋恚とを捨てよ",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "concentration", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "空屋で法を観じ、諸蘊の生滅と自己を省察する",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、制していたかの跡",
            "toNext": "見直しが、翌朝の諸根護持になる",
            "todayObserve": OBSERVE[373] + " " + OBSERVE[379],
            "todayAction": actions["DP25-P14"],
            "when": ["一日を閉じるとき", "自ら励まし省察する"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[373][:40] + "…",
            "secondaryObserve": "諸蘊の生滅を思念すれば、不死の歓喜と悦楽とを獲得す",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 25,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第25章（比丘品／比丘の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210沙門品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・比丘の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第２５章・比丘品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・沙門品（T4.571c）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusNodeId": "contact",
            "focusReason": "比丘品は諸根・戒・禅智への接触が実践の入口。既定の焦点は接触。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch25.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch25.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 26):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch25", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 23
    assert all(p["id"] == f"DP25-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(360, 383))
    assert all(p["alignment"]["chinese"]["status"] == "mapped" for p in pairs)
    assert set(by_nidana) == valid
    print("OK")


if __name__ == "__main__":
    main()
