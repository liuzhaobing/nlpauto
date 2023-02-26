# -*- coding:utf-8 -*-
import json

proResult = {"quresult": {"domain_id": 319, "domain": "constellation", "intent": "GetConstellation", "slots": {
    "question": {"key": "question", "value": "general_txt", "origin": "运势", "type": "sys.entity.question"},
    "star": {"key": "star", "value": "sheshou", "origin": "射手座", "type": "sys.entity.star"}}},
             "session": {"state": "4kpv5jbhjf",
                         "variables": {"answer_text": {"key": "answer_text", "value": "不好意思，未找到星座相关信息"},
                                       "api_constellation": {"key": "api_constellation",
                                                             "value": "{\"day\":{\"question_info\":{\"day_notice\":\"平平无奇的存在\",\"general_txt\":\"中规中矩的运势，整体表现也可能会是平平无奇。相对低调的一天，而且周围高手林立，想要脱颖而出并不容易，也容易受各种因素的干扰。生活方面容易受虚荣心的驱使，总是有暗自与人比较的情况，警惕别被物欲冲昏头脑。\",\"grxz\":\"金牛座\",\"love_star\":\"3\",\"love_txt\":\"单身的自私抠门的一面容易让好感度下降。恋爱中的总是以自我为中心，容易让恋人心累。\",\"lucky_color\":\"粉色\",\"lucky_direction\":\"东南方\",\"lucky_num\":\"2\",\"lucky_time\":\"12:00-14:00\",\"money_star\":\"3\",\"money_txt\":\"严格做好守财的把关，建议提高自己的理财意识，尽量别乱花钱，保持理性的消费。\",\"summary_star\":\"3\",\"time\":\"20220914\",\"work_star\":\"3\",\"work_txt\":\"不要冲着蝇头小利而行动，会导致捡了芝麻丢西瓜，错失更大的机会，需培养长远的目光。\"}},\"month\":{\"question_info\":{\"general_txt\":\"本月运程一般，单身者有原地踏步的可能，要学会主动制造爱情的机会；工作状态不错，小有进步；财运保持稳定，付出多少就能收获多少。\",\"grxz\":\"处女座\",\"love_star\":\"3\",\"love_txt\":\"单身者：\\n  月初爱情运路过梅雨季节，阴雨绵绵，完全找不到恋爱的影子，不妨把更多精力放在学习工作上，下半月爱情的天空会出现雨后天晴的清爽，多参加聚会活动吧，你的幽默会有意无意吸引到异性的关注。  有伴侣：\\n  恋人对感情的期望值太高，与对方沟通会出现这样那样的不顺，心情不佳。不要太过追求心目中的完美，包容与鼓励才是助长爱情幸福的最有效的肥料；已婚者要小心因为是否借钱给朋友这类事情，而与另一半发生不愉快，凡事要心平气和的沟通才能稳固婚姻。\",\"lucky_direction\":\"正西方\",\"lucky_num\":\"8\",\"money_star\":\"3\",\"money_txt\":\"乐观的心态推动了财运的提升，上半月不妨买点好吃的犒劳自己的工作努力。下半月荷包有机会因为短期投资获利而变得丰满，见好就收，脚踏实地才能使财运稳定。\",\"month_advantage\":\"工作心情愉悦，效率提升，进步明显。\",\"month_weakness\":\"期望越高，失望越大。\",\"summary_star\":\"3\",\"time\":\"202209\",\"work_star\":\"4\",\"work_txt\":\"上班族上班族心情舒畅，工作效率高。月初得益于同事的指点，能找到事半功倍的工作方法，省下不少时间为自己充电。下半月工作平平，没有大的起色，也没有错误发生，更没有把工作情绪带到生活中的情况出现。学生学生族受到周围积极向上的氛围影响，学习积极性高，不仅能及时完成老师布置的功课，还能增加课外知识量。下半月有机会参加校园公益活动，能结识到更多志同道合的朋友。\",\"xrxz\":\"天蝎座\",\"yfxz\":\"射手座\"}},\"tomorrow\":{\"question_info\":{\"day_notice\":\"全面地看待问题\",\"general_txt\":\"整体运势尚可，就是要警惕给自己泼冷水的行为，别轻易打击自己的士气。你能够学会俯视看问题的角度，尽可能地看得全面，也能换不同的切入点进行思考。生活方面可以多与积极上进的人群来往，能够给你带来正能量。\",\"grxz\":\"水瓶座\",\"love_star\":\"3\",\"love_txt\":\"单身的能将心比心，表现出温柔的一面。恋爱中的享受恋人付出的同时，也要为感情付出。\",\"lucky_color\":\"姜黄色\",\"lucky_direction\":\"正东方\",\"lucky_num\":\"1\",\"lucky_time\":\"0:00-2:00\",\"money_star\":\"4\",\"money_txt\":\"不管偏财还是正财，都将迎来陆续进账的机会，尤其偏财更是惊喜连连，能存到不少的钱。\",\"summary_star\":\"4\",\"time\":\"20220915\",\"work_star\":\"4\",\"work_txt\":\"相对成熟稳重的行事方式，你能够在三思后行动，利于规避犯错误，表现更有魄力。\"}},\"week\":{\"question_info\":{\"day_notice\":\"进行自我鞭策\",\"general_txt\":\"多姿多彩的一周，生活将会由聚会、休闲、娱乐、美食来填满，可以朝着自己向往的那种生活靠近。\",\"grxz\":\"处女座\",\"health_txt\":\"运程分析：本周的你无忧无虑，心情畅快，也不用担心健康会出现任何问题。开运饮食：粥易消化有营养是你本周的饮食佳品，特别是杏仁糯米粥还有健脾开胃，益智补脑的功效。健身保健：本周一有空不妨跟随动感的音乐节奏，进行有氧搏击，可锻炼你腰与腹部的力量。健康休闲：逛街虽然是最普通的休闲方式，但本周你在购物的过程中能获得到极大的满足。\",\"love_star\":\"3\",\"love_txt\":\"甜言蜜语本周对你而言极富杀伤力，你常常会因为得到异性的称赞而变得很开心，恋爱中的人会因此尽享甜蜜，单身者面对油嘴滑舌的异性则要多一份警惕心。\",\"lucky_color\":\"玉米黄\",\"lucky_day\":\"星期五\",\"lucky_num\":\"0\",\"money_star\":\"4\",\"money_txt\":\"你在等什么，好运可是站在你这边，短线、长线投资都能有盈利，该出手时就出手。本周尤利于出版、写作行业，靠笔头吃饭的亲，稿酬不错，过稿几率也不小哦！\",\"summary_star\":\"5\",\"time\":\"20220911-20220918\",\"week_notice\":\"心存目标，阔步向前。\",\"work_star\":\"5\",\"work_txt\":\"工作学习上你仿佛拿到了一张职场通行证，无论做什么都感觉很顺心，外出办事更是畅通无阻。若不满足于现状者，可以试着尝试有难度的事务，比较容易获得成就感。\",\"xrxz\":\"处女座\"}},\"year\":{\"question_info\":{\"general_index\":\"60分\",\"general_txt\":\"射手座在2022年会受到家人与恋人充分的滋润，也可能生育小孩或是收养宠物，在情感上会是十分丰富的一年，如果想要购置房屋，5月中以前可找到适合的物件，但工作会较为不稳定，职场口舌是非多，人事变动率高，常常使你处在身心灵较为焦虑的状态，但若能将情绪稳定下来，你的生活在2023年会更有所好转。\",\"health_txt\":\"健康运方面，受到日月蚀发生在健康宫位与心灵宫位的轴线上，射手座5月、10月～11月身体状况不佳，工作有过劳的倾向，注意心血管、肠胃，以及内分泌、腺体的问题。5月、10月～11月的日月蚀除了容易罹患急性疾病之外，心灵层面也会特别焦虑，睡眠品质不佳，情绪起伏剧烈，因此日月蚀期间要当心引发心理上的疾病，注意身心灵的平衡与健康。土星2022年会持续停留在交通宫位，依然要当心交通事故，以免造成身体损伤。\",\"love_index\":\"60分\",\"love_txt\":\"2022年上半年，射手座的爱情运势明显下滑，表现出很疲惫的样子。一向洒脱自由的射手座，面对感情从来不守约苏，同时也经常忽视对方的感受;处理与前任的感情也犹犹豫豫，容易与前任暧昧不清，纠缠反复。因此上半年射手座感情波折不断，很难寻求平静;感情容易夭折。\",\"money_index\":\"80分\",\"money_txt\":\"进入2022年的射手座正财运明显上涨，虽然没有升职加薪，但是射手座的意外之财非常旺盛;有不少的发财机会。个性洒脱自由的射手座，在职场中广结善缘，朋友遍布天下;人际交往上是一把好手，因此射手座但凡有困难，都能得到身边的帮助，贵人运极好。因此2022年射手座的资源人脉极好，是一笔不菲的财富。\",\"oneword\":\"感情波折不断，难求平静生活\",\"time\":\"2022\",\"work_index\":\"60分\",\"work_txt\":\"个性洒脱自由的射手座，在2022上半年的事业运势明显起伏比较大。特别是一门心思想要赚大钱的射手座们，过于急功近利，反而被束手束脚。对于职场小白射手座来说，事业得循序渐进;在职场中占据一定的位置，才有望事业有成。\"}}}"},
                                       "input_question": {"key": "input_question", "value": "general_txt"},
                                       "input_star": {"key": "input_star", "value": "sheshou"},
                                       "input_timeinterval": {"key": "input_timeinterval", "value": ""}}, "slots": {
                     "question": {"key": "question", "value": "general_txt", "origin": "运势",
                                  "type": "sys.entity.question", "deleted": False, "inherit": True},
                     "star": {"key": "star", "value": "sheshou", "origin": "射手座", "type": "sys.entity.star",
                              "deleted": False, "inherit": True}}}, "extra": {
        "api_info": {"http_code": 200, "params": {"date": "", "star": "sheshou"},
                     "response": "{\"star\":\"sheshou\",\"timeinterval_info\":{\"day\":{\"question_info\":{\"day_notice\":\"平平无奇的存在\",\"general_txt\":\"中规中矩的运势，整体表现也可能会是平平无奇。相对低调的一天，而且周围高手林立，想要脱颖而出并不容易，也容易受各种因素的干扰。生活方面容易受虚荣心的驱使，总是有暗自与人比较的情况，警惕别被物欲冲昏头脑。\",\"grxz\":\"金牛座\",\"love_star\":\"3\",\"love_txt\":\"单身的自私抠门的一面容易让好感度下降。恋爱中的总是以自我为中心，容易让恋人心累。\",\"lucky_color\":\"粉色\",\"lucky_direction\":\"东南方\",\"lucky_num\":\"2\",\"lucky_time\":\"12:00-14:00\",\"money_star\":\"3\",\"money_txt\":\"严格做好守财的把关，建议提高自己的理财意识，尽量别乱花钱，保持理性的消费。\",\"summary_star\":\"3\",\"time\":\"20220914\",\"work_star\":\"3\",\"work_txt\":\"不要冲着蝇头小利而行动，会导致捡了芝麻丢西瓜，错失更大的机会，需培养长远的目光。\"}},\"month\":{\"question_info\":{\"general_txt\":\"本月运程一般，单身者有原地踏步的可能，要学会主动制造爱情的机会；工作状态不错，小有进步；财运保持稳定，付出多少就能收获多少。\",\"grxz\":\"处女座\",\"love_star\":\"3\",\"love_txt\":\"单身者：\\n  月初爱情运路过梅雨季节，阴雨绵绵，完全找不到恋爱的影子，不妨把更多精力放在学习工作上，下半月爱情的天空会出现雨后天晴的清爽，多参加聚会活动吧，你的幽默会有意无意吸引到异性的关注。  有伴侣：\\n  恋人对感情的期望值太高，与对方沟通会出现这样那样的不顺，心情不佳。不要太过追求心目中的完美，包容与鼓励才是助长爱情幸福的最有效的肥料；已婚者要小心因为是否借钱给朋友这类事情，而与另一半发生不愉快，凡事要心平气和的沟通才能稳固婚姻。\",\"lucky_direction\":\"正西方\",\"lucky_num\":\"8\",\"money_star\":\"3\",\"money_txt\":\"乐观的心态推动了财运的提升，上半月不妨买点好吃的犒劳自己的工作努力。下半月荷包有机会因为短期投资获利而变得丰满，见好就收，脚踏实地才能使财运稳定。\",\"month_advantage\":\"工作心情愉悦，效率提升，进步明显。\",\"month_weakness\":\"期望越高，失望越大。\",\"summary_star\":\"3\",\"time\":\"202209\",\"work_star\":\"4\",\"work_txt\":\"上班族上班族心情舒畅，工作效率高。月初得益于同事的指点，能找到事半功倍的工作方法，省下不少时间为自己充电。下半月工作平平，没有大的起色，也没有错误发生，更没有把工作情绪带到生活中的情况出现。学生学生族受到周围积极向上的氛围影响，学习积极性高，不仅能及时完成老师布置的功课，还能增加课外知识量。下半月有机会参加校园公益活动，能结识到更多志同道合的朋友。\",\"xrxz\":\"天蝎座\",\"yfxz\":\"射手座\"}},\"tomorrow\":{\"question_info\":{\"day_notice\":\"全面地看待问题\",\"general_txt\":\"整体运势尚可，就是要警惕给自己泼冷水的行为，别轻易打击自己的士气。你能够学会俯视看问题的角度，尽可能地看得全面，也能换不同的切入点进行思考。生活方面可以多与积极上进的人群来往，能够给你带来正能量。\",\"grxz\":\"水瓶座\",\"love_star\":\"3\",\"love_txt\":\"单身的能将心比心，表现出温柔的一面。恋爱中的享受恋人付出的同时，也要为感情付出。\",\"lucky_color\":\"姜黄色\",\"lucky_direction\":\"正东方\",\"lucky_num\":\"1\",\"lucky_time\":\"0:00-2:00\",\"money_star\":\"4\",\"money_txt\":\"不管偏财还是正财，都将迎来陆续进账的机会，尤其偏财更是惊喜连连，能存到不少的钱。\",\"summary_star\":\"4\",\"time\":\"20220915\",\"work_star\":\"4\",\"work_txt\":\"相对成熟稳重的行事方式，你能够在三思后行动，利于规避犯错误，表现更有魄力。\"}},\"week\":{\"question_info\":{\"day_notice\":\"进行自我鞭策\",\"general_txt\":\"多姿多彩的一周，生活将会由聚会、休闲、娱乐、美食来填满，可以朝着自己向往的那种生活靠近。\",\"grxz\":\"处女座\",\"health_txt\":\"运程分析：本周的你无忧无虑，心情畅快，也不用担心健康会出现任何问题。开运饮食：粥易消化有营养是你本周的饮食佳品，特别是杏仁糯米粥还有健脾开胃，益智补脑的功效。健身保健：本周一有空不妨跟随动感的音乐节奏，进行有氧搏击，可锻炼你腰与腹部的力量。健康休闲：逛街虽然是最普通的休闲方式，但本周你在购物的过程中能获得到极大的满足。\",\"love_star\":\"3\",\"love_txt\":\"甜言蜜语本周对你而言极富杀伤力，你常常会因为得到异性的称赞而变得很开心，恋爱中的人会因此尽享甜蜜，单身者面对油嘴滑舌的异性则要多一份警惕心。\",\"lucky_color\":\"玉米黄\",\"lucky_day\":\"星期五\",\"lucky_num\":\"0\",\"money_star\":\"4\",\"money_txt\":\"你在等什么，好运可是站在你这边，短线、长线投资都能有盈利，该出手时就出手。本周尤利于出版、写作行业，靠笔头吃饭的亲，稿酬不错，过稿几率也不小哦！\",\"summary_star\":\"5\",\"time\":\"20220911-20220918\",\"week_notice\":\"心存目标，阔步向前。\",\"work_star\":\"5\",\"work_txt\":\"工作学习上你仿佛拿到了一张职场通行证，无论做什么都感觉很顺心，外出办事更是畅通无阻。若不满足于现状者，可以试着尝试有难度的事务，比较容易获得成就感。\",\"xrxz\":\"处女座\"}},\"year\":{\"question_info\":{\"general_index\":\"60分\",\"general_txt\":\"射手座在2022年会受到家人与恋人充分的滋润，也可能生育小孩或是收养宠物，在情感上会是十分丰富的一年，如果想要购置房屋，5月中以前可找到适合的物件，但工作会较为不稳定，职场口舌是非多，人事变动率高，常常使你处在身心灵较为焦虑的状态，但若能将情绪稳定下来，你的生活在2023年会更有所好转。\",\"health_txt\":\"健康运方面，受到日月蚀发生在健康宫位与心灵宫位的轴线上，射手座5月、10月～11月身体状况不佳，工作有过劳的倾向，注意心血管、肠胃，以及内分泌、腺体的问题。5月、10月～11月的日月蚀除了容易罹患急性疾病之外，心灵层面也会特别焦虑，睡眠品质不佳，情绪起伏剧烈，因此日月蚀期间要当心引发心理上的疾病，注意身心灵的平衡与健康。土星2022年会持续停留在交通宫位，依然要当心交通事故，以免造成身体损伤。\",\"love_index\":\"60分\",\"love_txt\":\"2022年上半年，射手座的爱情运势明显下滑，表现出很疲惫的样子。一向洒脱自由的射手座，面对感情从来不守约苏，同时也经常忽视对方的感受;处理与前任的感情也犹犹豫豫，容易与前任暧昧不清，纠缠反复。因此上半年射手座感情波折不断，很难寻求平静;感情容易夭折。\",\"money_index\":\"80分\",\"money_txt\":\"进入2022年的射手座正财运明显上涨，虽然没有升职加薪，但是射手座的意外之财非常旺盛;有不少的发财机会。个性洒脱自由的射手座，在职场中广结善缘，朋友遍布天下;人际交往上是一把好手，因此射手座但凡有困难，都能得到身边的帮助，贵人运极好。因此2022年射手座的资源人脉极好，是一笔不菲的财富。\",\"oneword\":\"感情波折不断，难求平静生活\",\"time\":\"2022\",\"work_index\":\"60分\",\"work_txt\":\"个性洒脱自由的射手座，在2022上半年的事业运势明显起伏比较大。特别是一门心思想要赚大钱的射手座们，过于急功近利，反而被束手束脚。对于职场小白射手座来说，事业得循序渐进;在职场中占据一定的位置，才有望事业有成。\"}}}}",
                     "url": "http://mmpp-api-server:8087/v1/search_star"}}}

input_star = proResult["session"]["variables"]["input_star"]["value"]
input_timeinterval = proResult["session"]["variables"]["input_timeinterval"]["value"]
input_question = proResult["session"]["variables"]["input_question"]["value"]


def check_input_star():
    """check invalidation of star"""
    if input_star == "":
        return "none"
    if input_star not in ["shuiping", "shuangyu", "baiyang", "jinniu", "shuangzi", "juxie",
                          "shizi", "chunv", "tiancheng", "tianxie", "sheshou", "mojie"]:
        return "false"
    return "true"


def check_input_timeinterval():
    """check invalidation of timeinterval"""
    if input_timeinterval == "":
        return "none"
    if input_timeinterval not in ["day", "tomorrow", "month", "year", "week"]:
        return "false"
    return "true"


def check_input_question():
    """check invalidation of question"""
    if input_question == "":
        return "none"
    if input_question not in ["grxz", "month_weakness", "lucky_direction", "love_index", "month_advantage",
                              "health_txt", "work_index", "work_star", "money_star", "general_txt", "lucky_day",
                              "lucky_time", "general_index", "money_txt", "oneword", "money_index",
                              "week_notice", "xrxz", "lucky_num", "day_notice", "love_txt", "summary_star",
                              "love_star", "lucky_color", "yfxz", "work_txt"]:
        return "false"
    return "true"


def constellation_answer():
    star = check_input_star()
    if star == "none" or star == "false":
        return "不好意思，未找到星座相关信息"

    timeinterval = check_input_timeinterval()
    if timeinterval == "none" or timeinterval == "false":
        timeinterval = "year"
    else:
        timeinterval = input_timeinterval

    question = check_input_question()
    if question == "none" or question == "false":
        question = "general_txt"
    else:
        question = input_question

    api_constellation_json = proResult["session"]["variables"]["api_constellation"]["value"]
    api_constellation = json.loads(api_constellation_json)
    answer = api_constellation[timeinterval]["question_info"][question]
    return answer


proResult["session"]["variables"]["answer_text"] = {"key": "answer_text", "value": constellation_answer()}
print(proResult["session"]["variables"]["answer_text"]["value"])
