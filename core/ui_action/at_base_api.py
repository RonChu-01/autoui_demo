# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/10/31.
# Copyright (c) 2019 3KWan.
# Description :
import os

from airtest.core.api import touch, init_device
from airtest.core.cv import Template
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoTargetTimeout


class ActionBaseApi:
    """  通用api封装 """

    def __init__(self, uuid):
        self.uuid = uuid
        self.poco = AndroidUiautomationPoco()
        self.dev = init_device(uuid=uuid)

    def do_click(self, objects, tpl_file_path=None, is_permission=False):
        """
        # todo 目前这个方法中初始化部分不够通用，如果后续有其它场景可考虑复写该方法，或者干脆将元素部分拆分？
        PS：要保持该方法的通用性，需UI对象层数据结构支持

        点击按钮，安装过程中所有的按钮点击的动作
        需要传入json配置文件中

        :param objects: UI元素对象
        :param is_permission: 是否为授权点击
        :param tpl_file_path: 图像识别文件保存地址
        :return:
        """
        # 通过UI属性定位元素
        if objects.get('poco'):
            offset = [0.5, 0.5]
            if objects.get('click'):
                offset = objects.get('click')
            self.do_click_by_poco_ui(objects.get('poco'), offset, is_permission=is_permission)

        # 通过图像识别定位元素
        elif objects.get('template'):
            if tpl_file_path:
                template = objects.get('template')
                img_file = os.path.join(tpl_file_path, template.get("img"))
                self.do_click_by_template(img_file, template.get('record_pos'), template.get('resolution'))
            else:
                print("-> 请提供图片地址")

    def do_click_by_poco_ui(self, resource_id, offset, is_permission=False, timeout=20):
        """
        根据控件的ID来确定控件并进行点击

        :param resource_id: 按钮的控件ID
        :param offset: 点击位置的偏移（oppo的某些机型安装过程需要点击一个控件右半部分）
        :param is_permission: 是否为授权点击
        :param timeout:
        :return:
        """

        # 是否是执行授权点击
        # 单次点击
        if not is_permission:
            try:
                button = self.poco(resource_id)
                button.wait_for_appearance(timeout=timeout)
            except PocoTargetTimeout as err:
                print(err.message)
            except Exception as e:
                print("error: %s" % (str(e)))
            else:
                button.click(offset)

        #  授权点击（循环点击）
        else:
            while True:
                try:
                    button = self.poco(resource_id)
                    button.wait_for_appearance(timeout=timeout)
                except PocoTargetTimeout as err:
                    print(err.message)
                    break
                except Exception as e:
                    print("error: %s" % (str(e)))
                    break
                else:
                    button.click(offset)

    @staticmethod
    def do_click_by_template(img_file, record_pos, resolution):
        """
        根据截图来确定按钮的点击
        oppo的设备执行到点击安装的步骤时，会将后台运行中的PocoService进程中断，无法通过poco获取对象，只能截图

        :param img_file: 手机屏幕的分辨率
        :param record_pos: 截图时对于手机屏幕的相对位置
        :param resolution: 手机屏幕的分辨率
        :return:
        """
        try:
            tmp = Template(img_file, record_pos=tuple(record_pos), resolution=tuple(resolution))
            touch(tmp)
        except Exception as e:
            print("error: %s" % (str(e)))

    def do_input_by_poco_ui(self, resource_id, text, timeout=10):
        """
        在输入框中输入文本，用于输入密码

        :param resource_id: 输入框的控件ID
        :param text: 需要输入的文本
        :param timeout:
        :return:
        """

        try:
            input_box = self.poco(resource_id)
            input_box.wait_for_appearance(timeout=timeout)
        except Exception as e:
            print("error: %s" % (str(e)))
        else:
            input_box.set_text(text)

    def start_install(self, apk_path):
        """
        安装apk
        todo： 这里注意，如需获取安装app情况，需调用方处理

        :param apk_path:
        :return: a subprocess
        """

        apk_name = apk_path.split('/')[-1]
        self.dev.adb.push(apk_path, "/data/local/tmp/")
        # todo 注意这里传的apk_path如果是路径+apk需要处理
        proc = self.dev.adb.start_shell("pm install /data/local/tmp/{0}".format(apk_name))

        return proc

    def start_app(self, package, activity=None):
        """
        启动app

        :param package:
        :param activity:
        :return:
        """
        self.dev.start_app(package, activity)

    def uninstall_apk(self, package, activity=None):
        """
        卸载app

        :param package:
        :param activity:
        :return:
        """
        self.dev.uninstall_app(package, activity)

