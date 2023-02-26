#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from utils.handler import Handlers

if __name__ == '__main__':

    database_info = {
        "host": "localhost",
        # "host": "172.16.23.33",
        "password": "",
        "dbname": "nlpautotest",
        "user": "root",
        "port": "3306",
        "dbtype": "mysql",
        "dbengine": "pymysql"
    }
    f = Handlers()
    f.excel_to_database(sql_engine=f.database_engine(database_info),
                        excel_path=r"C:\Users\admin\Desktop\线上badcase每周导入数据\原始标注数据\week-0627-0703.xlsx",
                        sheet_name="Sheet1",
                        db_table_name="skill_base_test")