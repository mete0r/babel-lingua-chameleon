# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest import makeSuite


class MYAPP_Test(TestCase):

    def test_nothing(self):
        pass


def test_suite():
    return makeSuite(MYAPP_Test)
