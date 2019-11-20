# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/18.
# Copyright (c) 2019 3KWan.
# Description :

import unittest


class BaseCase(unittest.TestCase):

    PRIORITY = 0  # 用于指定用例执行顺序

    """
        测试用例基类：TestCase classes that want to be parametrized should inherit from this class.

    """
    def __init__(self, method_name='runTest', uuid=None, group_name=None, apk_path=None, package_name=None):
        """
        重写unittest.TestCase的构造函数

        :param method_name:
        :param uuid:
        :param group_name:
        :param apk_path:
        :param package_name:
        """
        super(BaseCase, self).__init__(method_name)
        self.uuid = uuid
        self.group_name = group_name
        self.apk_path = apk_path
        self.package_name = package_name

    @staticmethod
    def parametrize(test_cls, uuid, group_name, apk_path, package_name):
        """
            自定义参数传递

            Create a suite containing all tests taken from the given subclass, passing them the parameters.
        """
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(test_cls)
        suite = unittest.TestSuite()
        for name in test_names:
            suite.addTest(test_cls(name, uuid, group_name, apk_path, package_name))
        return suite
