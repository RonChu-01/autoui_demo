# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/1.
# Copyright (c) 2019 3KWan.
# Description :
from airtest.cli.runner import AirtestCase

from core.ui_action.at_install_apk import ActionInstallApk
from core.ui_action.at_permission_allow import ActionAllowPermission


class TestCases(AirtestCase):
    """  业务场景用例 """
    # todo 这里后续可以将用例分层，拆分出去，继承Cases

    def __init__(self, uuid=None, apk_path=None, package=None, game_name=None):
        """

        :param uuid:
        :param apk_path:
        :param package:
        :param game_name:
        """
        super().__init__()
        self.uuid = self.args.device
        self.apk_path = "3139_wdsm_wdsm_3k_20191112_28835_28835.apk"
        self.package = "com.wdsm.kkkwan"
        self.game_name = "我的使命"

    def test_execute_install(self):
        """  执行安装 """

        install = ActionInstallApk(self.uuid)

        # 安装相关操作
        proc_ = install.start_install(self.apk_path)
        if install.ui_install_object_info.get('installing'):
            install.do_installing(install.ui_install_object_info.get('installing'))
        proc_.wait()  # 等待apk安装完毕，执行后续操作

        install.start_app(self.package)

        return

    def test_execute_allow_permission(self):
        """  执行授权 """

        permission = ActionAllowPermission(self.game_name, self.uuid)

        # todo 后续考虑维护不同的设备列表（不用授权操作的设备列表，用于优化执行时间）

        # 授权相关操作
        if permission.ui_allow_permission_object_info.get('allow_permission'):
            permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_permission'))

        # 其它授权（特殊）
        if permission.ui_allow_permission_object_info.get('allow_app_list'):
            permission.do_allow_app_list(permission.ui_allow_permission_object_info.get('allow_app_list'))

        # todo 坦克前线在HUAWEI_Nova_CAZ_AL10上权限弹框顺序会不同，先弹出获取应用列表权限，后弹出请求定位权限
        if self.game_name == "坦克前线" or self.game_name == "星辰奇缘" and self.uuid == "XPU4C17117022704":
            if permission.ui_allow_permission_object_info.get('allow_location'):
                permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_location'))

        return
