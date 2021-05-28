# Face-recognition
基于人脸识别+显著性检测的智能相册

# 实现过程
调用百度api识别我们指定的人，得到人脸预测框。
再用我们的U2GE-Net对图像处理，得到预测掩码
通过计算人脸预测框与预测掩码的重合度来决定照片的保存。

# 运行
如果你想要运行这个文件，请先安装百度api

pip install baidu-aip

可以在face_recognition.py文件中更改

    options['max_face_num'] = 4      # 最大识别人脸的个数（不超过10个人脸）
    options['match_threshold'] = 60  # 置信度

# 创新优点
我们的智能相册可以筛选出以指定人为**主体**的照片
![image](https://user-images.githubusercontent.com/73021377/119964978-55e95f00-bfdc-11eb-99bd-b44316fee1ca.png)
![image](https://user-images.githubusercontent.com/73021377/119965322-b6789c00-bfdc-11eb-9f3c-9789d628c1ad.png)


# 2021.5.28 创立了这个仓库，并上传了相关的代码。
