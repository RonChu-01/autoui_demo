# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/16
#
# enter python
import os

from core.libs.logs.logger import Logger
from airtest.cli.runner import *
# from airtest.cli.parser import
# from airtest.cli.info import
# from airtest.cli.__main__ import
# from airtest.


# 初始化日志模块
# logger = Logger(os.path.basename(__file__))
#
#     if string_util.is_empty(apk_path):
#         Logger.error("apk file's path can't be None or empty string")
#         return None
#
#     if not apk_path.endswith(".apk"):
#         Logger.error("apk_path not apk type file.....invok failure")
#         return None
#
#     # obtain package name and launchable-activity
#     game_name, package_name, launchable_activity = aapt_util.get_packagename_and_launchable_activity(apk_path)
#     print("game_name : " + game_name + ";package_name:" + package_name + ";launchable_activity:" + launchable_activity)
#     if model is not None:
#         return invoke_target_device(apk_path=apk_path, model=model, game_name=game_name, channel_name=channel_name, package_name=package_name, launchable_activity=launchable_activity)
#     else:
#         return invoke_multi_device(apk_path=apk_path, game_name=game_name, channel_name=channel_name, package_name=package_name, launchable_activity=launchable_activity)
#
#
# if __name__ == '__main__':
#     enter("2471_wdsm_wdsm_3k_20191011_28835_28835.apk", None, "baidu")
