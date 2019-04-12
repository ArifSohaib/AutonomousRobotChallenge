#loads and trains data using simple CPU data loading technique
#adapted from https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/r2/tutorials/load_data/images.ipynb#scrollTo=qj_U09xpDvOg

import pathlib 
import tensorflow as tf 
AUTOTUNE = tf.data.experimental.AUTOTUNE
def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    image /= 255.0  # normalize to [0,1] range
    return image

def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)

def caption_image(image_path):
    image_rel = pathlib.Path(image_path).relative_to(data_root)
    return "Image " + image_rel.parts[-1]

data_root_orig = "../datasetSearch/images/"
data_root = pathlib.Path(data_root_orig)

for item in data_root.iterdir():
    print(item)

import random
all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]
random.shuffle(all_image_paths)

image_count = len(all_image_paths)
print(f"total: {image_count} images")
label_names = sorted(item.name for item in data_root.glob('*/') if item.is_dir())
print(f"label_names:{label_names}")
label_to_index = dict((name, index) for index,name in enumerate(label_names))
print(f"label_indices: {label_to_index}")

all_image_labels = [label_to_index[pathlib.Path(path).parent.name]
                    for path in all_image_paths]

print("First 10 labels indices: ", all_image_labels[:10])

import matplotlib.pyplot as plt

img_path = all_image_paths[0]
image_path = all_image_paths[0]
label = all_image_labels[0]

plt.imshow(load_and_preprocess_image(img_path))
plt.grid(False)
plt.xlabel(caption_image(img_path))
plt.title(label_names[label].title())
plt.show()

path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)
print(path_ds)
image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=AUTOTUNE)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,8))
for n,image in enumerate(image_ds.take(4)):
    plt.subplot(2,2,n+1)
    plt.imshow(image)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.xlabel(caption_image(all_image_paths[n]))
plt.show()

label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))
image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))
print(image_label_ds)
ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))

# The tuples are unpacked into the positional arguments of the mapped function
def load_and_preprocess_from_path_label(path, label):
  return load_and_preprocess_image(path), label

image_label_ds = ds.map(load_and_preprocess_from_path_label)
image_label_ds
BATCH_SIZE = 32

# Setting a shuffle buffer size as large as the dataset ensures that the data is
# completely shuffled.
ds = image_label_ds.shuffle(buffer_size=image_count)
ds = ds.repeat()
ds = ds.batch(BATCH_SIZE)
# `prefetch` lets the dataset fetch batches, in the background while the model is training.
ds = ds.prefetch(buffer_size=AUTOTUNE)
ds = image_label_ds.apply(
  tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE)
ds = ds.prefetch(buffer_size=AUTOTUNE)
mobile_net = tf.keras.applications.MobileNetV2(input_shape=(192, 192, 3), include_top=False)
mobile_net.trainable=False

def change_range(image,label):
    return 2*image-1, label

keras_ds = ds.map(change_range)
# The dataset may take a few seconds to start, as it fills its shuffle buffer.
image_batch, label_batch = next(iter(keras_ds))
feature_map_batch = mobile_net(image_batch)
print(feature_map_batch.shape)
model = tf.keras.Sequential([
    mobile_net,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(len(label_names))])
logit_batch = model(image_batch).numpy()

print("min logit:", logit_batch.min())
print("max logit:", logit_batch.max())
print()

print("Shape:", logit_batch.shape)

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=["accuracy"])
len(model.trainable_variables)
model.summary()
steps_per_epoch=tf.math.ceil(len(all_image_paths)/BATCH_SIZE).numpy()
print(f'steps_per_epoch:{steps_per_epoch}')
checkpoint_path = "plant_model/cp.ckpt"
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
model.fit(ds, epochs=10, callbacks=[cp_callback])

# import time
# default_timeit_steps = 2*steps_per_epoch+1

# def timeit(ds, steps=default_timeit_steps):
#     overall_start = time.time()
#     # Fetch a single batch to prime the pipeline (fill the shuffle buffer),
#     # before starting the timer
#     it = iter(ds.take(steps+1))
#     next(it)

#     start = time.time()
#     for i,(images,labels) in enumerate(it):
#         if i%10 == 0:
#             print('.',end='')
#     print()
#     end = time.time()

#     duration = end-start
#     print("{} batches: {} s".format(steps, duration))
#     print("{:0.5f} Images/s".format(BATCH_SIZE*steps/duration))
    
#     print("Total time: {}s".format(end-overall_start))

# ds = image_label_ds.apply(
#   tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
# ds = ds.batch(BATCH_SIZE).prefetch(buffer_size=AUTOTUNE)
# print(f'ds:{ds}')

# #build tf_record
# image_ds = tf.data.Dataset.from_tensor_slices(all_image_paths).map(tf.io.read_file)
# tfrec = tf.data.experimental.TFRecordWriter('images.tfrec')
# tfrec.write(image_ds)
# image_ds = tf.data.TFRecordDataset('images.tfrec').map(preprocess_image)

# BATCH_SIZE=32
# s = tf.data.Dataset.zip((image_ds, label_ds))
# ds = ds.apply(
#     tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
# ds=ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)