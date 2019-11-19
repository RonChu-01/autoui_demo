# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/19.
# Copyright (c) 2019 3KWan.
# Description :


import unittest


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite


class TestOne(ParametrizedTestCase):
    def test_something(self):
        print('param =', self.param)
        self.assertEqual(1, 1)

    def test_something_else(self):
        self.assertEqual(2, 2)


# pychram 中python unittest 没有执行 if __name__=='__main__'（需要以python的姿势执行方可运行__main__下面的内容）
if __name__ == '__main__':
    suite_ = unittest.TestSuite()
    suite_.addTest(ParametrizedTestCase.parametrize(TestOne, param=42))
    suite_.addTest(ParametrizedTestCase.parametrize(TestOne, param=13))
    unittest.TextTestRunner(verbosity=2).run(suite_)
