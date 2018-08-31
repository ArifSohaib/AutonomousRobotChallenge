import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

data = np.load("train_data_wcc2.npy", encoding="latin1")
# each frame
ims = []
for i in range(len(data)):
    im = plt.imshow(data[i]['image'][:,:,::-1],animated=True)
    ims.append([im])


ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)

# ani.save('dynamic_images.mp4')

plt.show()
import cv2
import numpy as np
import matplotlib.pyplot as plt

data = np.load('train_data_wcc2.npy',encoding='latin1')
for i in range(len(data)):
    cv2.imshow("imgage",data[i]['image'])
    
