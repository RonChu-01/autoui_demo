# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/10/31.
# Copyright (c) 2019 3KWan.
# Description :
import os

from core.const.const_config import APP
from core.ui_action.at_base_api import ActionBaseApi
from core.utils.futils.json_util import file_to_json


class ActionInstallApk(ActionBaseApi):
    """  安装APK """

    def __init__(self, uuid):
        super().__init__(uuid)
        self.uuid = uuid
        self.ui_install_object_info = {}
        self.pwd = ""
        self.load_ui_install_object_info(uuid)  # 初始化UI信息

    def load_ui_install_object_info(self, uuid):
        """
        加载安装页面相关UI对象信息

        :param uuid:
        :return:
        """

        ui_install_object_info = file_to_json(APP.UI_INSTALL_PATH)  # 加载安装页面UI对象信息

        if ui_install_object_info:
            if ui_install_object_info.get(uuid):
                self.ui_install_object_info = ui_install_object_info.get(uuid)
                self.pwd = self.ui_install_object_info.get("password")
            else:
                raise ValueError('load device fail->：设备{0} 不存在，请检查配置文件'.format(uuid))
        else:
            print("配置文件不存在，请检查")

    def get_install_template_img_file_path(self):
        """
        获取图像识别图片保存路径

        :return:
        """
        device_name = self.ui_install_object_info.get("device_name")
        device_uuid = self.uuid
        img_file_path = os.path.join(APP.IMG_INSTALL_ROOT_PATH, device_name + "_" + device_uuid)
        return img_file_path

    def do_installing(self, installing):
        """
        安装过程中的特殊操作的处理
        这些操作都是从json配置文件里获取到的
        需要先处理好json配置文件
        才能保证这里能适配到大部分机型

        :param installing: ui_install.json 中 某个设备对象下的'installing'项

            点击按钮（涵盖安装过程中需要执行点击的操作）
            example:
                1、确认安装弹框处理
                2、点击安装
                3、点击打开ap/游戏
                4、获取已安装应用列表权限
                    需要该权限的设备：
                        1、XPU4C17117022704：华为HUAWEI Nova CAZ-AL10
                5、...
        :return:
        """

        # Oppo、Vivo等机型执行安装时，需要输入账号密码进行安装验证（可能出现、可能不出现）
        if installing.get("password_input"):
            password_input = installing.get("password_input")
            dialog_passwd = password_input.get("input").get("poco")
            try:
                # 等待密码框出现
                self.poco(dialog_passwd).wait_for_appearance(timeout=15)
            except Exception as e:
                print(str(e))
                pass
            else:
                if password_input.get("input"):
                    text_input = password_input.get("input")
                    if text_input.get('poco'):
                        self.do_input_by_poco_ui(text_input.get('poco'), self.pwd)
                if password_input.get("confirm_button"):
                    confirm_button = password_input.get("confirm_button")
                    self.do_click(confirm_button)

        # 安装确认
        if installing.get('continue_install'):
            if installing.get('continue_install').get('continue_button'):
                continue_button = installing.get('continue_install').get('continue_button')
                self.do_click(continue_button)

        # 执行安装
        if installing.get('install'):
            if installing.get('install').get('install_button'):
                install_button = installing.get('install').get('install_button')
                img_file_path = self.get_install_template_img_file_path()
                self.do_click(install_button, tpl_file_path=img_file_path)

        # 完成安装
        if installing.get('done'):
            if installing.get('done').get('done_button'):
                done_button = installing.get('done').get('done_button')
                self.do_click(done_button)

