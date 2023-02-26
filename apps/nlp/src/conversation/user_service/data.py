# -*- coding:utf-8 -*-
"""
qa多轮 介绍达闼
"""

thirteen_solutions = [{"id": 1, "name": "智慧城市",
                       "info1": "城市云脑方案，是利用达闼的“HARIX云端大脑”赋能智能城市数字底座，建设物联网+AI中台及城市插座，打造智能化城市数字云脑和孪生数字环境。可以理解为是一种数字基建。",
                       "info2": "这里提到的“HARIX云端大脑”，是达闼核心产品之一，除了机器人、它还可以用在智能设备和物联网上，它的操作系统叫“海睿OS”，像电脑的windows、手机的安卓一样，是人类第三台计算机——机器人的操作系统！"},
                      {"id": 2, "name": "智慧医院或方舱",
                       "info1": "智慧医院或抗疫方案，是基于达闼的“人形机器人Ginger、安保机器人Patrol、清洁机器人Cleaning、配送机器人GingerLite等产品，帮助医护人员完成看诊/测温/巡逻/消杀/送餐送药等工作，借助智能方舱医院平台，还可参与医院的运营/后勤/安全管理和患者服务。",
                       "info2": "达闼机器人在防疫方面的经验相当丰富，从2020年至今，已为国内外十几座城市的80余家医疗机构和方舱医院交付了云端机器人服务，深度参与了上海世博方舱、泉州方舱、武昌方舱、合肥方舱、泰国方舱等的抗疫工作。获得过“2020年度金紫竹奖通信抗疫特别贡献奖”等荣誉的肯定。"},
                      {"id": 3, "name": "智慧教育",
                       "info1": "智慧教育方案，是达闼联合各大高校开设教育课程，或为行业赛事提供平台支持，旨在培养应用型AI人才。借助HARIX RDK应用开发平台，学生不仅可以学习到理论知识，还可以动手开发训练出真实商业环境中所需要的机器人能力。",
                       "info2": "什么是HARIX RDK呢，它属于海睿生态里的一环，可以理解成是为开发者提供的一个开发工具包，它将云端大脑、智能机器人与数字孪生结合在一起，提供一个完整的应用开发环境，形成全球范围内开源开放的、活跃的UGC社区生态。"},
                      {"id": 4, "name": "智慧农业",
                       "info1": "智慧农业方案，是达闼基于多款自研的农业机器人应用，面向智能化全控工业温室，以及中大型果园等场景，帮助农业作业、预判农业全要素影响的整体解决方案。",
                       "info2": "达闼正在打磨全球首款农业采摘机器人，展厅目前还看不到，不过非常值得期待！\n\n它具有超强的视觉识别力，可以识别果实种类/状态/坐标/位置等，完成坐标转换，针对温室大棚等不同场景，完成采摘和装载转运的工作。\n\n此外，达闼还打造了喷药、割草等多款农业机器人。喷药机器人可解决宿迁千亩阳光玫瑰葡萄园与万亩苹果园的喷洒作业。"},
                      {"id": 5, "name": "智慧酒店或餐饮",
                       "info1": "智慧酒店/餐饮方案，是达闼为酒店和餐饮等行业打造的配送/服务/营销等全场景方案。当有客人光临时，机器人可主动提供迎宾拎包、领位带路、点菜跑腿、问答咨询等服务。闲时状态下，机器人可在室内清洁消毒、去室外安保巡逻等，特殊节假日还可以定制活动营销。",
                       "info2": "目前在这个领域，达闼的Ginger Lite D多职配送机器人表现最佳，模块化的设计让它具备高扩展性——可以载托盘、货柜、消毒器械等，接待员、业务员、配送员都是它！\n\n和您在海底捞见到的送餐机器人不同，达闼的机器人是基于云端大脑，有一个数字孪生指挥中心，可以多机多梯，云端监控，万物互联。稳定服务了包括：君诚国际酒店、希尔顿逸林酒店、金科大酒店、维也纳酒店、万豪酒店等在内的知名客户。"},
                      {"id": 6, "name": "智慧场馆",
                       "info1": "智慧场馆方案，是基于达闼的导览机器人Ginger、数字人Cloudia、安保机器人Patrol、清洁机器人Cleaning、配送机器人Ginger Lite等产品，面向科技馆、图书馆、体育馆、博物馆等不同类型的场馆，提供安防/清洁/接待等多种服务，降低场馆活动的运营成本。",
                       "info2": "比较经典的案例比如：Ginger”小智”在中国科技馆化身能歌善舞的讲解员，吸引了不少小朋友驻足观看；与博看合作的Cloudia云渲染数字人”小博“化身首席荐书官，不仅能查书看书还能聊书；与阿法迪合作的Ginger Lite“图小灵”在上海图书馆负责借书还书工作，干得风生水起。"},
                      {"id": 7, "name": "智慧地产",
                       "info1": "智慧地产方案，是基于达闼的迎宾机器人Ginger、安保机器人Patrol、清洁机器人Cleaning、零售机器人Vending等产品，面向地产公司、物业管理提供智能门禁/巡防/清洁/接待等服务。同时，基于机器人实时回传数据，助力地产物业利用云端大脑HARIX构建数字化智能社区管理平台，实现智能管理、降本增效。",
                       "info2": "目前达闼已经和保利、金地等知名地产商合作，售楼机器人不仅能与客户进行趣味互动，还能完成递送饮品、带领参观样板间、讲解沙盘、推荐房型等多种服务。"},
                      {"id": 8, "name": "智慧园区",
                       "info1": "智慧园区方案，是基于达闼云端智能架构及多款云端机器人的协同部署，面向工厂/商业/校园/公园/景点等不同类型的园区场所，提供智能服务、安保、零售等服务。综合运用物联网、大数据、云计算等技术，帮助园区提升数字化运营管理能力，实现智慧化升级。",
                       "info2": "目前达闼的Patrol、Ginger 、Ginger Lite、Cloudia等多款云端机器人已在上海七宝古镇、上海马桥人工智能试验区等项目上大展身手，完成安保巡逻、智能接待、智能配送等工作。"},
                      {"id": 9, "name": "智慧养老",
                       "info1": "智慧养老方案，是基于达闼的服务机器人Ginger、安保机器人Patrol、消毒Cleaning、配送机器人Ginger Lite等产品，围绕老人的健康、安全、陪伴、看护等需求，提供生活监督、健康监护、陪伴聊天、亲情互动等服务，给老年人带来身心双重关怀，独立或辅助老年人护理生活，以全新模式提高智慧康养水平。",
                       "info2": "随着我国迈入老龄化社会，养老机器人市场潜力巨大。达闼很早就开始关注养老事业，也做了很多落地：比如陆续为上海马桥养老院、上海长宁万宏悦馨第一养老院、成都锦欣家园等提供一系列智能机器人，完成药品配送、人员出入管理、夜间安全巡逻等工作，还负责陪伴老年人聊天、唱歌、跳舞，并具有消毒、测温等防疫功能，深受老年人欢迎。\n\n达闼在2021年更凭借“5G云端机器人的助残养老应用”项目，在工信部举办的第四届“绽放杯”5G应用征集大赛智慧生活专题赛中获得嘉奖。"},
                      {"id": 10, "name": "智慧交通",
                       "info1": "智慧交通方案，是基于达闼的导览机器人Ginger、安保机器人Patrol、消毒机器人Cleaning、零售机器人Vending、配送机器人Ginger Lite等多款云端机器人产品。在铁路、机场、汽车站等交通枢纽场所，提供导览、安保、清洁消毒、 零售、应急救援、危险物质检测等服务。",
                       "info2": "目前，达闼机器人已成功服务于北京大兴机场、湖北武当山机场、白洋淀高铁站等交通枢纽，提供航班/机票查询，机场介绍导览和周边生活服务推荐，让旅客体验科技进步带来的人性化出行的同时，也有助于交通运输部门提升智慧化运营管理和服务水平。"},
                      {"id": 11, "name": "智慧工业或能源",
                       "info1": "智慧工业/能源方案，主要依托达闼HARIX工业制造大脑，引入数字孪生技术，让云端机器人服务于诸多生产流程，实现“机器人生产机器人”的无人工厂方案，完成工厂制造、物流、安保、后勤管理的智慧化升级。",
                       "info2": "除了服务机器人行业，达闼在工业互联应用方面也有不少成功应用，比如部署建设了重庆恒隆智慧工厂、达闼新镇智慧园区等。此外，达闼的SD-WAN工业互联专网在满足工业对安全、可靠、高质量的信息传输诉求的同时，将物联网、SD-WAN、云网一体化部署，可以复制到所有移动终端接入到专网和云的业务场景中，为未来的机器人运营提供了新思路。"},
                      {"id": 12, "name": "智慧金融",
                       "info1": "智慧金融方案，是达闼面向金融机构、银行网点等服务场景，通过数字人Cloudia、导览机器人Ginger、递送机器人Ginger Lite等智能设备，满足行业客户对服务扩展能力、安全隔离能力、网点智能升级改造的定制化需求，助力金融机构提升精细化运营水平，创新服务模式，实现智能化转型。",
                       "info2": "例如达闼联合北京光大银行打造的“金融超市”，就由Xpepper机器人担任客服专员；在中国银行5G智能+湾区馆的升级改造中，达闼提供了多款5G云端机器人，配合网点工作人员共同实现“人工+智能”的一体化服务：Ginger在前台负责迎宾、Xpepper全程导览讲解、Ginger Lite则为客户提供点餐式服务。在广西南宁的GIG国际金融中心，Ginger和Ginger Lite为访客、来宾及工作人员提供迎宾接待、路线指引、送餐送物等多种智能化服务。"},
                      {"id": 13, "name": "智慧零售",
                       "info1": "智慧零售方案，指的是达闼借助5G、大数据、人工智能等技术，以多种类型的服务机器人为载体，通过HARIX云端大脑赋能传统零售行业。并基于大数据分析，为高效运营提供决策依据，提高坪效和货品流转，推动传统零售门店的数智化转型。",
                       "info2": "相比同类企业，达闼擅长且具备绝对优势的是智能终端的设计。达闼生产的各类智能机器人帮助供应商实现了柔性生产和库存高效去化，同时以数字广告提供全新盈利底。例如达闼曾与全美首家部署5G的移动运营商Sprint，联合推出了零售行业定制版的“Pepper机器人”，它能够融合客户情绪感知、人脸和物体识别以及多种语言交互，完成客户引导、产品销售等，方便快速部署在机场、便利店、快捷酒店或校园。"}]


def choose_one_solution(id=0, name=""):
    if name != "":
        for s in thirteen_solutions:
            if s["name"] == name:
                return s
    elif id != 0:
        if id > len(thirteen_solutions):
            return None
        return thirteen_solutions[id - 1]
    return None


def return_slot_value(slot_name):
    if proResult["quresult"].__contains__("slots"):
        if proResult["quresult"]["slots"].__contains__(slot_name):
            if proResult["quresult"]["slots"][slot_name].__contains__("value"):
                return proResult["quresult"]["slots"][slot_name]["value"]
            elif proResult["quresult"]["slots"][slot_name].__contains__("origin"):
                return proResult["quresult"]["slots"][slot_name]["origin"]
    return None


solution = return_slot_value("solution")
proResult["session"]["variables"]["solution_success"] = {"key": "solution_success", "value": "false"}
if solution:
    ss = choose_one_solution(id=int(solution))
    if ss:
        proResult["session"]["variables"]["solution_info1"] = {"key": "solution_info1", "value": ss["info1"]}
        proResult["session"]["variables"]["solution_info2"] = {"key": "solution_info2", "value": ss["info2"]}
        proResult["session"]["variables"]["solution_success"] = {"key": "solution_success", "value": "true"}
