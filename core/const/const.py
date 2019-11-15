# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/10/24.
# Copyright (c) 2019 3KWan.
# Description :


class Constant:
    """  常量 """

    class ConstantError(TypeError):
        pass

    class ConstantCaseError(ConstantError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstantError("can not rebind constance {0}".format(key))
        if not key.isupper():
            raise self.ConstantCaseError("constant name {0} is not all uppercase".format(key))
        self.__dict__[key] = value
