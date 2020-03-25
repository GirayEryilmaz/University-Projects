from keras.models import Model, Sequential
from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation, Cropping2D
from keras.preprocessing.image import load_img, save_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
from keras.models import model_from_json

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

class FaceRecognizer:

    def __init__(self, path_to_weights=None):
        
        self.__model = self.__make_vgg_model()
        if  path_to_weights is not None:
            self.__model.load_weights(path_to_weights)
        self.vgg_face_descriptor = Model(inputs=self.__model.layers[0].input, outputs=self.__model.layers[-2].output)

    
    def load_weights(self, path_to_weights):
        self.__model.load_weights(path_to_weights)
    
    def get_vgg_model(self):
        return self.__model

    def __make_vgg_model(self):
        model = Sequential()
        model.add(ZeroPadding2D((1,1),input_shape=(224,224, 3)))
        model.add(Convolution2D(64, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2,2), strides=(2,2)))

        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(128, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(128, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2,2), strides=(2,2)))

        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(256, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(256, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(256, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2,2), strides=(2,2)))

        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(512, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(512, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(512, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2,2), strides=(2,2)))

        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(512, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(512, (3, 3), activation='relu'))
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(512, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2,2), strides=(2,2)))

        model.add(Convolution2D(4096, (7, 7), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Convolution2D(4096, (1, 1), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Convolution2D(2622, (1, 1)))
        model.add(Flatten())
        model.add(Activation('softmax'))
        return model
    
    def preprocess_image(self, img_array):
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array   
    

    def distance(self, image1, image2, distance_function=distance.cosine):
        img1_representation = self.vgg_face_descriptor.predict(image1)[0,:]
        img2_representation = self.vgg_face_descriptor.predict(image2)[0,:]
        return distance_function(img1_representation, img2_representation)
    
    def get_features(self,img_array):
        return self.vgg_face_descriptor.predict(img_array)[0,:]