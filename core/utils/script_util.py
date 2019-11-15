# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/15

"""  脚本运行文件 """

import os
import sys


def do_script(task, android, py_file, tempDir, ext_infos):
    """
    :param task:任务实体
    :param android:android实体
    :param py_file:脚本python文件
    :param tempDir:脚本路径
    :param ext_infos:额外扩展参数
    :return: ret
    """
    if not os.path.exists(py_file):
        return

    if not py_file.endswith(".py"):
        return

    sys.path.append(tempDir)
    try:
        import script
        ret = script.execute(task, android, ext_infos)
        del sys.modules["script"]
        sys.path.remove(tempDir)
        return ret
    except ImportError as ie:
        sys.path.remove(tempDir)
        return
