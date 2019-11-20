# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/19.
# Copyright (c) 2019 3KWan.
# Description :

from core.ui_action.at_install_apk import ActionInstallApk
from core.ui_testcase.base import BaseCase


class TestUninstall(BaseCase):
    """  卸载 """

    def setUp(self):
        self.install = ActionInstallApk(self.uuid)

    def tearDown(self):
        pass

    def test_start_app(self):
        self.install.start_app(self.package_name)


