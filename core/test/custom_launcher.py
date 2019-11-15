# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/11/13.
# Copyright (c) 2019 3KWan.
# Description :
from airtest.cli.parser import runner_parser
from airtest.cli.runner import AirtestCase, run_script


class CustomTestCase(AirtestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


if __name__ == '__main__':
    ap = runner_parser()
    args = ap.parse_args()
    run_script(args, CustomTestCase)
