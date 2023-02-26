#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from apps.tts.src.common.text_to_vector import TextToVector
from apps.tts.src.common.vector_cluster import VectorCluster
from utils.handler import Handlers
from concurrent.futures import ThreadPoolExecutor


class Aggregation:
    def __init__(self, excel_file, output_file, sheet_name, column_name, distance, min_samples):
        self.list_data_duplicated = None
        self.slice_80_needed_column_list = None
        self.needed_column_list = None
        self.original_data_list_map = None
        self.excel_file = excel_file
        self.output_file = output_file
        self.sheet_name = sheet_name
        self.column_name = column_name
        self.distance = distance
        self.min_samples = min_samples
        self.start = Handlers.time_now_10s()
        self.vector_list_list = []  # 每n条数据组成的n/80组文本向量
        self.vector_datas = []  # 所有的文本向量
        self.cluster_datas = None  # 文本向量聚合后的裸结果
        self.text_result = []  # 还原后将写入excel的list[map]

    def pre1(self):
        """数据预处理 """
        self.original_data_list_map = Handlers.read_excel_as_list_map(io=self.excel_file, sheet_name=self.sheet_name)
        self.original_data_list_map = Handlers.list_map_split(self.original_data_list_map, self.column_name)
        self.list_data_duplicated = Handlers.list_duplicate_removal(self.original_data_list_map)
        self.needed_column_list = Handlers.read_column_as_list(self.list_data_duplicated, self.column_name)
        self.slice_80_needed_column_list = Handlers.list_slice_to_n(self.needed_column_list, 80)

    def convert(self, i, v):
        return self.vector_list_list.insert(i, TextToVector.run(v))

    def convert2(self):
        for s in self.vector_list_list:
            self.vector_datas += s
        return self.vector_datas

    def pre2(self):
        """数据转文本向量 多线程 好像有bug"""
        threadpool = ThreadPoolExecutor(10)
        for i in range(len(self.slice_80_needed_column_list)):
            print(Handlers.time_strf_now(), "processing vector %d/%d..." % (i, len(self.slice_80_needed_column_list)))
            threadpool.submit(self.convert, i, self.slice_80_needed_column_list[i])
        threadpool.shutdown(True)

    def pre22(self):
        """数据转文本向量 单线程"""
        for v in self.slice_80_needed_column_list:
            print(Handlers.time_strf_now(), "processing vector %d/%d..." % (self.slice_80_needed_column_list.index(v) + 1, len(self.slice_80_needed_column_list)))
            a_80 = TextToVector.run(v)
            self.vector_list_list.append(a_80)
        return self.vector_list_list

    def pre3(self):
        """文本向量进行聚类"""
        self.cluster_datas = VectorCluster.run(self.convert2(), self.distance, self.min_samples)
        return self.cluster_datas

    def pre4(self):
        """还原聚类后的数据"""
        for group_index, group_value in self.cluster_datas.items():
            for location in group_value:
                column_value = self.needed_column_list[location]
                for origin in self.original_data_list_map:
                    if origin[self.column_name] == column_value:
                        origin["Group"] = group_index
                        self.text_result.append(origin)
        return self.text_result

    def pre5(self):
        """还原后的数据写入excel"""
        Handlers.write_list_map_as_excel(self.text_result, excel_writer=self.output_file, sheet_name=self.sheet_name, index=False)
        end = Handlers.time_now_10s()
        print("it cost time: ", (end - self.start) / 60, "minutes")
        return self.output_file

    def main(self):
        self.pre1()
        self.pre22()
        self.pre3()
        self.pre4()
        self.pre5()


def main(excel_file, output_file, sheet_name, column_name, distance, min_samples):
    """
    根据excel某一列进行聚合生成新的excel
    :param excel_file: 待聚合Excel文件全路径
    :param output_file: 聚合结果Excel文件全路径
    :param sheet_name: 待聚合Excel表单名
    :param column_name: 待聚合Excel列名
    :param distance:
    :param min_samples:
    :return:聚合结果Excel文件全路径
    """
    Aggregation(excel_file, output_file, sheet_name, column_name, distance, min_samples).main()


if __name__ == '__main__':
    main(excel_file=r"D:\case\达闼科技导出记录2022-05-12-11-03-07.xlsx", sheet_name="Sheet1", column_name="问题",
         distance=0.2, min_samples=1, output_file=r"D:\case\达闼科技导出记录_聚类结果.xlsx")