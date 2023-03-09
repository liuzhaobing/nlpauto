# -*- coding:utf-8 -*-
"""
医院导览场景
"""
import copy

data = [{
            "illness": ["呼吸道感染", "支气管哮喘", "慢阻肺", "阻塞性肺病", "咳嗽", "呼吸困难", "呼吸不畅", "呼吸不上来", "气短", "憋气", "气喘", "咯痰", "咯血", "胸片异常", "胸部CT异常", "重症肺炎", "肺部感染", "肺部难治性感染", "ARDS", "急性COPD", "危重哮喘", "间质性肺病", "免疫缺陷者肺炎", "睡眠呼吸暂停", "肺癌", "呼吸障碍", "呼吸衰竭", "肺栓", "肺结节", "呼吸道", "支气管", "肺部小结节", "肺部结节", "胸腔积液", "肺心病", "呼吸康复", "间质性肺异常", "感冒", "咳痰", "咳血"],
            "examination": ["肺通气", "雾化", "肺活检", "胸膜活检", "胸腔镜", "纤支镜", "肺穿刺", "肺灌洗", "睡眠监测", "支气管镜", "无创呼吸机"],
            "department": "呼吸与危重症医学科",
            "position": "门诊二楼内科诊区。病区位于佑康18楼"
        },
        {
            "illness": ["肺结核", "肺病", "流感", "甲流"],
            "examination": ["PPD试验"],
            "department": "肺科门诊",
            "position": "佑安楼西南侧，发热门诊楼上"
        },
        {
            "illness": ["发烧", "发热", "新冠", "阳性", "阳了"],
            "examination": [],
            "department": "发热门诊",
            "position": "佑安楼西南侧，呼吸二区负一楼"
        },
        {
            "illness": ["便秘", "结肠", "胃肠", "肝胆胰", "消化道", "食管", "肠道", "胃", "痔", "肛肠", "肛门", "胆结石", "胆总管", "胆胰", "纵膈", "贲门", "肝", "胰", "十二指肠", "胆道", "消化系统", "胰腺", "肝硬化", "中毒", "拉肚子", "腹泻", "食欲", "腹痛", "腹水", "咽下困难", "消化性溃疡", "胃粘膜", "消化不良", "肠炎", "肠结核", " 腹膜", "肠系膜", "脾胃", "反酸", "消化不良", "肚子疼", "肚子痛", "腹胀", "排气", "黄疸", "厌食", "肝炎", "甲肝", "乙肝"],
            "examination": ["大肠水疗", "结肠透析", "食管测压", "肛管测压", "超声内镜", "消化内镜", "胃镜", "肠镜", "套扎", "放大内镜", "急诊内镜"],
            "department": "消化内科",
            "position": "门诊二楼内科诊区。病区位于佑康16楼"
        },
        {
            "illness": [],
            "examination": ["内窥镜", "胃部吹气", "胃吹气", "胃镜", "肠镜", "幽门螺旋杆菌"],
            "department": "内窥镜室",
            "position": "门诊三楼，楼梯旁边"
        },
        {
            "illness": ["心血管", "心肌", "心内膜.心律失常", "心力衰竭", "冠状动脉", "心脏", "心腔", "心动过速", "心动过缓", "房扑", "房颤", "冠心病", "血脂异常", "高血压", "心肌病", "心肌炎", "心脏瓣膜", "心衰", "早搏", "心律不齐", "主动脉夹层", "先心病", "高血脂", "心绞痛", "心包", "动脉", "低血压", "心跳快", "心率", "脉搏"],
            "examination": ["血压监测"],
            "department": "心血管内科",
            "position": "门诊一楼内科诊区。一病区位于佑康楼17层，二病区在佑康楼13层"
        },
        {
            "illness": [],
            "examination": ["心电图"],
            "department": "心电图室",
            "position": "门诊三楼，电梯直达，出电梯后右侧"
        },
        {
            "illness": [],
            "examination": ["脑电图", "经颅多普勒超声"],
            "department": "脑电图室",
            "position": "门诊三楼，电梯直达，出电梯后右侧"
        },
        {
            "illness": [],
            "examination": ["B超", "彩超"],
            "department": "超声医学科",
            "position": "门诊大厅一楼；住院部的超声医学科在佑安楼南侧一层"
        },
        {
            "illness": [],
            "examination": ["放射诊断", "CT", "X线", "MR", "DSA", "MRI", "胸片", "CTA"],
            "department": "医学影像科",
            "position": "佑康楼二楼CT室"
        },
        {
            "illness": [],
            "examination": ["磁共振"],
            "department": "磁共振室",
            "position": "学术文化厅一楼，和佑康楼一楼"
        },
        {
            "illness": ["脑血管", "痴呆", "帕金森", "癫痫", "睡眠障碍", "周围神经", "坐骨神经", "颅内感染", "神经心理疾病", "卒中", "脑出血", "脑缺血", "脑梗", "脑栓", "运动神经元", "头痛头晕", "抑郁", "焦虑", "强迫症", "恐惧症", "疑病症", "精神障碍", "疲劳综合征", "胸闷心慌", "呃逆腹胀", "心理障碍", "神经重症", "中枢神经", "眩晕", "记忆障碍", "神经系统变性", "颈腰椎病", "神经痛", "肢体麻木", "运动障碍", "失眠", "耳鸣", "耳聋", "神经遗传病", "认知失调", "肌无力", "脑炎", "脑膜炎", "神经衰弱", "神经症", "神经炎", "神经麻痹", "脊髓炎", "中风", "面瘫", "抽搐", "孤独症", "四肢无力", "嗜睡", "觉多"],
            "examination": [],
            "department": "神经内科",
            "position": "门诊一楼内科诊区。一病区位于佑康楼15层，二病区在佑康楼13层"
        },
        {
            "illness": ["糖尿病", "高血糖", "骨质疏松", "高尿酸血症", "痛风", "垂体", "性腺", "肾上腺", "继发性高血压", "肥胖症", "内分泌失调", "生长发育异常", "代谢病", "更年期综合征", "消瘦", "易怒", "食欲减退", "亢进", "大便增多", "多尿", "多饮", "尿多", "性早熟", "脾气变大", "脾气变差", "性冷淡", "性亢奋", "性亢进"],
            "examination": ["血糖监测"],
            "department": "内分泌内科",
            "position": "门诊二楼内科诊区。病区位于佑安楼北侧2楼"
        },
        {
            "illness": ["肾脏", "肾小球", "肾病", "肾炎", "肾损害", "膀胱炎", "肾衰竭", "血液病", "白血病", "淋巴瘤", "骨髓瘤", "贫血", "骨髓增生", "血小板", "紫癜", "类风湿性血管炎", "系统性红斑狼疮", "尿路感染", "肾间质损害", "免疫疾病", "血液肿瘤", "血栓", "泌尿系感染", "血液肿瘤", "噬血细胞", "CAEBV感染", "凝血", "泌尿道", "面部浮肿", "脸部浮肿", "尿毒症", "肾积水"],
            "examination": ["肾穿刺", "血浆置换", "细胞免疫", "造血干细胞移植", "血液净化", "溶栓", "血常规", "尿常规", "骨髓穿刺", "骨髓活检", ""],
            "department": "肾病血液科",
            "position": "门诊二楼内科诊区。病区位于佑安楼北侧4楼"
        },
        {
            "illness": [],
            "examination": ["透析"],
            "department": "血液净化室",
            "position": "佑安楼南侧4楼"
        },
        {
            "illness": ["风湿", "免疫性", "硬皮病", "多肌炎", "皮肌炎", "白塞病", "干燥综合征", "血管炎", "骨质疏松", "关节炎", "炎症性肌病", "系统性硬化症", "痛风", "脊柱炎", "滑囊", "肌腱", "筋膜", "脊柱关节", "免疫缺陷", "神经性关节病", "骨软化", "骨肥厚", "骨炎", "关节积液", "免疫抑制"],
            "examination": [],
            "department": "风湿免疫科",
            "position": "门诊二楼内科诊区。病区位于佑安楼北侧4楼"
        },
        {
            "illness": ["肿瘤", "癌", "瘤"],
            "examination": ["化疗", "热疗", "靶向治疗", "胸腹腔灌注", "免疫治疗"],
            "department": "肿瘤内科",
            "position": "门诊二楼内科诊区。病区位于佑安楼北侧3楼"
        },
        {
            "illness": [],
            "examination": ["放疗", "放射治疗"],
            "department": "放疗中心",
            "position": "肺科门诊南侧"
        },
        {
            "illness": [],
            "examination": ["肿瘤消融", "囊肿硬化", "置管引流", "穿刺活检", ""],
            "department": "超声介入科",
            "position": "门诊二楼内科诊区。病区位于佑安楼北侧一层"
        },
        {
            "illness": ["休克", "心跳骤停", "呼吸骤停", "多器官衰竭", "慢性病", "老年病"],
            "examination": ["家庭医生", "居家护理", "上门注射", "静脉血采集", "导管护理", "造瘘口护理", "压疮护理", "中药熏洗", "药物涂擦"],
            "department": "全科医学科",
            "position": "门诊二楼内科诊区。病区位于佑安楼北侧4楼"
        },
        {
            "illness": ["代谢综合征", "营养不良"],
            "examination": [],
            "department": "临床营养科",
            "position": "门诊二楼"
        },
        {
            "illness": [],
            "examination": ["PICC"],
            "department": "PICC护理门诊",
            "position": "门诊三楼"
        },
        {
            "illness": [],
            "examination": [],
            "department": "MDT门诊",
            "position": "门诊二楼"
        },
        {
            "illness": [],
            "examination": ["肌电图"],
            "department": "肌电图室",
            "position": "佑安楼一二楼康复科病房"
        },
        {
            "illness": ["康复", "假肢"],
            "examination": [],
            "department": "康复医学科",
            "position": "门诊三楼中间走廊处。病区位于佑安楼一二楼"
        },
        {
            "illness": ["精神障碍", "酒精依赖", "神经症", "身心疾病", "睡眠障碍", "焦虑障碍", "强迫症", "疑病症", "躯体形式障碍", "神经衰弱", "神经症性障碍", "心境障碍", "精神分裂", "精神病", "创伤后应激障碍", "适应障碍", "心理应激障碍", "人格障碍", "成瘾", "戒断", "进食障碍", "心理健康", "情绪障碍", "情感障碍", "心理疾病", "压力大", "戒烟", "厌食"],
            "examination": ["CBT", "认知行为疗法", "心理测量", "睡眠监测", "心理咨询", "心理筛查"],
            "department": "精神医学科",
            "position": "门诊二楼内科诊区。病区位于佑安楼南侧3楼"
        },
        {
            "illness": ["危重症", "急性中毒", "重症感染", "呼吸衰竭", "循环衰竭", "多发伤", "复合伤", "心梗", "心衰", "急症", "急诊", "抢救", "留观", "中毒", "蜂蛰伤", "咬伤", "急性创伤", "骨折", "烧伤"],
            "examination": [],
            "department": "重症医学科",
            "position": "门诊一楼。病区位于佑康楼7层"
        },
        {
            "illness": [],
            "examination": [],
            "department": "急诊内科",
            "position": "门诊一楼"
        },
        {
            "illness": ["交通伤", "意外伤", "四肢骨折", "骨盆骨折", "脊柱骨折", "肌腱损伤", "脏器损伤", "烧伤", "创伤急救", "脊柱损伤", "四肢外伤", "多发性创伤", "急性关节损伤", "韧带损伤", "胳膊疼", "摔伤", "摔倒", "摔跤", "交通事故", "撞车", "车祸", "擦伤", "刮伤", "撞伤"],
            "examination": [],
            "department": "急诊外科",
            "position": "门诊三楼外科诊区。病区位于佑康楼11楼"
        },
        {
            "illness": [],
            "examination": [],
            "department": "门诊大厅",
            "position": "天佑医院东南门，急诊科旁"
        },
        {
            "illness": [],
            "examination": [],
            "department": "综合诊疗科",
            "position": "门诊一楼。病区位于佑康楼19层"
        },
        {
            "illness": ["皮肤病", "性病", "疣", "鸡眼", "痣", "斑", "皮赘", "睑黄瘤", "皮肤纤维瘤", "肉芽肿", "皮肤增生", "脂溢性角化病", "湿疹", "疱疹", "疖", "痈", "丹毒", "疮", "脉管炎", "皮炎", "痒疹", "斑秃", "瘢痕", "血管瘤", "疥疮结节", "青春痘", "痘肌", "白化病", "银屑病", "脱发", "唇炎", "淋病", "红疹", "疹子", "梅毒", "艾滋", "指甲", "软甲", "甲沟"],
            "examination": ["冷冻治疗"],
            "department": "皮肤性病科",
            "position": "门诊二楼"
        },
        {
            "illness": ["荨麻疹", "花粉症", "过敏", "变应性结膜炎", "咳嗽变异性哮喘", ""],
            "examination": ["点刺"],
            "department": "过敏反应科",
            "position": "门诊二楼"
        },
        {
            "illness": ["颅脑", "神经重症", "脑血管", "颅内", "开颅", "面肌痉挛", "椎管肿瘤", "神经外科", "颅底", "脑外伤", "神经病"],
            "examination": [],
            "department": "神经外科",
            "position": "门诊三楼外科诊区。病区位于佑康楼10楼"
        },
        {
            "illness": ["脊柱退变", "脊柱创伤", "脊柱畸形", "脊柱肿瘤", "脊椎", "腰椎", "颈椎", "脊柱不稳", "骨母细胞瘤", "骨髓瘤", "脊索瘤", "骨肉瘤", "脊柱转移性肿瘤", "椎管内脂肪瘤", "神经纤维瘤", "神经鞘瘤", "脊柱侧凸", "侧后凸", "脊柱后凸", "平背", "骨化症", "脊柱结核", "脊柱退行性", "颈肩", "腰腿疼", "肩颈", "脖子疼", "脖子酸", "脖子痛", "腰间盘", "肩周"],
            "examination": [],
            "department": "脊柱骨科",
            "position": "门诊三楼外科诊区。病区位于佑康楼10楼"
        },
        {
            "illness": ["韧带", "半月板", "髁间窝", "关节脱位", "创面修复", "骨折", "肩关节", "膝关节", "髋关节", "肘关节", "踝关节", "骨不连接", "骨关节", "断指", "断肢", "肌腱", "软组织缺损", "骨外露", "手部先天性畸形", "肢体肿瘤", "骨缺损", "足趾移植", "手指再造", "骨头坏死", "关节炎", "肩袖修补", "运动损伤", "冻结肩", "肩峰撞击症", "关节畸形", "膝盖", "肩膀", "关节疼", "关节痛"],
            "examination": ["关节镜", "关节置换"],
            "department": "关节骨科",
            "position": "门诊三楼外科诊区。病区位于佑康楼11楼"
        },
        {
            "illness": ["腹股沟", "前列腺", "肾上腺", "尿道", "膀胱", "尿管", "尿失禁", "阴茎", "漏尿", "阴道", "泌尿系", "男科", "生殖系统", "肾肿瘤", "血尿", "尿痛", "尿急", "尿血", "尿频", "少尿", "尿少", "尿不尽", "包皮", "阳痿", "早泄", "不举", "勃起", "遗精", "包茎", "睾丸", "附睾", "尿路", "阴囊", "死精", "少精", "射精", "不射", "隐睾", "起夜", "小便"],
            "examination": ["肾移植", "膀胱镜"],
            "department": "泌尿外科",
            "position": "门诊三楼外科诊区。病区位于佑康楼9楼"
        },
        {
            "illness": ["肝脏肿瘤", "胰腺肿瘤", "胆道肿瘤", "肝血管瘤", "肝囊肿", "胆囊癌", "胆管癌", "甲状腺", "黄疸", "胆石症", "门脉高压症", "疝", "阑尾炎", "胆囊结石", "胆总管结石", "胆总管囊肿", "脾脏肿瘤", "腹股沟疝", "胰腺癌", "结肠癌", "肝癌", "直肠癌", "肝病", "腹胀"],
            "examination": ["腹腔镜", "胆道镜", "胆囊切除", "胆道手术", "胆管扩大", "胆管整形", "ERCP", "十二指肠镜"],
            "department": "肝胆胰外科",
            "position": "门诊三楼外科诊区。病区位于佑康楼12楼"
        },
        {
            "illness": ["痔", "直肠脱垂", "肛瘘", "肛周脓肿", "便秘", "胃癌", "结直肠癌", "胃肠道间质瘤", "肛管", "腹外疝", "保肛", "甲状腺癌", "阑尾", "便血", "大便带血", "大便有血", "腹胀"],
            "examination": ["腹腔镜", "阑尾切除"],
            "department": "胃肠外科",
            "position": "门诊三楼外科诊区。病区位于佑康楼12楼"
        },
        {
            "illness": ["甲状腺癌.乳腺癌", "乳腺肿瘤", "甲状腺结节", "甲状腺肿瘤", "乳腺结节", "乳房", "堵奶", "涨奶"],
            "examination": ["保乳手术", "甲状腺微创手术"],
            "department": "甲乳外科",
            "position": "门诊三楼外科诊区。病区位于佑康楼9楼"
        },
        {
            "illness": ["肺结节", "肺癌", "食管肿瘤", "纵隔肿瘤", "气管肿瘤", "胸壁肿瘤", "肺气肿", "胸壁畸形", "漏斗胸", "鸡胸", "胸部创伤", "肋骨骨折", "胸骨骨折", "血气胸", "胸腔积液", "心脏外伤", "心外伤", "食管裂孔疝", "膈疝", "支气管扩张", "主动脉夹层", "动脉瘤", "胸壁", "瓣膜", "胸腔", "静脉曲张"],
            "examination": ["胸腔镜", "冠脉搭桥"],
            "department": "心胸外科",
            "position": "门诊三楼外科诊区。病区位于佑康楼9楼"
        },
        {
            "illness": ["眼肿瘤", "眼眶", "泪道", "干眼", "青光眼", "白内障", "眼底", "角膜", "眼表", "近视", "斜视", "弱视", "屈光不正", "眼部", "眼病", "睑板腺", "睑缘炎", "视网膜", "玻璃体", "眼外伤", "眼球", "巩膜", "葡萄膜", "黄斑", "远视", "眼整形", "视力", "眼睛", "眼压", "人工晶体", "飞蚊症", "虹视", "怕光", "畏光", "睁不开", "倒睫", "视觉", "复视", "眼疾", "眼病", "眼肌", "视神经", "眼神经", "结膜炎", "配镜", "眼镜", "飞秒", "OK镜", "眼综合", "验光", "散瞳", "老花眼", "眼内", "散光", "内眼", "眼表", "麦粒肿", "眼睑", "对眼", "ICL", "脉络膜", "巩膜", "眼不好", "用眼"],
            "examination": ["ICL", "验光"],
            "department": "眼科",
            "position": "佑安楼二楼。病区位于佑康楼14层"
        },
        {
            "illness": ["鼻窦", "鼻咽喉", "鼻息肉", "鼻腔", "声带", "喉部", "甲状软骨", "聋", "鼓室", "嗓子", "乳突", "扁桃体", "耳鸣", "鼻中隔", "中耳", "耳硬化", "鼾", "耳蜗", "听神经瘤", "耳整形", "耳道", "耳朵", "鼻子", "咽喉", "镫骨", "内耳", "嘶哑", "鼻内翻", "耳畸形", "听觉", "嗅觉", "味觉", "鼻腔", "鼻颅底", "鼻炎", "听力", "耳鸣", "助听", "鼻塞", "流鼻涕", "喷嚏", "打呼噜"],
            "examination": ["鼻内镜", "喉镜"],
            "department": "耳鼻喉科",
            "position": "门诊三楼。病区位于佑康楼14层"
        },
        {
            "illness": ["畸形鼻", "泪沟", "眼窝凹陷", "颈纹", "拇外翻", "腋臭"],
            "examination": ["鼻畸形纠正", "面部填充", "面部轮廓整改", "乳房美容", "双眼皮", "开眼角", "提眉", "隆鼻", "肉毒素", "玻尿酸", "脂肪抽吸", "毛发移植", "开眼角", "眼袋整形", "除皱", "脂肪填充", "上睑下垂矫正", "去眼袋", "鼻头缩小", "鼻小柱延长", "鼻翼缩小", "鼻头塑型", "瘦脸", "下颌骨磨削术", "隆乳", "腰腹脂肪环吸术", "四肢脂肪环吸", "水光针", "线雕", "脂肪胶填充", "埋线", "甲床整形", "丰胸", "重睑术", "面部吸脂", "下颌填充", "光子嫩肤", "色斑治疗", "脱毛", "面部提升", "拉皮", "吸脂", "乳房缩小", "乳头整形", "褪眉", "褪眼线", "祛斑", "祛胎记", "面部精雕", "脂肪移植", "处女膜修复", "阴道紧缩"],
            "department": "医学美容科",
            "position": "佑康楼一楼。病区位于佑康楼14层"
        },
        {
            "illness": ["镇痛", "器官保护", "疼痛诊疗", "麻醉"],
            "examination": ["打麻醉", "全麻", "半麻"],
            "department": "麻醉科",
            "position": "佑康楼五楼"
        },
        {
            "illness": [],
            "examination": ["开刀", "手术"],
            "department": "中心手术室",
            "position": "佑康楼5楼"
        },
        {
            "illness": [],
            "examination": ["门诊手术", "上药", "换药"],
            "department": "换药室",
            "position": "门诊三楼外科"
        },
        {
            "illness": ["子宫", "卵巢", "妊娠", "盆腔", "不孕", "宫颈", "输卵管", "阴道", "尿失禁", "会阴", "小产", "引产", "流产", "月经", "闭经", "更年期综合征", "分娩", "助产", "盆底", "通乳", "催乳", "产前", "围产期", "剖宫", "产后", "经期", "宫腔", "胎盘", "痛经", "姨妈", "例假", "药流", "避孕", "白带", "回奶", "HPV", "外阴"],
            "examination": ["腹腔镜", "宫腔镜", "取环术", "产检"],
            "department": "妇产科",
            "position": "门诊二楼。病区位于佑康楼8层"
        },
        {
            "illness": ["新生儿", "胎龄", "产儿"],
            "examination": [],
            "department": "新生儿室",
            "position": "佑安楼3楼连廊处"
        },
        {
            "illness": ["矮小症", "小儿", "新生儿", "患儿", "小朋友", "小孩", "孩子", "小娃", "娃娃"],
            "examination": [],
            "department": "儿科",
            "position": "门诊负一楼，电梯直达。病区位于佑安楼南侧2楼"
        },
        {
            "illness": [],
            "examination": ["防疫针", "预防接种", "预防针", "打疫苗", "疫苗接种"],
            "department": "预防保健门诊",
            "position": "门诊负一楼，电梯直达。病区位于佑康楼3楼"
        },
        {
            "illness": ["育龄期"],
            "examination": [],
            "department": "妇女保健室",
            "position": "门诊四楼，电梯直达，出电梯后右侧"
        },
        {
            "illness": ["水肿", "结节", "穴位", "肾虚"],
            "examination": ["针刺", "艾灸", "针灸", "放血", "针药", "推拿", "按摩"],
            "department": "中西医结合科",
            "position": "佑安楼一楼连廊处。病区位于佑安楼三楼"
        },
        {
            "illness": [],
            "examination": ["取中药", "拿中药"],
            "department": "中药房",
            "position": "佑安楼一楼连廊处"
        },
        {
            "illness": [],
            "examination": ["取药", "拿药", "西药"],
            "department": "西药房",
            "position": "门诊一楼楼梯旁边"
        },
        {
            "illness": ["颌面", "牙齿", "口腔", "牙疼", "牙痛", "种牙", "做假牙", "镶牙", "牙周", "牙病", "牙龈", "牙髓", "牙体", "磨牙", "根管", "牙尖", "牙内", "阻生牙", "牙外伤", "颌关节", "义齿", "牙槽", "口腔黏膜", "前牙", "错颌", "唇腭裂", "舌头", "龋齿", "嘴巴里", "嘴里"],
            "examination": ["拔牙", "植牙", "牙齿正畸", "牙齿矫正", "洗牙", "洁牙", "牙修复"],
            "department": "口腔科",
            "position": "门诊四楼"
        },
        {
            "illness": [],
            "examination": ["病理切片", "病理诊断", "查病理", "病理检验", "病理检查"],
            "department": "病理科",
            "position": "佑康楼4楼"
        },
        {
            "illness": ["血型鉴定", "交叉配血"],
            "examination": ["手指血", "抽血", "验血", "血检验处", "化验室", "体液检验", "采血"],
            "department": "医学检验科",
            "position": "门诊二楼，楼梯右侧。病区位于佑康楼4楼"
        },
        {
            "illness": [],
            "examination": ["拿血", "输血", "血液发放", "血液储存"],
            "department": "输血科",
            "position": "佑康楼4楼"
        },
        {
            "illness": ["肠道", "肠炎"],
            "examination": [],
            "department": "肠道门诊",
            "position": "门诊一楼北门右侧"
        },
        {
            "illness": [],
            "examination": ["核酸", "咽拭子", "鼻拭子"],
            "department": "核酸门诊",
            "position": "门诊一楼"
        },
        {
            "illness": [],
            "examination": ["体检"],
            "department": "体检保健科",
            "position": "佑康楼三楼"
        },
        {
            "illness": [],
            "examination": ["打点滴", "输液", "皮下", "皮试"],
            "department": "急诊科输液室",
            "position": "门诊一楼"
        },
        {
            "illness": [],
            "examination": [],
            "department": "同济专家门诊",
            "position": "门诊二楼电梯右侧，知名专家诊室"
        },
        {
            "illness": [],
            "examination": [],
            "department": "太平间",
            "position": "佑安楼东侧"
        },
        {
            "illness": [],
            "examination": ["行政办公"],
            "department": "行政楼",
            "position": "佑康楼西北侧，进医院北门右转到达"
        },
        {
            "illness": [],
            "examination": [],
            "department": "门诊办公室",
            "position": "佑安楼四楼"
        },
        {
            "illness": [],
            "examination": [],
            "department": "医保办公室",
            "position": "佑安楼四楼"
        },
        {
            "illness": [],
            "examination": ["挂号收费", "挂号费", "挂号交费", "挂号缴费"],
            "department": "挂号缴费窗口",
            "position": "门诊一楼大厅"
        },
        {
            "illness": ["腹部疼痛", "腹部痛"],
            "examination": ["拔甲"],
            "department": "普通外科",
            "position": "门诊三楼外科诊区"
        },
        {
            "illness": [],
            "examination": ["停车", "泊车"],
            "department": "地下停车场",
            "position": "佑康楼负一层"
        },
        {
            "illness": [],
            "examination": [],
            "department": "一站式服务中心",
            "position": "门诊一楼"
        },
        {
            "illness": [],
            "examination": ["出院结账", "入院登记", "出院结算", "入院手续", "出院手续"],
            "department": "出入院办理",
            "position": "佑康楼一层"
        },
        {
            "illness": [],
            "examination": ["吃饭", "就餐", "堂食"],
            "department": "食堂",
            "position": "佑安北楼西侧"
        },
        {
            "illness": [],
            "examination": [],
            "department": "学术文化厅",
            "position": "佑安南楼东南侧"
        }
    ]


def check_department(illness1="", illness2="", examination1="", examination2="") -> list:
    """根据具体场景 查找科室和具体位置"""
    suggests = []
    for depart in data:
        if illness1 and illness1 in depart["illness"]:
            this_depart = copy.deepcopy(depart)
            this_depart["this_illness"] = illness1
            suggests.append(this_depart)
        if illness2 and illness2 in depart["illness"]:
            this_depart = copy.deepcopy(depart)
            this_depart["this_illness"] = illness2
            suggests.append(this_depart)
        if examination1 and examination1 in depart["examination"]:
            this_depart = copy.deepcopy(depart)
            this_depart["this_examination"] = examination1
            suggests.append(this_depart)
        if examination2 and examination2 in depart["examination"]:
            this_depart = copy.deepcopy(depart)
            this_depart["this_examination"] = examination2
            suggests.append(this_depart)

    return suggests


def return_answer_string(suggests: list) -> str:
    """根据详细需要 组装引导话术tts"""
    depart_dict = {}
    for r in suggests:
        if not depart_dict.__contains__(r["department"]):
            depart_dict[r["department"]] = {
                "this_illness": [r["this_illness"]] if r.__contains__("this_illness") else [],
                "this_examination": [r["this_examination"]] if r.__contains__("this_examination") else [],
                "position": r["position"]
            }
        else:
            if r.__contains__("this_illness"):
                depart_dict[r["department"]]["this_illness"].append(r["this_illness"])
            if r.__contains__("this_examination"):
                depart_dict[r["department"]]["this_examination"].append(r["this_examination"])
    answer_string = ""
    for department, item in depart_dict.items():
        if len(item["this_illness"]) > 1:
            answer_string += f"""{"、".join(item["this_illness"])}，出现这些症状建议您去{department}，位置在{item["position"]}。"""
        elif len(item["this_illness"]) > 0:
            answer_string += f"""{"、".join(item["this_illness"])}，建议您去{department}，位置在{item["position"]}；具体请根据自身情况选择前往。"""

        if len(item["this_examination"]) > 1:
            answer_string += f"""{"、".join(item["this_examination"])}，均去{department}，位置在{item["position"]}。"""
        elif len(item["this_examination"]) > 0:
            answer_string += f"""{"、".join(item["this_examination"])}，去{department}，位置在{item["position"]}。具体请前往咨询。"""
    return answer_string


if __name__ == '__main__':
    print(return_answer_string(check_department(illness1="高血糖", illness2="糖尿病", examination1="", examination2="")))
