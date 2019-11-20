# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/20.
# Copyright (c) 2019 3KWan.
# Description :


def underline_to_camel(underline_format):
    """
    下划线命名格式驼峰命名格式

    :param underline_format:
    :return:
    """
    camel_format = ""
    if isinstance(underline_format, str):
        for word in underline_format.split('_'):
            camel_format += word.capitalize()
    return camel_format


