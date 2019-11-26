# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/19.
# Copyright (c) 2019 3KWan.
# Description :

from core.ui_action.at_permission_allow import ActionAllowPermission
from core.ui_test_script.watcher import watcher
from core.ui_testcase.base import BaseCase


class TestAllowPermission(BaseCase):

    PRIORITY = 2  # 用于指定用例执行顺序

    def setUp(self):
        self.permission = ActionAllowPermission(self.uuid, self.group_name)

    def tearDown(self):
        pass

    def test_allow_permission(self):

        # # todo 后续考虑维护不同的设备列表（不用授权操作的设备列表，用于优化执行时间）
        #
        # # 授权相关操作
        # allow_permission = self.permission.ui_allow_permission_object_info.get('allow_permission')
        # if allow_permission:
        #     self.permission.do_allow_permission(allow_permission)
        #
        # # 其它授权（特殊）
        # allow_app_list = self.permission.ui_allow_permission_object_info.get('allow_app_list')
        # if allow_app_list:
        #     self.permission.do_allow_app_list(allow_app_list)
        #
        # # todo 坦克前线在HUAWEI_Nova_CAZ_AL10上权限弹框顺序会不同，先弹出获取应用列表权限，后弹出请求定位权限
        # if self.group_name == "坦克前线" or self.group_name == "星辰奇缘" and self.uuid == "XPU4C17117022704":
        #     allow_location = self.permission.ui_allow_permission_object_info.get('allow_location')
        #     if allow_location:
        #         self.permission.do_allow_permission(allow_location)

        # 授权弹框text列表
        btn_text = ["确认", "始终允许", "允许", "总是允许"]
        watcher(btn_text, poco=self.permission.poco)

