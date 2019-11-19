# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/1.
# Copyright (c) 2019 3KWan.
# Description :

import asyncio
import threading
import queue

from airtest.core.android.adb import ADB

from core.ui_action.at_install_apk import ActionInstallApk
from core.ui_action.at_permission_allow import ActionAllowPermission
from core.utils.aapt_util import get_packagename_and_launchable_activity


class Cases:
    """  业务场景用例 """
    # todo 这里后续可以将用例分层，拆分出去，继承Cases

    def __init__(self, q, apk_path, package, game_name, group_name=None):
        """
        todo: 后续需要添加一个group_name参数（UI文件路径是根据游戏组名查找）

        :param uuid:
        :param apk_path:
        :param package:
        :param game_name:
        """
        self.q = q
        self.apk_path = apk_path
        self.package = package
        self.game_name = game_name

    def execute_install(self, uuid):
        """  执行安装 """

        install = ActionInstallApk(uuid)

        # 安装相关操作
        proc_ = install.start_install(self.apk_path)
        if install.ui_install_object_info.get('installing'):
            install.do_installing(install.ui_install_object_info.get('installing'))
        proc_.wait()  # 等待apk安装完毕，执行后续操作

        install.start_app(self.package)

        return

    def execute_allow_permission(self, uuid):
        """  执行授权 """

        permission = ActionAllowPermission(self.game_name, uuid)

        # todo 后续考虑维护不同的设备列表（不用授权操作的设备列表，用于优化执行时间）

        # 授权相关操作
        if permission.ui_allow_permission_object_info.get('allow_permission'):
            permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_permission'))

        # 其它授权（特殊）
        if permission.ui_allow_permission_object_info.get('allow_app_list'):
            permission.do_allow_app_list(permission.ui_allow_permission_object_info.get('allow_app_list'))

        # todo 坦克前线在HUAWEI_Nova_CAZ_AL10上权限弹框顺序会不同，先弹出获取应用列表权限，后弹出请求定位权限
        if self.game_name == "坦克前线" or self.game_name == "星辰奇缘" and uuid == "XPU4C17117022704":
            if permission.ui_allow_permission_object_info.get('allow_location'):
                permission.do_allow_permission(permission.ui_allow_permission_object_info.get('allow_location'))

        return

    def execute(self):
        while 1:
            uuid = self.q.get()
            if uuid is None:
                break
            self.execute_install(uuid)
            self.execute_allow_permission(uuid)
            q.task_done()


if __name__ == '__main__':

    devices = [dev[0] for dev in ADB().devices()]
    APK = "3139_wdsm_wdsm_3k_20191112_28835_28835.apk"
    game_name, package_name, launchable_activity = get_packagename_and_launchable_activity(APK)

    q = queue.Queue()

    tasks = []
    threads = []

    for device in devices:
        q.put(device)

    for device in devices:
        cases = Cases(q, apk_path=APK, package=package_name, game_name=game_name)
        tasks.append(cases)

    # todo 使用多线程pocoservice出现crashed
    #  [pocoservice.apk] stdout: b'INSTRUMENTATION_RESULT: shortMsg=Process crashed.\r\nINSTRUMENTATION_CODE: 0
    for i in range(len(tasks)):
        t = threading.Thread(target=tasks[i].execute)
        threads.append(t)
        t.start()

    q.join()

    # 停止
    for i in range(len(devices)):
        q.put(None)

    for t in threads:
        t.join()




