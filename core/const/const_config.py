# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/10/24.
# Copyright (c) 2019 3KWan.
# Description :

import os
import time

from core.const.const import Constant

# == 应用配置 ==
APP = Constant()

APP.PROCESS_POOL_MAX_WORKERS = 20  # 进程池常量类

# ==项目路径相关配置==
APP.WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 根目录
APP.CONFIG_FILE_PATH = os.path.join(APP.WORKSPACE, "core", "config")  # 配置文件路径

# ==UI层元素对象相关配置==
APP.UI_OBJECT_ROOT_PATH = os.path.join(APP.WORKSPACE, "core", "ui_object")  # UI对象层路径
APP.UI_INSTALL_PATH = os.path.join(APP.UI_OBJECT_ROOT_PATH, "ui_install.json")  # 安装APK界面相关UI对象
APP.UI_BUSINESS_ROOT_PATH = os.path.join(APP.UI_OBJECT_ROOT_PATH, "game")  # 业务场景UI对象根路径
APP.UI_ALLOW_PERMISSION_FILE = "ui_allow_permission.json"  # 启动APP授权界面UI对象文件

# ==UI图像识别相关配置==
APP.IMG_INSTALL_ROOT_PATH = os.path.join(APP.UI_OBJECT_ROOT_PATH, "img_install")  # 安装业务场景，界面截图保存根路径

# ==APP日志文件相关配置==
APP.LOG_FILE_PATH = os.path.join(APP.WORKSPACE, "core", "logs")  # 日志文件路径
APP.LOG_FILE_FORMAT = '{0}.txt'.format(time.strftime("%Y_%m_%d_%H_%M_%S"))  # 日志文件保存格式
APP.LOG_FILE_NAME = os.path.join(APP.LOG_FILE_PATH, APP.LOG_FILE_FORMAT)  # 日志名

# ==Airtest库日志文件相关配置==
APP.AIRTEST_LOG_FILE_PATH = os.path.join(APP.WORKSPACE, "core", "log")

# 状态常量定义
APP.CODE_FAILURE = -1

# 环境
APP.IS_DEBUG = False


if __name__ == '__main__':
    print(APP.WORKSPACE)
