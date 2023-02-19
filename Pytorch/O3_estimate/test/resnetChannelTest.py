#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import torch
from torch import nn
from torchvision.models import resnet50

resnet_50 = resnet50()
rgb_input = torch.zeros((12, 3, 224, 224))
print(resnet_50(rgb_input).shape)
print(resnet_50.conv1)

weight = resnet_50.conv1.weight.sum(dim=1, keepdim=True)
print(weight.shape)
resnet_50.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
resnet_50.conv1.weight = nn.Parameter(weight)
# resnet_50.conv1.weight.data = temp
print(resnet_50.conv1.weight.requires_grad)

gray_input = torch.zeros((1, 1, 224, 224))
print(resnet_50(gray_input).shape)
