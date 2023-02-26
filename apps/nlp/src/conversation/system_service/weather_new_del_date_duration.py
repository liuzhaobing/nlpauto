# -*- coding:utf-8 -*-
import datetime

"""
解决date和duration冲突的问题
上一轮出现过date 本轮又新入duration 则清空的date 只向api中传递本轮的duration
"""
slot1 = "date"
slot2 = "duration"

input_slot1 = "input_date"
input_slot2 = "input_duration"
current_intent = proResult["quresult"]["intent"]


def del_date_or_duration():
    if proResult["session"].__contains__("slots") and proResult["quresult"].__contains__("slots"):
        session_slots = proResult["session"]["slots"]
        current_slots = proResult["quresult"]["slots"]
        if current_slots.__contains__(slot1) and session_slots.__contains__(slot2):
            proResult["session"]["variables"][input_slot2] = {"key": input_slot2, "value": ""}
        if current_slots.__contains__(slot2) and session_slots.__contains__(slot1):
            proResult["session"]["variables"][input_slot1] = {"key": input_slot1, "value": ""}
    else:
        return ""


def check_data_duration_string():
    """check invalidation of date and duration, service api support only recent a week weather info"""
    duration = proResult["session"]["variables"]["input_duration"]["value"]
    date = proResult["session"]["variables"]["input_date"]["value"]

    duration_ok = "yes"
    now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')

    if len(duration) == 21:
        duration_li = duration.split("/")
        date_1 = datetime.datetime.strptime(duration_li[0], '%Y-%m-%d')
        date_2 = datetime.datetime.strptime(duration_li[1], '%Y-%m-%d')

        if date_1 >= date_2:
            duration_ok = "no"
            return duration_ok

        """
        service api support only recent a week weather info (total 6 days)
        but SDK returns recent a week string (total 7 days)
        """
        if duration_li[0] == now.strftime('%Y-%m-%d') and \
                duration_li[1] == (now + datetime.timedelta(days=7)).strftime('%Y-%m-%d'):
            duration_li[1] = (now + datetime.timedelta(days=6)).strftime('%Y-%m-%d')
            proResult["session"]["variables"]["input_duration"]["value"] = "/".join(duration_li)
            duration_ok = "yes"
            return duration_ok

        if current_intent in ["GetPollution", "GetPollution_Followup"] \
                and ((date_2 - date_1).days > 2 or (date_2 - now).days > 3 or (date_1 - now).days > 6):
            duration_ok = "three_days"
            return duration_ok

        if current_intent in ["GetDressingIndex", "GetDressingIndex_Followup",
                              "GetExerciseIndex", "GetExerciseIndex_Followup",
                              "GetLivingIndex", "GetLivingIndex_Followup",
                              "GetWashingIndex", "GetWashingIndex_Followup"] \
                and ((date_2 - date_1).days != 0 or (date_2 - now).days != 0 or (date_1 - now).days != 0):
            duration_ok = "today"
            return duration_ok

        if (date_2 - date_1).days > 7 or (date_2 - now).days > 8 or (date_1 - now).days > 6:
            duration_ok = "no"
            return duration_ok

        return duration_ok

    if len(date) == 10:
        date_1 = datetime.datetime.strptime(date, '%Y-%m-%d')
        count_now_to_end = date_1 - now
        if current_intent in ["GetPollution", "GetPollution_Followup"] and count_now_to_end.days > 3:
            duration_ok = "three_days"
            return duration_ok

        if current_intent in ["GetDressingIndex", "GetDressingIndex_Followup",
                              "GetExerciseIndex", "GetExerciseIndex_Followup",
                              "GetLivingIndex", "GetLivingIndex_Followup",
                              "GetWashingIndex", "GetWashingIndex_Followup"] \
                and count_now_to_end.days != 0:
            duration_ok = "today"
            return duration_ok

        if count_now_to_end.days > 6:
            duration_ok = "no"
            return duration_ok

    return duration_ok


del_date_or_duration()
proResult["session"]["variables"]["duration_ok"] = {"key": "duration_ok", "value": check_data_duration_string()}
