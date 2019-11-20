# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/20.
# Copyright (c) 2019 3KWan.
# Description :
import os
import subprocess
import time
import traceback
import webbrowser

from jinja2 import Environment, FileSystemLoader

from core.const.const_config import APP


def run_one_report(air, dev, log_dir):
    """
        生成一个脚本的测试报告
        Build one test report for one air script
    """
    try:
        log = os.path.join(log_dir, 'log.txt')
        if os.path.isfile(log):
            cmd = [
                'python',
                '-m',
                "airtest",
                "report",
                air,
                "--log_root",
                log_dir,
                "--outfile",
                os.path.join(log_dir, 'log.html'),
                "--lang",
                "zh"
            ]
            ret = subprocess.call(cmd, shell=True, cwd=os.getcwd())
            return {
                    'status': ret,
                    'path': os.path.join(log_dir, 'log.html')
                    }
        else:
            print("Report build Failed. File not found in dir %s" % log)
    except Exception as e:
        traceback.print_exc()
    return {'status': -1, 'device': dev, 'path': ''}


def run_summary(data):
    """"
        生成汇总的测试报告
        Build sumary test report
    """
    try:
        summary = {
            'time': "%.3f" % (time.time() - data['start']),
            'success': [item['status'] for item in data['tests'].values()].count(0),
            'count': len(data['tests'])
        }
        summary.update(data)
        summary['start'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(data['start']))
        env = Environment(loader=FileSystemLoader(APP.AIRTEST_LOG_FILE_PATH),
                          trim_blocks=True)
        html = env.get_template('report_tpl.html').render(data=summary)
        with open("report.html", "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open('report.html')
    except Exception as e:
        traceback.print_exc()
