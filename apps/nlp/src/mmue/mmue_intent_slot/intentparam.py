# -*- coding:utf-8 -*-
import json

from utils.handler import Handlers
from utils.utils_mysql import DataBaseMySQL

"""required : select * from intentparam where agentid=1;
intentid : select id,intentname from intent where agentid=1;
domainid : select id,domainname from domain where agentid=1;
agentid : 1
resparam : sys.entity.song
fromparam : song
entityid : select id,entityname from entity where agentid=1;
"""


def get_intent_param_json_file(path):
    """读取SDK配置文件json中槽位等信息"""
    with open(path, "r") as f:
        data = json.load(f)

    all_slots = []
    all_intents = []
    for domain in data["domains"]:
        domain_name = domain["name"]
        slots_map = {}
        if domain.__contains__("allowed_entity_type"):
            for entity_type in domain["allowed_entity_type"]:
                li = entity_type.split(":")
                slots_map[li[1]] = li[0]

        if domain.__contains__("intents"):
            intent_list = domain["intents"]
            for intent in intent_list:
                intent_name = intent["name"]
                all_intents.append({
                    "domainname": domain_name,
                    "intentname": intent_name
                })
                if intent.__contains__("slots"):
                    intent_slots = intent["slots"]
                    for slot in intent_slots:
                        entity_type_1 = slots_map[slot]
                        intent_info = {
                            "domainname": domain_name,
                            "intentname": intent_name,
                            "resparam": entity_type_1,
                            "fromparam": slot
                        }
                        if 1 == 1:
                            if intent.__contains__("rename_domain"):
                                intent_info["domainname"] = intent["rename_domain"]
                        all_slots.append(intent_info)
    return all_slots, all_intents


def sql_query(db_info, query_string):
    """
    dbinfo = {'host': '172.16.13.134', 'user': 'bigdata_sync', 'password': 'xxx', 'port': 31145, 'dbname': 'kbs_cms'}
    """
    return DataBaseMySQL(db_info).query(query_string)


def get_exist_intent_param(db_info):
    """读取数据库中记录的槽位信息"""
    sql = "select intentid,domainid,agentid,resparam,fromparam,entityid from intentparam where agentid=1;"
    return sql_query(db_info=db_info, query_string=sql)


def get_domain_id(db_info):
    """获取数据库中domain/intent/slot 表id信息"""
    sql = "select id,domainname from domain where agentid=1;"
    domain_list = sql_query(db_info=db_info, query_string=sql)
    domains = []
    for domain in domain_list:
        domains.append({"domainname": domain["domainname"], "domainid": domain["id"]})
    return domains


def get_intent_id(db_info):
    """获取数据库中domain/intent/slot 表id信息"""
    sql = "select id,intentname from intent where agentid=1;"
    intent_list = sql_query(db_info=db_info, query_string=sql)
    intent_map = {}
    for intent in intent_list:
        intent_map[intent["intentname"]] = intent["id"]
    return intent_map


def get_slot_id(db_info):
    """获取数据库中domain/intent/slot 表id信息"""
    sql = "select id,entityname from entity where agentid=1;"
    slot_list = sql_query(db_info=db_info, query_string=sql)
    slot_map = {}
    for slot in slot_list:
        slot_map[slot["entityname"]] = slot["id"]
    return slot_map


def get_domain_and_intent_id(db_info):
    """从表domain和表intent中查询关联的domain和intent及各自的id信息"""
    sql = "select i.id intentid, i.intentname intentname, i.domainid domainid, d.domainname domainname from intent i, domain d where i.agentid=1 and d.id=i.domainid;"
    return sql_query(db_info=db_info, query_string=sql)


def get_domain_and_intent_and_slots_id(db_info):
    """从表intentparam和表domain和表intent中查询关联的domain、intent、entity及各自的id信息"""
    sql = "select i.id intentid, i.intentname intentname, i.domainid domainid, d.domainname domainname, p.entityid entityid, p.resparam resparam,p.fromparam fromparam from intent i, domain d, intentparam p where i.agentid=1 and d.id=p.domainid and i.id=p.intentid;"
    return sql_query(db_info=db_info, query_string=sql)


def check_json_not_in_database(db_info, sdk_json_file):
    """对比SDK JSON配置文件中有哪些数据不存在于database"""
    already_have = []  # 已经存在的
    sdk_slots_info, sdk_intents_info = get_intent_param_json_file(sdk_json_file)
    db_slots_info = get_domain_and_intent_and_slots_id(db_info)
    for sdk_slots in sdk_slots_info:
        for db_slots in db_slots_info:
            if sdk_slots["domainname"] == db_slots["domainname"] and sdk_slots["intentname"] == db_slots["intentname"]:
                fromparam_skd = sdk_slots["resparam"].split(".")[-1]
                fromparam_db = db_slots["resparam"].split(".")[-1]
                if fromparam_skd == fromparam_db and sdk_slots["resparam"] == db_slots["resparam"] and sdk_slots[
                    "fromparam"] == db_slots["fromparam"]:
                    already_have.append(sdk_slots)

    rest_slots = []  # 还需要新增的
    for sdk_slots in sdk_slots_info:
        if sdk_slots not in already_have:
            rest_slots.append(sdk_slots)

    return rest_slots


def get_detail_info_db_add_column(db_info, sdk_json_file):
    """sdk中有的而database中没有的数据 组装对应的格式"""
    needed_add_intentparam = check_json_not_in_database(db_info, sdk_json_file)
    entity_id_list = get_slot_id(db_info)
    needed = []
    for needed_add in needed_add_intentparam:
        entity_type = needed_add["resparam"].split(".")[-1]
        if entity_id_list.__contains__(entity_type):
            entity_id = entity_id_list[entity_type]
        else:
            entity_id = None
        needed_add["entityid"] = entity_id

        needed.append(needed_add)

    domain_intent = get_domain_and_intent_id(db_info)
    needed_add_new = []
    not_missing = []
    for needed_add in needed:
        for intent in domain_intent:
            new = needed_add.copy()
            if needed_add["domainname"] == intent["domainname"] and needed_add["intentname"] == intent["intentname"]:
                if needed_add not in not_missing:
                    not_missing.append(needed_add)
                new["domainid"] = intent["domainid"]
                new["intentid"] = intent["intentid"]
                if new not in needed_add_new:
                    needed_add_new.append(new)
    missing = []
    """
    missing 代表意图表中没有与domain关联的intent信息
    needed_add_new 代表意图表中有与domain关联的intent信息，也收集到了需要的id，可以直接添加
    """
    for x in needed:
        if x not in not_missing:
            missing.append(x)
    return needed_add_new, missing


def check_intent_and_entity_available(db_info, sdk_json_file):
    """将intent表和entity表缺失的部分补齐"""
    need_add_entity, need_add_intent = get_detail_info_db_add_column(db_info, sdk_json_file)
    # for intent in


def check_domain_database_not_exist(db_info, sdk_json_file):
    """检查数据库中没有 SDK中有的技能清单"""
    already_have = []  # 已经存在的
    sdk_all_slots, sdk_all_domains = get_intent_param_json_file(sdk_json_file)
    db_all_domains = get_domain_id(db_info)
    for sdk_domain in sdk_all_domains:
        for db_domain in db_all_domains:
            if sdk_domain["domainname"] == db_domain["domainname"]:
                already_have.append(sdk_domain)

    rest_domain = []
    for sdk_domains in sdk_all_domains:
        if sdk_domains not in already_have:
            rest_domain.append(sdk_domains)

    return rest_domain


def check_intent_database_not_exist(db_info, sdk_json_file):
    """检查数据库中没有 SDK中有的意图清单"""
    already_have = []  # 已经存在的
    sdk_all_slots, sdk_all_intents = get_intent_param_json_file(sdk_json_file)
    db_all_intents = get_domain_and_intent_id(db_info)

    for sdk_intents in sdk_all_intents:
        for db_intents in db_all_intents:
            if sdk_intents["domainname"] == db_intents["domainname"] and \
                    sdk_intents["intentname"] == db_intents["intentname"]:
                already_have.append(sdk_intents)

    rest_intents = []
    for sdk_intents in sdk_all_intents:
        if sdk_intents not in already_have:
            rest_intents.append(sdk_intents)

    return rest_intents


if __name__ == '__main__':
    # database_info = {'host': '172.16.23.85',
    #                  'user': 'root',
    #                  'password': 'Smartvoice1506',
    #                  'port': 32101,
    #                  'dbname': 'semantic'}
    database_info = {'host': '172.16.13.134',
                     'user': 'root',
                     'password': 'Smartvoice1506',
                     'port': 30027,
                     'dbname': 'semantic'}

    # 需要添加到intentparam表的数据：(如果entityid列为空，则需要先加对应的slot)
    needed_add_intentparam, missing = get_detail_info_db_add_column(database_info, "intentparam_v4.3.0.json")
    Handlers.write_list_map_as_excel(missing, excel_writer="missing.xlsx",
                                     sheet_name="Sheet1", index=False)

    # 需要添加到intent表的数据：
    # needed_add_intent = check_intent_database_not_exist(database_info, "intentparam_v4.3.0.json")
    # Handlers.write_list_map_as_excel(needed_add_intent, excel_writer="needed_add_intent.xlsx", sheet_name="Sheet1",
    #                                  index=False)

    # 需要添加到domain表的数据：
    # needed_add_domain = check_domain_database_not_exist(database_info, "intentparam_v4.3.0.json")
    # Handlers.write_list_map_as_excel(needed_add_domain, excel_writer="needed_add_domain.xlsx", sheet_name="Sheet1",
    #                                  index=False)
