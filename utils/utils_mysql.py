#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pymysql


# 读取db数据为list[map]
class DataBaseMySQL:
    def __init__(self, db_info):
        self.conn = pymysql.connect(host=db_info['host'], port=db_info['port'], user=db_info['user'],
                                    password=db_info['password'], db=db_info['dbname'],
                                    charset='utf8', autocommit=True)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 读取为列表+字典格式

    def query(self, query_string):
        self.cursor.execute(query_string)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    dbinfo1 = {
            'host': '172.16.23.33',
            'user': 'root',
            'password': '',
            'port': 3306,
            'dbname': 'nlpautotest'
        }
    dbinfo = {'host': '172.16.13.134', 'user': 'bigdata_sync', 'password': '1qaz@WSX',
     'port': 31145, 'dbname': 'kbs_cms'}
    res = DataBaseMySQL(dbinfo).query("select * from fqaitem;")
    print(res)