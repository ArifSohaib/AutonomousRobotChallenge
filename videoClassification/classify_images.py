#heavily modified from https://blog.coast.ai/continuous-online-video-classification-with-tensorflow-inception-and-a-raspberry-pi-785c8b1e13e1
import tensorflow as tf
import time 

class ClassifyImages:
    def __init__(self, model_path, label_path, model_name):
        """
        class for classifying images
        args:
            model_path = path to ".pb" file containing the model
            label_path = path to the labels
        """
        self.model_path = model_path
        self.label_path = label_path
        self.model_name = model_name
    def get_label(self):
        """get the labels from file
           returns:
            list containing labels
        """
        with open(self.label_path,'r') as fin:
            self.labels = [line.strip('\n') for line in fin]
            return self.labels

    def predict_on_image(self, image):
        """
        get predicted results on individual images
        args:
            image: jpeg image path
        returns:
            predicticted label
        """
        #read graph from file
        with tf.gfile.FastGFile(self.model_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name=self.model_name)

        with tf.Session() as sess:
            #possible change with the following later
            #softmax_tensor = sess.graph._get_tensor_by_tf_output
            softmax_tensor = sess.graph._get_tensor_by_name('final_result:0')
            #read in the image data
            image_data = tf.gfile.FastGFile(image, 'rb').read()
            try:
                predictions = sess.run(softmax_tensor,
                        {'DecodeJpeg/contents:0':image_data})
                prediction = predictions[0]
            except:
                print("error making prediction")
                sys.exit()

        #return the label of the top classification
        prediction = prediction.tolist()
        max_value = max(prediction)
        max_index = prediction.index(max_value)
        predicted_label = self.labels[max_index]
        return predicted_label

    def predict_on__pi_video(self):
        """
        get continous classification on Raspberry Pi Camera(NOT USB camera)
        """
        camera = PiCamera()
        camera.resolution = (320,240)
        camera.framerate = 10
        rawCapture = PiRGBArray(camera, size=(320,240))

        #warmup?
        time.sleep(2)
        #read graph from file
        with tf.gfile.FastGFile(self.model_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name=self.model_name)
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name("final_result:0")
            for i, image in enumerate(camera.capture_continous(rawCapture, format='bgr', use_video_port=True)):
                #get numpy version of the image
                decoded_image = image.array
                #make the prediction
                predictions = sess.run(softmax_tensor, {"DecodeJpeg:0":decoded_image})
                prediction = predictions[0]
                #get the highest confidence category
                prediction = prediction.tolist()
                max_value = max(prediction)
                max_index = prediction.index(max_value)
                predicted_label = self.labels[max_index]

                print("{} {.2f}%".format(predicted_label, max_value*100))
                #reset the buffer so we are ready for the next one
                rawCapture.truncate(0)
