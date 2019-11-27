# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/25.
# Copyright (c) 2019 3KWan.
# Description :

import threading
import time

from core.libs.logs.logger import Logger
logger = Logger("watcher")


def loop_watcher(poco, text, timeout):
    """
    每隔一秒，循环查找元素是否存在.
    如果元素存在，click操作
    :param poco:
    :param text: 待查找元素的text属性
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
            find_element = poco(text=text)
            find_element.wait_for_appearance(timeout=timeout)
        except Exception as e:
            logger.info("-> " + str(e))
            break
        else:
            # 每次轮询点击的时间间隔，api是1.44s
            logger.info("开始执行点击操作")
            time.sleep(1.5)
            find_element = find_element.wait()
            find_element.click()
            count += 1
            if count < 5:
                continue
            else:
                break


def watcher(texts: list = None, poco=None, timeout=15):
    """
    观察者函数: 根据text定位元素，用守护线程的方式，增加子线程循环查找元素，直到超时
    :param texts: 轮询对象text属性列表
    :param poco: poco实例
    :param timeout: 超时时间
    :return:
    """

    # 弹窗监听线程池
    threads = []

    if poco is None:
        raise Exception("poco is None")

    if texts:
        for text in texts:
            # 定义子线程: 循环查找目标元素
            t = threading.Thread(target=loop_watcher, name="".format(text), args=(poco, text, timeout))
            threads.append(t)
            # 增加守护线程，主线程结束，子线程也结束
            t.setDaemon(True)
            t.start()

        for i in range(len(threads)):
            threads[i].join()

    else:
        logger.info("请配置待监听的元素对象text")

