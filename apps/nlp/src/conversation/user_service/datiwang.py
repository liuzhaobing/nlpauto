# -*- coding:utf-8 -*-
"""对话管理 答题王"""
import json
import random

proResult = {"quresult": {"domain_id": 3448, "domain": "iamdata", "intent": "start",
                          "request_params": {"Default": "开始答题", "agentid": "1522", "devicetype": "ginger",
                                             "envinfo": "{\"devicetype\":\"\",\"timezone\":\"UTC\"}",
                                             "filter_query": "开始答题", "lang": "ZH", "position": "104.061;30.5444",
                                             "query": "开始答题", "robotid": "5C1AEC03573747D",
                                             "sessionid": "testAnno@@cloudminds", "tenantcode": "cloudminds",
                                             "traceid": "bbaafea3-e6e8-468d-91e3-2d8421d93943", "version": "v3"}},
             "session": {"state": "53cbmlo6qs", "variables": {"rounds": {"key": "rounds", "value": "10"}}}}

topic_list = [{"id": 1, "question": "足球运动员“C罗”的全名是“克里斯蒂亚诺.罗纳尔多”", "answer": "正确", "real_answer": "-", "type": "体育知识"},
              {"id": 2, "question": "足球运动员“C罗”，他效力的第一家俱乐部是“里斯本竞技”", "answer": "正确", "real_answer": "-", "type": "体育知识"},
              {"id": 3, "question": "2010年南非足球世界杯，夺得冠军的是西班牙球队", "answer": "正确", "real_answer": "-", "type": "体育知识"},
              {"id": 4, "question": "小说《水浒传》中卢俊义的外号是玉麒麟", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 5, "question": "小说《水浒传》中外号是黑旋风的是张飞", "answer": "错误", "real_answer": "李逵", "type": "经典名著"},
              {"id": 6, "question": "小说《水浒传》中杨志的外号是青面兽", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 7, "question": "小说《水浒传》中被称为智多星的是“宋江”", "answer": "错误", "real_answer": "吴用", "type": "经典名著"},
              {"id": 8, "question": "小说《水浒传》中“宋江”的外号是“及时雨”", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 9, "question": "三国时期曹操字仲谋", "answer": "错误", "real_answer": "孟德", "type": "经典名著"},
              {"id": 10, "question": "三国时期诸葛亮字孔明", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 11, "question": "三国时期刘备字仲谋", "answer": "错误", "real_answer": "玄德", "type": "经典名著"},
              {"id": 12, "question": "三国时期孙权字仲谋", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 13, "question": "《西游记》中，牛魔王的妻子是铁扇公主。", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 14, "question": "《西游记》中，第一个想和唐僧结婚的是女儿国王。", "answer": "错误", "real_answer": "玉兔精", "type": "经典名著"},
              {"id": 15, "question": "在《三国演义》中，＂一个愿打一个愿挨＂形容的是周瑜与黄盖的故事", "answer": "正确", "real_answer": "-",
               "type": "经典名著"},
              {"id": 16, "question": "西游记中，猪八戒在凡间去高老庄娶媳妇", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 17, "question": "西游记中，一直挑着担的是猪八戒", "answer": "错误", "real_answer": "沙僧", "type": "经典名著"},
              {"id": 18, "question": "西游记中，偷蟠桃的是弼马温", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 19, "question": "西游记中，偷袈裟的是白骨精", "answer": "错误", "real_answer": "黑熊怪", "type": "经典名著"},
              {"id": 20, "question": "西游记中，孙悟空的金箍棒重一万三千五百斤", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 21, "question": "西游记中，被压在五指山下的是唐僧", "answer": "错误", "real_answer": "孙悟空", "type": "经典名著"},
              {"id": 22, "question": "西游记中，白龙马最开始是棕色的", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 23, "question": "西游记中，最善良的妖怪是黄狮精", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 24, "question": "“闭月羞花”指的是古代的“貂蝉和杨贵妃”", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 25, "question": "“沉鱼落雁”指的是古代的“西施和貂蝉”", "answer": "错误", "real_answer": "西施和王昭君", "type": "历史知识"},
              {"id": 26, "question": "“两情若是长久时又岂在朝朝暮暮”该首诗句出自“鹊桥仙·纤云弄巧”", "answer": "正确", "real_answer": "-",
               "type": "诗歌文献"},
              {"id": 27, "question": "“两情若是长久时又岂在朝朝暮暮”该首诗句出自诗人“秦观”之手", "answer": "正确", "real_answer": "-",
               "type": "诗歌文献"},
              {"id": 28, "question": "“两情若是长久时又岂在朝朝暮暮”此诗是为歌咏“牛郎织女七夕相会”", "answer": "正确", "real_answer": "-",
               "type": "诗歌文献"},
              {"id": 29, "question": "＂海内存知己，天涯若比邻＂是张若虚的诗句。", "answer": "错误", "real_answer": "王勃", "type": "诗歌文献"},
              {"id": 30, "question": "《牡丹亭》又名《还魂记》", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 31, "question": "《梦溪笔谈》是北宋朝代沈括撰写的", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 32, "question": "＂海上生明月，天涯共此时＂出自唐朝诗人张若虚的《春江花夜月》。", "answer": "错误", "real_answer": " 张九龄（望月怀古）",
               "type": "诗歌文献"},
              {"id": 33, "question": "＂春蚕到死丝方尽，蜡炬成灰泪始干＂的作者是李白。", "answer": "错误", "real_answer": "李商隐", "type": "诗歌文献"},
              {"id": 34, "question": "被称为“诗仙”的是杜甫", "answer": "错误", "real_answer": "李白", "type": "诗歌文献"},
              {"id": 35, "question": "被称为“诗圣”的是李白", "answer": "错误", "real_answer": "杜甫", "type": "诗歌文献"},
              {"id": 36, "question": "被称为“诗魔”的是白居易", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 37, "question": "被称为“诗神”的是苏轼", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 38, "question": "被称为“诗鬼”的是李贺", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 39, "question": "被称为“诗豪”的是刘禹锡", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 40, "question": "被称为“诗杰”的是王勃", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 41, "question": "被称为“诗佛”的是王维", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 42, "question": "唐宋八大家之首是柳中元", "answer": "错误", "real_answer": "韩愈", "type": "诗歌文献"},
              {"id": 43, "question": "唐宋八大家中，韩愈、柳宗元是唐代的，其他六位是宋代的", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 44, "question": "李白是唐宋八大家之一", "answer": "错误", "real_answer": "韩愈、柳宗元、欧阳修、苏洵、苏轼、苏辙、王安石、曾巩",
               "type": "诗歌文献"},
              {"id": 45, "question": "杜甫是唐宋八大家之一", "answer": "错误", "real_answer": "韩愈、柳宗元、欧阳修、苏洵、苏轼、苏辙、王安石、曾巩",
               "type": "诗歌文献"},
              {"id": 46, "question": "李商隐和杜牧合称为“小李杜”", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 47, "question": "＂鹅鹅鹅，曲项向天歌，白毛浮绿水，红掌拨清波＂的作者是骆宾王。", "answer": "正确", "real_answer": "-",
               "type": "诗歌文献"},
              {"id": 48, "question": "唐诗《送孟浩然之广陵》是 李白 的作品", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 49, "question": "出塞至匈奴与呼韩邪单于和亲的是我国古代美女西施", "answer": "错误", "real_answer": "王昭君", "type": "历史知识"},
              {"id": 50, "question": "被称为“医仙”的是我国古代的“华佗”", "answer": "错误", "real_answer": "“张仲景”", "type": "历史知识"},
              {"id": 51, "question": "被称为“医圣”的是我国古代的“李时珍”", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 52, "question": "被称为“外科圣手”的是我国古代的“华佗”", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 53, "question": "涮羊肉起源于 元朝", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 54, "question": "号称＂六一居士＂的是欧阳修", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 55, "question": "曹操晚年废汉献帝自己称帝。", "answer": "错误", "real_answer": "曹丕称帝", "type": "历史知识"},
              {"id": 56, "question": "＂三过家门而不人＂是关于瞬的故事", "answer": "错误", "real_answer": "大禹", "type": "历史知识"},
              {"id": 57, "question": "奸臣魏忠贤是清代的宦官", "answer": "错误", "real_answer": "明朝", "type": "历史知识"},
              {"id": 58, "question": "《资治通鉴》的作者是司马迁", "answer": "错误", "real_answer": "司马光", "type": "历史知识"},
              {"id": 59, "question": "“一字千金”典故是由吕不韦而来", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 60, "question": "我国农学史上最早的名著之一是：《本草纲目》", "answer": "错误", "real_answer": "齐民要术", "type": "历史知识"},
              {"id": 61, "question": "康熙时期，中国与英国签订了《尼布楚条约》", "answer": "错误", "real_answer": "中国与俄国签订了《尼布楚条约》",
               "type": "历史知识"},
              {"id": 62, "question": "中国古代在位时间最长的皇帝是乾隆", "answer": "错误", "real_answer": "康熙", "type": "历史知识"},
              {"id": 63, "question": "近朱者赤近墨者黑，属于“扩散现象”", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 64, "question": "民间“过小年”祭拜的是“财神”", "answer": "错误", "real_answer": "灶神", "type": "百科知识"},
              {"id": 65, "question": "被称为“高原之舟的”动物是“羚羊”", "answer": "错误", "real_answer": "牦牛", "type": "百科知识"},
              {"id": 66, "question": "地球上牙齿最多的动物是“蜗牛”", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 67, "question": "被称为日本动画界的黑泽明是“高桥和希”", "answer": "错误", "real_answer": "宫崎骏", "type": "百科知识"},
              {"id": 68, "question": "一个杯子里装有水，水里一块冰，此时水已满杯，当冰溶后，杯里的水会溢出来。", "answer": "错误", "real_answer": "不会溢出",
               "type": "百科知识"},
              {"id": 69, "question": "世界上流经国家最多的河流是多瑙河", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 70, "question": "郑和下西洋的“西洋”是指大西洋", "answer": "错误", "real_answer": "印度洋和太平洋", "type": "百科知识"},
              {"id": 71, "question": "被称为＂地球之肺＂的是亚马逊位于南美洲的热带雨林", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 72, "question": "飞利浦电器是美国的品牌", "answer": "错误", "real_answer": "荷兰", "type": "百科知识"},
              {"id": 73, "question": "世界上最大的冰川在南极洲", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 74, "question": "最大的动物是蓝鲸", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 75, "question": "天然气主要成分是甲烷", "answer": "错误", "real_answer": "烷烃", "type": "百科知识"},
              {"id": 76, "question": "联合国秘书长潘基文是韩国人", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 77, "question": "葡萄牙航海家“迪亚士”发现了非洲最南端的好望角", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 78, "question": "我们常说的＂一打＂啤酒是指16瓶啤酒", "answer": "错误", "real_answer": "12瓶", "type": "百科知识"},
              {"id": 79, "question": "世界上所有蜜蜂的蜂窝都是正方形", "answer": "错误", "real_answer": "不止是正方形", "type": "百科知识"},
              {"id": 80, "question": "英国白金汉宫禁止打手机是因为女王不喜欢听铃声", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 81, "question": "老北京居民居住的院落式组合建筑一般被称作四合院", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 82, "question": "新西兰卫生部时常告诫游人小心剧毒的＂黑寡妇＂，＂黑寡妇＂是蜘蛛。", "answer": "正确", "real_answer": "-",
               "type": "百科知识"},
              {"id": 83, "question": "＂凯撒大帝＂是古罗马的杰出军事统领。", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 84, "question": "猪心情很好时尾巴会水平摆动", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 85, "question": "西洋乐器小提琴有4根弦", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 86, "question": "欧元创始国有11个国家", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 87, "question": "冬季奥运会是4年1次，以实际举办次数计算届次", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 88, "question": "飞得最高的鸟是海鸥", "answer": "错误", "real_answer": "兀鹫", "type": "百科知识"},
              {"id": 89, "question": "陈凯歌的电影《霸王别姬》里面张国荣饰演的角色叫项羽。", "answer": "错误", "real_answer": "张国荣饰演的是程蝶衣",
               "type": "百科知识"},
              {"id": 90, "question": "WTO是世界贸易组织的简称", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 91, "question": "民间常说有九条命的动物是猫", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 92, "question": "世界第一高峰是我国的珠穆朗玛峰", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 93, "question": "＂鱼翅＂是用鲨鱼的鳍所制成的", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 94, "question": "在中世纪欧洲流行的“黑死病”是鼠疫。", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 95, "question": "葡萄牙的首都是墨尔本", "answer": "错误", "real_answer": "里斯本", "type": "百科知识"},
              {"id": 96, "question": "第一个资本主义国家是英国", "answer": "错误", "real_answer": "荷兰", "type": "百科知识"},
              {"id": 97, "question": "有＂铁榔头＂一称的前中国排球女运动员是郎平", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 98, "question": "峨眉山是中国佛教四大名山之一", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 99, "question": "青城山是中国佛教四大名山之一", "answer": "错误", "real_answer": "青城山是道教", "type": "百科知识"},
              {"id": 100, "question": "武当山是中国道教四大名山之一", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 101, "question": "龙虎山是中国道教四大名山之一", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 102, "question": "冰箱或空调泄露的氟利昂会破坏大气层臭氧层", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 103, "question": "中国唐代第一大画家，被尊称为＂画圣＂的是吴道子", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 104, "question": "＂三下五除二＂是使用算盘的口诀之一", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 105, "question": "“只要有恒心”的下一句是“点石可成金”。", "answer": "错误", "real_answer": "铁杵磨成针", "type": "诗歌文献"},
              {"id": 106, "question": "被称为青莲居士的是中国唐代的李白。", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 107, "question": "而立之年是指40岁", "answer": "错误", "real_answer": "30岁而立", "type": "百科知识"},
              {"id": 108, "question": "1945年美国先后在广岛、长崎投下两枚原子弹", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 109, "question": "清朝后宫中，六宫粉黛无颜色的六宫之首是老佛爷", "answer": "错误", "real_answer": "六宫之首是皇后",
               "type": "历史知识"},
              {"id": 110, "question": "我国流水最大的瀑布是山西壶口瀑布", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 111, "question": "世界上最长的河流是尼罗河", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 112, "question": "中国最长的河流是黄河", "answer": "错误", "real_answer": "长江", "type": "百科知识"},
              {"id": 113, "question": "世界上最大的平原是亚马逊平原", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 114, "question": "中国最大的平原是黄土平原", "answer": "错误", "real_answer": "东北平原", "type": "百科知识"},
              {"id": 115, "question": "中国最大的盆地是塔里木盆地", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 116, "question": "中国最大的淡水湖是潘阳湖", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 117, "question": "中国最大的湖泊是潘阳湖", "answer": "错误", "real_answer": "青海湖", "type": "百科知识"},
              {"id": 118, "question": "世界上最高的山峰是珠穆朗玛峰", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 119, "question": "世界上最深的海沟是马里亚纳海沟", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 120, "question": "世界上最小的国家是梵蒂冈", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 121, "question": "世界上最大的国家是美国", "answer": "错误", "real_answer": "俄罗斯", "type": "百科知识"},
              {"id": 122, "question": "世界上最大的海洋是大西洋", "answer": "错误", "real_answer": "太平洋", "type": "百科知识"},
              {"id": 123, "question": "嫦娥在月亮上住的行宫叫广寒宫", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 124, "question": "中国面积最大、最深的海是东海", "answer": "错误", "real_answer": "南海", "type": "百科知识"},
              {"id": 125, "question": "文房四宝中的四宝是指笔、墨、纸、砚", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 126, "question": "指南针是中国四大发明之一", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 127, "question": "中国四大发明是造纸术、指南针、地震仪、印刷术", "answer": "错误", "real_answer": "造纸术、指南针、火药、印刷术",
               "type": "历史知识"},
              {"id": 128, "question": "地震仪是张衡发明的", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 129, "question": "历史上第一位皇帝是汉高祖", "answer": "错误", "real_answer": "秦始皇", "type": "历史知识"},
              {"id": 130, "question": "西游记的作者是罗贯中", "answer": "错误", "real_answer": "吴承恩", "type": "经典名著"},
              {"id": 131, "question": "三国演义的作者是吴承恩", "answer": "错误", "real_answer": "罗贯中", "type": "经典名著"},
              {"id": 132, "question": "水浒传的作者是施耐庵", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 133, "question": "中国四大名著分别是《水浒传》《三国演义》《西游记》《红楼梦》", "answer": "正确", "real_answer": "-",
               "type": "经典名著"},
              {"id": 134, "question": "最早的宗教是佛教", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 135, "question": "佛教起源于古中国", "answer": "错误", "real_answer": "古印度", "type": "百科知识"},
              {"id": 136, "question": "中国四大宗教分别是佛教、道教、基督教和伊斯兰教", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 137, "question": "世界三大宗教分别是佛教、道教、基督教", "answer": "错误", "real_answer": "佛教、基督教、伊斯兰教",
               "type": "百科知识"},
              {"id": 138, "question": "跑得最快的鸟是鸵鸟", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 139, "question": "泼水节是我国傣族的传统节日也是他们的新年", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 140, "question": "清朝时的＂满汉全席＂共有108道菜", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 141, "question": "中国古代科举制度考试，殿试第一名为状元，第二名榜眼，第三名叫探花", "answer": "正确", "real_answer": "-",
               "type": "历史知识"},
              {"id": 142, "question": "人体消化道中最长的器官是大肠", "answer": "错误", "real_answer": "-", "type": "百科知识"},
              {"id": 143, "question": "李大钊是中国共产党的创始人之一", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 144, "question": "中国共产党的创始人一共是十六位", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 145, "question": "中国共产党成立于1921年7月23日", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 146, "question": "孙中山是中国共产党的创始人之一", "answer": "错误", "real_answer": "孙中山建立了国民党", "type": "历史知识"},
              {"id": 147, "question": "孙中山是国民党的建立者", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 148, "question": "孙中山被尊称为国民党“国父”", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 149, "question": "宋庆龄是孙中山的妻子", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 150, "question": "宋庆龄是宋美龄的妹妹", "answer": "错误", "real_answer": "是姐姐", "type": "历史知识"},
              {"id": 151, "question": "宋美龄是蒋介石的妻子", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 152, "question": "日本是1949年宣布投降的", "answer": "错误", "real_answer": 1945, "type": "历史知识"},
              {"id": 153, "question": "大熊猫只有中国才有", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 154, "question": "《小桔灯》的作者，原名为谢婉莹的作家，笔名叫冰心", "answer": "正确", "real_answer": "-", "type": "诗歌文献"},
              {"id": 155, "question": "我国的吉利汽车公司成功收购了外国沃尔沃100%的股权", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 156, "question": "人体最大的解毒器官是肝脏", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 157, "question": "名医华佗为董卓所杀", "answer": "错误", "real_answer": "曹操", "type": "经典名著"},
              {"id": 158, "question": "金庸武侠小说《天龙八部》中段誉与木婉清是同父异母的兄妹。", "answer": "错误", "real_answer": "原著不是兄妹",
               "type": "诗歌文献"},
              {"id": 159, "question": "中国拉萨有日光之城的美称", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 160, "question": "金庸先生原本姓査。", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 161, "question": "中国第一个世界冠军是许海峰", "answer": "错误", "real_answer": "容国团", "type": "百科知识"},
              {"id": 162, "question": "历史上李靖是唐朝将领", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 163, "question": "《睡莲》和《日出》是法国印象派画家代表人物梵高的作品", "answer": "错误", "real_answer": "莫奈的作品",
               "type": "百科知识"},
              {"id": 164, "question": "馒头是诸葛亮发明的", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 165, "question": "隋炀帝杨广死于兵败自杀", "answer": "错误", "real_answer": "宇文化及杀的", "type": "历史知识"},
              {"id": 166, "question": "＂三无食品＂是指无厂名、无厂址和无生产日期食品", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 167, "question": "世界上第一个颁布药典的国家是中国唐朝", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 168, "question": "《指环王》中的指环可以让人透视", "answer": "错误", "real_answer": "隐身", "type": "百科知识"},
              {"id": 169, "question": "农夫有17只羊，除了9只以外都病死了，农夫还剩8只羊", "answer": "错误", "real_answer": "剩9只阳",
               "type": "百科知识"},
              {"id": 170, "question": "清朝＂太平天国＂运动的发起人，后成为太平天国天王的人是洪秀全", "answer": "正确", "real_answer": "-",
               "type": "历史知识"},
              {"id": 171, "question": "人的泪水里的咸味是从血液中来", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 172, "question": "联合国的总部设在美国首部华盛顿", "answer": "错误", "real_answer": "纽约", "type": "百科知识"},
              {"id": 173, "question": "可口可乐是碳酸饮料", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 174, "question": "联合国安理会常任理事国都拥有氢弹", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 175, "question": "“江山社稷”中的“稷”是指五谷之神", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 176, "question": "2008年北京奥运会开幕式和闭幕式的总导演是李安", "answer": "错误", "real_answer": "张艺谋", "type": "百科知识"},
              {"id": 177, "question": "由于可能出现山洪暴发，沙漠中最大的危险之一是溺水", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 178, "question": "刘欢演唱的《好汉歌》是《三国演义》的主题曲", "answer": "错误", "real_answer": "水浒传", "type": "经典名著"},
              {"id": 179, "question": "鱼是有耳朵的", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 180, "question": "鱼会流眼泪的", "answer": "错误", "real_answer": "不会，鱼没有泪腺", "type": "百科知识"},
              {"id": 181, "question": "《西游记》中孙悟空把金箍棒缩小后藏在头发里", "answer": "错误", "real_answer": "耳朵", "type": "经典名著"},
              {"id": 182, "question": "蒲公英是靠风力传播种子。", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 183, "question": "＂飞雪连天射白鹿，笑书神侠倚碧鸳＂是金庸的14部著作简称", "answer": "正确", "real_answer": "-",
               "type": "经典名著"},
              {"id": 184, "question": "第一架望远镜是由爱迪生发明", "answer": "错误", "real_answer": "汉斯·利伯希", "type": "百科知识"},
              {"id": 185, "question": "第一个参加NBA赛事的中国球员是易建联", "answer": "错误", "real_answer": "姚明", "type": "体育知识"},
              {"id": 186, "question": "一些轿车车身后面有1.6 1.8 2.9等数字这是指发动机的排量。", "answer": "正确", "real_answer": "-",
               "type": "百科知识"},
              {"id": 187, "question": "我国自主研发的载人深潜器是和谐号", "answer": "错误", "real_answer": "蛟龙号", "type": "百科知识"},
              {"id": 188, "question": "第一个登陆月球的宇航员阿姆斯特朗", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 189, "question": "希腊神话中雅典娜掌管战争", "answer": "正确", "real_answer": "-", "type": "经典名著"},
              {"id": 190, "question": "扶桑和东瀛指的是日本", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 191, "question": "与中国的云南省接壤的国家分别是缅甸、老挝和越南。", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 192, "question": "我国的泰山在江西", "answer": "错误", "real_answer": "山东", "type": "百科知识"},
              {"id": 193, "question": "中国四大名山是华山、泰山、黄山、横山", "answer": "错误", "real_answer": "华山、泰山、黄山、峨眉山",
               "type": "百科知识"},
              {"id": 194, "question": "我国华山在中国陕西", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 195, "question": "我国的黄山在安徽省", "answer": "正确", "real_answer": "-", "type": "百科知识"},
              {"id": 196, "question": "八国联军分别是日本、俄罗斯、英国、美国、法国、奥匈帝国、意大利、匈牙利", "answer": "正确", "real_answer": "-",
               "type": "历史知识"},
              {"id": 197, "question": "鸦片战争是1840年开始的", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 198, "question": "第一次世界大战是1914年开始的", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 199, "question": "第二次世界大战是1931年开始的", "answer": "正确", "real_answer": "-", "type": "历史知识"},
              {"id": 200, "question": "南京条约是中国和法国签订的不平等条约", "answer": "错误", "real_answer": "和英国签订的南京条约",
               "type": "历史知识"}]


def get_n_topics():
    """从题库随机抽取n道题目 存入变量topics中"""
    rounds = proResult["session"]["variables"]["rounds"]["value"]
    topics = random.sample(topic_list, int(rounds))
    proResult["session"]["variables"]["topics"] = {"key": "topics", "value": json.dumps(topics, ensure_ascii=False)}


def get_one_topic():
    """从题库抽取1道题目 分别存入变量 now_question now_answer now_round 中"""
    # 从题库中随机抽取一题
    topics = proResult["session"]["variables"]["topics"]["value"]
    topic_list = json.loads(topics)
    now_topic = topic_list.pop()

    # 将题目全部信息存入 now_topic
    proResult["session"]["variables"]["now_topic"] = {"key": "now_topic",
                                                      "value": json.dumps(now_topic, ensure_ascii=False)}
    # 将剩余题目放回原处 topics
    proResult["session"]["variables"]["topics"] = {"key": "topics",
                                                   "value": json.dumps(topic_list, ensure_ascii=False)}
    # 设置当前是第几轮 now_round
    if proResult["session"]["variables"].__contains__("now_round"):
        now_round = int(proResult["session"]["variables"]["now_round"]["value"]) + 1
    else:
        now_round = 1
    proResult["session"]["variables"]["now_round"] = {"key": "now_round", "value": str(now_round)}

    # 将向用户投放题目存入变量 now_question now_answer
    now_question = now_topic["question"]
    now_answer = now_topic["answer"]
    proResult["session"]["variables"]["now_question"] = {"key": "now_question", "value": now_question}
    proResult["session"]["variables"]["now_answer"] = {"key": "now_answer", "value": now_answer}


def check_answer():
    """判断答复是否符合预期 并输出话术到变量 now_reply """
    right_answer_tmp_list = ["答对了，好厉害！", "太棒了，答对了！", "回答正确！", "答对了，真棒！"]
    wrong_answer_tmp_list = ["很遗憾答错了", "答错了，加油哦！", "不对哦，下一题", "答错了，要加油呀！", "错了哦，要努力哦！"]

    now_answer = proResult["session"]["variables"]["now_answer"]["value"]
    user_answer = proResult["session"]["variables"]["user_answer"]["value"]

    if user_answer == now_answer:
        # 回答正确，返回正确答复前缀
        now_reply = random.sample(right_answer_tmp_list, 1)[0]
        # 回答正确，记录正确次数
        if proResult["session"]["variables"].__contains__("right_count"):
            count = json.loads(proResult["session"]["variables"]["right_count"]["value"])
            proResult["session"]["variables"]["right_count"]["value"] = str(int(count) + 1)
        else:
            proResult["session"]["variables"]["right_count"] = {"key": "right_count", "value": "1"}
    else:
        # 回答错误，返回错误答复前缀
        now_reply = random.sample(wrong_answer_tmp_list, 1)[0]

    proResult["session"]["variables"]["now_reply"] = {"key": "now_reply", "value": now_reply}


def summary_for_topic():
    """答题结束 统计答题正确数 返回回复话术"""
    if proResult["session"]["variables"].__contains__("right_count"):  # 若一次都没回答正确 就不会产生变量right_count
        right_count = proResult["session"]["variables"]["right_count"]["value"]
    else:
        right_count = 0

    rounds = proResult["session"]["variables"]["rounds"]["value"]
    if int(right_count) >= int(0.6 * int(rounds)):
        answer_final = f"太棒了，本轮游戏您共回答正确{right_count}道题，恭喜您获得“答题王”荣誉称号。"
    else:
        answer_final = f"很遗憾，本轮游戏，您只回答正确了{right_count}道题，没能获得“答题王”荣誉称号，加油哦。"

    proResult["session"]["variables"]["game_over_reply"] = {"key": "game_over_reply", "value": answer_final}


if __name__ == '__main__':
    rounds = proResult["session"]["variables"]["rounds"]["value"]

    get_n_topics()
    for r in range(int(rounds)):
        get_one_topic()
        print(proResult["session"]["variables"]["now_question"]["value"])

        proResult["session"]["variables"]["user_answer"] = {"key": "user_answer", "value": input()}
        check_answer()
        print(proResult["session"]["variables"]["now_reply"]["value"])
