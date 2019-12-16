#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2019/4/3 0:03
# @Author  : zhanhui
# @File    : my_subprocess.py


import subprocess


def my_popen(cmd_line, get_result=False):
    """
    封装subprocess的popen
    :return:
    """

    result = None
    error = None

    if cmd_line:
        # 运行传入的命令
        p = subprocess.Popen(cmd_line, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)

        # 查看是否需要获取命令执行结果
        if get_result:
            result, error = p.communicate()

    return result, error
