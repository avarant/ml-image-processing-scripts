
import sys
import cv2
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN

if len(sys.argv) < 2:
    sys.exit()

####################

# def main():
#     faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     img = cv2.imread(sys.argv[1])
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     detections = faces.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=6)
#     print(detections)

####################


def main():
    detector = MTCNN()
    img = plt.imread(sys.argv[1])
    faces = detector.detect_faces(img)

    if faces:
        for face in faces:
            bounding_box = face['box']
            x = cv2.rectangle(img,
                              (bounding_box[0], bounding_box[1]),
                              (bounding_box[0]+bounding_box[2],
                                  bounding_box[1] + bounding_box[3]),
                              (0, 155, 255),
                              5)
            plt.imshow(x)
        # print(bounding_box)
        plt.show()


if __name__ == "__main__":
    main()
