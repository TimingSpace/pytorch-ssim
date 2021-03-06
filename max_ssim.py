import pytorch_ssim
import torch
from torch import optim
import cv2
import numpy as np

npImg1 = cv2.imread("einstein.png")

img1 = torch.from_numpy(np.rollaxis(npImg1, 2)).float().unsqueeze(0)/255.0
img2 = torch.rand(img1.size())

if torch.cuda.is_available():
    img1 = img1.cuda()
    img2 = img2.cuda()


img2.requires_grad = True


# Functional: pytorch_ssim.ssim(img1, img2, window_size = 11, size_average = True)
ssim_value = pytorch_ssim.ssim(img1, img2).item()
print("Initial ssim:", ssim_value)

# Module: pytorch_ssim.SSIM(window_size = 11, size_average = True)
ssim_loss = pytorch_ssim.SSIM()

optimizer = optim.Adam([img2], lr=0.01)

while ssim_value < 0.95:
    optimizer.zero_grad()
    mask = torch.Tensor(np.ones((img1.shape[0],img1.shape[2],img1.shape[3])))
    mask[0,:,0:img1.shape[3]//2]=0
    ssim_out = -ssim_loss(img1, img2,mask)
    ssim_value = - ssim_out.data.item()
    print(ssim_value)
    ssim_out.backward()
    optimizer.step()
    ssim_map = pytorch_ssim.ssim_map(img1,img2)
    img_show = img2.detach().numpy().squeeze().transpose(1,2,0)
    img_ssim = ssim_map.detach().numpy().squeeze().transpose(1,2,0)
    cv2.imshow('img',img_show)
    cv2.imshow('ssim',img_ssim)
    key = cv2.waitKey()
    if key&255==ord('q'):
        break
