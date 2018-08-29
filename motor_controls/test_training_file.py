import numpy as np 
from drive_model import default_linear
import tensorflow as tf 
import matplotlib.pyplot as plt 
import cv2


data= np.load("train_data.npy", encoding='latin1')

img = plt.imshow(data[100]["image"][:,:,::-1])

plt.show()

images = []
labels = []
for i in range(len(data)):
    images.append(data[i]['image'])
    labels.append(data[i]['input'])

images = np.array(images)
labels = np.array(labels)
features_placeholder = tf.placeholder(images.dtype, images.shape)
labels_placeholder = tf.placeholder(labels.dtype, labels.shape)

dataset = tf.data.Dataset.from_tensor_slices((features_placeholder, labels_placeholder))
iterator = dataset.make_initializable_iterator()
sess = tf.Session()
sess.run(iterator.initializer, feed_dict={features_placeholder: images,
                                          labels_placeholder: labels})
sess.close()
