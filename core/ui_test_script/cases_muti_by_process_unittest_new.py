# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/1.
# Copyright (c) 2019 3KWan.
# Description :

import asyncio
import os
import subprocess
import threading
import queue
import concurrent.futures
import time
import traceback
import webbrowser
from concurrent.futures import ProcessPoolExecutor, as_completed
import unittest
import glob
from fnmatch import fnmatch
import importlib

from airtest.cli.runner import AirtestCase
from airtest.core.android.adb import ADB
from airtest.core.api import auto_setup, init_device, assert_equal
from jinja2 import Environment, FileSystemLoader

from core.const.const_config import APP
from core.ui_action.at_install_apk import ActionInstallApk
from core.ui_action.at_permission_allow import ActionAllowPermission
from core.ui_testcase.base import BaseCase
from core.ui_testcase.test_allow_permission import TestAllowPermission
from core.ui_testcase.test_install import TestInstall
from core.utils.aapt_util import get_packagename_and_launchable_activity


class Cases:
    """  业务场景用例 """
    # todo 这里后续可以将用例分层，拆分出去，继承Cases

    @staticmethod
    def execute_install(uuid, apk_path, package_name):
        """  执行安装 """

        install = ActionInstallApk(uuid)

        # 安装相关操作
        proc_ = install.start_install(apk_path)
        if install.ui_install_object_info.get('installing'):
            install.do_installing(install.ui_install_object_info.get('installing'))
        proc_.wait()  # 等待apk安装完毕，执行后续操作

        install.start_app(package_name)

    @staticmethod
    def execute_allow_permission(uuid, game_name):
        """  执行授权 """

        permission = ActionAllowPermission(uuid, game_name)

        # todo 后续考虑维护不同的设备列表（不用授权操作的设备列表，用于优化执行时间）

        # 授权相关操作
        if permission.ui_allow_permission_object_info.get('allow_permission'):
            permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_permission'))

        # 其它授权（特殊）
        if permission.ui_allow_permission_object_info.get('allow_app_list'):
            permission.do_allow_app_list(permission.ui_allow_permission_object_info.get('allow_app_list'))

        # todo 坦克前线在HUAWEI_Nova_CAZ_AL10上权限弹框顺序会不同，先弹出获取应用列表权限，后弹出请求定位权限
        if game_name == "坦克前线" or game_name == "星辰奇缘" and uuid == "XPU4C17117022704":
            if permission.ui_allow_permission_object_info.get('allow_location'):
                permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_location'))

    @staticmethod
    def execute(uuid, apk_path, package_name, game_name):

        # todo 需要加上这一句，否则pocoservice会报错
        # init_device(uuid=uuid)
        log_dir = os.path.join(APP.AIRTEST_LOG_FILE_PATH, uuid, time.strftime("%Y_%m_%d_%H_%M_%S"))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # todo 需要加上这一句，否则pocoservice会报错
        auto_setup(basedir=APP.WORKSPACE, devices=["Android:///" + uuid], logdir=log_dir)

        Cases.execute_install(uuid, apk_path, package_name)
        Cases.execute_allow_permission(uuid, game_name)

        ret = run_one_report(os.path.join(APP.AIRTEST_LOG_FILE_PATH, "empty.py"), uuid, log_dir)

        return uuid, ret






