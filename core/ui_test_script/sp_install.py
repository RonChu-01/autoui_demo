# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/18.
# Copyright (c) 2019 3KWan.
# Description :

from core.ui_action.at_install_apk import ActionInstallApk
from core.ui_action.at_permission_allow import ActionAllowPermission


class ScriptInstall:
    """  业务场景用例 """
    # todo 这里后续可以将用例分层，拆分出去，继承Cases

    @staticmethod
    def execute_install(uuid, apk_path, package):
        """  执行安装 """

        install = ActionInstallApk(uuid)

        # 安装相关操作
        proc_ = install.start_install(apk_path)
        if install.ui_install_object_info.get('installing'):
            install.do_installing(install.ui_install_object_info.get('installing'))
        proc_.wait()  # 等待apk安装完毕，执行后续操作

        install.start_app(package)

    @staticmethod
    def execute_allow_permission(uuid, game_name):
        """  执行授权 """

        permission = ActionAllowPermission(game_name, uuid)

        # todo 后续考虑维护不同的设备列表（不用授权操作的设备列表，用于优化执行时间）

        # 授权相关操作
        if permission.ui_allow_permission_object_info.get('allow_permission'):
            permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_permission'))

        # 其它授权（特殊）
        if permission.ui_allow_permission_object_info.get('allow_app_list'):
            permission.do_allow_app_list(permission.ui_allow_permission_object_info.get('allow_app_list'))

        # todo 坦克前线在HUAWEI_Nova_CAZ_AL10上权限弹框顺序会不同，先弹出获取应用列表权限，后弹出请求定位权限
        if game_name == "坦克前线" or game_name == "星辰奇缘" and uuid == "XPU4C17117022704":
            if permission.ui_allow_permission_object_info.get('allow_location'):
                permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_location'))
