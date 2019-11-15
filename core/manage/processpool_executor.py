# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/14
#

"""  ProcessPoolExecutor """

from concurrent.futures import ProcessPoolExecutor
from core.const.const_config import APP


class ProcessPool:

    def __init__(self):
        self.__processPool = ProcessPoolExecutor(max_workers=APP.PROCESS_POOL_MAX_WORKERS)
        self.__allFutures = []  # 用于存放当前运行的进程池的所有future

    def submit(self, func, *args, **kwargs):
        """
        提交(通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞)

        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        temp_future = self.__processPool.submit(func, *args, **kwargs)
        if temp_future not in self.__allFutures:
            self.__allFutures.append(temp_future)
        return temp_future

    def get_all_futures(self):
        """  获取所有的future """
        return self.__allFutures

    @staticmethod
    def done(future=None):
        """
        用于判定某个任务是否完成)

        :param future:
        :return:
        """
        if future is None:
            return False

        return future.done()

    @staticmethod
    def cancel(future):
        """
        cancel取消任务,该任务没有放入线程池中才能取消成功

        :param future:
        :return:
        """
        if future is None:
            return False

        return future.cancel()

    @staticmethod
    def result(future):
        """
        result方法可以获取task的执行结果

        :param future:
        :return:
        """
        if future is None:
            return False

        return future.result()





