#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
1.先读取到数据库已有的case
2.将已有case的question放入一个列表A中
3.将需要新增的excel case导入成list[map]
4.遍历此list[map] 查看其question是否在列表A中
5.如果不存在，则将该条case加入到新的list[map] 同时将question加入一个临时的列表B中 继续向下遍历
6.遍历过程中查看其question是否在列表A和列表B中
7.如果不存在，则将该条case加入到新的list[map]
8.遍历结束，将新的list[map]导出成excel 保存到本地
"""
from utils.handler import Handlers
from utils.utils_mysql import DataBaseMySQL


def case_duplicate(file_name, sheet_name="Sheet1"):
    dbinfo1 = {
                'host': '172.16.23.33',
                'user': 'root',
                'password': '',
                'port': 3306,
                'dbname': 'nlpautotest'
            }
    database_cases = DataBaseMySQL(dbinfo1).query("select * from skill_base_test;")
    database_cases_q = Handlers.read_column_as_list(database_cases, "question")

    excel_cases = Handlers.read_excel_as_list_map(io=file_name, sheet_name=sheet_name)
    new_list_map = []
    new_q = []

    for case in excel_cases:
        if case["question"] not in database_cases_q:
            if case["question"] not in new_q:
                new_list_map.append(case)
                new_q.append(case["question"])

    Handlers.write_list_map_as_excel(new_list_map, excel_writer=file_name+".new.xlsx", sheet_name=sheet_name, index=False)


if __name__ == '__main__':
    file = r"C:\Users\admin\Desktop\20220622_skill_new.xlsx"
    case_duplicate(file)
