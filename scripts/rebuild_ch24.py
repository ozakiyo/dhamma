#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch24.json (愛欲品) to match ch1–ch23 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-24"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0570"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap24/"
)

QUOTES = {
    334: "〔気づきを〕怠るままに歩む人間の、渇愛〔の思い〕は増え行く──蔓草が〔生い茂る〕ように。彼は、あの〔世〕からあの〔世〕へと浮きただよう（輪廻を繰り返す）──林のなかで果実を求めている猿のように。",
    335: "渇愛が、世における執着が、この卑しむべきものが、彼を打ち負かすなら、彼の、諸々の憂いは増え行く──雨を得たビーラナ〔草〕のように。",
    336: "しかしながら、渇愛を、世における超え難きものを、この卑しむべきものを、彼が打ち負かすなら、彼から、諸々の憂いは落ち行く──蓮〔の葉〕から、水の滴（しずく）が〔落ちる〕ように。",
    337: "〔わたしは〕それを、あなたたちに説く。あなたたちに、幸せ〔有れ〕──ここにおいて集いあつまった、そのかぎりの者たちは。渇愛の根を掘り崩せ──ウシーラ（ビーラナ草の根・香料として使う）〔の採取〕を義（目的）とする者が、ビーラナ〔草〕を〔掘る〕ように。あなたたちを、まさしく、流れが葦を〔打ちひしぐ〕ように、悪魔が、繰り返し、打ち砕くことがあってはならない。",
    338: "あたかも、また、根が無禍にして堅固であるなら、たとえ、切断された木でも、まさしく、ふたたび成長するように、このように、また、渇愛の悪習（随眠：潜在煩悩）が打破されていないなら、この苦しみは、繰り返し発現する。",
    339: "彼に、意に適うもの（欲望の対象）へと流れ行く、激しい三十六の流れがあるなら、貪欲〔の思い〕に依存した諸々の妄想が運び手となり、悪しき見解を運び来る。",
    340: "諸々の〔渇愛の〕流れは、一切所に流れ行く。〔貪欲の〕蔓草は、芽生えては止住する。そして、その蔓草が生じたのを見て、智慧によって、〔その〕根を断て。",
    341: "諸々の〔渇愛の〕流れがあり、かつまた、諸々の愛執〔の対象〕があり、人の、諸々の悦意（満足の思い）が有る。彼らは、快楽に依存する者たちであり、安楽を探し求める者たちである。彼らは、まさに、人として、生と老に近しく赴く者たちである。",
    342: "渇愛〔の思い〕で〔特定のものを〕偏重する人々は、捕縛された兎のように這い回る。束縛するもの（欲望の対象）に執着〔の思い〕ある有情たちは、長きにわたり、繰り返し、苦しみに近づく。",
    343: "渇愛〔の思い〕で〔特定のものを〕偏重する人々は、捕縛された兎のように這い回る。自己の離貪を望んでいる者よ、それゆえに、渇愛〔の思い〕を除き去るがよい。",
    344: "〔まさに〕その、〔欲の〕林の下生えなき者となりながら、〔欲の〕林に向かう者──〔欲の〕林から解き放たれたのに、まさしく、〔欲の〕林へと走り行く。来たれ、見よ、その人物を──〔欲の結縛から〕解き放たれたのに、まさしく、〔欲の〕結縛へと走り行く。",
    345: "〔まさに〕その、鉄でできているものも、木でできているものも、そして、葦〔の縄紐〕も──慧者たちは、それを、堅固な結縛と言わない。諸々の宝珠や耳飾にたいする貪染〔の思い〕に染まったもの──子たちにたいする、さらに、妻たちにたいする、〔まさに〕その、期待〔の思い〕なるもの──",
    346: "重くのしかかり、緩やかではあるが、解き放ち難きもの──慧者たちは、これを、堅固な結縛と言う。これをもまた断ち切って、〔慧者たちは〕遍歴遊行する──期待なき者たちとなり、欲望の安楽を捨棄して。",
    347: "彼ら、貪欲〔の思い〕に染まった者たちは、〔渇愛の〕流れに従い行く──蜘蛛が、自ら作った網に〔からまる〕ように。これをもまた断ち切って、慧者たちは行く──期待なき者たちとなり、一切の苦しみを捨棄して。",
    348: "過去にあるものを解き放て（過去の記憶に振り回されない）──未来にあるものを解き放て（未来に期待せず願望を抱かない）──中間（現在）にあるものを解き放て（今この瞬間に執着の対象を作らない）──〔迷いの〕生存（有）の彼岸に至る者となり。一切所において、意図が解脱した〔あなた〕は、ふたたび、生と老に近づくことはないであろう。",
    349: "乱れた思考の人に、強き貪欲ある浄美の随観者に（不浄のものを「美しく価値がある」と見る者に）、渇愛〔の思い〕は、より一層、増え行く。この者は、まさに、結縛を堅固に作り為す。",
    350: "しかしながら、彼が、思考の寂止に喜びある者であり、不浄〔の表象〕（不浄想：身体を不浄と見る観察）を修める、常に気づきある者であるなら、この者は、まさに、〔貪欲の〕終息を為すであろう。この者は、悪魔の結縛を断ち切るであろう。",
    351: "究極〔の境地〕に赴き、恐慌せず、渇愛を離れ、穢れなき者は、諸々の〔迷いの〕生存の矢を断ち切った。これは、最後の積身である（死後、涅槃に行く）。",
    352: "渇愛〔の思い〕を離れ、執取〔の思い〕なく、語と句の熟知者として、諸々の文字の配列を〔知り〕、そして、〔それらの〕前後〔関係〕を知るなら、彼は、まさに、「最後の肉体ある者（解脱者）」「大いなる智慧ある者」「大いなる人士たる者」と説かれる。",
    353: "わたしは、一切を征服する者として、一切を知る者として、一切の法（事象）に汚されない者として、〔世に〕存する。一切を捨棄する者は、渇愛の滅尽（涅槃の境処）において解脱した者は、自ら証知して、誰を、〔師と〕定めよう。",
    354: "法（真理）の施しは、一切の施しに勝つ。法（真理）の味わいは、一切の味わいに勝つ。法（真理）の喜びは、一切の喜びに勝つ。渇愛の滅尽は、一切の苦しみに勝つ。",
    355: "諸々の財物は、思慮浅き者を打ち砕く。しかしながら、彼岸を探し求める者たちを〔打ち砕くことは〕ない。思慮浅き者は、財物にたいする渇愛〔の思い〕のために、他者たちを〔打ち砕く〕ようにして、自己を打ち砕く。",
    356: "雑草という汚点あるのが、諸々の田畑である。貪欲（貪）という汚点あるのが、この、〔世の〕人々である。まさに、それゆえに、貪欲から離れた者たちにおいて、施されたものは、大いなる果と成る。",
    357: "雑草という汚点あるのが、諸々の田畑である。憤怒（瞋）という汚点あるのが、この、〔世の〕人々である。まさに、それゆえに、憤怒から離れた者たちにおいて、施されたものは、大いなる果と成る。",
    358: "雑草という汚点あるのが、諸々の田畑である。迷妄（痴）という汚点あるのが、この、〔世の〕人々である。まさに、それゆえに、迷妄から離れた者たちにおいて、施されたものは、大いなる果と成る。",
    359: "雑草という汚点あるのが、諸々の田畑である。欲求という汚点あるのが、この、〔世の〕人々である。まさに、それゆえに、欲求から離れた者たちにおいて、施されたものは、大いなる果と成る。",
}

OBSERVE = {
    334: "放逸に行う人の愛欲はつる草の如く増長す。 彼は生より生に漂う、あたかも林中に果実を求むる猿の如くに。",
    335: "この世に於て、この猛悪にして纏綿たる愛欲に征服せられたる人には、雨を受けたるビーラナ草の如く、その憂患増長す。",
    336: "この世に於て、この猛悪にして克服し難き愛欲を征服したる人には、蓮葉より水滴の〔落つる〕如く、憂患彼より去る。",
    337: "我この善事を汝らに告ぐ。 ここに集まれる汝らは、ウシーラ香を求むる者のビーラナ草を〔掘る〕如く、愛欲の根を掘るべし。 流水の葦を〔損なう〕如く、魔王をして再々汝らを壌らしむることなかれ。",
    338: "樹根損なわれずして固ければ、樹は伐らるるとも再び生ずるが如く、愛欲の執着断たれざれば、この苦（生死の苦）は再々生起す。",
    339: "その三十六流（内外各十八の愛欲）水勢盛んに快楽に向かいて流るる邪見者を、この奔流〔すなわち〕貪欲に執着せる意思は漂蕩し去る。",
    340: "〔愛欲の〕流れは至る所に流れ、〔その〕つるは芽を発して茂る。 このつるの生ずるを見ば、智慧を以てその根を断て。",
    341: "人の喜悦は奔放にして、かつ愛着す。 歓楽に耽り快楽を求むる人、かかる人は実に生と老とを受く。",
    342: "愛欲に満たされたる人は、罠に係れる兎の如く馳せ回る。 繋縛と執着とに捉えられ、久しき間再々苦を受く。",
    343: "愛欲に満たされたる人は、罠に係れる兎の如く馳せ回る。 故に比丘は自己の離欲を望みて愛欲を除くべし。",
    344: "欲林を出でて欲林に心を傾け、欲林を脱してまた欲林に走る者、実にこの人を見よ。 彼は〔繋縛を〕脱してまた繋縛に走るなり。",
    345: "賢者は、鉄・木または草よりなる縄縛を堅牢なりと言わず。 珠・環・妻・子に対する恋着こそ極めて強し。",
    346: "賢者は、この牽引力に富み、弛くしてしかも脱し難き縄縛を堅牢なりと言う。 この〔縄〕を断ちて恋着なき人は、欲楽を捨てて出家す。",
    347: "貪欲に執着する者は、〔欲の〕流れに随いて行くこと、蜘蛛の自ら作れる網に〔随うが〕如し。 これを断ちて恋着なき賢者は一切の苦を捨てて遊行す。",
    348: "有の彼岸に達し、前（未来の煩悩）を離れよ、後（過去の煩悩）を離れよ、中（現在の煩悩）を離れよ。 意一切処に於て解脱せば、汝は再び生と老とを受くることなし。",
    349: "疑惑に擾乱せられ、貪欲熾烈にして享楽を事とする人の愛欲は、ますます増長す。 かかる人は実に〔その〕繋縛を堅くす。",
    350: "疑惑の静止を喜び、身の不浄を観じ、常に熟慮する人は、実に魔王の繋縛を除かん、彼はこれを断たん。",
    351: "円成の境に達して畏怖なく、愛欲を離れて罪穢なく、有の矢を断てり。 これ〔その〕最後身なり。",
    352: "愛欲を離れて執着なく、聖典の語義に通暁し、前後の順序に従いて配列せられたる文字を知る人は、実に最後身を具する者にして、大智者・大丈夫と称せらる。",
    353: "我は一切を征服し、一切を知悉し、一切の法に於て汚さるることなし。 一切を捨て愛欲を滅して解脱せり。 自ら悟りて誰をか〔師と〕いわん。",
    354: "法施は一切の施に勝ち、法味は一切の味に勝ち、法楽は一切の楽に勝ち、愛欲の滅尽は一切の苦に勝つ。",
    355: "財は愚者を滅ぼし、決して彼岸を求むる者を〔滅ぼさ〕ず。 愚者は財欲によりて自己を滅ぼすこと、他人を〔滅ぼすが〕如し。",
    356: "田は雑草により損なわれ、この世の衆生は貪欲により損なわる。 されば貪欲を離れし人への施与は大果報あり。",
    357: "田は雑草により損なわれ、この世の衆生は瞋恚により損なわる。 されば瞋恚を離れし人への施与は大果報あり。",
    358: "田は雑草により損なわれ、この世の衆生は愚痴により損なわる。 されば愚痴を離れし人への施与は大果報あり。",
    359: "田は雑草により損なわれ、この世の衆生は欲望により損なわる。 されば欲望を離れし人への施与は大果報あり。",
}

PIN32 = "愛欲品（T210 第32品）"
PIN28 = "道行品（T210 第28品）"
NOTE = "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。"

CHINESE = {
    334: {"status": "mapped", "pin": PIN32, "t210": "T210-32-001",
          "text": "心放在婬行，欲愛增枝條，分布生熾盛，超躍貪果猴。", "satLocus": "大正蔵 T4.570c 愛欲品第1頌"},
    335: {"status": "mapped", "pin": PIN32, "t210": "T210-32-002",
          "text": "以為愛忍苦，貪欲著世間，憂患日夜長，莚如蔓草生。", "satLocus": "大正蔵 T4.570c 愛欲品第2頌"},
    336: {"status": "mapped", "pin": PIN32, "t210": "T210-32-003",
          "text": "人為恩愛惑，不能捨情欲，如是憂愛多，潺潺盈于池。", "satLocus": "大正蔵 T4.570c 愛欲品第3頌"},
    337: {"status": "mapped", "pin": PIN32, "t210": "T210-32-007",
          "text": "為道行者，不與欲會，先誅愛本，無所植根，勿如刈葦，令心復生。", "satLocus": "大正蔵 T4.570c 愛欲品第7頌"},
    338: {"status": "mapped", "pin": PIN32, "t210": "T210-32-008",
          "text": "如樹根深固，雖截猶復生，愛意不盡除，輒當還受苦。", "satLocus": "大正蔵 T4.570c 愛欲品第8頌"},
    339: {"status": "mapped", "pin": PIN32, "t210": "T210-32-010",
          "text": "貪意為常流，習與憍慢并，思想猗婬欲，自覆無所見。", "satLocus": "大正蔵 T4.570c 愛欲品第10頌"},
    340: {"status": "mapped", "pin": PIN32, "t210": "T210-32-011",
          "text": "一切意流衍，愛結如葛藤，唯慧分別見，能斷意根源。", "satLocus": "大正蔵 T4.570c 愛欲品第11頌"},
    341: {"status": "mapped", "pin": PIN32, "t210": "T210-32-012",
          "text": "夫從愛潤澤，思想為滋蔓，愛欲深無底，老死是用增。", "satLocus": "大正蔵 T4.570c 愛欲品第12頌"},
    342: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ愛欲品342はT210に対応なし（蘇錦坤對照表）。"},
    343: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ愛欲品343はT210に対応なし（蘇錦坤對照表）。"},
    344: {"status": "mapped", "pin": PIN32, "t210": "T210-32-009",
          "text": "猨猴得離樹，得脫復趣樹，眾人亦如是，出獄復入獄。", "satLocus": "大正蔵 T4.570c 愛欲品第9頌"},
    345: {"status": "mapped", "pin": PIN32, "t210": "T210-32-014",
          "text": "雖獄有鉤鍱，慧人不謂牢，愚見妻子息，染著愛甚牢。", "satLocus": "大正蔵 T4.571a 愛欲品第14頌"},
    346: {"status": "mapped", "pin": PIN32, "t210": "T210-32-015",
          "text": "慧說愛為獄，深固難得出，是故當斷棄，不視欲能安。", "satLocus": "大正蔵 T4.571a 愛欲品第15頌"},
    347: {"status": "mapped", "pin": PIN32, "t210": "T210-32-017",
          "text": "以婬樂自裹，譬如蠶作繭，智者能斷棄，不眄除眾苦。", "satLocus": "大正蔵 T4.571a 愛欲品第17頌"},
    348: {"status": "mapped", "pin": PIN28, "t210": "T210-28-013",
          "text": "釋前解後，脫中度彼，一切念滅，無復老死。", "satLocus": "大正蔵 T4.569b 道行品第13頌",
          "note": "パーリ愛欲品348はT210愛欲品ではなく道行品に対応（蘇錦坤對照表）。"},
    349: {"status": "mapped", "pin": PIN32, "t210": "T210-32-018",
          "text": "心念放逸者，見婬以為淨，恩愛意盛增，從是造獄牢。", "satLocus": "大正蔵 T4.571a 愛欲品第18頌"},
    350: {"status": "mapped", "pin": PIN32, "t210": "T210-32-019",
          "text": "覺意滅婬者，常念欲不淨，從是出邪獄，能斷老死患。", "satLocus": "大正蔵 T4.571a 愛欲品第19頌"},
    351: {"status": "mapped", "pin": PIN32, "t210": "T210-32-029",
          "text": "無欲無有畏，恬惔無憂患，欲除使結解，是為長出淵。", "satLocus": "大正蔵 T4.571a 愛欲品第29頌"},
    352: {"status": "mapped", "pin": PIN32, "t210": "T210-32-021",
          "text": "離欲滅愛迹，出網無所弊，盡道除獄縛，一切此彼解，已得度邊行，是為大智士。", "satLocus": "大正蔵 T4.571a 愛欲品第21頌"},
    353: {"status": "mapped", "pin": PIN32, "t210": "T210-32-023",
          "text": "若覺一切法，能不著諸法，一切愛意解，是為通聖意。", "satLocus": "大正蔵 T4.571a 愛欲品第23頌"},
    354: {"status": "mapped", "pin": PIN32, "t210": "T210-32-024",
          "text": "眾施經施勝，眾味道味勝，眾樂法樂勝，愛盡勝眾苦。", "satLocus": "大正蔵 T4.571a 愛欲品第24頌"},
    355: {"status": "mapped", "pin": PIN32, "t210": "T210-32-025",
          "text": "愚以貪自縛，不求度彼岸，貪為財愛故，害人亦自害。", "satLocus": "大正蔵 T4.571a 愛欲品第25頌"},
    356: {"status": "mapped", "pin": PIN32, "t210": "T210-32-026",
          "text": "愛欲意為田，婬怒癡為種，故施度世者，得福無有量。", "satLocus": "大正蔵 T4.571a 愛欲品第26頌"},
    357: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ愛欲品357はT210に対応なし（蘇錦坤對照表）。"},
    358: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ愛欲品358はT210に対応なし（蘇錦坤對照表）。"},
    359: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None,
          "note": "パーリ愛欲品359はT210に対応なし（蘇錦坤對照表）。"},
}

VERSE_PRACTICE = {
    334: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "放逸すれば愛欲はつる草の如く増長する"},
    335: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "愛欲に征服されれば憂患が増長する"},
    336: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "愛欲を征服すれば憂患は蓮葉の水滴の如く去る"},
    337: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "愛欲の根を掘り崩し、魔に壊されぬ"},
    338: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "愛欲の根が残れば苦は再々生起する"},
    339: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "三十六の欲流が邪見を運び来る"},
    340: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "つるの生じるを見て、智慧で根を断つ"},
    341: {"nidanaId": "feeling", "pathFactors": ["正念", "正思惟"], "reason": "喜悦・快楽の受に耽れば生と老を受ける"},
    342: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "愛欲の偏重は罠の兎のように這い回る掴み"},
    343: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "離欲を望むなら愛欲を除き去る"},
    344: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "欲林を脱しても再び欲林へ走る欲しがり"},
    345: {"nidanaId": "clinging", "pathFactors": ["正念", "正命"], "reason": "妻子・珠環への恋着こそ堅牢な掴み"},
    346: {"nidanaId": "clinging", "pathFactors": ["正念", "正業"], "reason": "脱し難き縄縛を断ち、欲楽を捨てる"},
    347: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "蜘蛛の自作の網のような貪欲の掴みを断つ"},
    348: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "前・後・中を解き放ち、有の彼岸を見直す"},
    349: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "疑惑と貪欲で愛欲が増長し繋縛を堅くする"},
    350: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "不浄観と熟慮で魔の繋縛を断つ"},
    351: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "愛欲を離れ有の矢を断った最後身"},
    352: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "愛欲を離れ聖典に通暁する大智者として見直す"},
    353: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "一切を征服し愛欲を滅して解脱する"},
    354: {"nidanaId": "contact", "pathFactors": ["正語", "正念"], "reason": "法施・法味・法楽に触れ、愛欲の滅尽を知る"},
    355: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "財欲は愚者を滅ぼし、自己を打ち砕く"},
    356: {"nidanaId": "feeling", "pathFactors": ["正念", "正思惟"], "reason": "貪欲という汚点が衆生を損なうと知る"},
    357: {"nidanaId": "feeling", "pathFactors": ["正念", "正業"], "reason": "瞋恚という汚点が衆生を損なうと知る"},
    358: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "愚痴という汚点に触れ、離れた施に大果あり"},
    359: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "欲望という汚点が衆生を損なうと知る"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [(f"DP24-P{i:02d}", 333 + i) for i in range(1, 27)]


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault("note", NOTE)
    return c


def main():
    old = json.loads((DATA / "ch24.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 渇愛の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第２４章・愛欲品 第{verse}偈（#ch02-24）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第24章・愛欲品（渇愛の章）"
    SHORT = "愛欲品（渇愛の章）"
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
            "pathLabel": "つるの芽生えと法施に触れ、智慧で根を見る",
            "chapterHint": SHORT,
            "fromPrev": "前夜の解き放ちが、今朝の蔓への気づきになる",
            "toNext": "接触のあと、喜悦や汚点の受が立ち上がる",
            "todayObserve": OBSERVE[340],
            "todayAction": actions["DP24-P07"],
            "when": ["欲が芽生えた", "法を伝える"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[340][:40] + "…",
            "secondaryObserve": "法施は一切の施に勝ち、愛欲の滅尽は一切の苦に勝つ",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "喜悦と貪瞋の受を観察し、損なわれていないか見る",
            "chapterHint": SHORT,
            "fromPrev": "蔓に触れたあと、快楽や怒り・貪欲の受が来る",
            "toNext": "受けた快を、つる草の欲しがりへ落とさない",
            "todayObserve": OBSERVE[341],
            "todayAction": actions["DP24-P08"],
            "when": ["楽しければいいと思った", "怒りが湧いた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[341][:40] + "…",
            "secondaryObserve": "田は雑草により損なわれ、衆生は貪欲・瞋恚により損なわる",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "つる草の欲しがりを観察し、根へ向かう",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、愛欲の蔓が増長する",
            "toNext": "止めないと妻子・網の掴みへ進む",
            "todayObserve": OBSERVE[334],
            "todayAction": actions["DP24-P01"],
            "when": ["もっとほしい", "断った欲に戻る"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[334][:40] + "…",
            "secondaryObserve": "欲林を脱してまた欲林に走る者を見よ",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "罠・妻子・蜘蛛の網という掴みを断つ",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、恋着・執着として掴む手前",
            "toNext": "掴むと憂患と輪廻の苦が太る",
            "todayObserve": OBSERVE[345] + " " + OBSERVE[346],
            "todayAction": actions["DP24-P12"],
            "when": ["期待と執着が生じた", "自ら作った縛りに気づいた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[345][:40] + "…",
            "secondaryObserve": "蜘蛛の自ら作れる網に随うが如し",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "愛欲と財欲の掴みが、憂患と自滅の苦になると知る",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、憂患と生死の苦が熟す",
            "toNext": "見れば、根を掘り憂患を落とす実践へ向き直る",
            "todayObserve": OBSERVE[335],
            "todayAction": actions["DP24-P02"],
            "when": ["憂いが増えている", "財欲が自己を損なう"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[335][:40] + "…",
            "secondaryObserve": "愛欲の執着断たれざれば、この苦は再々生起す",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "根を掘り、不浄観で魔の繋縛を断ち離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、征服と離欲へ向き直る",
            "toNext": "離すと、前中後を解き放つ見直しへつながる",
            "todayObserve": OBSERVE[336] + " " + OBSERVE[337],
            "todayAction": actions["DP24-P03"],
            "when": ["欲を征服したい", "根を掘りたい"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[336][:40] + "…",
            "secondaryObserve": "身の不浄を観じ、常に熟慮する人は魔の繋縛を断つ",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "concentration", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "前・後・中を解き放ち、愛欲なき一夜を閉じる",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、蔓を伸ばしたかの跡",
            "toNext": "見直しが、翌朝の根への気づきになる",
            "todayObserve": OBSERVE[348],
            "todayAction": actions["DP24-P15"],
            "when": ["一日を閉じるとき", "過去未来現在の執着を手放す"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[348][:40] + "…",
            "secondaryObserve": "意一切処に於て解脱せば、再び生と老とを受くることなし",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 24,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第24章（愛欲品／渇愛の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210愛欲品ほか）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・渇愛の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第２４章・愛欲品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・愛欲品（T4.570c）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "愛欲品は渇愛の増長と根の断絶が中心。既定の焦点は欲しがる。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch24.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch24.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 25):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch24", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 26
    assert all(p["id"] == f"DP24-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(334, 360))
    assert all(p["alignment"]["chinese"]["status"] in ("mapped", "unmapped") for p in pairs)
    unmapped_ids = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] == "unmapped"]
    assert unmapped_ids == ["DP24-P09", "DP24-P10", "DP24-P24", "DP24-P25", "DP24-P26"], unmapped_ids
    assert set(by_nidana) == valid
    print("OK")


if __name__ == "__main__":
    main()
