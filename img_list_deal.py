from aip import AipFace
import base64

from net import test
import cv2
import math
import numpy as np

import os
import glob
import shutil

"""API"""
def API():
    """ 你的 APPID AK SK """
    APP_ID = '24259538'
    API_KEY = 'xkY5T9de3lpnUB04FDAkNAhO'
    SECRET_KEY = 'RQSCqL6wC9jxfoMcL0yI3QFK4i8EiekA '
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    return client

"""计算重要性"""
def caluate_ratio(image_path,client):
    """参数"""
    pic = open(image_path, "rb")
    pic_base64 = base64.b64encode(pic.read())
    pic_base64 = str(pic_base64, 'utf-8')

    imageType = "BASE64"
    groupIdList = '1'

    """ 如果有可选参数 """
    options = {}
    options['max_face_num'] = 4
    options['match_threshold'] = 50  # 置信度

    """人脸搜索 M:N 识别"""
    search_result = client.multiSearch(pic_base64, imageType, groupIdList, options)
    result = search_result['result']
    if result==None:
        return 0
    face_num = result['face_num']
    box = []
    for i in range(face_num):
        face_list = result['face_list'][i]
        location = face_list["location"]
        user_list = face_list["user_list"]
        if len(user_list) == 0:
            continue

        """获取坐标"""
        left = math.ceil(location['left'])
        top = math.ceil(location['top'])
        width = math.ceil(location['width'])
        height = math.ceil(location['height'])
        index = [left, top, width, height]
        box.append(index)

        """画图"""
        # image=cv2.imread(image_path)
        # image_gray=image[:,:,0]
        # cv2.imshow('d',image_gray[top:top+height,left:left+width])
        # cv2.waitKey(0)
        # cv2.imwrite('./final.jpg',image_gray[top:top+height,left:left+width])
    if len(box)==0:
        return 0

    """掩码"""
    mask = test(image_path)[:, :, 0]

    """计算占比"""
    T = 0
    total = 0
    for i in range(len(box)):
        left, top, width, height = box[i]
        a = mask[top:top + height, left:left + width]
        T += np.sum(mask[top:top + height, left:left + width])
        total += height * width
    ratio = T / total
    print('Ratio：', ratio)
    return ratio

"""创立文件夹"""
def mkdir(path_photo,photo_del,photo_undel):

    folder_photo = os.path.exists(path_photo)
    folder_del = os.path.exists(photo_del)
    folder_undel = os.path.exists(photo_undel)

    if not folder_photo:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path_photo)  # makedirs 创建文件时如果路径不存在会创建这个路径
    if not folder_del:
        os.makedirs(photo_del)
    if not folder_undel:
        os.makedirs(photo_undel)

if __name__ == "__main__":
    #路径
    """文件夹路径"""
    file = os.path.join(os.getcwd()+os.sep)
    path_photo=file+'photo'
    photo_del=path_photo+'/photo_del'
    photo_undel=path_photo+'/photo_undel'

    """图片路径"""
    photo_path_list=os.path.join(os.getcwd()+os.sep+'my_photo'+os.sep)
    img_name_list = glob.glob(photo_path_list + os.sep + '*')

    # 创文件
    mkdir(path_photo,photo_del,photo_undel)

    #连接API
    client=API()

    #筛选图片
    """重要性"""
    for i in img_name_list:
        ratio=caluate_ratio(i,client)
        if ratio<0.8:
            shutil.copy(i, photo_del)
            print(i,'delete')
        else:
            shutil.copy(i,photo_undel)
            print(i,'save')
