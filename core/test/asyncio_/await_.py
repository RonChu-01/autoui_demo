# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/18.
# Copyright (c) 2019 3KWan.
# Description :


import asyncio


async def nested():
    return 20


async def main():
    # data = await nested()
    # print(data)

    task = asyncio.create_task(nested())
    data = await task
    print(data)

asyncio.run(main())

