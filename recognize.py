import cv2
import datetime
import argparse
import imutils
import sys
import os

import tensorflow as tf
from imutils.video import VideoStream
from utils import detector_utils as detector_utils


def detection():
    print("in detection")
    # detect hand and generate height and width of frame in which hand is detected
    # out :- frame co-ordinates to image_store()

    detection_graph, sess = detector_utils.load_inference_graph()

    # Detection confidence threshold to draw bounding box
    score_thresh = 0.60

    # Get stream from webcam and set parameters)
    vs = VideoStream().start()

    # max number of hands we want to detect/track
    num_hands_detect = 1

    im_height, im_width = (None, None)
    try:
        while True:
            # Read Frame and process
            frame = vs.read()
            frame = cv2.resize(frame, (640, 480))
            if im_height == None:
                im_height, im_width = frame.shape[:2]
            
            # Convert image to rgb since opencv loads images in bgr, if not accuracy will decrease
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                print("Error converting to RGB")
            
            # Run image through tensorflow graph
            boxes, scores, classes = detector_utils.detect_objects(
                frame, detection_graph, sess)
            
            # Draw bounding boxeses and text
            detector_utils.draw_box_on_image(
                num_hands_detect, score_thresh, scores, boxes, classes, im_width, im_height, frame)
            
            cv2.imshow('Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                vs.stop()
                break
    except KeyboardInterrupt:
        pass#print("Average FPS: ", str("{0:.2f}".format(fps)))
        
def classify():
    # classify image from a image in path 
    # in :- image path
    # out :- var with probability 
    # Disable tensorflow compilation warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

    image_path = "/home/varadvanjape/Code/Python/Sem_2/MegaProject_sem2/Images/image1.png"

    # Read the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()


    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                       in tf.gfile.GFile("output_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
