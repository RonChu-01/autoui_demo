# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/20.
# Copyright (c) 2019 3KWan.
# Description :
import concurrent
import os
import time
import unittest

from airtest.core.android.adb import ADB
from airtest.core.api import auto_setup

from core.const.const_config import APP
from core.libs.logs.logger import Logger
from core.m_report import run_summary, run_one_report
from core.m_suite import suite_all_case
from core.ui_testcase.base import BaseCase
from core.ui_testcase.test_allow_permission import TestAllowPermission
from core.ui_testcase.test_install import TestInstall
from core.utils.aapt_util import get_packagename_and_launchable_activity


# 获取日志记录器
logger = Logger("run")


# 测试运行结果模板
results = {
    "start": time.time(),
    "script": "",
    "tests": {}
}


def run_case_auto(uuid, apk_path):
    """
    自动添加测试用例文件下全部用例（执行顺序需按照既定的规则）

    :param uuid:
    :param apk_path:
    :return:
    """

    log_dir = os.path.join(APP.AIRTEST_LOG_FILE_PATH, uuid, time.strftime("%Y_%m_%d_%H_%M_%S"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # todo 需要加上这一句，否则pocoservice会报错
    auto_setup(basedir=APP.WORKSPACE, devices=["Android:///" + uuid], logdir=log_dir)

    game_name, package_name, activity = get_packagename_and_launchable_activity(apk_path)

    # todo: 需要实现测试发现功能
    #  这里需要注意一下：后续会开放多个接口，有一键执行多个用例接口，有执行特定用例接口；
    suite = suite_all_case(uuid, group_name=game_name, apk_path=apk_path, package_name=package_name)

    try:
        unittest.TextTestRunner().run(suite)
    except Exception as e:
        logger.info(str(e))
        return uuid, {}
    else:
        # 运行报告
        result = run_one_report(os.path.join(APP.AIRTEST_LOG_FILE_PATH, "empty.py"), uuid, log_dir)
        return uuid, result


def run_case_by_custom(uuid, apk_path):
    """
    手动添加测试用例，确保用例执行顺序

    :param uuid:
    :param apk_path:
    :return:
    """

    log_dir = os.path.join(APP.AIRTEST_LOG_FILE_PATH, uuid, time.strftime("%Y_%m_%d_%H_%M_%S"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # todo 需要加上这一句，否则pocoservice会报错
    auto_setup(basedir=APP.WORKSPACE, devices=["Android:///" + uuid], logdir=log_dir)

    game_name, package_name, activity = get_packagename_and_launchable_activity(apk_path)

    # 测试用例添加进测试套件
    suite = unittest.TestSuite()
    param = (uuid, game_name, apk_path, package_name)  # 参数
    suite.addTest(BaseCase.parametrize(TestInstall,  *param))
    suite.addTest(BaseCase.parametrize(TestAllowPermission, *param))

    try:
        unittest.TextTestRunner().run(suite)
    except Exception as e:
        logger.info(str("run_case_by_custom error: {0}".format(e)))
        return uuid, {}
    else:
        # 运行报告
        result = run_one_report(os.path.join(APP.AIRTEST_LOG_FILE_PATH, "empty.py"), uuid, log_dir)
        return uuid, result


def run(func, apk_path, target_device: list = None):
    """
    程序主入口（多机运行）

    :param func:
    :param apk_path:
    :param target_device: 如果未指定，则运行在所有在线设备上
    :return:
    """

    # 添加类型转换，防止传参错误
    if target_device:
        target_device = list(target_device)

    # 获取在线设备
    devices = [dev[0] for dev in ADB().devices()] if not target_device else target_device

    # todo: 进程数量可以用在线设备数关联，如果在线设备数量 > 20 则用常量值，否则用在线设备数
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(func, uuid, apk_path) for uuid in devices]

        for future in concurrent.futures.as_completed(futures):
            try:
                uuid, ret = future.result()
            except Exception as e:
                logger.info("generated an exception: {0}".format(e))
                logger.info("测试出错请检查")
            else:
                if ret:
                    results["tests"][uuid] = ret
                else:
                    logger.info("测试出错请检查")

    run_summary(results)


if __name__ == '__main__':
    APK = "3139_wdsm_wdsm_3k_20191112_28835_28835.apk"
    run(run_case_by_custom, APK)




