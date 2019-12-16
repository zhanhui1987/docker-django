#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/5/9 0:32
# @Author  : zhanhui
# @File    : my_tool.py


"""
    本包主要用于封装django views.py中常用的一些函数。
"""


def init_response_data(list_field=None, dict_field=None, zero_field=None):
    # 初始化页面返回的数据。list_field用于接受需要其初始化为空数组的字段，用英文","连接多个字段；dict_field
    # 用于接受需要初始化为空字段的字段，用英文","连接多个字段;zero_field用于接受需初始化为0的字段，用英文","连接多个字段

    response_data = {"results": [], "results_count": 0, "data": {}, "error_msg": "", "total": 0}

    # 将list_field传入的字段初始化为空数组
    if list_field is not None:
        for field in list_field.split(","):
            response_data[field] = []

    # 将dict_field传入的字段初始化为空字典
    if dict_field is not None:
        for field in dict_field.split(","):
            response_data[field] = dict()

    # 将zero_field传入的字段初始化为0
    if zero_field is not None:
        for field in zero_field.split(","):
            response_data[field] = 0

    return response_data


def init_update_response_data():
    # 初始化更新操作类api的返回函数

    response_data = {"success": 0, "error_msg": ""}

    return response_data


def get_choice_map(choice):
    # 将models中定义的CHOISCE，转换成dict结构

    choice_dict = dict()

    # choice应该是元组结构，其中包含了多个小元组，每一个小元组都应包含两个元素，第一个作为键，第二个作为值
    if isinstance(choice, tuple):
        for row in choice:
            if isinstance(row, tuple) and len(row) == 2:
                choice_dict[row[0]] = row[1]

    return choice_dict


def set_field_detail(data, field, detail_map=None, choice=None, delete_origin_key=False, replace_origin_str=False):
    # 将数据库中一些choice类型的数据，转换成页面显示的样式（通过设置detail的方式来实现）

    if isinstance(data, dict):
        if detail_map is None and choice is not None:
            detail_map = get_choice_map(choice)

        filed_value = data.get(field)
        if isinstance(detail_map, dict) and filed_value is not None:
            # 查看是否需要将原始值进行替换，还是重新赋新的值
            if replace_origin_str:
                data[field] = detail_map.get(filed_value) or filed_value
            else:
                data["%s_detail" % field] = detail_map.get(filed_value) or filed_value

            # 获取到显示用的值之后，查看是否需要将原始键删除
            if delete_origin_key:
                del data[field]
