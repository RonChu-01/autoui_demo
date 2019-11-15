# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/15

""" 主入口文件 """

from core import handle


def invoke_one_device(pak_path):
    """
    调用一台设备,随机调用一台设备，至于那台设备，由系统随机分配

    :param pak_path:
    :return:
    """
    pass


def invoke_multi_device(apk_path, game_name="", channel_name="", package_name="", launchable_activity=""):
    """
    调用多台设备

    :param apk_path:
    :param devices:
    :param game_name:
    :param channel_name:
    :param package_name:
    :param launchable_activity:
    :return:
    """
    return handle.invoke_multi_device(apk_path=apk_path, game_name=game_name, channel_name=channel_name, package_name=package_name, launchable_activity=launchable_activity)


def invoke_target_device(apk_path, model=None, game_name="", channel_name="", package_name="", launchable_activity=""):
    """
    调用指定设备,根据手机型号调用指定的设备，如果此设备不包含在内，则调用失败

    :param apk_path:
    :param devices:
    :param game_name:
    :param channel_name:
    :param package_name:
    :param launchable_activity:
    :return:
    """
    return handle.invoke_target_device(apk_path=apk_path, model=model, game_name=game_name, channel_name=channel_name, package_name=package_name, launchable_activity=launchable_activity)
