# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/15
#

"""  配置文件加载类 """

from core.const import const
from core.libs.logs.logger import Logger
from core.utils.path_util import *


def load_local_config(device_file):
    config_file = get_config_path("local/" + device_file)
    if not os.path.exists(config_file):
        Logger.error("local.properties is not exists. " + config_file)
        return None

    cf = open(config_file, "r")
    lines = cf.readlines()
    cf.close()

    config = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue

        dup = line.split('=')
        config[dup[0]] = dup[1]

    return config


def find_uuid_from_device(device):
    """
    通过serial_no查找对应设备uuid

    :param device:
    :return:
    """
    if device is None or device == "":
        return None

    # 获取设备配置文件
    devices = load_local_config(const.DEVICE_FILE)
    if devices is None or len(devices) <= 0:
        return None

    if device in devices:
        return devices[device]

    return None
