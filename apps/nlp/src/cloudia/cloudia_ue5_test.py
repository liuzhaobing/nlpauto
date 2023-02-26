#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import time
import xlwt

"""cloudia 新旧UE引擎对比测试 监控CPU、GPU、MEM占用情况"""


def cloudia_cpu(file_path, addr):
    """持续监控某个地址的CPU、GPU、MEM情况"""
    cpu_logfile = file_path + str(time.time()) + "cpu.log"
    gpu_logfile = file_path + str(time.time()) + "gpu.log"

    file_cpu = open(cpu_logfile, "a")
    file_gpu = open(gpu_logfile, "a")

    for i in range(900):
        os.system("adb connect {}".format(addr))
        os.system("adb root")

        with os.popen("adb shell cat /sys/class/kgsl/kgsl-3d0/gpu_busy_percentage", "r") as f:
            gpus = f.read()
        file_gpu.write(str(gpus))

        with os.popen('adb shell "top -d 1 -n 1 -b | grep  com.CloudMinds.RobotEngine"', "r") as f:
            cpus = f.read()
        file_cpu.write(str(cpus))

        time.sleep(2)

    file_gpu.close()
    file_cpu.close()

    return cpu_logfile, gpu_logfile


def log_row_format(info):
    """将一行数据 格式化到list 并删掉所有的空元素"""
    new = []
    li = info.split(" ")
    for i in li:
        if i != "":
            new.append(i)
    return new


def log_to_list_list(file):
    """将cpu.log文件 读取为list[map]"""
    data = []
    with open(file, 'r') as f:
        ds = f.readlines()
    for d in ds:
        data.append(log_row_format(d))

    return data


def list_write_to_excel(data, file_name):
    """将list[list]写入excel表格"""
    f = xlwt.Workbook('encoding=utf-8')
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=False)
    headers = ["PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "ARGS"]

    for v in range(len(headers)):
        sheet1.write(0, v, headers[v])
    for y in range(len(data)):
        for x in range(len(data[y])):

            value = data[y][x][:-1]

            if data[y][x][-1] == "G":
                data[y][x] = float(value) * 1024

            elif data[y][x][-1] == "K":
                data[y][x] = float(value) / 1024

            elif data[y][x][-1] == "M":
                data[y][x] = float(value)

            sheet1.write(y + 1, x, data[y][x])

    f.save(file_name + 'test.xlsx')


def main(log_file):
    cpu_logfile, gpu_logfile = cloudia_cpu(log_file, "10.12.97.45:5555")

    data = log_to_list_list(cpu_logfile)
    list_write_to_excel(data, cpu_logfile)


if __name__ == '__main__':
    log_path = r"D:\cloudia\20220624\data\4301\logs"
    main(log_path)
