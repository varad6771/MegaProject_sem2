import cv2
import os

import tensorflow as tf

from imutils.video import VideoStream
from utils import detector_utils as detector_utils

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def predict(image_data):
    predictions = sess.run(softmax_tensor,
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

# TODO (need to test)clicking q key does not work. the app stays in actions_invoke please check control flow


def detect():
    global sess
    global label_lines
    global softmax_tensor
    global res
    global score
    global frame
    global fist
    global two
    global three
    global four
    global five
    color = (0, 255, 0)
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("output_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    detection_graph, sessD = detector_utils.load_inference_graph()
    fist=0
    two=0
    three=0
    four=0
    five=0
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

                if im_height is None:
                    im_height, im_width = frame.shape[:2]

                # Convert image to rgb since opencv loads images in bgr, if not accuracy will decrease
                try:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                except:
                    print("Error converting to RGB")

                # Run image through tensorflow graph
                boxes, scores, classes = detector_utils.detect_objects(
                    frame, detection_graph, sessD)

                if scores[0] > score_thresh:
                    (left, right, top, bottom) = (boxes[0][1] * im_width, boxes[0][3] * im_width,
                                                  boxes[0][0] * im_height, boxes[0][2] * im_height)
                    height = bottom - top
                    width = right - left
                    img_cropped = frame[int(top):int(top + height), int(left):int(left + width)]
                    img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_RGB2BGR)
                    image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()

                    res, score = predict(image_data)
                    cv2.putText(frame, '%s' % (res.upper()), (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
                    cv2.putText(frame, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
                    #print(res)
                    #print("score of label ", score)

                    actions_invoke(res, score)        
                    
                    cv2.putText(frame, res, (int(left), int(top) - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    cv2.putText(frame, 'Accuracy: ' + str("{0:.2f}".format(score)),
                                (int(left), int(top) - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Draw bounding boxeses and text
                detector_utils.draw_box_on_image(
                    num_hands_detect, score_thresh, scores, boxes, classes, im_width, im_height, frame)

                cv2.imshow('Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    vs.stop()
                    break
        except KeyboardInterrupt:
            pass  # print("Average FPS: ", str("{0:.2f}".format(fps)))


def actions_invoke(res, score):
    global fist,two,three,four,five
    if score >= 0.6 and res == "fist": 
        fist=fist+1
        two=0
        three=0
        four=0
        five=0        
        print("{} fist".format(fist))
        if(fist==3):
            print("{} Invoked".format(app_pref1))
            os.startfile(app_pref1)
            fist=0
    elif score >= 0.6 and res == "two":
        two=two+1
        fist=0
        three=0
        four=0
        five=0
        print("{} two".format(two))
        if(two==3):
            print("{} invoked".format(app_pref2))
            os.startfile(app_pref2)
            two=0
    elif score >= 0.6 and res == "three":
        three=three+1
        fist=0
        two=0
        four=0
        five=0
        print("{} three".format(three))
        if(three==3):
            print("{} invoked".format(app_pref3))
            os.startfile(app_pref3)
            three=0
    elif score >= 0.6 and res == "four":
        four=four+1
        fist=0
        two=0
        three=0
        five=0
        print("{} four".format(four))
        if(four==3):
            print("{} invoked".format(app_pref4))
            os.startfile(app_pref4)
            four=0
    elif score >= 0.6 and res == "five":
        five=five+1
        fist=0
        two=0
        three=0
        four=0
        print("{} five".format(five))
        if(five==3):
            print("{} invoked".format(app_pref5))
            os.startfile(app_pref5)
            five=0


def get_user_prefs(pref1, pref2, pref3, pref4, pref5):
    print("in get_user_prefs")
    global app_pref1, app_pref2, app_pref3, app_pref4, app_pref5
    app_pref1 = pref1
    app_pref2 = pref2
    app_pref3 = pref3
    app_pref4 = pref4
    app_pref5 = pref5


def get_res_score():
    return res,score

# if __name__ == '__main__':
#     detect()
#     predict()

