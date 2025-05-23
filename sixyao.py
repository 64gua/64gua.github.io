# -*- coding: utf-8 -*-#
import random, datetime, os,itertools, time, sxtwl,pickle
#经验：要对齐中文，打印的空格也必须是全角
#log=open("c:\\pythoncode\iching\log.txt", mode="w", encoding = "utf-8")      
#print(guadetails, file = log)    guacont=f.read()

dic64GuaName={11: '乾为天', 12: '天泽履', 13: '天火同人', 14: '天雷无妄', 15: '天风姤', 16: '天水讼', 17: '天山遁', 18: '天地否',
              21: '泽天夬', 22: '兑为泽', 23: '泽火革', 24: '泽雷随', 25: '泽风大过', 26: '泽水困', 27: '泽山咸', 28: '泽地萃',
              31: '火天大有', 32: '火泽睽', 33: '离为火', 34: '火雷噬嗑', 35: '火风鼎', 36: '火水未济', 37: '火山旅', 38: '火地晋',
              41: '雷天大壮', 42: '雷泽归妹', 43: '雷火丰', 44: '震为雷', 45: '雷风恒', 46: '雷水解', 47: '雷山小过', 48: '雷地豫',
              51: '风天小畜', 52: '风泽中孚', 53: '风火家人', 54: '风雷益', 55: '巽为风', 56: '风水涣', 57: '风山渐', 58: '风地观',
              61: '水天需', 62: '水泽节', 63: '水火既济', 64: '水雷屯', 65: '水风井', 66: '坎为水', 67: '水山蹇', 68: '水地比',
              71: '山天大畜', 72: '山泽损', 73: '山火贲', 74: '山雷颐', 75: '山风蛊', 76: '山水蒙', 77: '艮为山', 78: '山地剥',
              81: '地天泰', 82: '地泽临', 83: '地火明夷', 84: '地雷复', 85: '地风升', 86: '地水师', 87: '地山谦', 88: '坤为地'}

dic64GuaShort={11: '乾', 12: '履', 13: '同人', 14: '无妄', 15: '姤', 16: '讼', 17: '遁', 18: '否',
               21: '夬', 22: '兑', 23: '革', 24: '随', 25: '大过', 26: '困', 27: '咸', 28: '萃',
               31: '大有', 32: '睽', 33: '离', 34: '噬嗑', 35: '鼎', 36: '未济', 37: '旅', 38: '晋',
               41: '大壮', 42: '归妹', 43: '丰', 44: '震', 45: '恒', 46: '解', 47: '小过', 48: '豫',
               51: '小畜', 52: '中孚', 53: '家人', 54: '益', 55: '巽', 56: '涣', 57: '渐', 58: '观',
               61: '需', 62: '节', 63: '既济', 64: '屯', 65: '井', 66: '坎', 67: '蹇', 68: '比',
               71: '大畜', 72: '损', 73: '贲', 74: '颐', 75: '蛊', 76: '蒙', 77: '艮', 78: '剥',
               81: '泰', 82: '临', 83: '明夷', 84: '复', 85: '升', 86: '师', 87: '谦', 88: '坤'}

dicEightGongCode={
                 1: [11,15,17,18,58,78,38,31],
                 2:[22,26,28,27,67,87,47,42],
                 3:[33,37,35,36,76,56,16,13],
                 4:[44,48,46,45,85,65,25,24],
                 5:[55,51,53,54, 14,34,74,75],
                 6:[66,62, 64, 63, 23, 43, 83, 86],
                 7:[77,73, 71, 72, 32, 12, 52, 57],
                 8:[88, 84, 82,81, 41, 21, 61, 68]
                          }

dicGuaName={ 1: ['乾', '姤', '遁', '否', '观', '剥', '晋', '大有'],
                        2: ['兑', '困', '萃', '咸', '蹇', '谦', '小过', '归妹'],
                        3: ['离', '旅', '鼎', '未济', '蒙', '涣', '讼', '同人'],
                        4: ['震', '豫', '解', '恒', '升', '井', '大过', '随'],
                        5: ['巽', '小畜', '家人', '益', '无妄', '噬嗑', '颐', '蛊'],
                        6: ['坎', '节', '屯', '既济', '革', '丰', '明夷', '师'],
                        7: ['艮', '贲', '大畜', '损', '睽', '履', '中孚', '渐'],
                        8: ['坤', '复', '临', '泰', '大壮', '夬', '需', '比']
                       }

dicWuXing={1: ["戌土","申金","午火","辰土","寅木","子水"],
                      2: ["未土","酉金","亥水","丑土","卯木","巳火"],
                      3: ["巳火","未土","酉金","亥水","丑土","卯木"],
                      4: ["戌土","申金","午火","辰土","寅木","子水"],
                      5: ["卯木","巳火","未土","酉金","亥水","丑土"],
                      6: ["子水","戌土","申金","午火","辰土","寅木"],
                      7: ["寅木","子水","戌土","申金","午火","辰土"],
                      8: ["酉金","亥水","丑土","卯木","巳火","未土"]
                 }

dicSixFamily={1: {"金":"兄弟","水": "子孙","木":"妻财", "火":"官鬼","土":"父母"},
                       2: {"金":"兄弟","水": "子孙","木":"妻财", "火":"官鬼","土":"父母"},
                       3: {"火":"兄弟","土": "子孙","金":"妻财", "水":"官鬼","木":"父母"},
                       4: {"木":"兄弟","火": "子孙","土":"妻财", "金":"官鬼","水":"父母"},
                       5: {"木":"兄弟","火": "子孙","土":"妻财", "金":"官鬼","水":"父母"},
                       6: {"水":"兄弟","木": "子孙","火":"妻财", "土":"官鬼","金":"父母"},
                       7: {"土":"兄弟","金": "子孙","水":"妻财", "木":"官鬼","火":"父母"},
                       8: {"土":"兄弟","金": "子孙","水":"妻财", "木":"官鬼","火":"父母"}
                        }
             
#乾1: 111, 阳阳阳  兑2： 阴阳阳
yaoxianglist = ["111","211","121","221","112","212","122", "222"]
str1 ="天泽火雷风水山地"
str2 ="乾兑离震巽坎艮坤"

tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
dizhiOrder=[ '亥','子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌']
#每个卦的世爻应爻位置
dicSY =  {('乾', '坎', '坤', '离', '震', '艮', '巽', '兑'): '100200      ',
        ('姤', '豫', '节', '贲', '复', '小畜', '旅', '困'): '002001      ',
        ('遁', '解', '屯', '大畜', '临', '家人', '鼎', '萃'): '020010      ',
        ('否', '恒', '既济', '损', '泰', '益', '未济', '咸'): '200100      ',
        ('观', '升', '革', '睽', '大壮', '无妄', '蒙', '蹇'): '001002      ',
        ('剥', '井', '丰', '履', '夬', '噬嗑', '涣', '谦'): '010020      ',
        ('晋', '大过', '明夷', '中孚', '需', '颐', '讼', '小过'): '001002(游魂)',
        ('大有', '随', '师', '渐', '比', '蛊', '同人', '归妹'): '200100(归魂)'}

dicSixSheng={"甲":   ["玄武","白虎","腾蛇","勾陈","朱雀","青龙"],
                       "乙" :  ["玄武","白虎","腾蛇","勾陈","朱雀","青龙"],
                       "丙":   ["青龙","玄武","白虎","腾蛇","勾陈","朱雀"],
                       "丁":   ["青龙","玄武","白虎","腾蛇","勾陈","朱雀"],
                       "戊":   ["朱雀","青龙","玄武","白虎","腾蛇","勾陈"],
                        "己":  ["勾陈","朱雀","青龙","玄武","白虎","腾蛇"],
                         "庚": ["腾蛇","勾陈","朱雀","青龙","玄武","白虎"],
                        "辛":  ["腾蛇","勾陈","朱雀","青龙","玄武","白虎"],
                        "壬":  ["白虎","腾蛇","勾陈","朱雀","青龙","玄武"],
                        "癸":  ["白虎","腾蛇","勾陈","朱雀","青龙","玄武"]
                      }

dicXunKong={"戌亥": ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉'],
                      "申酉":['甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未'],
                      "午未": ['甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳'],
                      "辰巳":['甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯'],
                      "寅卯": ['甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑'],
                      "子丑":['甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']   }
dicIching={'乾': {0: '乾，本卦。元，亨，利，贞。用九：见群龙无首，吉。', 1: '初九：潜龙，勿用。', 2: '九二：见龙在田，利见大人。', 3: '九三：君子终日乾乾，夕惕若，厉无咎。', 4: '九四：或跃在渊，无咎。', 5: '九五：飞龙在天，利见大人。', 6: '上九：亢龙有悔。', 7: '彖︰大哉乾元，万物资始，乃统天。云行雨施，品物流形，大明终始，六位时成，时乘六龙以御天。乾道变化，各正性命，保合大和，乃利贞。首出庶物，万国咸宁。'},
           '坤': {0: '坤，元，亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。 安贞，吉。用六：利永贞。', 1: '初六：履霜，坚冰至。', 2: '六二：直，方，大，不习无不利。', 3: '六三：含章可贞。 或从王事，无成有终。', 4: '六四：括囊﹔无咎，无誉。', 5: '六五：黄裳，元吉。', 6: '上六：龙战于野，其血玄黄。', 7: '彖︰至哉坤元，万物资生，乃顺承天。坤厚载物，德合无疆，含弘光大，品物咸亨。牝马地类，行地无疆，柔顺利贞。君子攸行，先迷失道，后顺得常。西南得朋，乃与类行。东北丧朋，乃终有庆。安贞之吉，应地无疆。'}, 
           '否': {0: '否之匪人，不利君子贞，大往小来。', 1: '初六：拔茅茹，以其夤，贞吉亨。', 2: '六二：包承。 小人吉，大人否亨。', 3: '六三：包羞。', 4: '九四：有命无咎，畴离祉。', 5: '九五：休否，大人吉。 其亡其亡，系于苞桑。', 6: '上九：倾否，先否后喜。', 7: '彖︰否之匪人，不利君子贞，大往小来，则是天地不交而万物不通也，上下不交而天下无邦也。内阴而外阳，内柔而外刚，内小人而外君子。小人道长，君子道消也。'}, 
           '遁': {0: '亨，小利贞。', 1: '初六：遯尾，厉，勿用有攸往。', 2: '六二：执之用黄牛之革，莫之胜说。', 3: '九三：系遯，有疾厉，畜臣妾吉。', 4: '九四：好遯君子吉，小人否。', 5: '九五：嘉遯，贞吉。', 6: '上九：肥遯，无不利。', 7: '彖︰遯亨，遯而亨也。刚当位而应，与时行也。小利贞，浸而长也。遯之时义大矣哉。'}, 
           '讼': {0: '有孚，窒。 惕中吉。 终凶。 利见大人，不利涉大川。', 1: '初六：不永所事，小有言，终吉。', 2: '九二：不克讼，归而逋，其邑人三百户，无眚。', 3: '六三：食旧德，贞厉，终吉，或从王事，无成。', 4: '九四：不克讼，复自命，渝安贞，吉。', 5: '九五：讼元吉。', 6: '上九：或锡之鞶带，终朝三褫之。', 7: '彖︰讼，上刚下险，险而健，讼。讼有孚，窒惕，中吉，刚来而得中也。终凶，讼不可成也。利见大人，尚中正也。不利涉大川，入于渊也。'}, 
           '姤': {0: '女壮，勿用取女。', 1: '初六：系于金柅，贞吉，有攸往，见凶，羸豕孚踟躅。', 2: '九二：包有鱼，无咎，不利宾。', 3: '九三：臀无肤，其行次且，厉，无大咎。', 4: '九四：包无鱼，起凶。', 5: '九五：以杞包瓜，含章，有陨自天。', 6: '上九：姤 其角，吝，无咎。', 7: '彖︰姤，遇也，柔遇刚也。勿用取女，不可与长也。天地相遇，品物咸章也；刚遇中正，天下大行也，姤之时义大矣哉。'}, 
           '无妄': {0: '元，亨，利，贞。 其匪正有眚，不利有攸往。', 1: '初九：无妄，往吉。', 2: '六二：不耕获，不菑畲，则利有攸往。', 3: '六三：无妄之灾，或系之牛，行人之得，邑人之灾。', 4: '九四：可贞，无咎。', 5: '九五：无妄之疾，勿药有喜。', 6: '上九：无妄，行有眚，无攸利。', 7: '彖︰无妄，刚自外来而为主于内，动而健，刚中而应，大亨以正，天之命也，其匪正有眚，不利有攸往。无妄之往，何之矣。天命不祐，行矣哉。'}, 
           '同人': {0: '同人于野，亨。 利涉大川，利君子贞。', 1: '初九：同人于门，无咎。', 2: '六二：同人于宗，吝。', 3: '九三：伏戎于莽，升其高陵，三岁不兴。', 4: '九四：乘其墉，弗克攻，吉。', 5: '九五：同人，先号啕而后笑。 大师克相遇。', 6: '上九：同人于郊，无悔。', 7: '彖︰同人，柔得位得中而应乎乾，曰同人。同人曰，同人于野，亨，利涉大川，乾行也。文明以健，中正而应，君子正也，唯君子为能通天下之志。'}, 
           '履': {0: '履虎尾，不咥人，亨。', 1: '初九：素履，往无咎。', 2: '九二：履道坦坦，幽人贞吉。', 3: '六三：眇能视，跛能履，履虎尾，咥人，凶。 武人为于大君。', 4: '九四：履虎尾，愬愬终吉。', 5: '九五：夬履，贞厉。', 6: '上九：视履考祥，其旋元吉。', 7: '彖︰履，柔履刚也。说而应乎乾，是以履虎尾，不咥人，亨。刚中正，履帝位而不疚，光明也。'}, 
           '兑': {0: '亨，利贞。', 1: '初九：和兑，吉。', 2: '九二：孚兑，吉，悔亡。', 3: '六三：来兑，凶。', 4: '九四：商兑，未宁，介疾有喜。', 5: '九五：孚于剥，有厉。', 6: '上六：引兑。', 7: '彖︰兑，说也。刚中而柔外，说以利贞，是以顺乎天而应乎人。说以先民，民忘其劳，说以犯难，民忘其死，说之大，民劝矣哉。'}, 
           '萃': {0: '亨。 王假有庙，利见大人，亨，利贞。 用大牲吉，利有攸往。', 1: '初六：有孚不终，乃乱乃萃，若号一握为笑，勿恤，往无咎。', 2: '六二：引吉，无咎，孚乃利用禴。', 3: '六三：萃如，嗟如，无攸利，往无咎，小吝。', 4: '九四：大吉，无咎。', 5: '九五：萃有位，无咎。 匪孚，元永贞，悔亡。', 6: '上六：齎咨涕洟，无咎。', 7: '彖︰萃，聚也。顺以说，刚中而应，故聚也。王假有庙，致孝享也；利见大人，亨，聚以正也；用大牲，吉，利有攸往，顺天命也。观其所聚，而天地万物之情可见矣。'}, 
           '咸': {0: '亨，利贞，取女吉。', 1: '初六：咸其拇。', 2: '六二：咸其腓，凶，居吉。', 3: '九三：咸其股，执其随，往吝。', 4: '九四：贞吉悔亡，憧憧往来，朋从尔思。', 5: '九五：咸其脢，无悔。', 6: '上六：咸其辅，颊，舌。', 7: '彖︰咸，感也。柔上而刚下，二气感应以相与，止而说，男下女，是以亨，利贞，取女吉也。天地感而万物化生，圣人感人心而天下和平。观其所感，而天地万物之情可见矣。'}, 
           '困': {0: '亨，贞，大人吉，无咎，有言不信。', 1: '初六：臀困于株木，入于幽谷，三岁不见。', 2: '九二：困于酒食，朱绂方来，利用亨祀，征凶，无咎。', 3: '六三：困于石，据于蒺藜，入于其宫，不见其妻，凶。', 4: '九四：来徐徐，困于金车，吝，有终。', 5: '九五：劓刖，困于赤绂，乃徐有说，利用祭祀。', 6: '上六：困于葛藟，于臲卼，曰动悔。 有悔，征吉。', 7: '彖︰困，刚揜也。险以说，困而不失其所亨，其唯君子乎。贞大人吉，以刚中也；有言不信，尚口乃穷也。'},
           '大过': {0: '栋桡，利有攸往，亨。', 1: '初六：藉用白茅，无咎。', 2: '九二：枯杨生稊，老夫得其女妻，无不利。', 3: '九三：栋桡，凶。', 4: '九四：栋隆，吉﹔有它吝。', 5: '九五：枯杨生华，老妇得士夫，无咎无誉。', 6: '上六：过涉灭顶，凶，无咎。', 7: '彖︰大过，大者过也。栋桡，本末弱也。刚过而中，巽而说行，利有攸往，乃亨，大过之时大矣哉。'},
           '随': {0: '元亨利贞，无咎。', 1: '初九：官有渝，贞吉。 出门交有功。', 2: '六二：係小子，失丈夫。', 3: '六三：係丈夫，失小子， 随有求得，利居贞。', 4: '九四：随有获，贞凶，有孚在道，以明，何咎。', 5: '九五：孚于嘉，吉。', 6: '上六：拘係之，乃从维之。 王用亨于西山。', 7: '彖︰随，刚来而下柔，动而说，随。大亨贞，无咎，而天下随时，随时之义大矣哉！'}, 
           '革': {0: '巳日乃孚，元亨利贞，悔亡。', 1: '初九：巩用黄牛之革。', 2: '六二：巳日乃革之，征吉，无咎。', 3: '九三：征凶，贞厉，革言三就，有孚。', 4: '九四：悔亡，有孚改命，吉。', 5: '九五：大人虎变，未占有孚。', 6: '上六：君子豹变，小人革面，征凶，居贞吉。', 7: '彖︰革，水火相息，二女同居，其志不相得，曰革。巳日乃孚；革而信也。文明以说，大亨以正，革而当，其悔乃亡。天地革而四时成，汤武革命，顺乎天而应乎人，革之时大矣哉！'}, 
           '夬': {0: '扬于王庭，孚号，有厉，告自邑，不利即戎，利有攸往。', 1: '初九：壮于前趾，往不胜为咎。', 2: '九二：惕号，莫夜有戎，勿恤。', 3: '九三：壮于頄，有凶。 君子夬夬，独行遇雨，若濡有愠，无咎。', 4: '九四：臀无肤，其行次且。 牵羊悔亡，闻言不信。', 5: '九五：苋陆夬夬，中行无咎。', 6: '上六：无号，终有凶。', 7: '彖︰夬，决也，刚决柔也。健而说，决而和，扬于王庭，柔乘五刚也。孚号有厉，其危乃光也。告自邑，不利即戎，所尚乃穷也。利有攸往，刚长乃终也。'}, 
           '离': {0: '利贞，亨。 畜牝牛，吉。', 1: '初九：履错然，敬之无咎。', 2: '六二：黄离，元吉。', 3: '九三：日昃之离，不鼓缶而歌，则大耋之嗟，凶。', 4: '九四：突如其来如，焚如，死如，弃如。', 5: '六五：出涕沱若，戚嗟若，吉。', 6: '上九：王用出征，有嘉折首，获其匪丑，无咎。', 7: '彖︰离，丽也；日月丽乎天，百穀草木丽乎土，重明以丽乎正，乃化成天下。柔丽乎中正，故亨；是以畜牝牛吉也。'}, 
           '晋': {0: '康侯用锡马蕃庶，昼日三接。', 1: '初六：晋如，摧如，贞吉。 罔孚，裕无咎。', 2: '六二：晋如，愁如，贞吉。 受兹介福，于其王母。', 3: '六三：众允，悔亡。', 4: '九四：晋如硕鼠，贞厉。', 5: '六五：悔亡，失得勿恤，往吉无不利。', 6: '上九：晋其角，维用伐邑，厉吉无咎，贞吝。', 7: '彖︰晋，进也。明出地上，顺而丽乎大明，柔进而上行。是以康侯用锡马蕃庶，昼日三接也。'},
           '旅': {0: '小亨，旅贞吉。', 1: '初六：旅琐琐，斯其所取灾。', 2: '六二：旅即次，怀其资，得童僕贞。', 3: '九三：旅焚其次，丧其童僕，贞厉。', 4: '九四：旅于处，得其资斧，我心不快。', 5: '六五：射雉一矢亡，终以誉命。', 6: '上九：鸟焚其巢，旅人先笑后号啕。 丧牛于易，凶。', 7: '彖︰旅，小亨，柔得中乎外，而顺乎刚，止而丽乎明，是以小亨，旅贞吉也。旅之时义大矣哉！'},
           '未济': {0: '亨，小狐汔济，濡其尾，无攸利。', 1: '初六：濡其尾，吝。', 2: '九二：曳其轮，贞吉。', 3: '六三：未济，征凶，利涉大川。', 4: '九四：贞吉，悔亡，震用伐鬼方，三年有赏于大国。', 5: '六五：贞吉，无悔，君子之光，有孚，吉。', 6: '上九：有孚于饮酒，无咎，濡其首，有孚失是。', 7: '彖︰未济，亨；柔得中也。小狐汔济，未出中也。濡其尾，无攸利；不续终也。虽不当位，刚柔应也。'}, 
           '鼎': {0: '元吉，亨。', 1: '初六：鼎颠趾，利出否，得妾以其子，无咎。', 2: '九二：鼎有实，我仇有疾，不我能即，吉。', 3: '九三：鼎耳革，其行塞，雉膏不食，方雨亏悔，终吉。', 4: '九四：鼎折足，覆公餗，其形渥，凶。', 5: '六五：鼎黄耳金铉，利贞。', 6: '上九：鼎玉铉，大吉，无不利。', 7: '彖︰鼎，象也。以木巽火，亨饪也。圣人亨以享上帝，而大亨以养圣贤。巽而耳目聪明，柔进而上行，得中而应乎刚，是以元亨。'}, 
           '噬嗑': {0: '亨。 利用狱。', 1: '初九：履校灭趾，无咎。', 2: '六二：噬肤灭鼻，无咎。', 3: '六三：噬腊肉，遇毒﹔小吝，无咎。', 4: '九四：噬乾胏，得金矢，利艰贞，吉。', 5: '六五：噬乾肉，得黄金，贞厉，无咎。', 6: '上九：何校灭耳，凶。', 7: '彖︰颐中有物，曰噬嗑，噬嗑而亨。刚柔分，动而明，雷电合而章。柔得中而上行，虽不当位，利用狱也。'},
           '睽': {0: '小事吉。', 1: '初九：悔亡，丧马勿逐，自复﹔见恶人无咎。', 2: '九二：遇主于巷，无咎。', 3: '六三：见舆曳，其牛掣，其人天且劓，无初有终。', 4: '九四：睽孤，遇元夫，交孚，厉无咎。', 5: '六五：悔亡，厥宗噬肤，往何咎。', 6: '上九：睽孤， 见豕负涂，载鬼一车， 先张之弧，后说之弧，匪寇婚媾，往遇雨则吉。', 7: '彖︰睽，火动而上，泽动而下；二女同居，其志不同行；说而丽乎明，柔进而上行，得中而应乎刚；是以小事吉。天地睽，而其事同也；男女睽，而其志通也；万物睽，而其事类也；睽之时用大矣哉！'}, 
           '大有': {0: '元亨。', 1: '初九：无交害，匪咎，艰则无咎。', 2: '九二：大车以载，有攸往，无咎。', 3: '九三：公用亨于天子，小人弗克。', 4: '九四：匪其彭，无咎。', 5: '六五：厥孚交如，威如﹔吉。', 6: '上九：自天佑之，吉无不利。', 7: '彖︰大有，柔得尊位，大中而上下应之，曰大有。其德刚健而文明，应乎天而时行，是以元亨。'},
           '震': {0: '亨。 震来虩虩，笑言哑哑。 震惊百里，不丧匕鬯。', 1: '初九：震来虩虩，后笑言哑哑，吉。', 2: '六二：震来厉，亿丧贝，跻于九陵，勿逐，七日得。', 3: '六三：震苏苏，震行无眚。', 4: '九四：震遂泥。', 5: '六五：震往来厉，亿无丧，有事。', 6: '上六：震索索，视矍矍，征凶。 震不于其躬，于其邻，无咎。 婚媾有言。', 7: '彖︰震，亨。震来虩虩，恐致福也。笑言哑哑，后有则也。震惊百里，惊远而惧迩也。出可以守宗庙社稷，以为祭主也'},
           '豫': {0: '利建侯行师。', 1: '初六：鸣豫，凶。', 2: '六二：介于石，不终日，贞吉。', 3: '六三：盱豫，悔。 迟有悔。', 4: '九四：由豫，大有得。勿疑。 朋盍簪。', 5: '六五：贞疾，恆不死。', 6: '上六：冥豫，成有渝，无咎。', 7: '彖︰豫，刚应而志行，顺以动，豫。豫，顺以动，故天地如之，而况建侯行师乎？天地以顺动，故日月不过，而四时不忒；圣人以顺动，则刑罚清而民服。豫之时义大矣哉！'}, 
           '小过': {0: '亨，利贞，可小事，不可大事。飞鸟遗之音，不宜上宜下，大吉。', 1: '初六：飞鸟以凶。', 2: '六二：过其祖，遇其妣；不及其君，遇其臣；无咎。', 3: '九三：弗过防之，从或戕之，凶。', 4: '九四：无咎，弗过遇之。 往厉必戒，勿用永贞。', 5: '六五：密云不雨，自我西郊，公弋取彼在穴。', 6: '上六：弗遇过之，飞鸟离之，凶，是谓灾眚。', 7: '彖︰小过，小者过而亨也。过以利贞，与时行也。柔得中，是以小事吉也。刚失位而不中，是以不可大事也。有飞鸟之象焉，有飞鸟遗之音，不宜上宜下，大吉；上逆而下顺也。'},
           '解': {0: '利西南，无所往，其来复吉。 有攸往，夙吉。', 1: '初六：无咎。', 2: '九二：田获三狐，得黄矢，贞吉。', 3: '六三：负且乘，致寇至，贞吝。', 4: '九四：解而拇，朋至斯孚。', 5: '六五：君子维有解，吉；有孚于小人。', 6: '上六：公用射隼，于高墉之上，获之，无不利。', 7: '彖︰解，险以动，动而免乎险，解。解利西南，往得众也。其来复吉，乃得中也。有攸往夙吉，往有功也。天地解，而雷雨作，雷雨作，而百果草木皆甲坼，解之时大矣哉！'}, 
           '恒': {0: '亨，无咎，利贞，利有攸往。', 1: '初六：浚恆，贞凶，无攸利。', 2: '九二：悔亡。', 3: '九三：不恆其德，或承之羞，贞吝。', 4: '九四：田无禽。', 5: '六五：恆其德，贞，妇人吉，夫子凶。', 6: '上六：振恆，凶。', 7: '彖︰恆，久也。刚上而柔下，雷风相与，巽而动，刚柔皆应，恆。恆亨无咎，利贞；久于其道也，天地之道，恆久而不已也。利有攸往，终则有始也。日月得天，而能久照，四时变化，而能久成，圣人久于其道，而天下化成；观其所恆，而天地万物之情可见矣！'}, 
           '丰': {0: '亨，王假之，勿忧，宜日中。', 1: '初九：遇其配主，虽旬无咎，往有尚。', 2: '六二：丰其蔀，日中见斗，往得疑疾，有孚发若，吉。', 3: '九三：丰其沛，日中见昧，折其右肱，无咎。', 4: '九四：丰其蔀，日中见斗，遇其夷主，吉。', 5: '六五：来章，有庆誉，吉。', 6: '上六：丰其屋，蔀其家，窥其户，阒其无人，三岁不见，凶。', 7: '彖︰丰，大也。明以动，故丰。王假之，尚大也。勿忧宜日中，宜照天下也。日中则昃，月盈则食，天地盈虚，与时消息，而况人于人乎？况于鬼神乎？'},
           '归妹': {0: '征凶，无攸利。', 1: '初九：归妹以娣，跛能履，征吉。', 2: '九二：眇能视，利幽人之贞。', 3: '六三：归妹以须，反归以娣。', 4: '九四：归妹愆期，迟归有时。', 5: '六五：帝乙归妹，其君之袂，不如其娣之袂良，月几望，吉。', 6: '上六：女承筐无实，士刲羊无血，无攸利。', 7: '彖︰归妹，天地之大义也。天地不交，而万物不兴，归妹人之终始也。说以动，所归妹也。征凶，位不当也。无攸利，柔乘刚也。'},
           '大壮': {0: '利贞。', 1: '初九：壮于趾，征凶，有孚。', 2: '九二：贞吉。', 3: '九三：小人用壮，君子用罔，贞厉。 羝羊触藩，羸其角。', 4: '九四：贞吉悔亡，藩决不羸，壮于大舆之輹。', 5: '六五：丧羊于易，无悔。', 6: '上六：羝羊触藩，不能退，不能遂，无攸利，艰则吉。', 7: '彖︰大壮，大者壮也。刚以动，故壮。大壮利贞；大者正也。正大而天地之情可见矣！'}, 
           '巽': {0: '小亨，利攸往，利见大人。', 1: '初六：进退，利武人之贞。', 2: '九二：巽在床下，用史巫纷若，吉无咎。', 3: '九三：频巽，吝。', 4: '六四：悔亡，田获三品。', 5: '九五：贞吉悔亡，无不利。 无初有终，先庚三日，后庚三日，吉。', 6: '上九：巽在床下，丧其资斧，贞凶。', 7: '彖︰重巽以申命，刚巽乎中正而志行。柔皆顺乎刚，是以小亨，利有攸往，利见大人。'},
           '观': {0: '盥而不荐，有孚顒若。', 1: '初六：童观，小人无咎，君子吝。', 2: '六二：窥观，利女贞。', 3: '六三：观我生，进退。', 4: '六四：观国之光，利用宾于王。', 5: '九五：观我生，君子无咎。', 6: '上九：观其生，君子无咎。', 7: '彖︰大观在上，顺而巽，中正以观天下。观，盥而不荐，有孚顒若，下观而化也。观天之神道，而四时不忒，圣人以神道设教，而天下服矣。'},
           '渐': {0: '女归吉，利贞。', 1: '初六：鸿渐于干，小子厉，有言，无咎。', 2: '六二：鸿渐于磐，饮食衎衎，吉。', 3: '九三：鸿渐于陆，夫征不复，妇孕不育，凶；利御寇。', 4: '六四：鸿渐于木，或得其桷，无咎。', 5: '九五：鸿渐于陵，妇三岁不孕，终莫之胜，吉。', 6: '上九：鸿渐于逵，其羽可用为仪，吉。', 7: '彖︰渐之进也，女归吉也。进得位，往有功也。进以正，可以正邦也。其位刚，得中也。止而巽，动不穷也。'}, 
           '涣': {0: '亨。 王假有庙，利涉大川，利贞。', 1: '初六：用拯马壮，吉。', 2: '九二：涣奔其机，悔亡。', 3: '六三：涣其躬，无悔。', 4: '六四：涣其群，元吉。 涣有丘，匪夷所思。', 5: '九五：涣汗其大号，涣王居，无咎。', 6: '上九：涣其血，去逖出，无咎。', 7: '彖︰涣，亨。刚来而不穷，柔得位乎外而上同。王假有庙，王乃在中也。利涉大川，乘木有功也。'},
           '益': {0: '利有攸往，利涉大川。', 1: '初九：利用为大作，元吉，无咎。', 2: '六二：或益之，十朋之龟弗克违，永贞吉。 王用享于帝，吉。', 3: '六三：益之用凶事，无咎。 有孚中行，告公用圭。', 4: '六四：中行，告公从。 利用为依迁国。', 5: '九五：有孚惠心，勿问元吉。 有孚惠我德。', 6: '上九：莫益之，或击之，立心勿恆，凶。', 7: '彖︰益，损上益下，民说无疆，自上下下，其道大光。利有攸往，中正有庆。利涉大川，木道乃行。益动而巽，日进无疆。天施地生，其益无方。凡益之道，与时偕行。'},
           '家人': {0: '利女贞。', 1: '初九：闲有家，悔亡。', 2: '六二：无攸遂，在中馈，贞吉。', 3: '九三：家人嗃嗃，悔厉吉﹔妇子嘻嘻，终吝。', 4: '六四：富家，大吉。', 5: '九五：王假有家，勿恤吉。', 6: '上九：有孚威如，终吉。', 7: '彖︰家人，女正位乎内，男正位乎外，男女正，天地之大义也。家人有严君焉，父母之谓也。父父，子子，兄兄，弟弟，夫夫，妇妇，而家道正；正家而天下定矣。'},
           '中孚': {0: '豚鱼吉，利涉大川，利贞。', 1: '初九：虞吉，有他不燕。', 2: '九二：鸣鹤在阴，其子和之，我有好爵，吾与尔靡之。', 3: '六三：得敌，或鼓或罢，或泣或歌。', 4: '六四：月几望，马匹亡，无咎。', 5: '九五：有孚挛如，无咎。', 6: '上九：翰音登于天，贞凶。', 7: '彖︰中孚，柔在内而刚得中。说而巽，孚，乃化邦也。豚鱼吉，信及豚鱼也。利涉大川，乘木舟虚也。中孚以利贞，乃应乎天也。'}, 
           '小畜': {0: '亨。 密云不雨，自我西郊。', 1: '初九：复自道，何其咎，吉。', 2: '九二：牵复，吉。', 3: '九三：舆说辐，夫妻反目。', 4: '六四：有孚，血去惕出，无咎。', 5: '九五：有孚挛如，富以其邻。', 6: '上九：既雨既处，尚德载，妇贞厉。 月几望，君子征凶。', 7: '彖︰小畜，柔得位，而上下应之，曰小畜。健而巽，刚中而志行，乃亨。密云不雨，尚往也。自我西郊，施未行也。'}, 
           '坎': {0: '习坎，有孚，维心亨，行有尚。', 1: '初六：习坎，入于坎窞，凶。', 2: '九二：坎有险，求小得。', 3: '六三：来之坎坎，险且枕，入于坎窞，勿用。', 4: '六四：樽酒簋贰，用缶，纳约自牖，终无咎。', 5: '九五：坎不盈，只既平，无咎。', 6: '上六：係用徽纆，置于丛棘，三岁不得，凶。', 7: '彖︰习坎，重险也。水流而不盈，行险而不失其信。维心亨，乃以刚中也。行有尚，往有功也。天险不可升也，地险山川丘陵也，王公设险以守其国，坎之时用大矣哉！'}, 
           '比': {0: '吉。 原筮元永贞，无咎。 不宁方来，后夫凶。', 1: '初六：有孚比之，无咎。 有孚盈缶，终来有他，吉。', 2: '六二：比之自内，贞吉。', 3: '六三：比之匪人。', 4: '六四：外比之，贞吉。', 5: '九五：显比，王用三驱，失前禽。 邑人不戒，吉。', 6: '上六：比之无首，凶。', 7: '彖︰比，吉也，比，辅也，下顺从也。原筮元永贞，无咎，以刚中也。不宁方来，上下应也。后夫凶，其道穷也。'}, 
           '蹇': {0: '利西南，不利东北；利见大人，贞吉。', 1: '初六：往蹇，来誉。', 2: '六二：王臣蹇蹇，匪躬之故。', 3: '九三：往蹇来反。', 4: '六四：往蹇来连。', 5: '九五：大蹇朋来。', 6: '上六：往蹇来硕，吉；利见大人。', 7: '彖︰蹇，难也，险在前也。见险而能止，知矣哉！蹇利西南，往得中也；不利东北，其道穷也。利见大人，往有功也。当位贞吉，以正邦也。蹇之时用大矣哉！'}, 
           '井': {0: '改邑不改井，无丧无得，往来井井。汔至，亦未繘井，羸其瓶，凶。', 1: '初六：井泥不食，旧井无禽。', 2: '九二：井谷射鲋，瓮敝漏。', 3: '九三：井渫不食，为我民恻，可用汲，王明，并受其福。', 4: '六四：井甃，无咎。', 5: '九五：井冽，寒泉食。', 6: '上六：井收勿幕，有孚元吉。', 7: '彖︰巽乎水而上水，井；井养而不穷也。改邑不改井，乃以刚中也。汔至亦未繘井，未有功也。羸其瓶，是以凶也。'}, 
           '屯': {0: '元，亨，利，贞，勿用，有攸往，利建侯。', 1: '初九：磐桓﹔利居贞，利建侯。', 2: '六二：屯如邅如，乘马班如。 匪寇婚媾，女子贞不字，十年乃字。', 3: '六三：既鹿无虞，惟入于林中，君子几不如舍，往吝。', 4: '六四：乘马班如，求婚媾，无不利。', 5: '九五：屯其膏，小贞吉，大贞凶。', 6: '上六：乘马班如，泣血涟如。', 7: '彖︰屯，刚柔始交而难生，动乎险中，大亨贞。雷雨之动满盈，天造草昧，宜建侯而不宁。'}, 
           '既济': {0: '亨，小利贞，初吉终乱。', 1: '初九：曳其轮，濡其尾，无咎。', 2: '六二：妇丧其茀，勿逐，七日得。', 3: '九三：高宗伐鬼方，三年克之，小人勿用。', 4: '六四：繻有衣袽，终日戒。', 5: '九五：东邻杀牛，不如西邻之禴祭，实受其福。', 6: '上六：濡其首，厉。', 7: '彖︰既济，亨，小者亨也。利贞，刚柔正而位当也。初吉，柔得中也。终止则乱，其道穷也。'}, 
           '节': {0: '亨。 苦节不可贞。', 1: '初九：不出户庭，无咎。', 2: '九二：不出门庭，凶。', 3: '六三：不节若，则嗟若，无咎。', 4: '六四：安节，亨。', 5: '九五：甘节，吉﹔往有尚。', 6: '上六：苦节，贞凶，悔亡。', 7: '彖︰节，亨，刚柔分，而刚得中。苦节不可贞，其道穷也。说以行险，当位以节，中正以通。天地节而四时成，节以制度，不伤财，不害民。'}, 
           '需': {0: '有孚，光亨，贞吉。 利涉大川。', 1: '初九：需于郊。 利用恆，无咎。', 2: '九二：需于沙。 小有言，终吉。', 3: '九三：需于泥，致寇至。', 4: '六四：需于血，出自穴。', 5: '九五：需于酒食，贞吉。', 6: '上六：入于穴，有不速之客三人来，敬之终吉。', 7: '彖︰需，须也；险在前也。刚健而不陷，其义不困穷矣。需有孚，光亨，贞吉。位乎天位，以正中也。利涉大川，往有功也。'},
           '艮': {0: '艮其背，不获其身，行其庭，不见其人，无咎。', 1: '初六：艮其趾，无咎，利永贞。', 2: '六二：艮其腓，不拯其随，其心不快。', 3: '九三：艮其限，列其夤，厉薰心。', 4: '六四：艮其身，无咎。', 5: '六五：艮其辅，言有序，悔亡。', 6: '上九：敦艮，吉。', 7: '彖︰艮，止也。时止则止，时行则行，动静不失其时，其道光明。艮其止，止其所也。上下敌应，不相与也。是以不获其身，行其庭不见其人，无咎也。'}, 
           '剥': {0: '不利有攸往。', 1: '初六：剥床以足，蔑贞凶。', 2: '六二：剥床以辨，蔑贞凶。', 3: '六三：剥之，无咎。', 4: '六四：剥床以肤，凶。', 5: '六五：贯鱼，以宫人宠，无不利。', 6: '上九：硕果不食，君子得舆，小人剥庐。', 7: '彖︰剥，剥也，柔变刚也。不利有攸往，小人长也。顺而止之，观象也。君子尚消息盈虚，天行也。'}, 
           '蒙': {0: '亨。 匪我求童蒙，童蒙求我。 初噬告，再三渎，渎则不告。利贞。', 1: '初六：发蒙，利用刑人，用说桎梏，以往吝。', 2: '九二：包蒙吉，纳妇吉，子克家。', 3: '六三：勿用娶女，见金夫，不有躬，无攸利。', 4: '六四：困蒙，吝。', 5: '六五：童蒙，吉。', 6: '上九：击蒙，不利为寇，利御寇。', 7: '彖︰蒙，山下有险，险而止，蒙。蒙亨，以亨行时中也。匪我求童蒙，童蒙求我，志应也。初噬告，以刚中也。再三渎，渎则不告，渎蒙也。蒙以养正，圣功也。'}, 
           '蛊': {0: '元亨，利涉大川。 先甲三日，后甲三日。', 1: '初六：干父之蛊，有子考无咎，厉终吉。', 2: '九二：干母之蛊，不可贞。', 3: '九三：干父之蛊，小有悔，无大咎。', 4: '六四：裕父之蛊，往见吝。', 5: '六五：干父之蛊，用誉。', 6: '上九：不事王侯，高尚其事。', 7: '彖︰蛊，刚上而柔下，巽而止，蛊。蛊，元亨，而天下治也。利涉大川，往有事也。先甲三日，后甲三日，终则有始，天行也。'}, 
           '颐': {0: '贞吉。观颐，自求口实。', 1: '初九：舍尔灵龟，观我朵颐，凶。', 2: '六二：颠颐，拂经，与丘颐，征凶。', 3: '六三：拂颐，贞凶，十年勿用，无攸利。', 4: '六四：颠颐吉，虎视眈眈，其欲逐逐，无咎。', 5: '六五：拂经，居贞吉，不可涉大川。', 6: '上九：由颐，厉吉，利涉大川。', 7: '彖︰颐贞吉，养正则吉也。观颐，观其所养也；自求口实，观其自养也。天地养万物，圣人养贤，以及万民；颐之时大矣哉！'}, 
           '贲': {0: '亨。 小利有所往。', 1: '初九：贲其趾，舍车而徒。', 2: '六二：贲其须。', 3: '九三：贲如濡如，永贞吉。', 4: '六四：贲如皤如，白马翰如，匪寇婚媾。', 5: '六五：贲于丘园，束帛戋戋，吝，终吉。', 6: '上九：白贲，无咎。', 7: '彖︰贲，亨；柔来而文刚，故亨。分刚上而文柔，故小利有攸往。天文也；文明以止，人文也。观乎天文，以察时变；观乎人文，以化成天下。'},
           '损': {0: '有孚，元吉，无咎，可贞，利有攸往。曷之用，二簋可用享。', 1: '初九：已事遄往，无咎，酌损之。', 2: '九二：利贞，征凶，弗损益之。', 3: '六三：三人行，则损一人；一人行，则得其友。', 4: '六四：损其疾，使遄有喜，无咎。', 5: '六五：或益之，十朋之龟弗克违，元吉。', 6: '上九：弗损益之，无咎，贞吉，利有攸往，得臣无家。', 7: '彖︰损，损下益上，其道上行。损而有孚，元吉，无咎，可贞，利有攸往。曷之用？二簋可用享；二簋应有时。损刚益柔有时，损益盈虚，与时偕行。'},
           '大畜': {0: '利贞，不家食吉，利涉大川。', 1: '初九：有厉利已。', 2: '九二：舆说辐。', 3: '九三：良马逐，利艰贞。 曰闲舆卫，利有攸往。', 4: '六四：童牛之牿，元吉。', 5: '六五：豶豕之牙，吉。', 6: '上九：何天之衢，亨。', 7: '彖︰大畜，刚健笃实辉光，日新其德，刚上而尚贤。能止健，大正也。不家食吉，养贤也。利涉大川，应乎天也。'}, 
           '谦': {0: '亨，君子有终。', 1: '初六：谦谦君子，用涉大川，吉。', 2: '六二，鸣谦，贞吉。', 3: '九三，劳谦，君子有终，吉。', 4: '六四：无不利，撝谦。', 5: '六五：不富，以其邻，利用侵伐，无不利。', 6: '上六：鸣谦，利用行师，征邑国。', 7: '彖︰谦，亨，天道下济而光明，地道卑而上行。天道亏盈而益谦，地道变盈而流谦，鬼神害盈而福谦，人道恶盈而好谦。谦尊而光，卑而不可踰，君子之终也。'}, 
           '师': {0: '贞，丈人，吉无咎。', 1: '初六：师出以律，否臧凶。', 2: '九二：在师中，吉无咎，王三锡命。', 3: '六三：师或舆尸，凶。', 4: '六四：师左次，无咎。', 5: '六五：田有禽，利执言，无咎。长子帅师，弟子舆尸，贞凶。', 6: '上六：大君有命，开国承家，小人勿用。', 7: '彖︰师，众也，贞正也，能以众正，可以王矣。刚中而应，行险而顺，以此毒天下，而民从之，吉又何咎矣。'}, 
           '升': {0: '元亨，用见大人，勿恤，南征吉。', 1: '初六：允升，大吉。', 2: '九二：孚乃利用禴，无咎。', 3: '九三：升虚邑。', 4: '六四：王用亨于岐山，吉无咎。', 5: '六五：贞吉，升阶。', 6: '上六：冥升，利于不息之贞。', 7: '彖︰柔以时升，巽而顺，刚中而应，是以大亨；用见大人，勿恤，有庆也；南征吉，志行也。'}, 
           '复': {0: '亨。 出入无疾，朋来无咎。 反复其道，七日来复，利有攸往。', 1: '初九：不复远，无只悔，元吉。', 2: '六二：休复，吉。', 3: '六三：频复，厉无咎。', 4: '六四：中行独复。', 5: '六五：敦复，无悔。', 6: '上六：迷复，凶，有灾眚。用行师，终有大败，以其国君凶﹔至于十年不克征。', 7: '彖︰复，亨。刚反，动而以顺行，是以出入无疾，朋来无咎。反复其道，七日来复，天行也。利有攸往，刚长也。复，其见天地之心乎。'}, 
           '明夷': {0: '利艰贞。', 1: '初九：明夷于飞，垂其翼。 君子于行，三日不食， 有攸往，主人有言。', 2: '六二：明夷，夷于左股，用拯马壮，吉。', 3: '九三：明夷于南狩，得其大首，不可疾贞。', 4: '六四：入于左腹，获明夷之心，出于门庭。', 5: '六五：箕子之明夷，利贞。', 6: '上六：不明晦，初登于天，后入于地。', 7: '彖︰明入地中，明夷。内文明而外柔顺，以蒙大难，文王以之。利艰贞，晦其明也。内难而能正其志，箕子以之。'}, 
           '临': {0: '元，亨，利，贞。 至于八月有凶。', 1: '初九：咸临，贞吉。', 2: '九二：咸临，吉无不利。', 3: '六三：甘临，无攸利。 既忧之，无咎。', 4: '六四：至临，无咎。', 5: '六五：知临，大君之宜，吉。', 6: '上六：敦临，吉无咎。', 7: '彖︰临，刚浸而长，说而顺，刚中而应，大亨以正，天之道也。至于八月有凶，消不久也。'}, 
           '泰': {0: '小往大来，吉亨。', 1: '初九：拔茅茹，以其夤，征吉。', 2: '九二：包荒，用冯河，不遐遗，朋亡，得尚于中行。', 3: '九三：无平不陂，无往不复，艰贞无咎。 勿恤其孚，于食有福。', 4: '六四：翩翩不富，以其邻，不戒以孚。', 5: '六五：帝乙归妹，以祉元吉。', 6: '上六：城复于隍，勿用师。 自邑告命，贞吝。', 7: '彖︰泰，小往大来，吉亨，则是天地交而万物通也，上下交而其志同也。内阳而外阴，内健而外顺，内君子而外小人。君子道长，小人道消也。'}}

class Zhugua :
      #八宫对应的卦组合字典
    def __init__(self):
        #base = os.path.abspath(os.path.dirname(__file__))
        #path = os.path.join(base, 'data.pkl')
        #data = pickle.load(open(path, "rb"))
        #self.sixtyfourgua = self.data.get("數字排六十四卦")
        #self.sixtyfourgua_description = data.get("易經卦爻詳解")
        #print(self.sixtyfourgua_description)     
        self.guacode1=11   #默认是乾卦11， 同人13， 巽55
        self.guacode2=11
        self.isJingGua=True
         
    #由13这个code 制出天火同人的卦  
    def makeGuaByCode(self, zhucode, biancode):
        self.guacode1=zhucode
        self.up1=self.guacode1//10
        self.down1=self.guacode1%10
        self.longguaname1=dic64GuaName[zhucode]
        self.longguaname2=dic64GuaName[biancode]
        self.guaname1=dic64GuaShort[zhucode]
        self.guaname2=dic64GuaShort[biancode]
        self.yaoxiang1=self.countYaoXiang(zhucode)
        self.gongindex1,self.gong1=self.countGong(zhucode)
        self.wuxing1=self.countWuXing(zhucode)     
        self.guacode2=biancode
        self.up2=self.guacode2//10
        self.down2=self.guacode2%10
        self.yaoxiang2=self.countYaoXiang(biancode)
        
        self.gongindex2,self.gong2=self.countGong(biancode)
        
        self.wuxing2=self.countWuXing(biancode)
        #变卦五行不变，但是六神跟主卦宫位定性一致
        self.SixFamily1,self.SixFamily2=self.countSixFamily(self.gongindex1)
         #有两个卦的号码计算出每个爻的组合：少阴，少阳，老阴，老阳等
        yaoString=""
        for i in range(0,6):
            temp=self.yaoxiang1[i]
            if self.yaoxiang1[i] !=self.yaoxiang2[i] and self.yaoxiang1[i]=='1':
                temp="3"
            if self.yaoxiang1[i] !=self.yaoxiang2[i] and self.yaoxiang1[i]=='2':
                temp="0"
            yaoString+=temp
        #print(yaoString)
            #计算动爻位置必须知道那个是老阴 老阳
        self.dongyao=self.drawdongyao(yaoString)
        self.sy1,self.gui1=self.countShiYing(self.guaname1)
        self.sy2,self.gui2=self.countShiYing(self.guaname2)
        #print(self.sy1, self.gui1)
        self.yaoline1=self.drawyaoline(self.yaoxiang1)
        self.yaoline2=  self.drawyaoline(self.yaoxiang2)
        self.fu_wuxing, self.fu_SixFamily =self.countFu()      
        if zhucode==biancode:
            self.isJingGua=True
        else:
            self.isJingGua=False
        
    def makeGuaByYaostring(self, yaostring):   #yaostring=" 123012", 0为老阴，1少阳 2少阴 3 老阳
        ystring1=yaostring.replace("0","2").replace("3","1")
        ystring2=yaostring.replace("0","1").replace("3","2")      
        self.up1=yaoxianglist.index(ystring1[0:3])+1
        self.down1=yaoxianglist.index(ystring1[3:6])+1
        zhucode=self.up1*10+self.down1        
        self.up2=yaoxianglist.index(ystring2[0:3])+1
        self.down2=yaoxianglist.index(ystring2[3:6])+1
        biancode=self.up2*10+self.down2     
        self.makeGuaByCode(zhucode,biancode)

    def makeGuaByName (self, zhuName, bianName):
        code1=self.countGuacode(zhuName)
        code2=self.countGuacode(bianName)
        self.makeGuaByCode(code1,code2)
        
        #主卦代号+单爻动
    def makeGuaByDongyao(self, zhucode, dongpos):
        self.yaoxiang1=self.countYaoXiang(zhucode)
        #print(self.yaoxiang1)
        li=list(self.yaoxiang1)
        li[6-dongpos]=str((int(li[6-dongpos])+2)%4)
        str1="".join(li)
        #print(str1)
        self.makeGuaByYaostring(str1)  
        
    #主卦代号+双爻动
    def makeGuaByDongyao2(self, zhucode, dongpos1,dongpos2):
        self.yaoxiang1=self.countYaoXiang(zhucode)
        #print(self.yaoxiang1)
        li=list(self.yaoxiang1)
        li[6-dongpos1]=str((int(li[6-dongpos1])+2)%4)
        li[6-dongpos2]=str((int(li[6-dongpos2])+2)%4)
        str1="".join(li)
        #print(str1)
        self.makeGuaByYaostring(str1)  
        
      #计算卦的宫位      
    def countGong (self,code):
        up=code//10
        down=code%10
        for index in range(1,9):
            for loc in range(0,8):
                if dicEightGongCode[index][loc]==code:
                    #return index,  str2[index-1]+"宫", dicGuaName[index][loc]
                    return index,  str2[index-1]+"宫"
              
    def countYaoXiang (self, code):
        up=code//10
        down=code%10
        return  yaoxianglist[up-1]+yaoxianglist[down-1]
                  
    def countWuXing (self,code):
        up=code//10
        down=code%10     
        return dicWuXing[up][0:3]+dicWuXing[down][3:6]

    def countSixFamily (self, gong):
        list1=[]
        list2=[]
        for i in range(0,6):
            wu1=self.wuxing1[i][1]
            six1=dicSixFamily[gong][wu1]
            list1.append(six1)
            wu2=self.wuxing2[i][1]
            six2=dicSixFamily[gong][wu2]
            list2.append(six2)
        return list1,list2
    
    def drawdongyao (self, yaostr):
        donglist=[]
        for i in range(0,6):
            if   yaostr[i]=='0':
                dongyao="Ｘ→"
            elif   yaostr[i]=='3':
                dongyao="Ｏ→" 
            else:
                dongyao="　　"
            donglist.append(dongyao)
        self.dongyao1=donglist
        #print(self.dongyao1)
        return donglist

    def drawyaoline (self, yaostr):
        list=[]
        for i in range(0,6):
            if yaostr[i]=='1' or yaostr[i]=="3":
                line="▅▅▅▅▅"
            else:
                #yaostr[i]=='2' or yaostr[i]=="0":
                line="▅▅  ▅▅"
            list.append(line)
        return list

    def countShiYing (self, gname):
        strSY=self.multi_key_dict_set(dicSY, gname)
        #print("systring:", strSY)
        list=[]
        for i in range(0,6):
            if strSY[i]=='0':
                str="　"
            elif strSY[i]=='1':
                str="世"
            else:
                str="应"
            list.append(str)
        signal=strSY[6:]
        return list, signal

    def countFu (self):
        #print("gongindex1=", self.gongindex1)
        zhugongcode=self.gongindex1*11
        fu_wuxing=self.countWuXing(zhugongcode)
        fu_SixFamily=[]
        for i in range(0,6):
            wu1=fu_wuxing[i][1]
            six1=dicSixFamily[self.gongindex1][wu1]
            fu_SixFamily.append(six1)
        for i in range(0,6):
            for j in range(0,6):
                if fu_wuxing[i][1]==self.wuxing1[j][1]:
                    fu_wuxing[i]="　"*2
                    fu_SixFamily[i]="　"*2
        #self.fu_wuxing=fu_wuxing
        #self.fu_SixFamily=fu_SixFamily
        return fu_wuxing, fu_SixFamily
            
        #字典的主键为列表，而键值只有一个，如dictOK
    def multi_key_dict_set (self, d, k):
        for keys, v in d.items():
            if k in keys:
                return v
        return None

    def countGuacode (self, strGuaName):
        for index in range(1,9):
            for loc in range(0,8):
                if dicGuaName[index][loc]==strGuaName:
                    return dicEightGongCode[index][loc]
                         
    #计算爻卦日的天干地支，本段为搬运
    def gangzhi (self, year, month, day, hour):
        if hour == 23:
            d = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S") + datetime.timedelta(hours=1)
        else:
            d = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S") 
        cdate = sxtwl.fromSolar(d.year, d.month, d.day)
        print(d)
        print(d.year, d.month,d.day)
        return [tiangan[cdate.getYearGZ().tg] + dizhi[cdate.getYearGZ().dz], tiangan[cdate.getMonthGZ().tg] + dizhi[cdate.getMonthGZ().dz], tiangan[cdate.getDayGZ().tg] + dizhi[cdate.getDayGZ().dz], tiangan[cdate.getHourGZ(d.hour).tg] + dizhi[cdate.getHourGZ(d.hour).dz]]         

    def gangzhibystr (self, datestring="2023-02-04"):
        d=datetime.datetime.strptime(datestring, "%Y-%m-%d")
        cdate = sxtwl.fromSolar(d.year, d.month, d.day)
        return [ tiangan[cdate.getYearGZ().tg] + dizhi[cdate.getYearGZ().dz],
                   tiangan[cdate.getMonthGZ().tg] + dizhi[cdate.getMonthGZ().dz],
                   tiangan[cdate.getDayGZ().tg] + dizhi[cdate.getDayGZ().dz] ]         

    def setDate (self, datestring="2023-02-04"):
        datelist=self.gangzhibystr(datestring)
        self.datestring=datestring
        self.dategangzhi=datelist[0]+"年"+datelist[1]+"月"+datelist[2]+"日"
        self.xunkong=self.countXunKong(datelist[2])
        
        daygang=datelist[2][0]   #提取日干
        self.sixsheng=dicSixSheng[daygang]
        return self.dategangzhi
    
    def countXunKong(self, daygangzhi ):
        for key, values in dicXunKong.items():
            if daygangzhi in values:
                return key

    def displayDoubleGuaText(self,has_yaochi=True):  #前置条件必须设置了摇卦日期 setDate, 否则无法计算六神
        textbuffer=[]
        textbuffer.append(f"时间: {self.datestring}" )
        textbuffer.append(f"干支: {self.dategangzhi}      (旬空: {self.xunkong} )" )        
        if self.isJingGua==False:
           # print("　"*10+self.guaname1 +self.gui1+ "　"*10+self.guaname2+self.gui2)
            textbuffer.append(f"　               {self.longguaname1}{self.gui1}               {self.longguaname2}{self.gui2}")
            outstring=self.guaname1+"之"+self.guaname2
            #print("六神　伏神　　本　　卦　　　　　　　变　　卦")
            textbuffer.append("六神　伏神　　本　　卦　　　　　　　          变　　卦")
            for i in range(0,6):
                str1=self.sixsheng[i]+"　"+self.fu_SixFamily[i]+self.fu_wuxing[i]+self.yaoline1[i]+"   "+ self.SixFamily1[i]+self.wuxing1[i]+"　"+self.sy1[i]+self.dongyao1[i]
                str2="　"+ self.yaoline2[i]+"　"+self.SixFamily2[i]+self.wuxing2[i]+"　"+self.sy2[i]
                textbuffer.append(str1+str2)                          
        else:
            textbuffer.append(f"         {self.guaname1}静卦")
            #print(self.guaname1+"静卦")
            #print(self.longguaname1+"静卦")
            outstring=self.guaname1+"静卦"
            textbuffer.append(self.gui1)
            for i in range(0,6):
                str1=self.sixsheng[i]+"　"+self.fu_SixFamily[i]+self.fu_wuxing[i]+self.yaoline1[i]+"　"+ self.SixFamily1[i]+self.wuxing1[i]+"　"+ self.sy1[i]
                textbuffer.append(str1)           
        index=self.guaname1
        if has_yaochi==True:
            content1=dicIching[index]
            for i in range(0,8):
                textbuffer.append(content1[i])
        strContent=""
        for item in textbuffer:
            strContent=strContent+item+"\n"           
        return outstring, strContent
           
def statistics():
    import csv
    #fp=open("兄子相生.csv","w",newline="")
    fp=open("单爻动变化v2.csv","w",newline="")
    writer=csv.writer(fp)
    list1=["卦名", "六亲变化"," 五行变化"]
    writer.writerow(list1)
    gua=Zhugua()
    day="2024-09-22"
    gua.setDate(day)
    for gong in range(1, 9):
        gonglist=dicEightGongCode[gong]
        for num in gonglist:
            for i in range(0,6):
                gua.makeGuaByDongyao(num, i+1)
                dongbian=""
                if gua.wuxing1[5-i][1]==gua.wuxing2[5-i][1]:
                    if dizhiOrder.index(gua.wuxing1[5-i][0]) < dizhiOrder.index(gua.wuxing2[5-i][0]):
                        dongbian=gua.SixFamily1[5-i][0]+"化进"
                    elif dizhiOrder.index(gua.wuxing1[5-i][0]) > dizhiOrder.index(gua.wuxing2[5-i][0]):
                        dongbian=gua.SixFamily1[5-i][0]+"化退"
                    else:
                        dongbian=gua.SixFamily1[5-i][0]+"伏吟"
                else:
                    dongbian=gua.SixFamily1[5-i][0]+"化"+gua.SixFamily2[5-i][0]
                wuxing_change=gua.wuxing1[5-i][0]+"化"+gua.wuxing2[5-i][0]  
                guaname_change=gua.guaname1+"之"+gua.guaname2              
                list2=[guaname_change, dongbian,wuxing_change ]
                print(list2)
                writer.writerow(list2)             
    fp.close()
    print("Statistic is finishing")    

def statistics_2_active():
    import csv
    fp=open("ghost_father.csv","w",newline="")
    writer=csv.writer(fp)
    # list1=["主卦", " 变卦 " , " 动爻位置",    "主卦六亲"," 变卦六亲"]
    # writer.writerow(list1)
    gua=Zhugua()
    day="2024-09-22"
    gua.setDate(day)
    for gong in range(1, 9):
        gonglist=dicEightGongCode[gong]
        for num in gonglist:
            for i in range(0,6):
                for j in range(i+1,6):
                    gua.makeGuaByDongyao2(num, i+1,j+1)
                    sig="官父连生"
                    six1=gua.SixFamily1[5-i]
                    six12=gua.SixFamily2[5-i]
                    six2=gua.SixFamily1[5-j]
                    six22=gua.SixFamily2[5-j]
                    if (six1=="官鬼" and six2=="父母") or (six2=="官鬼" and six1=="父母"):
                        list2=[gua.guaname1, gua.guaname2, sig ]
                        print(list2)
                        writer.writerow(list2)             
    fp.close()
    print("Statistic is finishing")     

def statistics_ghost2son():
    import csv
    fp=open("testWu.csv","w",newline="")
    writer=csv.writer(fp)
    # list1=["主卦", " 变卦 " , " 动爻位置",    "主卦六亲"," 变卦六亲"]
    # writer.writerow(list1)
    gua=Zhugua()
    day="2024-09-22"
    gua.setDate(day)
    for gong in range(1, 9):
        gonglist=dicEightGongCode[gong]
        for num in gonglist:
            for i in range(0,6):
                gua.makeGuaByDongyao(num, i+1)
                sig="鬼化子"
                dong_six=gua.SixFamily1[5-i]
                bian_six=gua.SixFamily2[5-i]
                if (dong_six=="官鬼" and bian_six=="子孙") :
                    list2=[gua.guaname1, gua.guaname2, sig ]
                    print(list2)
                    writer.writerow(list2)             
    fp.close()
    print("Statistic is finishing")     

def paipan(day_str,gua_name_str):
    gua=Zhugua()
    # day1=self.txtGuaDate.text()
    # namestr=self.txtGuaName.text()
    if day_str=="" or gua_name_str=="":
        return  "错误操作：没有卦名和日期，无法排卦！"      
    if '之' in gua_name_str:
        split_string=gua_name_str.split('之')
        name1 = split_string[0].strip() 
        name2 = split_string[1].strip() 
    else:
        name1=gua_name_str.strip("静卦")
        name2=name1
    gzstring=gua.setDate(day_str)
    gua.makeGuaByName(name1,name2)
    outGuaName,guacont=gua.displayDoubleGuaText(has_yaochi=False)
    return guacont
    
if __name__ == "__main__": 
    # gua1=Zhugua()
    # #前置条件必须设置了摇卦日期 setDate
    day1="2023-05-15"
    # gzstring=gua1.setDate(day1)
    # gua1.makeGuaByName("旅","大有")
    # guaname, guacontent=gua1.displayDoubleGuaText(has_yaochi=False)
    # print(guaname)
    # print(guacontent)
    guacont=paipan(day1,"旅之升")
    print(guacont)
    # statistics_2_active()
    #statistics_ghost2son()
    # statistics()
       
           
           
    

    
        
        
        
    
    



    
    
    




        
