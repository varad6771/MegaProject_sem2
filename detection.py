import cv2
import datetime
import argparse
import imutils
import time
import sys
import os

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import copy
import tensorflow as tf

from imutils.video import VideoStream
from utils import detector_utils as detector_utils


# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


def predict(image_data):
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})

    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    max_score = 0.0
    res = ''
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if score > max_score:
            max_score = score
            res = human_string
    return res, max_score

def detect():
    global sess
    global label_lines
    global softmax_tensor
    global res
    global score
    global frame
    global mode_val
    mode_val = 0


    color = (0,255,0)
    label_lines = [line.rstrip() for line
                       in tf.gfile.GFile("output_labels.txt")]
				   
    # Unpersists graph from file
    with tf.gfile.FastGFile("output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    detection_graph, sessD = detector_utils.load_inference_graph()

    with tf.Session() as sess:
        score_thresh = 0.60
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        # Get stream from webcam and set parameters)
        vs = VideoStream().start()

        # max number of hands we want to detect/track
        num_hands_detect = 1

        im_height, im_width = (None, None)
        try:
            while True:
                # Read Frame and process
                frame = vs.read()
                frame = cv2.flip(frame, 1)			
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
                    frame, detection_graph, sessD)

                if (scores[0] > score_thresh):
                    (left, right, top, bottom) = (boxes[0][1] * im_width, boxes[0][3] * im_width,
                                              boxes[0][0] * im_height, boxes[0][2] * im_height)
                    height = bottom - top;
                    width = right - left;
                    img_cropped = frame[int(top):int(top+height), int(left):int(left+width)]	
                    img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_RGB2BGR)			
                    image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()		
    
                    res, score = predict(image_data)
                    print(res)
                    print("score of label ",score)

                    #if(score >= 0.6 and res == "fist" ):
                    #    command_mode(mode_val)
                    command_mode(res, score, mode_val)

                    cv2.putText(frame, res, (int(left), int(top)-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5 , color, 2)

                    cv2.putText(frame, 'Accuracy: '+str("{0:.2f}".format(score)),
                        (int(left),int(top)-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

                    # cv2.putText(frame, '%s' % (res.upper()), (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
                    # cv2.putText(frame, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
                	
                # Draw bounding boxeses and text
                detector_utils.draw_box_on_image(
                    num_hands_detect, score_thresh, scores, boxes, classes, im_width, im_height, frame)

                cv2.imshow('Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    

                start = time.time()
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    vs.stop()
                    break
        except KeyboardInterrupt:
            pass#print("Average FPS: ", str("{0:.2f}".format(fps)))


def normal_mode(mode_val):
    # cv2.putText(frame,"in normal_mode mode",  (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
    # print("in normal mode")

    if(score >= 0.6 and res == "fist" and mode_val == 1):
        mode_val = 0
        command_mode( mode_val)


def command_mode(res, score, mode_val):
    # cv2.putText(frame,"in command mode",  (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
    # print("in command mode")
    
    if (score >= 0.6 and res == "three"):
        mode_val = 1
        normal_mode(mode_val)
    elif (score >= 0.6 and res == "fist" and mode_val != 1):
        print("rest of the functions")




if __name__ == '__main__':
    detect()
    predict()
