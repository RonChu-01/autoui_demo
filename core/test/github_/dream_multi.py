# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/19.
# Copyright (c) 2019 3KWan.
# Description :

import unittest


def hello():

    class TestSomething(unittest.TestCase):

        def test_add(self):
            print("test add")

        def test_2(self):
            print("test 2")

    suite = unittest.makeSuite(TestSomething)
    return suite
    # suite = unittest.TestSuite()
    # suite.addTest(TestSomething("test_add"))
    # suite.addTest(TestSomething("test_2"))
    # return suite


def world():

    class TestOther(unittest.TestCase):

        def test_a(self):
            print("test a")

        def test_b(self):
            print("test b")

    # suite = unittest.TestSuite()
    # suite.addTest(TestOther("test_a"))
    # suite.addTest(TestOther("test_b"))
    # return suite


if __name__ == '__main__':
    suite_1 = hello()
    # suite_2 = world()
    suite_base = unittest.TestSuite()
    suite_base.addTests(suite_1)
    # suite_base.addTest(suite_2)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite_base)
