# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/18.
# Copyright (c) 2019 3KWan.
# Description :

import time
import asyncio


async def say_hello(delay, msg):
    await asyncio.sleep(delay)
    print(msg)


async def main():
    print("-> start at: {0}".format(time.strftime("%Y-%M-%d %H:%M:%S")))
    await say_hello(1, "hello")
    await say_hello(2, "world")
    print("-> end at: {0}".format(time.strftime("%Y-%M-%d %H:%M:%S")))


async def task_main():
    task_1 = asyncio.create_task(say_hello(1, "hello"))
    task_2 = asyncio.create_task(say_hello(2, "world"))

    print("-> start at: {0}".format(time.strftime("&Y-%M-%d %H:%M:%S")))
    await task_1
    await task_2
    print("-> finished at: {0}".format(time.strftime("&Y-%M-%d %H:%M:%S")))

asyncio.run(task_main())
