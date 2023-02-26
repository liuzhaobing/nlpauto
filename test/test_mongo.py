#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymongo


if __name__ == '__main__':
    con = pymongo.MongoClient("mongodb://root:123456@10.12.32.30:27017")
    db = con["nlpauto"]
    col2 = db["col"]

    _id = col2.insert_one({"result": 1})
    print(_id.inserted_id)
