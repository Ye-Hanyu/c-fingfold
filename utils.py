'''
Author: YeHanyu
Date: 2022-07-22 13:47:25
LastEditors: YeHanyu
LastEditTime: 2022-07-25 16:59:51
FilePath: /c-fingfold/utils.py
Description: 

Copyright (c) 2022 by ye 237239045@qq.com, All Rights Reserved. 
'''

import numpy as np
import logging
import glob
import platform
import os
import random
import shutil
import sys
import xml.etree.cElementTree as ET
from xml.dom import minidom
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

'''
description: Bonding Box 类
param {*} score 置信度
param {*} x 左上角点x
param {*} y 左上角点y
param {*} r 右下角点x
param {*} b 右下角点y
param {*} label 类别标签
'''
class BBox():
    def __init__(self, x = 0, y = 0,r = 0, b = 0, score = 0, label = 0, classname = ''):
        self.x = x
        self.y = y
        self.r = r
        self.b = b
        self.score = score
        self.label = label
        self.classname = classname

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
        # 变换大小 sourceSize(width, height), dstSize(width, height)
        out = BBox()
        out.x = self.x / sourceSize[0] * dstSize[0];
        out.y = self.y / sourceSize[1] * dstSize[1];
        out.r = self.r / sourceSize[0] * dstSize[0];
        out.b = self.b / sourceSize[1] * dstSize[1];
        return out
    
    def offset(self, position):
        # 偏移position(x,y)
        self.x += position.x;
        self.y += position.y;
        self.r += position.x;
        self.b += position.y;
    
    def tl(self):
        return(self.x, self.y)
    
    def rb(self):
        return(self.r, self.b)
    
    def mergeOf(self, b):
        # 求两者最小外界矩形框
        out = BBox()
        out.x = min(self.x, b.x);
        out.y = min(self.y, b.y);
        out.r = max(self.r, b.r);
        out.b = max(self.b, b.b);
        return out
    
    '''
    description: 按边缘扩展
    param {*} margin 边缘大小
    param {*} limit 尺寸限制(width, height)
    '''
    def expandMargin(self, margin=0, limit=(0,0)):
        expandbox = BBox()
        expandbox.x = int(self.x-margin)
        expandbox.y = int(self.y-margin)
        expandbox.r = int(self.r+margin)
        expandbox.b = int(self.b+margin)
        
        if limit !=(0,0):
            if expandbox.width()>limit[0]:
                center = expandbox.center()
                expandbox.x = int(center[0]-limit[0]/2)
                expandbox.r = int(center[0]+limit[0]/2)
            if expandbox.height()>limit[1]:
                center = expandbox.center()
                expandbox.y = int(center[1]-limit[1]/2)
                expandbox.b = int(center[1]+limit[1]/2)
        
        return expandbox

    '''
    description: 按比例扩展
    param {*} margin 比例大小，1为不变
    param {*} limit 尺寸限制(width, height)
    '''
    def expand(self, ratio=1, limit=(0,0)):
        expandbox = BBox()
        center = self.center()
        expandbox.x = int(center[0]-self.width()*ratio/2)
        expandbox.y = int(center[1]-self.height()*ratio/2)
        expandbox.r = int(center[0]+self.width()*ratio/2)
        expandbox.b = int(center[1]+self.height()*ratio/2)
        
        if limit !=(0,0):
            if expandbox.width()>limit[0]:
                center = expandbox.center()
                expandbox.x = int(center[0]-limit[0]/2)
                expandbox.r = int(center[0]+limit[0]/2)
            if expandbox.height()>limit[1]:
                center = expandbox.center()
                expandbox.y = int(center[1]-limit[1]/2)
                expandbox.b = int(center[1]+limit[1]/2)
        
        return expandbox
    
    def iouMinOf(self, b):
        # iou计算，按两个框中小的作为分母
        xmax = max(self.x, b.x)
        ymax = max(self.y, b.y)
        xmin = min(self.r, b.r)
        ymin = min(self.b, b.b)
        uw = (xmin - xmax) if (xmin - xmax > 0) else 0
        uh = (ymin - ymax) if (ymin - ymax > 0) else 0
        iou = uw * uh
        return iou / min(self.area(), b.area())
    
    def iouOf(self, b):
        # iou计算，两框的并集作分母
        xmax = max(self.x, b.x)
        ymax = max(self.y, b.y)
        xmin = min(self.r, b.r)
        ymin = min(self.b, b.b)
        uw = (xmin - xmax) if (xmin - xmax > 0) else 0
        uh = (ymin - ymax) if (ymin - ymax > 0) else 0
        iou = uw * uh
        return iou / (self.area() + b.area() - iou)
    
def patternMatch(str, matcher_list, igrnoe_case=True):
    for i in range(len(matcher_list)):
        if igrnoe_case:
            str = str.lower()
            matcher = matcher_list[i].lower()
            
        if matcher[0] == '*':
            count = 0
            for j in range(len(matcher)-1):
                if str[-1-j]==matcher[-1-j]:
                    count += 1
                    continue
                else:
                    break
            if count==(len(matcher)-1):
                return True
            else:
                continue
        
        elif len(str)<len(matcher):
            continue
        
        else:
            count = 0
            for j in range(len(str)):
                if matcher[j] == '?':
                    count += 1
                    continue
                elif str[j] == matcher[j]:
                    count += 1
                    continue
                else:
                    break
            if count==len(str):
                return True
            else:
                continue
    return False

def loadxml(file):
    xml_tree = ET.parse(file)
    objs = xml_tree.findall('object')
    output=[]
    for i, obj in enumerate(objs): 
        out = BBox()
        out.classname = obj.find('name').text
        out.x = int(obj.find('bndbox').find('xmin').text)
        out.y = int(obj.find('bndbox').find('ymin').text)
        out.r = int(obj.find('bndbox').find('xmax').text)
        out.b = int(obj.find('bndbox').find('ymax').text)
        output.append(out)
    return output

def savexml(xml_path, img_full_path, width, height, obj_list):
    """
    生成矩形框标注文件
    :param xml_path: 标注文件路径
    :param img_full_path: 图像文件路径
    :param obj_list: 目标位置信息列表  (xmin,ymin,xmax,ymax,label)
    :param width:图像宽
    :param height:图像宽
    """
    # 1.创建DOM树对象
    dom = minidom.Document()
    # 2.创建根节点。每次都要用DOM对象来创建任何节点。
    root_node = dom.createElement('annotation')
    # 3.用DOM对象添加根节点
    dom.appendChild(root_node)

    # 用DOM对象创建元素子节点
    folder_node = dom.createElement('folder')
    # 用父节点对象添加元素子节点
    root_node.appendChild(folder_node)
    img_folder_path=os.path.basename(img_full_path)
    folder__node_text = dom.createTextNode(img_folder_path)
    # 用添加了文本的节点对象（看成文本节点的父节点）添加文本节点
    folder_node.appendChild(folder__node_text)

    filename_node = dom.createElement('filename')
    root_node.appendChild(filename_node)
    file_name=img_full_path.split('\\')[-1]
    filename_node_text = dom.createTextNode(file_name)
    filename_node.appendChild(filename_node_text)

    path_node = dom.createElement('path')
    root_node.appendChild(path_node)
    path_node_text = dom.createTextNode(img_full_path)
    path_node.appendChild(path_node_text)

    source_node = dom.createElement('source')
    root_node.appendChild(source_node)

    database_node = dom.createElement('database')
    source_node.appendChild(database_node)
    database_node_text = dom.createTextNode('Unknown')
    database_node.appendChild(database_node_text)

    size_node = dom.createElement('size')
    root_node.appendChild(size_node)

    width_node = dom.createElement('width')
    size_node.appendChild(width_node)
    width_node_text = dom.createTextNode(str(width))
    width_node.appendChild(width_node_text)

    height_node = dom.createElement('height')
    size_node.appendChild(height_node)
    height_node_text = dom.createTextNode(str(height))
    height_node.appendChild(height_node_text)

    depth_node = dom.createElement('depth')
    size_node.appendChild(depth_node)
    depth_node_node_text = dom.createTextNode(str(3))
    depth_node.appendChild(depth_node_node_text)

    segmented_node = dom.createElement('segmented')
    root_node.appendChild(segmented_node)
    segmented_node_text = dom.createTextNode(str(0))
    segmented_node.appendChild(segmented_node_text)

    for obj in obj_list:
        object_node = dom.createElement('object')
        root_node.appendChild(object_node)

        name_node = dom.createElement('name')
        object_node.appendChild(name_node)
        name_node_text = dom.createTextNode(str(obj.classname))
        name_node.appendChild(name_node_text)

        pose_node = dom.createElement('pose')
        object_node.appendChild(pose_node)
        pose_node_text = dom.createTextNode('Unspecified')
        pose_node.appendChild(pose_node_text)

        truncated_node = dom.createElement('truncated')
        object_node.appendChild(truncated_node)
        truncated_node_text = dom.createTextNode(str(0))
        truncated_node.appendChild(truncated_node_text)

        difficult_node = dom.createElement('difficult')
        object_node.appendChild(difficult_node)
        difficult_node_text = dom.createTextNode('0')
        difficult_node.appendChild(difficult_node_text)

        bndbox_node = dom.createElement('bndbox')
        object_node.appendChild(bndbox_node)

        xmin_node = dom.createElement('xmin')
        bndbox_node.appendChild(xmin_node)
        xmin_node_text = dom.createTextNode(str(obj.x))
        xmin_node.appendChild(xmin_node_text)

        ymin_node = dom.createElement('ymin')
        bndbox_node.appendChild(ymin_node)
        ymin_node_text = dom.createTextNode(str(obj.y))
        ymin_node.appendChild(ymin_node_text)

        xmax_node = dom.createElement('xmax')
        bndbox_node.appendChild(xmax_node)
        xmax_node_text = dom.createTextNode(str(obj.r))
        xmax_node.appendChild(xmax_node_text)

        ymax_node = dom.createElement('ymax')
        bndbox_node.appendChild(ymax_node)
        ymax_node_text= dom.createTextNode(str(obj.b))
        ymax_node.appendChild(ymax_node_text)

    try:
        with open(xml_path, 'w', encoding='UTF-8') as fh:
            # 4.writexml()第一个参数是目标文件对象,第二个参数是根节点的缩进格式,第三个参数是其他子节点的缩进格式,
            # 第四个参数制定了换行格式,第五个参数制定了xml内容的编码。
            dom.writexml(fh, addindent=" ", newl="\n",encoding='UTF-8')
            # print('写入xml OK!')
    except Exception as err:
        print('错误信息：{0}'.format(err))
        

