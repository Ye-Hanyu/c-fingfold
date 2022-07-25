
from utils import *

bbox_a = BBox(0,0,100,100)
bbox_b = BBox(50,50,150,150)
bbox_c = bbox_a.mergeOf(bbox_b)
bbox_e = bbox_a.expand(0.5)
iou = bbox_a.iouOf(bbox_b)
same = patternMatch('abcdefg.png', ('dsa.png','AbcDefg.pnga','*.png'))
# str1 = 'abcdefg.png'
# str2 = ('abcdefg.png','abcdefg.png')
# teststr=str1[0][0]
str2="hahs.png;asdf.png"
str2+='/'
filelist= glob('/home/ye/图片/**',recursive=True)
path = Path('/home/ye/图片/')
dirs = [e for e in path.iterdir() if e.is_dir()]
str3 = str2.split('s')
objs = loadxml('/home/ye/图片/test2.xml',CoCo)
savexml('/home/ye/图片/test3.xml','/',1344,1344,objs,VOC)
end = 0