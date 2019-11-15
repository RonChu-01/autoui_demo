# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/10/24.
# Copyright (c) 2019 3KWan.
# Description :
import json


def file_to_json(file_path):
    """
    从文件读取json数据

    :param file_path:
    :return:
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(str(e))
        return None


def json_to_file(file_path):
    """
    写json数据到文件

    :param file_path:
    :return:
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(f)
    except Exception as e:
        print(str(e))
