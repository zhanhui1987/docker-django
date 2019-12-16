#!/usr/bin/env python
# coding: utf-8

# @Time    : 2018/12/26 17:57
# @Author  : Zhanhui
# @File    : process_monitor.py


"""
监控z1987_web的一些主要进程，发现有进程异常退出时，将其进行重启。
"""


import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sysadmin.z1987_glib.my_conf import ConfFile, get_int_option
from sysadmin.z1987_glib.my_subprocess import my_popen


def main():
    while True:
        # 查看脚本是否已在运行中
        if _get_current_pid_count(__file__) > 1:
            break

        monitor()

        time.sleep(5)


def monitor():
    # 获取Process monitor: 配置文件信息
    conf_dict = _get_conf_dict()

    if conf_dict:
        for section, s_dict in conf_dict.items():
            active = get_int_option(s_dict.get("active"))

            if active == 1:
                cmd_line = s_dict.get("cmd_line")
                sub_cmd_line = s_dict.get("sub_cmd_line")
                pid_count = get_int_option(s_dict.get("pid_count"))
                init_cmd_line = s_dict.get("init_cmd_line")
                stop_cmd_line = s_dict.get("stop_cmd_line")
                premise_file = s_dict.get("premise_file")

                # 检测前置文件是否存在
                if premise_file and not os.path.isfile(premise_file):
                    continue

                if cmd_line and pid_count:
                    current_pid_count = _get_current_pid_count(cmd_line)

                    if current_pid_count != pid_count:
                        _restart_cmdline(cmd_line, sub_cmd_line, init_cmd_line, stop_cmd_line)


def _get_conf_dict():
    """
    从监控配置文件中获取配置信息
    :return:
    """

    conf_file = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "process_monitor.ini"))

    cf_obj = ConfFile(conf_file)
    conf_dict = cf_obj.conf_dict

    return conf_dict


def _restart_cmdline(cmd_line, sub_cmd_line=None, init_cmd_line=None, stop_cmd_line=None):
    """
    重启cmd_line。在重启前，需要将相应的进程kill掉。
    :param cmd_line:
    :param sub_cmd_line:
    :return:
    """

    kill_cmd_line = "kill -s 9 `ps -ef | grep '%s' | grep -v grep | awk '{print $2}'`"

    # 将残余的子进程kill掉
    if sub_cmd_line is not None:
        for sub_cmd in sub_cmd_line.split("<>"):
            my_popen(kill_cmd_line % sub_cmd)

    # 将残余的主进程kill掉
    if cmd_line:
        my_popen(kill_cmd_line % cmd_line)

        # 查看是否有stop_cmd_line，是的话将其执行
        if stop_cmd_line is not None:
            my_popen(kill_cmd_line % stop_cmd_line)

        # 将主进程重启
        if init_cmd_line is not None:
            my_popen(init_cmd_line)
        else:
            my_popen(cmd_line)


def _get_current_pid_count(cmd_line):
    """
    获取当前进程的pid总数
    :param cmd_line:
    :return:
    """

    count = 0

    if cmd_line:
        # 获取进程命令的总数
        ps_cmd_line = "ps -ef | grep '%s' | grep -v grep | wc -l" % cmd_line

        result, error = my_popen(ps_cmd_line, True)
        if error is None:
            count = get_int_option(result.strip())

    return count


if __name__ == "__main__":
    main()
