#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild dhammapada ch26.json (婆羅門品) to match ch1–ch25 source alignment."""
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ARANA_URL = (
    "https://sites.google.com/view/arana-tipitaka/"
    "%E7%9B%AE%E6%AC%A1/%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8/"
    "%E5%B0%8F%E9%83%A8%E7%B5%8C%E5%85%B8%E3%83%80%E3%83%B3%E3%83%9E%E3%83%91%E3%83%80"
)
TB_URL = "https://true-buddhism.com/sutra/dhammapada/#ch02-26"
SAT_URL = "https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0210_%2C04%2C0572"
MAP_URL = (
    "https://nanda.online-dhamma.net/tipitaka/sutta/khuddaka/dhammapada/"
    "dhp-correspondence-tables/dhp-correspondence-tables-pali-chap26/"
)

QUOTES = {
    383: "婆羅門よ、〔渇愛の〕流れを断て。〔道心堅固に〕勤しんで、諸々の欲望を除け。諸々の形成〔作用〕（諸行：形成されたもの・現象世界）の滅尽を知って、婆羅門よ、作られざるもの（涅槃）を知る者として、〔あなたは〕存する。",
    384: "すなわち、〔対立する〕二つの法（事象）について、彼岸に至る者（善悪の彼岸にいる者）として、婆羅門が〔世に〕有るとき、そこで、彼の一切の束縛は〔自ずと〕滅却に至る──〔彼が、あるがままに〕知っているなら。",
    385: "彼に、彼岸が〔見出されず〕、あるいは、此岸が〔見出されず〕、彼岸と此岸が〔両者ともに〕見出されないなら、懊悩を離れ、束縛を離れた者であり、わたしは、彼を「婆羅門」と説く。",
    386: "〔世俗の〕塵を離れ〔林に〕坐す瞑想者を、為すべきことを為した煩悩なき者を、最上の義（目的）を獲得した者を──わたしは、彼を「婆羅門」と説く。",
    387: "日は、昼に輝き、月は、夜に明らむ。士族は、武装者として輝き、婆羅門は、瞑想者として輝く。そこで、覚者は、昼夜全てに、威光によって輝く。",
    388: "悪を拒否した者（バーヒタ）、ということで、「婆羅門（ブラーフマナ）」〔と説かれる〕。平静（サマ）なる性行あることから、「沙門（サマナ）」と説かれる。自己の垢を〔常に〕払っている者（パッバージャヤント）は、それゆえに、「出家者（パッバジタ）」と説かれる。",
    389: "婆羅門を打たないように。婆羅門は、彼（婆羅門を打つ者）に、〔怒りの思いを〕解き放たないように。婆羅門を傷つける者は、厭わしい。彼（婆羅門を打つ者）に、〔怒りの思いを〕解き放つなら、彼（婆羅門を打つ者）よりも、厭わしい。",
    390: "すなわち、諸々の愛しくあるものから〔身を〕慎む意図（心の制御）あるとき、婆羅門にとって、このことは、少なからず、より勝っている。そのたび、そのたびに、害する意が退転することから、そのたび、そのたびに、苦しみは、まさしく、静まる。",
    391: "彼に、身体（身）と言葉（口・語）と意（意）による悪行が存在しないなら、三つの境位（身・口・意の三業）によって統御された者であり、わたしは、彼を「婆羅門」と説く。",
    392: "彼から、正等覚者によって説示された法（真理）を識知するなら、謹んで、彼を礼拝するがよい──婆羅門が、祭火に捧げものを〔献じる〕ように。",
    393: "諸々の結髪にあらず、氏姓にあらず、出生にあらず──〔彼が〕婆羅門と成るのは。彼において、かつまた、真理があり、かつまた、法（教え）があるなら、彼は、清らかな者であり、そして、彼は、婆羅門と〔成る〕。",
    394: "思慮浅き者よ、あなたにとって、諸々の結髪が、何になるというのだろう。あなたにとって、皮衣が、何になるというのだろう。あなたには、内なる収め取り（執着）がある。〔あなたは〕外に〔見てくれを〕繕っている。",
    395: "糞掃衣（ぼろ布）を〔身に〕付ける人を、痩せ細り〔浮き出た〕血管が〔身体中に〕広がった者を、林のなかで、独り、瞑想している者を──わたしは、彼を「婆羅門」と説く。",
    396: "そして、わたしは、〔婆羅門の〕胎から生じ、〔婆羅門の〕母から発生する者を、「婆羅門」と説かない。彼が、もし、〔執着ある〕所有者として〔世に〕有るなら、彼は、「ボーヴァーディン（「君よ」と呼びかける者）」という名で〔世に〕有る〔だけのこと〕。無一物で、無執取の者を──わたしは、彼を「婆羅門」と説く。",
    397: "一切の束縛するものを断ち切って、彼が、まさに、思い悩まないなら、執着を超え行く者であり、束縛を離れた者であり、わたしは、彼を「婆羅門」と説く。",
    398: "紐（憤怒）を断ち切って、そして、緒（渇愛）を〔断ち切って〕、手綱（煩悩）と共に、綱（六十二の悪見）を〔断ち切って〕、閂（無明）を引き抜いた覚者を──わたしは、彼を「婆羅門」と説く。",
    399: "罵倒を、さらに、殴打と結縛を、彼が、怒ることなく忍受するなら、忍耐の力ある者であり、力ある軍隊〔に匹敵する者〕であり、わたしは、彼を「婆羅門」と説く。",
    400: "忿激せず、掟ある者を、〔渇愛の〕増長なく、戒ある者を、〔自己が〕調御され、最後の肉体ある者を──わたしは、彼を「婆羅門」と説く。",
    401: "蓮の葉にある水〔滴〕のように、錐の先にある芥子〔粒〕のように、彼が、諸々の欲望〔の対象〕に汚されないなら、わたしは、彼を「婆羅門」と説く。",
    402: "彼が、苦しみの〔滅尽を〕覚知し、まさしく、この〔世において〕、自己の滅尽を〔覚知するなら〕、〔生の〕重荷を降ろした者であり、〔世の〕束縛を離れた者であり、わたしは、彼を「婆羅門」と説く。",
    403: "深遠なる智慧ある者にして思慮ある者を、道と道ならざるものを熟知する者を、最上の義（目的）を獲得した者を──わたしは、彼を「婆羅門」と説く。",
    404: "在家の者たちと交わらず、さらに、同様に、家なき者たちと〔交わらず〕、家なくして行く、少なき欲求の者を──わたしは、彼を「婆羅門」と説く。",
    405: "動くものたちにたいし、さらに、動かないものたちにたいし、〔一切の〕生類にたいし、棒（武器）を置いて、彼が、〔他者を〕殺さず、〔他者をして他者を〕殺させないなら、わたしは、彼を「婆羅門」と説く。",
    406: "〔道を〕遮る者たちのなかにいながら遮ることなき者（一切にたいし敵意なき者）を、棒（武器）を取った者たちのなかにいながら涅槃に到達した者を、執取〔の思い〕を有する者たちのなかにいながら執取〔の思い〕なき者を──わたしは、彼を「婆羅門」と説く。",
    407: "彼の、そして、貪欲（貪）が、かつまた、憤怒（瞋）が、〔我想の〕思量（慢）が、さらに、〔虚栄の〕偽装（覆）が、芥子〔粒〕が錐の先から〔落ちる〕ように打ち倒されたなら、わたしは、彼を「婆羅門」と説く。",
    408: "粗野ではなく、〔はっきりと意味を〕識知させる、真理の言葉を発し、それによって、誰であれ、傷つけないなら、わたしは、彼を「婆羅門」と説く。",
    409: "彼が、この〔世において〕、あるいは、長いものも、あるいは、短いものも、微細なるものや粗大なるものも、浄美なるものや浄美ならざるものも、世において、与えられていないものを、〔何ひとつ〕取らないなら、わたしは、彼を「婆羅門」と説く。",
    410: "この世において、さらに、他〔の世〕において、彼に、諸々の願望（自己中心的な期待や思惑）が見出されないなら、願求なき者であり、束縛を離れた者であり、わたしは、彼を「婆羅門」と説く。",
    411: "彼に、諸々の〔生存の〕基底（阿頼耶：固執の思いが定着する場）が見出されず、〔一切を〕了知して、懐疑なき者となるなら、不死への沈潜（涅槃）を獲得した者であり、わたしは、彼を「婆羅門」と説く。",
    412: "彼が、この〔世において〕、そして、善を、さらに、悪を、両者ともに、執着〔の思い〕を超え行ったなら、憂いなく、〔世俗の〕塵を離れる、清浄の者であり、わたしは、彼を「婆羅門」と説く。",
    413: "月のように垢（汚れ）を離れ、〔心が〕清浄で澄浄で混濁なき者を、愉悦〔の思い〕と〔迷いの〕生存が完全に滅尽した者を──わたしは、彼を「婆羅門」と説く。",
    414: "彼が、この障害と悪路と輪廻と迷妄を超え行ったなら、〔激流を〕超え彼岸に至った瞑想者であり、動揺なく懐疑なき者であり、〔何も〕執取せずして涅槃に到達した者であり、わたしは、彼を「婆羅門」と説く。",
    415: "彼が、この〔世において〕、諸々の欲望〔の対象〕を捨棄して、家なき者として遍歴遊行するなら、欲望〔の対象〕と〔迷いの〕生存が完全に滅尽した者であり、わたしは、彼を「婆羅門」と説く。",
    416: "彼が、この〔世において〕、渇愛〔の思い〕を打破して、家なき者として遍歴遊行するなら、渇愛〔の思い〕と〔迷いの〕生存が完全に滅尽した者であり、わたしは、彼を「婆羅門」と説く。",
    417: "人間の束縛を捨棄して、天の束縛を超え行ったなら、一切の束縛による束縛を離れた者であり、わたしは、彼を「婆羅門」と説く。",
    418: "そして、歓楽を、さらに、不満を、〔両者ともに〕捨棄して、〔心が〕清涼と成った者を、〔生存の〕依り所（依存の対象）なき者を、一切の世を征服する勇者を──わたしは、彼を「婆羅門」と説く。",
    419: "彼が、有情たちの死滅を、さらに、再生を、全てにわたり知ったなら、〔一切に〕執着なき者であり、善き至達者たる覚者であり、わたしは、彼を「婆羅門」と説く。",
    420: "天〔の神々〕たちが、音楽神や人間たちが、彼の赴く所を知らないなら、煩悩の滅尽者たる阿羅漢であり、わたしは、彼を「婆羅門」と説く。",
    421: "かつまた、過去に、かつまた、未来に、かつまた、〔その〕中間（現在）において、彼のものが、何も存在しないなら、無一物の者であり、無執取の者であり、わたしは、彼を「婆羅門」と説く。",
    422: "〔勇猛果敢な〕雄牛たる最も優れた勇者を、〔一切の〕征圧者たる偉大なる聖賢を、不動の沐浴者（梵行終了者）たる覚者を──わたしは、彼を「婆羅門」と説く。",
    423: "彼が、過去（前世）の居住を知ったなら、かつまた、〔人々が死後に赴く〕天上と悪所を〔あるがままに〕見るなら、そこで、生の滅尽に至り得た者であるなら、〔あるがままの〕証知が完成された牟尼であり、一切が完成された完成者を、わたしは、彼を「婆羅門」と説く。",
}

OBSERVE = {
    383: "婆羅門よ、勇敢に〔欲の〕流れを断て、諸欲を去れ。 万象の滅尽を知りて汝は無作（涅槃）を知る。",
    384: "婆羅門もし二法（止観）に於て彼岸に達すれば、この智者に一切の繋縛（けばく）は終息す。",
    385: "彼岸（来世）も此岸（現世）もなく、彼此両岸もなく、畏怖を去り、繋縛（けばく）を捨てたる人、我はこれを婆羅門と呼ぶ。",
    386: "禅定に入り、垢穢なく安住し、為すべきをなし、煩悩を去り、最上義（阿羅漢果）に達せる人、我はこれを婆羅門と呼ぶ。",
    387: "日は昼に輝き、月は夜に照らし、刹帝利（せっていり）は武装して輝き、婆羅門は禅定に入りて輝く。 されど仏陀はその光明により、全昼夜に輝く。",
    388: "婆羅門とは悪業を除ける者の意にして、行う所寂静なるが故に沙門と称せらる。 自己の垢穢を去る者は、これによりて出家と称せらる。",
    389: "婆羅門を打つべからず。 〔打たるるも〕婆羅門はこれに敵対すべからず。 婆羅門を打つ者に災いあれ。 〔打たれて〕これに敵対する者に、更に災いあれ。",
    390: "婆羅門もし愛好するものより心を抑制せば、彼に少なからざる利益あり。 害心の消滅するに随い、苦悩もこれに随いて静止す。",
    391: "身と語と意とによる悪業なく、この三処に於て抑制せる人、我はこれを婆羅門と呼ぶ。",
    392: "正等覚者の説示せる法を、いかなる人より学び得たりとも、その人を恭しく敬礼すべし、あたかも婆羅門が祭火を〔敬う〕が如く。",
    393: "螺髻（らけい）・族・姓によりて婆羅門たるに非ず。 真実と法とを具する者、彼は幸福なり、彼はまた〔真の〕婆羅門なり。",
    394: "愚者よ、螺髻（らけい）汝に何の用かあらん、皮衣汝に何の用かあらん。 汝の内は〔不浄の〕密林なり。 汝は外を清掃するのみ。",
    395: "糞掃衣（ふんぞうえ）（弊衣）を着け、痩せて脈管露われ、独り林中に於て禅定を修する人、我はこれを婆羅門と呼ぶ。",
    396: "我はまた、胎により母系によりて婆羅門と呼ばず。 彼は〔不遜にも世尊を〕「ボー」（「友よ」の義）と呼び、彼は実に富裕なれども執着あり。 無一物にして執着なき人、我はこれを婆羅門と呼ぶ。",
    397: "一切の結縛を断ち、畏怖なく執着を超越し、繋縛（けばく）を離れたる人、我はこれを婆羅門と呼ぶ。",
    398: "紐と緒と綱とこれに属するものとを断ち、障礙を除きて覚りたる人、我はこれを婆羅門と呼ぶ。",
    399: "罪なくして罵詈と体刑と縄縛とを忍び、忍辱（にんにく）を力とし、勇力を軍兵として有する人、我はこれを婆羅門と呼ぶ。",
    400: "忿怒なく、戒を持して徳行あり、欲を離れ、調御（ちょうご）して最後身に達せる人、我はこれを婆羅門と呼ぶ。",
    401: "蓮葉に於ける水の如く、錐の尖端に於ける芥子粒の如く、諸欲に染着せざる人、我はこれを婆羅門と呼ぶ。",
    402: "既にこの世に於て、自己の苦の滅尽を悟り、重担を下ろし、繋縛（けばく）を離れたる人、我はこれを婆羅門と呼ぶ。",
    403: "智慧深く、賢慮ありて道・非道を弁え、最上義に達せる人、我はこれを婆羅門と呼ぶ。",
    404: "在家とも出家とも、二つながら交わらず、家なく遊行し、少欲なる人、我はこれを婆羅門と呼ぶ。",
    405: "弱きも強きも一切の有情の中にありて刀杖を捨て、殺すことなく、殺さしむることなき人、我はこれを婆羅門と呼ぶ。",
    406: "害意ある者の中にありて害意なく、刀杖を手にせる者の中にありて温順に、執着ある者の中にありて執着なき人、我はこれを婆羅門と呼ぶ。",
    407: "その貪欲と瞋恚（しんに）と慢心と虚偽との脱落せること、あたかも錐の尖端より芥子粒の〔落つる〕如くなる人、我はこれを婆羅門と呼ぶ。",
    408: "粗暴ならず、教訓的なる真実の語を発し、これによりて何者をも怒らしめざる人、我はこれを婆羅門と呼ぶ。",
    409: "この世に於て、長きも短きも、小なるも大なるも、浄きも浄からざるも、与えられざるものを取らざる人、我はこれを婆羅門と呼ぶ。",
    410: "この世に対しても、かの世に対しても、欲望なく愛着なく、繋縛（けばく）を離れたる人、我はこれを婆羅門と呼ぶ。",
    411: "執着の存するなく、悟り終わりて疑惑なく、甘露（涅槃）の奥底に到達せる人、我はこれを婆羅門と呼ぶ。",
    412: "この世に於て善悪両種の執着を超脱し、憂患なく垢穢なく清浄なる人、我はこれを婆羅門と呼ぶ。",
    413: "月の如く無垢・清浄・澄明にして暗影なく、快楽の生起を滅尽したる人、我はこれを婆羅門と呼ぶ。",
    414: "この泥濘（貪欲等）と越え難き輪廻と愚痴とを越え、渡りて彼岸に達し、禅定に住し、無欲にして疑惑なく、執着を捨てて寂静なる人、我はこれを婆羅門と呼ぶ。",
    415: "この世に於て欲楽を捨て、家なくして遊行し、欲楽の生起を滅尽したる人、我はこれを婆羅門と呼ぶ。",
    416: "この世に於て愛欲を捨て、家なくして遊行し、愛欲の生起を滅尽したる人、我はこれを婆羅門と呼ぶ。",
    417: "人間の束縛を捨て、天上の束縛を脱し、一切の束縛より離れたる人、我はこれを婆羅門と呼ぶ。",
    418: "楽と不楽とを捨て、清涼にして煩悩なく、一切世界を克服せる勇者、我はこれを婆羅門と呼ぶ。",
    419: "有情の消滅と生起とを完全に知り、執着なく安泰にして覚りたる人、我はこれを婆羅門と呼ぶ。",
    420: "諸天も乾闥婆（けんだつば）も人間も、彼の赴く道を知らず、煩悩を滅尽して阿羅漢となりし人、我はこれを婆羅門と呼ぶ。",
    421: "前（過去）にも、後（未来）にも、中（現在）にも何物をも有せず、無一物にして執着なき人、我はこれを婆羅門と呼ぶ。",
    422: "雄牛〔の如く強く〕、最も勝れ、勇者にして大仙、勝利に富み、無欲にして〔心垢を〕洗滌し、覚りたる人、我はこれを婆羅門と呼ぶ。",
    423: "前生を知り、天界と悪趣とを見、更に生の滅尽に達し、智に於て完成したる牟尼（むに）（賢人）、一切円満成就の人、我はこれを婆羅門と呼ぶ。",
}

CHINESE = {
    383: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-001", "text": "截流而渡，無欲如梵，知行已盡，是謂梵志。", "satLocus": "大正蔵 T4.572b 梵志品第1頌"},
    384: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-002", "text": "以無二法，清淨渡淵，諸欲結解，是謂梵志。", "satLocus": "大正蔵 T4.572b 梵志品第2頌"},
    385: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-003", "text": "適彼無彼，彼彼已空，捨離貪婬，是謂梵志。", "satLocus": "大正蔵 T4.572b 梵志品第3頌"},
    386: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-004", "text": "思惟無垢，所行不漏，上求不起，是謂梵志。", "satLocus": "大正蔵 T4.572b 梵志品第4頌"},
    387: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-005", "text": "日照於晝，月照於夜，甲兵照軍，禪照道人，佛出天下，照一切冥。", "satLocus": "大正蔵 T4.572b 梵志品第5頌"},
    388: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-007", "text": "出惡為梵志，入正為沙門，棄我眾穢行，是則為捨家。", "satLocus": "大正蔵 T4.572b 梵志品第7頌"},
    389: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None, "note": "パーリ婆羅門品389はT210に対応なし（蘇錦坤對照表）。"},
    390: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None, "note": "パーリ婆羅門品390はT210に対応なし（蘇錦坤對照表）。"},
    391: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-009", "text": "身口與意，淨無過失，能攝三行，是謂梵志。", "satLocus": "大正蔵 T4.572b 梵志品第9頌"},
    392: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-010", "text": "若心曉了，佛所說法，觀心自歸，淨於為水。", "satLocus": "大正蔵 T4.572b 梵志品第10頌"},
    393: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-011", "text": "非蔟結髮，名為梵志，誠行法行，清白則賢。", "satLocus": "大正蔵 T4.572b 梵志品第11頌"},
    394: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-012", "text": "飾髮無慧，草衣何施？內不離著，外捨何益？", "satLocus": "大正蔵 T4.572b 梵志品第12頌"},
    395: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-013", "text": "被服弊惡，躬承法行，閑居思惟，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第13頌"},
    396: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-006", "text": "非剃為沙門，稱吉為梵志，謂能捨眾惡，是則為道人。", "satLocus": "大正蔵 T4.572b 梵志品第6頌"},
    397: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-015", "text": "絕諸可欲，不婬其志，委棄欲數，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第15頌"},
    398: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-016", "text": "斷生死河，能忍起度，自覺出塹，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第16頌"},
    399: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-017", "text": "見罵見擊，默受不怒，有忍辱力，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第17頌"},
    400: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-018", "text": "若見侵欺，但念守戒，端身自調，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第18頌"},
    401: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-019", "text": "心棄惡法，如蛇脫皮，不為欲污，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第19頌"},
    402: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-020", "text": "覺生為苦，從是滅意，能下重擔，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第20頌"},
    403: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-021", "text": "解微妙慧，辯道不道，體行上義，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第21頌"},
    404: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-022", "text": "棄捐家居，無家之畏，少求寡欲，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第22頌"},
    405: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-023", "text": "棄放活生，無賊害心，無所嬈惱，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第23頌"},
    406: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-024", "text": "避爭不爭，犯而不慍，惡來善待，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第24頌"},
    407: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-025", "text": "去婬怒癡，憍慢諸惡，如蛇脫皮，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第25頌"},
    408: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-026", "text": "斷絕世事，口無麤言，八道審諦，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第26頌"},
    409: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-027", "text": "所世惡法，修短巨細，無取無捨，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第27頌"},
    410: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-028", "text": "今世行淨，後世無穢，無習無捨，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第28頌"},
    411: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-028", "text": "今世行淨，後世無穢，無習無捨，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第28頌", "note": "T210では410–411付近を同頌系で対応（蘇錦坤對照表）。"},
    412: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-030", "text": "於罪與福，兩行永除，無憂無塵，是謂梵志。", "satLocus": "大正蔵 T4.572c 梵志品第30頌"},
    413: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-031", "text": "心喜無垢，如月盛滿，謗毀已除，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第31頌"},
    414: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-032", "text": "見癡往來，墮塹受苦，欲單渡岸，不好他語，唯滅不起，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第32頌"},
    415: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-032", "text": "見癡往來，墮塹受苦，欲單渡岸，不好他語，唯滅不起，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第32頌", "note": "T210では414–415付近を同頌系で対応（蘇錦坤對照表）。"},
    416: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-033", "text": "已斷恩愛，離家無欲，愛有已盡，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第33頌"},
    417: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-034", "text": "離人聚處，不墮天聚，諸聚不歸，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第34頌"},
    418: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-035", "text": "棄樂無樂，滅無熅燸，健違諸世，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第35頌"},
    419: {"status": "unmapped", "pin": None, "t210": None, "text": None, "satLocus": None, "note": "パーリ婆羅門品419はT210に対応なし（蘇錦坤對照表）。"},
    420: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-037", "text": "已度五道，莫知所墮，習盡無餘，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第37頌"},
    421: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-038", "text": "于前于後，乃中無有，無操無捨，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第38頌"},
    422: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-039", "text": "最雄最勇，能自解度，覺意不動，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第39頌"},
    423: {"status": "mapped", "pin": "梵志品（T210 第35品）", "t210": "T210-35-040", "text": "自知宿命，本所更來，得要生盡，叡通道玄，明如能默，是謂梵志。", "satLocus": "大正蔵 T4.573a 梵志品第40頌"},
}

VERSE_PRACTICE = {
    383: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "欲の流れを断ち、万象の滅尽を知る"},
    384: {"nidanaId": "release", "pathFactors": ["正定", "正見"], "reason": "止観の二法で彼岸に達し繋縛が終息する"},
    385: {"nidanaId": "release", "pathFactors": ["正見", "正念"], "reason": "彼此両岸なく、畏怖と繋縛を捨てる"},
    386: {"nidanaId": "contact", "pathFactors": ["正定", "正念"], "reason": "禅定・無垢・所作已弁の婆羅門に触れる"},
    387: {"nidanaId": "contact", "pathFactors": ["正念", "正見"], "reason": "仏陀の光明が全昼夜を照らすと知る"},
    388: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "悪業を除き垢穢を去る"},
    389: {"nidanaId": "clinging", "pathFactors": ["正業", "正念"], "reason": "打つ・敵対という掴みをせず災いを避ける"},
    390: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "可意への愛着を制止し苦を鎮める"},
    391: {"nidanaId": "clinging", "pathFactors": ["正念", "正語"], "reason": "身語意の悪行を掴まず三行を浄む"},
    392: {"nidanaId": "contact", "pathFactors": ["正念", "正語"], "reason": "正法を学ぶ師への礼敬に触れる"},
    393: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "辮髪ではなく真実と法で婆羅門となる"},
    394: {"nidanaId": "craving", "pathFactors": ["正念", "正見"], "reason": "外見を整えても内心の欲林が残る"},
    395: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "糞掃衣・林中禅定で離す"},
    396: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "無一物にして執着なき者が婆羅門"},
    397: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "一切の結縛を断ち離軛する"},
    398: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "紐・結縛を断ち覚めて離す"},
    399: {"nidanaId": "feeling", "pathFactors": ["正念", "正業"], "reason": "罵詈打撃を忍辱で受ける"},
    400: {"nidanaId": "release", "pathFactors": ["正念", "正業"], "reason": "不瞋・守戒・自制で最後身へ"},
    401: {"nidanaId": "feeling", "pathFactors": ["正念", "正思惟"], "reason": "五欲に染まらない蓮葉の受"},
    402: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "苦を知り重担を下ろす"},
    403: {"nidanaId": "contact", "pathFactors": ["正見", "正念"], "reason": "道と非道を弁別する智慧に触れる"},
    404: {"nidanaId": "craving", "pathFactors": ["正念", "正命"], "reason": "少欲知足で家への欲しがりを緩める"},
    405: {"nidanaId": "release", "pathFactors": ["正業", "正念"], "reason": "生類への刀杖を置き不害に離す"},
    406: {"nidanaId": "feeling", "pathFactors": ["正念", "正業"], "reason": "敵意の中で敵意なく温順に受ける"},
    407: {"nidanaId": "clinging", "pathFactors": ["正念", "正思惟"], "reason": "貪瞋慢を芥子の如く振り落とす"},
    408: {"nidanaId": "feeling", "pathFactors": ["正語", "正念"], "reason": "柔和・真実・有益な語の受"},
    409: {"nidanaId": "clinging", "pathFactors": ["正念", "正業"], "reason": "与えられていないものを掴まず取る"},
    410: {"nidanaId": "craving", "pathFactors": ["正念", "正思惟"], "reason": "此世彼世への欲望を手放す"},
    411: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "疑惑なく甘露に達して離す"},
    412: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "善悪両執着を超えて清浄を見直す"},
    413: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "月のように清明で有への喜楽を断つ"},
    414: {"nidanaId": "suffering", "pathFactors": ["正見", "正念"], "reason": "危険・輪廻・愚痴という苦を越える"},
    415: {"nidanaId": "craving", "pathFactors": ["正念", "正命"], "reason": "感官欲を捨て遊行する"},
    416: {"nidanaId": "release", "pathFactors": ["正念", "正精進"], "reason": "渇愛を打破し愛有を滅尽する"},
    417: {"nidanaId": "clinging", "pathFactors": ["正念", "正見"], "reason": "人趣・天界の結縛を掴まず離す"},
    418: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "楽不楽を捨て清涼な英雄となる"},
    419: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "死と転生を理解し無執着を見直す"},
    420: {"nidanaId": "release", "pathFactors": ["正念", "正定"], "reason": "漏尽し行方知れず解脱する"},
    421: {"nidanaId": "review", "pathFactors": ["正念", "正定"], "reason": "前中後に無一物の軽さを見直す"},
    422: {"nidanaId": "release", "pathFactors": ["正精進", "正念"], "reason": "垢を洗い勇者として歩む"},
    423: {"nidanaId": "review", "pathFactors": ["正念", "正見"], "reason": "宿命・生尽・完成を静かに振り返る"},
}

LABEL_TO_ID = {
    "正見": "view", "正思惟": "intention", "正語": "speech", "正業": "action",
    "正命": "livelihood", "正精進": "effort", "正念": "mindfulness", "正定": "concentration",
}

PAIR_META = [
    ("DP26-P01", 383),
    ("DP26-P02", 384),
    ("DP26-P03", 385),
    ("DP26-P04", 386),
    ("DP26-P05", 387),
    ("DP26-P06", 388),
    ("DP26-P07", 389),
    ("DP26-P08", 390),
    ("DP26-P09", 391),
    ("DP26-P10", 392),
    ("DP26-P11", 393),
    ("DP26-P12", 394),
    ("DP26-P13", 395),
    ("DP26-P14", 396),
    ("DP26-P15", 397),
    ("DP26-P16", 398),
    ("DP26-P17", 399),
    ("DP26-P18", 400),
    ("DP26-P19", 401),
    ("DP26-P20", 402),
    ("DP26-P21", 403),
    ("DP26-P22", 404),
    ("DP26-P23", 405),
    ("DP26-P24", 406),
    ("DP26-P25", 407),
    ("DP26-P26", 408),
    ("DP26-P27", 409),
    ("DP26-P28", 410),
    ("DP26-P29", 411),
    ("DP26-P30", 412),
    ("DP26-P31", 413),
    ("DP26-P32", 414),
    ("DP26-P33", 415),
    ("DP26-P34", 417),
    ("DP26-P35", 418),
    ("DP26-P36", 419),
    ("DP26-P37", 420),
    ("DP26-P38", 421),
    ("DP26-P39", 422),
    ("DP26-P40", 423),
]

NOTE = "パーリ偈との内容対応（蘇錦坤『法句経』偈頌對照表）。品内番号・品名はパーリとずれる場合あり。"


def chinese_block(verse):
    c = dict(CHINESE[verse])
    c["satUrl"] = SAT_URL
    c["mapTableUrl"] = MAP_URL
    if c.get("status") == "mapped":
        c.setdefault("note", NOTE)
    return c


def main():
    old = json.loads((DATA / "ch26.json").read_text(encoding="utf-8"))
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
                    "locus": f"小部・ダンマパダ 婆羅門の章 第{verse}偈",
                    "url": ARANA_URL,
                },
                "modern": {
                    "source": "true-buddhism（南伝大蔵経系・現代語表記）",
                    "locus": f"第２６章・婆羅門品 第{verse}偈（#ch02-26）",
                    "url": TB_URL,
                },
                "chinese": chinese_block(verse),
            },
        })

    # normalize keys if json dumped as str
    for p in pairs:
        if not isinstance(p["observe"], str):
            raise SystemExit("bad observe")

    by_nidana = defaultdict(list)
    for p in pairs:
        by_nidana[p["nidanaId"]].append(p["id"])

    TITLE = "ダンマパダ 第26章・婆羅門品（婆羅門の章）"
    SHORT = "婆羅門品（婆羅門の章）"
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
            "pathLabel": "仏の光明・真実と法・道非道に触れ、一日を始める",
            "chapterHint": SHORT,
            "fromPrev": "前夜の無一物の見直しが、今朝の光明への接触になる",
            "toNext": "接触のあと、忍辱と不染の受が立ち上がる",
            "todayObserve": OBSERVE[387],
            "todayAction": actions["DP26-P05"],
            "when": ["朝の始まり", "外見より内実を確かめる"],
            "sources": by_nidana.get("contact", []),
            "leadQuote": QUOTES[387][:40] + "…",
            "secondaryObserve": "辮髪ではなく、誠行・法行・清白が婆羅門",
        },
        {
            "id": "feeling", "weekday": 2, "categoryId": "mindfulness", "nidanaLabel": "受ける",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "罵詈を忍辱で受け、欲に染まらず柔和に住む",
            "chapterHint": SHORT,
            "fromPrev": "法に触れたあと、打たれ・欲・敵意の受が来る",
            "toNext": "受けた不快を、可意や家への欲しがりへ落とさない",
            "todayObserve": OBSERVE[399],
            "todayAction": actions["DP26-P17"],
            "when": ["不当な扱いを受けた", "欲の対象に触れた"],
            "sources": by_nidana.get("feeling", []),
            "leadQuote": QUOTES[399][:40] + "…",
            "secondaryObserve": "蓮葉に水が染まらぬが如く、五欲に染まらぬ",
        },
        {
            "id": "craving", "weekday": 3, "categoryId": "mindfulness", "nidanaLabel": "欲しがる／拒む",
            "pathFactors": ["正念", "正思惟"], "pathFactorIds": ["mindfulness", "intention"],
            "pathLabel": "可意・外見・少欲・家欲への欲しがりを緩める",
            "chapterHint": SHORT,
            "fromPrev": "受が強まると、可意や世間への欲しがりへ",
            "toNext": "止めないと身語意・結縛の掴みへ進む",
            "todayObserve": OBSERVE[390],
            "todayAction": actions["DP26-P08"],
            "when": ["強く惹かれる", "持ちすぎ・求めすぎ"],
            "sources": by_nidana.get("craving", []),
            "leadQuote": QUOTES[390][:40] + "…",
            "secondaryObserve": "少求寡欲、家への欲しがりを捨てよ",
        },
        {
            "id": "clinging", "weekday": 4, "categoryId": "mindfulness", "nidanaLabel": "掴む",
            "pathFactors": ["正念", "正業"], "pathFactorIds": ["mindfulness", "action"],
            "pathLabel": "敵対・我執・慢・不与取・結縛を掴まず浄む",
            "chapterHint": SHORT,
            "fromPrev": "欲しがりが、敵対・所有・慢として掴む手前",
            "toNext": "掴むと苦の重担と輪廻が見える",
            "todayObserve": OBSERVE[396],
            "todayAction": actions["DP26-P14"],
            "when": ["これは私のものだ", "慢心が湧いた"],
            "sources": by_nidana.get("clinging", []),
            "leadQuote": QUOTES[396][:40] + "…",
            "secondaryObserve": "与えられていないものを取らず、結縛を掴まぬ",
        },
        {
            "id": "suffering", "weekday": 5, "categoryId": "view", "nidanaLabel": "苦が太る",
            "pathFactors": ["正見", "正念"], "pathFactorIds": ["view", "mindfulness"],
            "pathLabel": "苦の重担と輪廻・愚痴の塹を見て下ろす",
            "chapterHint": SHORT,
            "fromPrev": "掴んだ結果として、苦と輪廻の塹が熟す",
            "toNext": "見れば、流れを断ち結縛を断つ実践へ向き直る",
            "todayObserve": OBSERVE[402],
            "todayAction": actions["DP26-P20"],
            "when": ["重担を感じた", "迷いの塹に落ちそう"],
            "sources": by_nidana.get("suffering", []),
            "leadQuote": QUOTES[402][:40] + "…",
            "secondaryObserve": "危険・悪趣・輪廻・愚痴を超えて彼岸へ",
        },
        {
            "id": "release", "weekday": 6, "categoryId": "effort", "nidanaLabel": "気づいて離す",
            "pathFactors": ["正精進", "正念"], "pathFactorIds": ["effort", "mindfulness"],
            "pathLabel": "流れを断ち、結縛を断ち、勇者として離す",
            "chapterHint": SHORT,
            "fromPrev": "苦が見えれば、止観と離欲へ向き直る",
            "toNext": "離すと、善悪を超えた夜の見直しへつながる",
            "todayObserve": OBSERVE[383],
            "todayAction": actions["DP26-P01"],
            "when": ["欲の流れを断つ", "垢を洗って歩く"],
            "sources": by_nidana.get("release", []),
            "leadQuote": QUOTES[383][:40] + "…",
            "secondaryObserve": "一切の結縛を断ち、楽不楽を捨て清涼となる",
        },
        {
            "id": "review", "weekday": 0, "categoryId": "concentration", "nidanaLabel": "夜に見直す",
            "pathFactors": ["正定", "正念"], "pathFactorIds": ["concentration", "mindfulness"],
            "pathLabel": "善悪を超え、月のように清明に、前中後を手放す",
            "chapterHint": SHORT,
            "fromPrev": "一日の行いは、婆羅門として歩んだかの跡",
            "toNext": "見直しが、翌朝の光明への接触になる",
            "todayObserve": OBSERVE[412] + " " + OBSERVE[421],
            "todayAction": actions["DP26-P30"],
            "when": ["一日を閉じるとき", "完成への一歩を確かめる"],
            "sources": by_nidana.get("review", []),
            "leadQuote": QUOTES[412][:40] + "…",
            "secondaryObserve": "于前于後、乃中無有──無一物にして執着なし",
        },
    ]

    out = {
        "title": TITLE,
        "chapter": 26,
        "shortTitle": SHORT,
        "source": {
            "primary": "パーリ・ダンマパダ第26章（婆羅門品／婆羅門の章）偈単位対応",
            "note": "経典の言葉＝アラナ精舎和訳、現代語訳＝true-buddhism掲載文、対応漢訳＝SAT法句経（T210梵志品）を偈単位でマッピング。",
            "verifyLinks": {
                "pali": {"label": "アラナ精舎（ダンマパダ・婆羅門の章）", "url": ARANA_URL, "note": "パーリ和訳出典"},
                "modern": {"label": "true-buddhism（第２６章・婆羅門品）", "url": TB_URL, "note": "南伝大蔵経系の現代語表記"},
                "chinese": {"label": "SAT 法句経・梵志品（T4.572b）", "url": SAT_URL, "note": "漢訳対応は偈ごとに異なる。対応表: 蘇錦坤"},
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
            "focusReason": "婆羅門品は流れ・結縛を断ち解脱する実践が中心。既定の焦点は離す。表示は現在の偈の縁起に合わせる。",
            "selectionMode": "pair-nidana",
        },
        "pairs": pairs,
        "versePracticeMap": {str(k): v for k, v in VERSE_PRACTICE.items()},
    }

    (DATA / "ch26.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote ch26.json", len(pairs))

    PATH_ORDER = ["view", "intention", "speech", "action", "livelihood", "effort", "mindfulness", "concentration"]
    entries = {k: [] for k in PATH_ORDER}
    for ch_id in range(1, 27):
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

    psi = {"version": 1, "scope": "dhammapada-ch1-ch26", "entries": entries}
    (DATA / "path-scene-index.json").write_text(json.dumps(psi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("path-scene-index", psi["scope"])

    valid = {"contact", "feeling", "craving", "clinging", "suffering", "release", "review"}
    bad = [(p["id"], p["nidanaId"]) for p in pairs if p["nidanaId"] not in valid]
    assert not bad, bad
    assert len(pairs) == 40
    assert all(p["id"] == f"DP26-P{i:02d}" for i, p in enumerate(pairs, 1))
    assert set(VERSE_PRACTICE) == set(range(383, 424))
    assert 416 not in [p["verse"] for p in pairs]
    assert all(p["alignment"]["chinese"]["status"] in ("mapped", "unmapped") for p in pairs)
    unmapped_ids = [p["id"] for p in pairs if p["alignment"]["chinese"]["status"] == "unmapped"]
    assert unmapped_ids == ["DP26-P07", "DP26-P08", "DP26-P36"], unmapped_ids
    assert set(by_nidana) == valid
    print("OK")


if __name__ == "__main__":
    main()
