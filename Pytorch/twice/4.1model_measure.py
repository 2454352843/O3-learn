'''
    单图测试
'''

import torch
from torchvision.models import resnet18
from PIL import Image
import torchvision.transforms as transforms
import os
from sklearn.metrics import r2_score
from Pytorch.twice import models
from Pytorch.twice.Dataset import LoadData

transform_BZ= transforms.Normalize(
    mean=[0.46402064, 0.45047238, 0.37801373],  # 取决于数据集
    std=[0.2007732, 0.196271, 0.19854763]
)


def padding_black(img,img_size = 512):  # 如果尺寸太小可以扩充
    w, h = img.size
    scale = img_size / max(w, h)
    img_fg = img.resize([int(x) for x in [w * scale, h * scale]])
    size_fg = img_fg.size
    size_bg = img_size
    img_bg = Image.new("RGB", (size_bg, size_bg))
    img_bg.paste(img_fg, ((size_bg - size_fg[0]) // 2,
                          (size_bg - size_fg[1]) // 2))
    img = img_bg
    return img

if __name__=='__main__':

    train_dataset = LoadData("Resource/test.txt", True)
    print("数据个数：", len(train_dataset))
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=1,
                                               shuffle=True)

    # 如果显卡可用，则用显卡进行训练
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")

    finetune_net = models.resnet18().to(device)

    state_dict = torch.load(r"output/resnet18_StepLR/resnet18_no_pretrain_last.pth")
    # print("state_dict = ",state_dict)
    finetune_net.load_state_dict(state_dict)
    finetune_net.eval()
    with torch.no_grad():

        # 读取数据
        for batch, (image, label) in enumerate(train_loader):


            img_tensor = image.to(device)
            result = finetune_net(img_tensor)
            # print("result = ",result.argmax(1))

            result = float(result)
            print("pred is : {pred} ,and label is:{lab}".format(pred = result*300 , lab = float(label)*300))
