import sys
import cv2
import os
import argparse
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# if len(sys.argv) < 2:
#     sys.exit()

parser = argparse.ArgumentParser(description="identifies faces and returns bounding boxes (output: face.csv)")
parser.add_argument("images", help="path to directory containing images")
args = parser.parse_args()

##############

# faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# img = cv2.imread(sys.argv[1])
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# detections = faces.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=6)
# print(detections)

##############

# detector = MTCNN()
# img = plt.imread(sys.argv[1])
# faces = detector.detect_faces(img)

# for face in faces:
#     bounding_box = face['box']
#     x=cv2.rectangle(img,
#         (bounding_box[0], bounding_box[1]),
#         (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
#         (0,155,255),
#         5)
#     plt.imshow(x)
# print(bounding_box)
# plt.show()

####################

detector = MTCNN()

path_to_images = args.images
images = [f for f in os.listdir(path_to_images) if os.path.isfile(os.path.join(path_to_images, f))]

f = open("faces.csv",'w')
f.write("name,x1,x2,y1,y2\n")

n = len(images)
i,j = 0,0
for img in images:
    im = plt.imread(os.path.join(path_to_images, img))
    faces = detector.detect_faces(im)

    for face in faces:
        bounding_box = face['box']
        f.write("%s,%d,%d,%d,%d\n"%(img, bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]))
        
        j += 1

    i += 1

    sys.stdout.write("\r%d/%d"%(i,n))
    sys.stdout.flush()

f.close()
print("\n%d files, %d faces"%(i,j))

####################
