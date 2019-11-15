# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/15

"""  路径相关操作工具模块 """

import os
import sys
from six import PY3

if PY3:
    def decode_path(path):
        return path
else:
    def decode_path(path):
        return path.decode(sys.getfilesystemencoding()) if path else path

CURRENT_PATH = decode_path(os.path.dirname(os.path.realpath(__file__)))  # 获取当前文件所在路径


def get_root_path():
    """
    获取根目录

    :return:
    """
    return os.path.dirname(os.path.dirname(CURRENT_PATH))


def get_config_path(file_path):
    """
    获取config文件夹路径

    :param file_path:
    :return:
    """
    return double_slanting_bar_change(os.path.join(get_root_path(), "core", "config", file_path))

#获取服务器临时存放apk地址路径
def get_service_save_apk_path():
    return double_slanting_bar_change(os.path.join(get_root_path(), "services", "temp/apk"))

def get_cells_backup_path():
    return double_slanting_bar_change(os.path.join(get_root_path(), "services", "temp/files/backup.json"))

def get_devices_list_file():
    return os.path.join(get_root_path(), "core", "ui_action", "ui_install.json")

#获取设备的脚本路径

def get_device_script_path():
    """
    获取设备的脚本路径

    :return:
    """
    return double_slanting_bar_change(os.path.join(get_root_path(), "core","ui_action", "device"))


def get_game_script_path():
    """
    获取游戏的脚本路径

    :return:
    """
    return double_slanting_bar_change(os.path.join(get_root_path(), "script", "game"))


def get_log_save_path():
    """
    获取log文件存放路径

    :return:
    """
    log_save_path = double_slanting_bar_change(os.path.join(get_root_path(), "logs"))
    if not os.path.exists(log_save_path):
        os.makedirs(log_save_path)

    return log_save_path


def check_dir_or_create(path):
    """

    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_aapt_path():
    """
    获取aapt文件路径

    :return:
    """
    return double_slanting_bar_change(os.path.join(get_root_path(), "core/tools/win", "aapt"))


def double_slanting_bar_change(path):
    """

    :param path:
    :return:
    """
    if path is None or path == "":
        return path

    if "\\" in path:
        return path.replace('\\', '/')
    return path
