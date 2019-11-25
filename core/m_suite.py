# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/20.
# Copyright (c) 2019 3KWan.
# Description :
import importlib
import re
import unittest

from core.const.const_config import APP
from core.m_discover import get_all_case
from core.ui_testcase.base import BaseCase
from core.utils.futils.fmt_util import underline_to_camel


def suite_all_case(uuid, group_name, apk_path, package_name):
    """
    将测试用例下所有用例加入测试套件

    todo：这里有个问题是用例的执行顺序（暂时是自行添加一个字段做标识）

    :param uuid:
    :param group_name:
    :param apk_path:
    :param package_name:
    :return:
    """

    suite = unittest.TestSuite()

    classes_name = []

    for info in get_all_case(APP.TEST_CASE_ROOT_PATH):
        file_path, file_name = info

        # todo: 添加类型检测与异常处理，以及日志埋点信息

        # 获取模块路径
        # todo: 这里注意，如果是在unix或者linux系统需要分平台处理
        file_path = re.sub(r'.*core', 'core', file_path).replace("\\", ".")

        # 动态导入模块
        model = importlib.import_module(".{0}".format(file_name.split(".")[0]), package=file_path)

        # （通过反射）获取类对象（这里需要按照我们自己的规则来编写测试用例）
        class_name = getattr(model, underline_to_camel(file_name.split(".")[0]))

        classes_name.append((class_name, class_name.PRIORITY))

    # 按执行步骤排序
    classes_name = sorted(classes_name, key=lambda x: x[1])

    # 按照排定的顺序添加用例类
    # todo： 里面的执行顺序可以再观察，或者添加数字标识，或者直接添加的模式
    for class_name in classes_name:
        suite.addTest(BaseCase.parametrize(class_name[0],
                                           uuid=uuid,
                                           group_name=group_name,
                                           apk_path=apk_path,
                                           package_name=package_name
                                           ))

    return suite


def suite_target_case(uuid, case_path, group_name, apk_path, package_name):
    """
    添加特定的测试用例至测试套件

    :param uuid:
    :param case_path:
    :param group_name:
    :param apk_path:
    :param package_name:
    :return:
    """
    suite = unittest.TestSuite()

    for info in get_all_case(case_path):
        file_path, file_name = info
        file_path = file_path.split(":")[1].replace("\\", ".").replace(".workspace.autoui_demo.", "")

        # 动态导入模块
        model = importlib.import_module(".{0}".format(file_name.split(".")[0]), package=file_path)

        # 获取类对象（这里需要按照我们自己的规则来编写测试用例）（通过反射）)
        class_name = getattr(model, underline_to_camel(file_name.split(".")[0]))

        suite.addTest(BaseCase.parametrize(class_name,
                                           uuid=uuid,
                                           group_name=group_name,
                                           apk_path=apk_path,
                                           package_name=package_name
                                           ))

    return suite

