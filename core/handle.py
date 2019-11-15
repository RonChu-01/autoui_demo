# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/15
#
# oril python file

"""  主要负责任务的生成和分配 """
import time
import os
from core.utils import path_util
from core.const.const_config import APP
from core.entity.task import Task
from core.entity.apk import Apk
from core.entity.system import System
from core.entity.base_report import BaseReport

from concurrent.futures import ProcessPoolExecutor, as_completed

# 生成system对象
executor = ProcessPoolExecutor(max_workers=APP.PROCESS_POOL_MAX_WORKERS)
system = System()
# 报告对象
report = BaseReport()
# 日志格式实体
results = {
        "start": time.time(),
        "script": os.path.join(path_util.get_config_path("local"), "template.py"),
        "tests": {}
    }


def invoke_target_device(apk_path, model, game_name="", channel_name="", package_name="", launchable_activity=""):
    """
    调用指定设备,根据手机型号调用指定的设备，如果此设备不包含在内，则调用失败
    :param apk_path:
    :param model:
    :param game_name:
    :param channel_name:
    :param package_name:
    :param launchable_activity:
    :return:
    """
    # 生成任务对象
    apk = Apk(apk_path=apk_path, game_name=game_name, channel_name=channel_name, package_name=package_name, launchable_activity=launchable_activity)
    if len(system.conn_devices) <= 0:
        return -1

    uuid = ""
    for device in system.conn_devices:
        if model == device[1]:
            uuid = device[0]

    if uuid is None:
        return -1

    task = Task(apk=apk, uuid=uuid, model=model)
    # 将task对象提交到进程池内
    exec_1 = executor.submit(task.run)
    ret, task_log, uuid, model = exec_1.result()
    # 正常运行结束
    results["tests"][model] = report.run_one_report(model, task_log)
    results["tests"][model]["status"] = ret

    report_file = report.run_mutli_report(results)
    print("task run over... : " + str(ret))
    return 1, report_file


def invoke_multi_device(apk_path, game_name="", channel_name="", package_name="", launchable_activity=""):
    """
    :param apk_path:
    :param game_name:
    :param channel_name:
    :param package_name:
    :param launchable_activity:
    :return:
    """
    # 先获取目前系统所支持的所有设备
    devices = system.conn_devices
    if devices is None or len(devices) <= 0:
        return -1

    all_tasks = []
    for dev in devices:
        apk = Apk(apk_path=apk_path, game_name=game_name, channel_name=channel_name, package_name=package_name,
                  launchable_activity=launchable_activity)
        task = Task(apk=apk, uuid=dev[0], model=dev[1])
        # 进程池执行
        all_tasks.append(executor.submit(task.run))

    for future in as_completed(all_tasks):
        ret, task_log, uuid, model= future.result()
        results["tests"][model] = report.run_one_report(model, task_log)
        results["tests"][model]["status"] = ret

    # 生成多设备总的报告
    report_file = report.run_mutli_report(results)
    return 1, report_file





