# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/18.
# Copyright (c) 2019 3KWan.
# Description :

from core.ui_action.at_install_apk import ActionInstallApk
from core.ui_testcase.base import BaseCase


class TestInstall(BaseCase):
    """  安装 """

    PRIORITY = 1  # 用于指定用例执行顺序

    def setUp(self):
        self.install = ActionInstallApk(self.uuid)

    def tearDown(self):
        pass

    def test_install(self):
        # 检测是否已经安装过该包
        if self.package_name not in self.install.dev.list_app():
            # 安装相关操作
            proc_ = self.install.start_install(self.apk_path)
            if self.install.ui_install_object_info.get('installing'):
                self.install.do_installing(self.install.ui_install_object_info.get('installing'))
            proc_.wait()  # 等待apk安装完毕，执行后续操作

        self.install.stop_app(self.package_name)

    def test_start_app(self):
        self.install.start_app(self.package_name)
