# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/20.
# Copyright (c) 2019 3KWan.
# Description :

import os
from fnmatch import fnmatch


def get_all_case(path):
    """
    获取目下所有测试文件

        说明：递归遍历文件目录，获取当前路径下所有test开头的py文件；

    :param path:
    :return:
         返回文件路径和文件名
    """

    result = []

    for root, dirs, files in os.walk(path):
        for file in files:
            # 过滤文件
            if fnmatch(file, "test*.py"):
                result.append((root, file))

    return result


def get_all_case_2(path):
    """
    递归遍历文件目录

    :param path:
    :return:
        返回一个生成器generator
    """

    for root, dirs, files in os.walk(path):
        for file in files:
            # 过滤文件
            if fnmatch(file, "test*.py"):
                yield file


def get_all_case_3(path):
    """
    非递归（添加过滤）

    :param path:
    :return:
    """
    result = [file for file in os.listdir(path) if fnmatch(file, "test*.py")]
    return result
