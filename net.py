import os
from skimage import io, transform
import torch
import torchvision
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms  # , utils
# import torch.optim as optim

import numpy as np
from PIL import Image
import glob

from data_loader import RescaleT
from data_loader import ToTensor
from data_loader import ToTensorLab
from data_loader import SalObjDataset
import cv2
from model import GCT_net
# normalize the predicted SOD probability map


def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d-mi)/(ma-mi)

    return dn


def save_output(image_name, pred):

    predict = pred
    predict = predict.squeeze()

    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray(predict_np*255).convert('RGB')
    image = cv2.imread(image_name, 1)

    imo = im.resize((image.shape[1], image.shape[0]), resample=Image.BILINEAR)
    img = np.array(imo)
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return img/255

def mat(img, mask):
    mat = cv2.bitwise_and(img, mask)
    tmp = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    b, g, r = cv2.split(mat)

    rgba = [b, g, r, tmp]
    dst = cv2.merge(rgba, 4)
    return dst


def IOU(pred, mask):
    assert pred.shape == mask.shape, '!'

    temp = np.abs(mask-pred)
    t = np.sum(temp > 5)  # 并集减交集
    temp = mask+pred
    union = np.sum(temp > 254)  # 求出并集
    inter = union-t
    iou = inter/union

    return iou


def test(image_dir):

    image_dir=[image_dir]

    # --------- 1. get image path and name ---------
    model_name = 'u2netp'  # u2netp)
    prediction_dir = os.path.join(
        os.getcwd(), 'test_data', 'u3' + os.sep)
    model_dir = os.path.join(os.getcwd()+os.sep)
    mat_dir = os.path.join(os.getcwd(), 'test_data', 'u3_mat'+os.sep)

    # --------- 2. dataloader ---------
    # 1. dataloader
    test_salobj_dataset = SalObjDataset(img_name_list=image_dir,
                                        lbl_name_list=[],
                                        transform=transforms.Compose([RescaleT(320),
                                                                      ToTensorLab(flag=0)])
                                        )
    test_salobj_dataloader = DataLoader(test_salobj_dataset,
                                        batch_size=1,
                                        shuffle=False,
                                        num_workers=0)

    # --------- 3. model define ---------
    if(model_name == 'u2net'):
        print("...load U2NET---173.6 MB")
    elif(model_name == 'u2netp'):
        print("...load U2NEP---4.7 MB")
        net = torch.load(
            model_dir+'boundary_loss3itr_109200_train_3.459103_tar_0.373074.pth', map_location='cpu')


    net.eval()
    i = 0
    # --------- 4. inference for each image ---------
    for i_test, data_test in enumerate(test_salobj_dataloader):

        i += 1
        print(i)
        inputs_test = data_test['image']
        inputs_test = inputs_test.type(torch.FloatTensor)

        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)

        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

        pred = d1[:, 0, :, :]
        pred = normPRED(pred)

        # save results to test_results folder
        if not os.path.exists(prediction_dir):
            os.makedirs(prediction_dir, exist_ok=True)
        img=save_output(image_dir[0], pred)

        del d1, d2, d3, d4, d5, d6, d7
    return img
