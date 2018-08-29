from tensorflow.python.keras.layers import Input
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Convolution2D, MaxPool2D, Reshape
from tensorflow.python.keras.layers import Dropout, Flatten, Dense
from tensorflow.python.keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
def default_linear():
    "fully connected version of the default linear model"
    img_in = Input(shape=(224, 224, 3), name='img_in')
    x = img_in

    # Convolution2D class name is an alias for Conv2D
    x = Convolution2D(filters=24, kernel_size=(5, 5), strides=(2, 2), activation='elu')(x) #output shape 110x110
    x = Convolution2D(filters=32, kernel_size=(5, 5), strides=(2, 2), activation='elu')(x) #output shape 53x53
    x = Convolution2D(filters=64, kernel_size=(5, 5), strides=(2, 2), activation='elu')(x) #output shape 25x25
    x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='elu')(x) #output shape 12x12
    x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='elu')(x) #output shape 10x10
    x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='elu')(x) #output shape 5x5
    x = Convolution2D(filters=100, kernel_size=(3,3), strides=(2, 2), activation='elu')(x)
    # x = Reshape([None, 100])(x)
    x = Flatten(name='flattened')(x)
    # x = Dense(units=100, activation='linear')(x)
    # x = Dropout(rate=.1)(x)
    # x = Dense(units=50, activation='linear')(x)
    # x = Dropout(rate=.1)(x)
    # categorical output of the angle
    control_out = Dense(units=4, activation='relu', name='control_out')(x)

    # continous output of throttle for later possibly
    # throttle_out = Dense(units=1, activation='linear', name='throttle_out')(x)

    model = Model(inputs=[img_in], outputs=[control_out])

    model.compile(optimizer='adam',
                  loss={'control_out': 'categorical_crossentropy'})

    return model

def main():
    data= np.load("train_data_wcc.npy", encoding='latin1')

    images = []
    labels = []
    for i in range(len(data)):
        images.append(data[i]['image'])
        labels.append(data[i]['input'])

    images = np.array(images)
    labels = np.array(labels)

    model = default_linear()
    model.fit(images, labels, batch_size=32, epochs=100)

    #test model 
    preds = model.predict(images[:10])
    for i in range(len(preds)):
        print(np.argmax(preds[i]), np.argmax(labels[i]))


if __name__ == "__main__":
    main()