# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/10/15
#

"""  aapt util """

import sys
import subprocess
import platform
import importlib
from core.utils import config_util, path_util


def get_packagename_and_launchable_activity(apk_path):
    """
    :param apk_path: apk file's path
    :return: packagename, launchable_activity
    """
    cmd = path_util.get_aapt_path() + " dump badging " + apk_path
    print("cmd : " + cmd)
    cmd = config_util.double_slanting_bar_change(cmd)
    ret = 0

    try:
        importlib.reload(sys)
        s = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdoutput, erroutput = s.communicate()

        if platform.system() == "windows":
            stdoutput = stdoutput.decode("gbk")

        stdoutput = str(stdoutput, "UTF-8")
        package_name = ""
        launchable_activity = ""
        game_name = ""
        list_stdoutput = stdoutput.split("\n")
        for item in list_stdoutput:
            if "package: name" in item:
                lst1 = item.split(" ")
                for child in lst1:
                    if "name" in child and "compileSdkVersionCodename" not in child:
                        child1 = child.split("='")
                        package_name = child1[1].replace("'", "")
                        package_name = package_name.strip()

            elif "launchable-activity" in item:
                list1 = item.split(" ")
                for child in list1:
                    if "name=" in child:
                        child1 = child.split("=")
                        launchable_activity = child1[1].replace("'", "")
                        launchable_activity = launchable_activity.strip()

            elif "application-label" in item:
                list1 = item.split(":'")
                game_name = list1[1].replace("'", "")
                game_name = game_name.strip()

        return game_name, package_name, launchable_activity

    except Exception as e:
        print(e)
        return
