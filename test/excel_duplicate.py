#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from utils.handler import Handlers
"""单个excel case自去重"""

if __name__ == '__main__':
    data = Handlers.read_excel_as_list_map(io=r"C:\Users\admin\Desktop\data_case1.xlsx", sheet_name="Sheet1")
    new_data = []
    new_q = []
    for d in data:
        for q in d["question"].split("&&"):
            if q not in new_q:
                new_q.append(q)
                new_data.append({"question": q, "answer": d["answer"]})

    Handlers.write_list_map_as_excel(new_data, excel_writer=r"C:\Users\admin\Desktop\data_case2.xlsx", sheet_name="Sheet1", index=False)
