# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/18.
# Copyright (c) 2019 3KWan.
# Description :

import unittest

from core.ui_action.at_install_apk import ActionInstallApk


class TestInstall(unittest.TestCase):
    """  安装测试用例 """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_install_app(self, uuid, apk_path, package_name):
        """  安装 """

        install = ActionInstallApk(uuid)

        # 安装相关操作
        proc_ = install.start_install(apk_path)
        if install.ui_install_object_info.get('installing'):
            install.do_installing(install.ui_install_object_info.get('installing'))
        proc_.wait()  # 等待apk安装完毕，执行后续操作

        install.start_app(package_name)

    def test_start_app(self):
        pass

    def test_allow_permission(self):
        pass

    @staticmethod
    def execute():
        unittest.main()


if __name__ == '__main__':
    pass
