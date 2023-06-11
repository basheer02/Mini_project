# Import Libraries
import cv2
import numpy as np
import datetime

import mysql.connector

mydb = mysql.connector.connect(host = "localhost", username = "root", password = "", database = "example")

mycursor = mydb.cursor()

date_data = {
    'Mon' : 6,
    'Tue' : 5,
    'Wed' : 4,
    'Thu' : 3,
    'Fri' : 2,
    'Sat' : 1,
    'Sun' : 0
}

# The gender model architecture
# https://drive.google.com/open?id=1W_moLzMlGiELyPxWiYQJ9KFaXroQ_NFQ
GENDER_MODEL = 'deploy_gender.prototxt'
# The gender model pre-trained weights
# https://drive.google.com/open?id=1AW3WduLk1haTVAxHOkVS_BEzel1WXQHP
GENDER_PROTO = 'gender_net.caffemodel'
# Each Caffe Model impose the shape of the input image also image preprocessing is required like mean
# substraction to eliminate the effect of illunination changes
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
# Represent the gender classes
GENDER_LIST = ['Male', 'Female']
# https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
FACE_PROTO = "deploy.prototxt.txt"
# https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
FACE_MODEL = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
# The model architecture
# download from: https://drive.google.com/open?id=1kiusFljZc9QfcIYdU2s7xrtWHTraHwmW
AGE_MODEL = 'deploy_age.prototxt'
# The model pre-trained weights
# download from: https://drive.google.com/open?id=1kWv0AjxGSN0g31OeJa02eBGM0R_jcjIl
AGE_PROTO = 'age_net.caffemodel'
# Represent the 8 age classes of this CNN probability layer
AGE_INTERVALS = ['(0-3)', '(4-9)', '(10-15)', '(16-20)',
                 '(21-30)', '(31-40)', '(41-53)', '(55+)']
# Initialize frame size
frame_width = 1280
frame_height = 720
# load face Caffe model
face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
# Load age prediction model
age_net = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)
# Load gender prediction model
gender_net = cv2.dnn.readNetFromCaffe(GENDER_MODEL, GENDER_PROTO)

def get_faces(frame, confidence_threshold=0.5):
    # convert the frame into a blob to be ready for NN input
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
    # set the image as input to the NN
    face_net.setInput(blob)
    # perform inference and get predictions
    output = np.squeeze(face_net.forward())
    # initialize the result list
    faces = []
    # Loop over the faces detected
    for i in range(output.shape[0]):
        confidence = output[i, 2]
        if confidence > confidence_threshold:
            box = output[i, 3:7] * \
                np.array([frame.shape[1], frame.shape[0],
                         frame.shape[1], frame.shape[0]])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int_)
            # widen the box a little
            start_x, start_y, end_x, end_y = start_x - \
                10, start_y - 10, end_x + 10, end_y + 10
            start_x = 0 if start_x < 0 else start_x
            start_y = 0 if start_y < 0 else start_y
            end_x = 0 if end_x < 0 else end_x
            end_y = 0 if end_y < 0 else end_y
            # append to our list
            faces.append((start_x, start_y, end_x, end_y))
    return faces


# from: https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    # resize the image
    return cv2.resize(image, dim, interpolation = inter)


def get_gender_predictions(face_img):
    blob = cv2.dnn.blobFromImage(
        image=face_img, scalefactor=1.0, size=(227, 227),
        mean=MODEL_MEAN_VALUES, swapRB=False, crop=False
    )
    gender_net.setInput(blob)
    return gender_net.forward()


def get_age_predictions(face_img):
    blob = cv2.dnn.blobFromImage(
        image=face_img, scalefactor=1.0, size=(227, 227),
        mean=MODEL_MEAN_VALUES, swapRB=False
    )
    age_net.setInput(blob)
    return age_net.forward()



def predict_age_and_gender():
    """Predict the gender of the faces showing in the image"""
    a,b,c = 1,25,1
    lst = []
    # create a new cam object
    cap = cv2.VideoCapture(0)
    while True:
        _, img= cap.read()
        # Take a copy of the initial image and resize it
        frame = img.copy()
        # resize if higher than frame_width
        if frame.shape[1] > frame_width:
            frame = image_resize(frame, width=frame_width)
        # predict the faces
        faces = get_faces(frame)
        # Loop over the faces detected
        # for idx, face in enumerate(faces):
        for i, (start_x, start_y, end_x, end_y) in enumerate(faces):

            a += 1

            face_img = frame[start_y: end_y, start_x: end_x]
            # predict age
            age_preds = get_age_predictions(face_img)
            # predict gender
            gender_preds = get_gender_predictions(face_img)
            i = gender_preds[0].argmax()
            gender = GENDER_LIST[i]
            gender_confidence_score = gender_preds[0][i]
            i = age_preds[0].argmax()
            age = AGE_INTERVALS[i]
            age_confidence_score = age_preds[0][i]
            # Draw the box
            label = f"{gender}-{gender_confidence_score*100:.1f}%, {age}-{age_confidence_score*100:.1f}%"
            # label = "{}-{:.2f}%".format(gender, gender_confidence_score*100)
            #print(label)
            lst.append(age)
            if a == (b*c):
                print(f'Gender: {gender}')
                age = max(set(lst), key=lst.count)
                print(f'Age: {age[1:-1]} years')
                c += 1

                #set Date
                year, month, day = 2023,6,14
                today = datetime.date(year, month, day)
                cur_day = today.strftime("%a")
                day = int(today.strftime("%d")) + date_data[cur_day]                   
                month = int(today.strftime("%m"))
                year = today.strftime("%Y")

                if day > 30:
                    day = day % 10
                    month += 1

                date = year + '-' + str(month) + '-' + str(day)

                da = [date]

                k,flag = 1,1
                val = (gender,age[1:-1])
                mycursor.execute("select gender,age from gender_data where date = %s",da)
                result = mycursor.fetchall()

                for x in result:
                    if x == val:
                        sql = "update gender_data set count = count+1 where date = %s and gender = %s and age = %s"
                        v = [date,gender,age[1:-1]]
                        mycursor.execute(sql,v)
                        mydb.commit()
                        flag = 0

                if flag:
                    sql = "insert into gender_data(date,gender,age,count) values(%s,%s,%s,%s)"
                    val = (date,gender,age[1:-1],str(k))
                    mycursor.execute(sql,val)
                    mydb.commit()
                
                lst = []



            yPos = start_y - 15
            while yPos < 15:
                yPos += 15
            box_color = (255, 0, 0) if gender == "Male" else (147, 20, 255)
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), box_color, 2)
            # Label processed image
            cv2.putText(frame, label, (start_x, yPos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.54, box_color, 2)

            # Display processed image
        #cv2.imshow("Captured frame", frame)
        #cv2.waitKey(1000)
        cv2.imshow("live frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break
        # uncomment if you want to save the image
        # cv2.imwrite("output.jpg", frame)
        #time.sleep(5.0)
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    predict_age_and_gender()
