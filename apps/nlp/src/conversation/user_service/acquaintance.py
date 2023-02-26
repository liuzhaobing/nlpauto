# -*- coding:utf-8 -*-
import json

relative = {
    "score1": "A",
    "score2": "B",
    "score3": "C",
    "score4": "D"
}

question_list = [
    {
        "id": 0,
        "theme": 0,
        "theme_type": 0,
        "question": "您平时工作之余，最喜欢做以下哪件事情呢？\nA. 看动漫；\nB. 听音乐；\nC. 摄影；\nD. 看电影;",
        "score1": 3,
        "score2": 8,
        "score3": 8,
        "score4": 4
    },
    {
        "id": 1,
        "theme": "A",
        "theme_type": "动漫",
        "question": "《鬼灭之刃》主角的名字是？\nA、灶门炭治郎；\nB、我妻善逸；\nC、嘴平伊之助；\nD、宇髓天元;",
        "score1": 1,
        "score2": 0,
        "score3": 0,
        "score4": 0
    },
    {
        "id": 2,
        "theme": "A",
        "theme_type": "动漫",
        "question": "拔剑神曲出自以下哪部作品？\nA、《黑岩射手》；\nB、《化物语》；\nC、《魔法少女小圆》；\nD、《罪恶王冠》;",
        "score1": 0,
        "score2": 0,
        "score3": 0,
        "score4": 2
    },
    {
        "id": 3,
        "theme": "A",
        "theme_type": "动漫",
        "question": "都是谁的错？《Fate Zero》\nA、间桐慎二；\nB、远坂时臣；\nC、卫宫切嗣；\nD、韦伯;",
        "score1": 0,
        "score2": 3,
        "score3": 0,
        "score4": 0
    },
    {
        "id": 4,
        "theme": "A",
        "theme_type": "动漫",
        "question": "《刀剑神域》主角桐谷和人的外号是什么？\nA、明亮闪光；\nB、黑衣剑士；\nC、无双刺客；\nD、苍蓝蔷薇;",
        "score1": 0,
        "score2": 4,
        "score3": 0,
        "score4": 0
    },
    {
        "id": 5,
        "theme": "B",
        "theme_type": "音乐",
        "question": "您平均每天听音乐的时长是？\nA、1小时及以下；\nB、1至2小时；\nC、2至3小时；\nD、3小时以上或一有时间就会听;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 6,
        "theme": "B",
        "theme_type": "音乐",
        "question": "您是否追求HI-FI无损音质体验？\nA、从不；\nB、偶尔；\nC、经常；\nD、总是;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 7,
        "theme": "B",
        "theme_type": "音乐",
        "question": "您会购买最前沿最专业的音响设备或耳机产品来聆听音乐？\nA、从不；\nB、偶尔；\nC、经常；\nD、总是;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 8,
        "theme": "B",
        "theme_type": "音乐",
        "question": "您觉得音乐是？\nA、消遣打发时间的一种手段；\nB、音乐帮助我思考；\nC、音乐带给我生活的活力和激情；\nD、音乐是生活必不可少的一部分;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 9,
        "theme": "C",
        "theme_type": "摄影",
        "question": "您是否会花时间提升自己的摄影技巧？\nA、从不；\nB、偶尔；\nC、经常；\nD、总是;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 10,
        "theme": "C",
        "theme_type": "摄影",
        "question": "您平时会如何处理您拍摄的照片？\nA、仅存储在电脑或手机中；\nB、打印出来；\nC、在社交网站上分享；\nD、用Photoshop等软件修片后再保存或分享;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 11,
        "theme": "C",
        "theme_type": "摄影",
        "question": "您会购买最前沿最专业的摄影设备来摄影？\nA、从不；\nB、偶尔；\nC、经常；\nD、总是;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 12,
        "theme": "C",
        "theme_type": "摄影",
        "question": "您觉得摄影是？\nA、消遣打发时间的一种手段；\nB、摄影帮助我记录生活的美好；\nC、摄影带给我生活的活力和激情；\nD、摄影是生活必不可少的一部分;",
        "score1": 1,
        "score2": 2,
        "score3": 3,
        "score4": 4
    },
    {
        "id": 13,
        "theme": "D",
        "theme_type": "电影",
        "question": "《生化危机》的女主角的名字是？\nA、玛丽；\nB、艾玛；\nC、安妮；\nD、爱丽丝;",
        "score1": 0,
        "score2": 0,
        "score3": 0,
        "score4": 2
    },
    {
        "id": 14,
        "theme": "D",
        "theme_type": "电影",
        "question": "以下哪部电影出自索尼影视？\nA、《花木兰》；\nB、《蜘蛛侠》；\nC、《星球大战》；\nD、《复仇者联盟》;",
        "score1": 0,
        "score2": 2,
        "score3": 0,
        "score4": 0
    },
    {
        "id": 15,
        "theme": "D",
        "theme_type": "电影",
        "question": "电影《达芬奇密码》的故事发生在以下哪个地点？\nA、卢浮宫博物馆；\nB、奥赛博物馆；\nC、大英博物馆；\nD、纽约博物馆;",
        "score1": 1,
        "score2": 0,
        "score3": 0,
        "score4": 0
    },
    {
        "id": 16,
        "theme": "D",
        "theme_type": "电影",
        "question": "哥斯拉在受到强烈的核辐射前是什么动物？\nA、鳄鱼；\nB、恐龙；\nC、蜥蜴；\nD、穿山甲;",
        "score1": 0,
        "score2": 0,
        "score3": 3,
        "score4": 0
    }]


def get_theme_questions(theme=None, theme_type=None):
    """获取某个主题下的所有题目 存到questions"""
    theme_questions = []
    for question in question_list:
        if theme:
            if question["theme"] == theme:
                theme_questions.append(question)
        elif theme_type:
            if question["theme_type"] == theme_type:
                theme_questions.append(question)
    return theme_questions


def get_a_question(questions, index):
    """取一题存到now_question 剩余题存到questions"""
    if questions:
        now_question = questions[index]
        proResult["session"]["variables"]["now_question"] = {"key": "questions",
                                                             "value": json.dumps(now_question, ensure_ascii=False)}
        proResult["session"]["variables"]["questions"] = {"key": "questions",
                                                          "value": json.dumps(questions, ensure_ascii=False)}
        return True
    return False


def check_answer(now_answer, score):
    """检查答案对应的得分 并统计到当前答题总得分score"""
    if now_answer:
        now_question = json.loads(proResult["session"]["variables"]["now_question"]["value"])
        this_score = now_question[now_answer]
        proResult["session"]["variables"]["score"]["value"] = str(int(score) + int(this_score))
        return True
    return False


def run():
    now_round = proResult["session"]["variables"]["now_round"]["value"]
    now_answer = proResult["session"]["variables"]["now_answer"]["value"]
    now_theme = proResult["session"]["variables"]["now_theme"]["value"]
    score = proResult["session"]["variables"]["score"]["value"]

    """判断是否为第0轮 是则给出主题题目"""
    if now_round == "0":
        questions = question_list[0]
        proResult["session"]["variables"]["now_question"] = {"key": "now_question",
                                                             "value": json.dumps(questions, ensure_ascii=False)}
        return

    """判断是否为最后一轮"""
    if now_round == "5":
        result = get_final_score(score, now_theme)
        proResult["session"]["variables"]["summary"] = {"key": "summary", "value": result}
        return

    """判断是否为第一轮 是第一轮则去取题目"""
    if now_round == "1":
        now_theme = relative[now_answer]
        questions = get_theme_questions(theme=now_theme)
        proResult["session"]["variables"]["now_theme"] = {"key": "now_theme", "value": now_theme}
        proResult["session"]["variables"]["questions"] = {"key": "questions",
                                                          "value": json.dumps(questions, ensure_ascii=False)}

    """进入答题+积分环节"""
    """先检查上一题答得对不对"""
    if now_round != "1" and now_round != "0":
        result = check_answer(now_answer, score)
        if not result:
            print("请输入用户答案！")

    """再取下一道题"""
    questions = json.loads(proResult["session"]["variables"]["questions"]["value"])
    result = get_a_question(questions, int(now_round) - 1)
    if not result:
        print("未获取到下一个question")


def get_final_score(score, now_theme):
    target = question_list[0]

    for x, y in relative.items():
        if now_theme == y:
            if int(score) >= target[x]:
                return "发烧友"
            return "爱好者"


run()
