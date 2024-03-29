# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/12.
# Copyright (c) 2019 3KWan.
# Description :

import time
import logging
import os

from core.const.const_config import APP

# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(APP.LOG_FILE_PATH):
    os.mkdir(APP.LOG_FILE_PATH)


class Logger(object):
    """  日志模块 """

    def __init__(self, file_name=None):
        """

        :param file_name: 文件名
        """
        # 文件的命名
        self.log_name = os.path.join(APP.LOG_FILE_PATH, APP.LOG_FILE_NAME)
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.DEBUG)

        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(name)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        """

        :param level:
        :param message:
        :return:
        """

        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close()  # 关闭打开的文件

    def debug(self, message):
        """

        :param message:
        :return:
        """
        self.__console('debug', message)

    def info(self, message):
        """

        :param message:
        :return:
        """
        self.__console('info', message)

    def warning(self, message):
        """

        :param message:
        :return:
        """
        self.__console('warning', message)

    def error(self, message):
        """

        :param message:
        :return:
        """
        self.__console('error', message)
