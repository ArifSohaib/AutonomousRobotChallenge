from tensorflow.python.keras.layers import Input
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Convolution2D, MaxPool2D, Reshape
from tensorflow.python.keras.layers import Dropout, Flatten, Dense
from tensorflow.python.keras.callbacks import ModelCheckpoint, EarlyStopping
import tensorflow as tf
import os
import numpy as np

def donkey_model():
    img_in = Input(shape=(224, 224, 3), name='img_in')
    x = img_in

    # Convolution2D class name is an alias for Conv2D
    x = Convolution2D(filters=24, kernel_size=(5, 5), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(filters=32, kernel_size=(5, 5), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(filters=64, kernel_size=(5, 5), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu')(x)

    x = Flatten(name='flattened')(x)
    x = Dense(units=100, activation='linear')(x)
    x = Dropout(rate=.1)(x)
    x = Dense(units=50, activation='linear')(x)
    x = Dropout(rate=.1)(x)

    # continous output of throttle
    control_out = Dense(units=5, activation='linear', name='control_out')(x)

    model = Model(inputs=[img_in], outputs=[control_out])

    model.compile(optimizer='adam',
                  loss={'control_out': 'categorical_crossentropy'},
                  metrics=['acc'])

    return model

def default_linear():
    "fully connected version of the default linear model"
    img_in = Input(shape=(224, 224, 3), name='img_in')
    x = img_in

    # Convolution2D class name is an alias for Conv2D
    x = Convolution2D(filters=64, kernel_size=(5, 5), strides=(2, 2), activation='elu')(x) #output shape 110x110
    
    x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='elu')(x) #output shape 27x27
    x = MaxPool2D(pool_size=(2,2))(x) 
    x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='relu')(x) #output shape 7x7
    x = MaxPool2D(pool_size=(2,2))(x)
    x = Convolution2D(filters=5, kernel_size=(3,3), strides=(2, 2), activation='relu')(x)
    x = MaxPool2D(pool_size=(2,2))(x) #output 5x5
    control_out = Flatten(name='control_out')(x)
    # control_out = Dense(units=4, activation='relu', name='control_out')(x)

    # continous output of throttle for later possibly
    # throttle_out = Dense(units=1, activation='linear', name='throttle_out')(x)

    model = Model(inputs=[img_in], outputs=[control_out])

    model.compile(optimizer='adam',
                  loss={'control_out': 'categorical_crossentropy'},
                  metrics=['acc'])

    return model

def main():
    data= np.load("train_data.npy", encoding='latin1')

    images = []
    labels = []
    for i in range(len(data)):
        images.append(data[i]['image'])
        labels.append(data[i]['input'])

    images = np.array(images)
    labels = np.array(labels)

    model = default_linear()
    print(model.summary())
    checkpoint_path = "training_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create checkpoint callback
    #cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, 
    #                                             save_weights_only=True,
    #                                             verbose=1)
    model.fit(images, labels, batch_size=20, epochs=500, validation_split=0.2)#, callbacks = [cp_callback])
    model.save_weights("training_1/model.h5")
    #test model 
    preds = model.predict(images[:10])
    for i in range(len(preds)):
        print(np.argmax(preds[i]), np.argmax(labels[i]))


if __name__ == "__main__":
    main()