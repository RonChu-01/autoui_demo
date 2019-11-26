# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/25.
# Copyright (c) 2019 3KWan.
# Description :

import threading
import time

from core.libs.logs.logger import Logger

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

    # 计数（用于轮询，目前设为最多执行5次点击）
    count = 0
    while True:
        try:
            logger.info("开始执行轮询")
            find_element.wait_for_appearance(timeout=timeout)
        except Exception as e:
            logger.info("-> " + str(e))
            break
        else:
            logger.info("开始执行点击操作")
            find_element.click()
            # 每次轮询点击的时间间隔，api是1.44s
            time.sleep(1.5)
            count += 1
            if count < 5:
                continue
            else:
                break


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
