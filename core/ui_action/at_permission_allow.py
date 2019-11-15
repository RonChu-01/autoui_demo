# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/10/31.
# Copyright (c) 2019 3KWan.
# Description :
import os

from core.const.const_config import APP
from core.ui_action.at_base_api import ActionBaseApi
from core.utils.futils.json_util import file_to_json


class ActionAllowPermission(ActionBaseApi):
    """  执行授权 """

    def __init__(self, uuid, game_name):
        super().__init__(uuid)
        self.game_name = game_name
        self.uuid = uuid
        self.ui_allow_permission_object_info = {}
        self.load_ui_allow_permission_object_info(uuid)  # 初始化UI信息

    def load_ui_allow_permission_object_info(self, uuid):
        """
        加载授权页面相关ui信息

        :param uuid:
        :return:
        """

        file_path = os.path.join(APP.UI_BUSINESS_ROOT_PATH, self.game_name, APP.UI_ALLOW_PERMISSION_FILE)

        ui_allow_permission_object_info = file_to_json(file_path)  # 加载授权页面UI对象信息

        if ui_allow_permission_object_info:
            if ui_allow_permission_object_info.get(uuid):
                self.ui_allow_permission_object_info = ui_allow_permission_object_info.get(uuid)
            else:
                raise ValueError("load_ui_allow_permission_object_info fail-> 设备{0} 不存在，请检查配置文件".format(uuid))
        else:
            print("load_ui_allow_permission_object_info fail->: 配置文件不存在，请检查")

    def do_allow_permission(self, allowance):
        """
        应用权限

        note：
            1、第一次安装需申请权限，后续启动无需此操作；
        :param allowance:
        :return:
        """
        if allowance.get('allow_button'):
            allow_button = allowance.get('allow_button')
            self.do_click(allow_button, is_permission=True)

    def do_allow_app_list(self, app_allowance):
        """
         获取已安装应用列表权限，目前只在 HUAWEI Nova CAZ-AL10 中出现

        :param app_allowance:
        :return:
        """
        if app_allowance.get('allow_button'):
            allow_button = app_allowance.get('allow_button')
            self.do_click(allow_button)


