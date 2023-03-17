import torch
import numpy as np
from  osgeo import gdal
a= torch.arange(0,10)
size = a.size()
t = a.view(1,a.size()[0])
print(t)
print(t.shape)