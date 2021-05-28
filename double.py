from aip import AipFace
from net import test
import cv2
import base64
import math
import numpy as np

""" 你的 APPID AK SK """
APP_ID = '24259538'
API_KEY = 'xkY5T9de3lpnUB04FDAkNAhO'
SECRET_KEY = 'RQSCqL6wC9jxfoMcL0yI3QFK4i8EiekA '
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

"""参数"""
image_path='4.jpg'
pic = open(image_path, "rb")
pic_base64 = base64.b64encode(pic.read())
pic_base64 = str(pic_base64,'utf-8')

imageType="BASE64"
groupIdList='1'


""" 如果有可选参数 """
options = {}
options['max_face_num']=4
options['match_threshold']=20   #置信度


"""人脸搜索 M:N 识别"""
search_result=client.multiSearch(pic_base64, imageType, groupIdList,options)
print(search_result)
result=search_result['result']
face_num=result['face_num']
box=[]
for i in range(face_num):
    face_list=result['face_list'][i]
    location=face_list["location"]
    user_list=face_list["user_list"]
    if len(user_list)==0:
        continue

    """获取坐标"""
    left=math.ceil(location['left'])
    top=math.ceil(location['top'])
    width=math.ceil(location['width'])
    height=math.ceil(location['height'])
    index=[left,top,width,height]
    box.append(index)
    print(face_list)
    print('left,top,width,height',left,top,width,height)

    # """画图"""
    # image=cv2.imread(image_path)
    # image_gray=image[:,:,0]
    # cv2.imshow('d',image_gray[top:top+height,left:left+width])
    # cv2.waitKey(0)
    # cv2.imwrite('./final.jpg',image_gray[top:top+height,left:left+width])

assert len(box)>0,"小甜心不在里面呢"

"""掩码"""
mask=test(image_path)[:,:,0]
cv2.imwrite('./22.png',mask*255)

"""计算占比"""
T=0
total=0
for i in range(len(box)):
    left, top, width, height=box[i]
    a=mask[top:top+height,left:left+width]
    T+=np.sum(mask[top:top+height,left:left+width])
    total+= height*width
ratio=T/total
print('Ratio：',ratio)