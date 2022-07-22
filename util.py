'''
Author: YeHanyu
Date: 2022-07-22 13:47:25
LastEditors: YeHanyu
LastEditTime: 2022-07-22 15:41:43
FilePath: /c-fingfold/util.py
Description: 

Copyright (c) 2022 by ye 237239045@qq.com, All Rights Reserved. 
'''

from black import out
import numpy as np
import logging
import os
import random
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional
from glob import glob
import cv2 as cv
import matplotlib.pyplot as plt



DEFAULT_FMT = "%(asctime)s - %(levelname)s - %(message)s"


'''
description: 
param {str} module_name
param {str} fmt
param {Optional} datefmt
param {Optional} logger_handler
return {*}
'''
def get_logger(
    module_name: str = "util",
    fmt: str = DEFAULT_FMT,
    datefmt: Optional[str] = None,
    logger_handler: Optional[logging.Handler] = None,
):
    logger = logging.getLogger(module_name)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if logger_handler is not None:
        logger.addHandler(logger_handler)
    return logger

def setRandomSeed(seed):
    np.random.seed(seed)
    random.seed(seed)

class BBox:
    def __init__(self, score = 0, x = 0, y = 0,r = 0, b = 0, label = 0):
        self.score = score
        self.x = x
        self.y = y
        self.r = r
        self.b = b
        self.label = label

    def width(self):
        return(self.r-self.x)
    
    def height(self):
        return(self.b-self.y)
    
    def center(self):
        return ((self.x + self.r) * 0.5, (self.y + self.b) * 0.5)
    
    def area(self):
        return self.width() * self.height()
    
    def box(self):
        return (self.x, self.y, self.width(),self.height())
    
    def transfrom(self, sourceSize, dstSize):
        # sourceSize(width, height), dstSize(width, height)
        out =BBox()
        out.x = self.x / sourceSize[0] * dstSize[0];
        out.y = self.y / sourceSize[1] * dstSize[1];
        out.r = self.r / sourceSize[0] * dstSize[0];
        out.b = self.b / sourceSize[1] * dstSize[1];
        return out