# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/18.
# Copyright (c) 2019 3KWan.
# Description :

import asyncio


async def hello():
    print("hello")
    await asyncio.sleep(1)
    print("world")

asyncio.run(hello())

