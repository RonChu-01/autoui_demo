# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/13.
# Copyright (c) 2019 3KWan.
# Description :
import concurrent

from airtest.core.android.adb import ADB
from airtest.core.api import init_device

from core.ui_testcase.cases import Cases
from core.utils.aapt_util import get_packagename_and_launchable_activity


class Task:

    @staticmethod
    def run(uuid):

        # todo：恶心啊 如果不加这句，多进程运行会报错
        #  [pocoservice.apk] stdout: b'INSTRUMENTATION_RESULT: shortMsg=Process crashed.\r\nINSTRUMENTATION_CODE: 0\r\n'
        #  并且多进程执行时会出现报错（疑似隔离问题，加上这句初始化后正常）

        init_device(uuid=uuid)

        APK = "3139_wdsm_wdsm_3k_20191112_28835_28835.apk"
        game_name, package_name, launchable_activity = get_packagename_and_launchable_activity(APK)

        case = Cases(uuid=uuid, apk_path=APK, package=package_name, game_name=game_name)
        case.execute()

        return "success!"




