import numpy as np 

data= np.load("train_data_wcc.npy", encoding='latin1')

import matplotlib.pyplot as plt 
import cv2
img = plt.imshow(data[100]["image"][:,:,::-1])
print(type(img))
plt.show()