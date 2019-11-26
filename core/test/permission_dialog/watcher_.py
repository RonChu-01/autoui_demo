# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/25.
# Copyright (c) 2019 3KWan.
# Description :
import threading
import time

from airtest.core.api import init_device
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from core.libs.logs.logger import Logger
from core.utils.aapt_util import get_packagename_and_launchable_activity

logger = Logger("watcher")


def loop_watcher(find_element, timeout):
    """
    每隔一秒，循环查找元素是否存在.
    如果元素存在，click操作
    :param find_element: 要查找元素，需要是poco对象
    :param timeout: 超时时间，单位：秒
    :return:
    """

    thread_name = threading.currentThread().name

    logger.info('thread {0} is running...'.format(thread_name))

    start_time = time.time()
    # 计数（用于循环点击，目前设为最多执行5次点击）
    count = 0
    while True:
        if find_element.exists():
            find_element.click()
            count += 1
            logger.info("观察者线程 {0} 发现".format(thread_name))
            if count < 5:
                continue
            else:
                break
        elif (time.time() - start_time) < timeout:
            logger.info("观察者线程 {} 等待1秒".format(thread_name))
            time.sleep(1)
        else:
            logger.info("观察者线程 {} 超时未发现".format(thread_name))
            break

    logger.info('thread {0} ended...'.format(thread_name))


def watcher(texts: list = None, poco=None, timeout=15):
    """
    观察者函数: 根据text定位元素，用守护线程的方式，增加子线程循环查找元素，直到超时
    :param texts: 元素的text
    :param timeout: 超时时间
    :param poco: poco实例
    :return:
    """

    # 弹窗监听线程池
    threads = []

    # 目标元素
    find_element = None
    if poco is None:
        raise Exception("poco is None")

    for text in texts:

        if text:
            find_element = poco(text=text)

        # 定义子线程: 循环查找目标元素
        t = threading.Thread(target=loop_watcher, name="".format(text), args=(find_element, timeout))
        threads.append(t)
        # 增加守护线程，主线程结束，子线程也结束
        t.setDaemon(True)
        t.start()

    for i in range(len(texts)):
        threads[i].join()


if __name__ == '__main__':

    # apk = "3139_wdsm_wdsm_3k_20191112_28835_28835.apk"
    # apk = "2905_wdsm_wdsmzgl_qq3k_20191108_28156_28156.apk"

    # apk = "620_wzzg_wzzg_360_20190920_0_21381.apk"
    # apk = "1903_wzzg_wzzgjymz_qq3k_20191012_24007_24007.apk"

    # apk = "2322_xcqy_xcqymhxy_qq3k_20190930_26519_26519.apk"

    # apk = "3165_tkqx_tkqx_3k_20191106_2833_2833.apk"
    apk = "3372_tkqx_tkqxzh_qq3k_20191112_23875_23875.apk"

    game_name, package_name, activity = get_packagename_and_launchable_activity(apk)

    dev = init_device()
    if package_name not in dev.list_app():
        # 使用这种方式不会因为遇到弹框而阻塞
        dev.adb.push(apk, "/data/local/tmp/")
        proc = dev.adb.start_shell("pm install /data/local/tmp/{0}".format(apk))

    dev.stop_app(package_name)
    dev.start_app(package_name)

    poco = AndroidUiautomationPoco()
    # 权限框弹窗处理
    btn_text = ["确认", "始终允许", "允许", "总是允许"]
    watcher(btn_text, poco=poco)
