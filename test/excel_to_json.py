# -*- coding:utf-8 -*-
import json

import pandas as pd


def read_excel_as_list_map(*args, **kwargs):
    """提取全部excel数据 存入list[map]"""
    df = pd.read_excel(*args, **kwargs)
    list_map = [dict(zip(list(df.columns), line)) for line in df.values]
    return list_map


def format_excel_to_json(file_path, sheet_name):
    new_json_path = file_path.split(".")[-2] + ".json"
    data = read_excel_as_list_map(io=file_path, sheet_name=sheet_name)
    json_data = json.dumps(data, ensure_ascii=False)
    with open(new_json_path, "w") as f:
        f.writelines(json_data)


if __name__ == '__main__':
    path = r"C:\Users\admin\Downloads\pepper个性化标签题库.xlsx"
    sheet = "Sheet1"
    format_excel_to_json(path, sheet)
