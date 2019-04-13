"""converts data to tf_record file """
import tensorflow as tf 
import pathlib
import random
import preprocessing
import matplotlib.pyplot as plt 
BATCH_SIZE = 32
AUTOTUNE = tf.data.experimental.AUTOTUNE

#retrieve the images
data_root_orig = "../datasetSearch/images/"
data_root = pathlib.Path(data_root_orig)
print(data_root)

#check the images
for item in data_root.iterdir():
    print(item)

#shuffle images
all_image_paths = list(data_root.glob("*/*"))
all_image_paths = [str(path) for path in all_image_paths]
random.shuffle(all_image_paths)
image_count = len(all_image_paths)
print(f"loaded {image_count} images")

#get labels for images
label_names = sorted(item.name for item in data_root.glob("*/") if item.is_dir())
print(f"labels{set(label_names)}")
#add index to labels
label_to_index = dict((name, index) for index, name in enumerate(label_names))
#create label dict
all_image_labels = [label_to_index[pathlib.Path(path).parent.name] for path in all_image_paths]
print(f"First 10 label indices:\n {all_image_labels[:10]}")

"""NORMAL METHOD"""
'''
#build a tf.data.Dataset
path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)
print(f"path dataset: {path_ds}")
image_ds = path_ds.map(preprocessing.load_and_preprocess_image, num_parallel_calls=AUTOTUNE)
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))
#print first 10 labels
for label in label_ds.take(10):
    print(label)
#since the datasets are in the same order, we can zip them to get a dataset of (image, label) pairs
image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))
for data in image_label_ds.take(2):
    plt.imshow(data[0], label=data[1])
    plt.legend()
    plt.show()
'''
"""Serialized dataset"""
paths_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)
image_ds = paths_ds.map(preprocessing.load_and_preprocess_image) 
ds = image_ds.map(tf.io.serialize_tensor)
tfrec = tf.data.experimental.TFRecordWriter('../datasetSearch/images.tfrec')
tfrec.write(ds)

ds = tf.data.TFRecordDataset('../datasetSearch/images.tfrec')
ds = ds.map(preprocessing.parse, num_parallel_calls=AUTOTUNE)
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))
image_label_ds = tf.data.Dataset.zip((ds, label_ds))

ds = image_label_ds.apply(tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = image_label_ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)

model = tf.keras.models.load_model("plant_model/model.h5")
model.fit(ds, epochs=10)
tf.saved_model.save(model,"plant_model")