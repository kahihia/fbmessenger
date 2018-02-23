#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from background_task import background

import time

@background(schedule=10)
def  testing_it(test):
    for i in range(100):
        print(test)
        time.sleep(10)
