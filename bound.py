import sys
import os
import argparse

##############

# def main():
#     faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     img = cv2.imread(sys.argv[1])
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     detections = faces.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=6)
#     print(detections)

##############

# def main():
#     detector = MTCNN()
#     img = plt.imread(sys.argv[1])
#     faces = detector.detect_faces(img)

#     for face in faces:
#         bounding_box = face['box']
#         x=cv2.rectangle(img,
#             (bounding_box[0], bounding_box[1]),
#             (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
#             (0,155,255),
#             5)
#         plt.imshow(x)
#     print(bounding_box)
#     plt.show()

####################


def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    parser = argparse.ArgumentParser(
        description="identifies faces and returns bounding boxes as csv")
    parser.add_argument("images", help="path to directory containing images")
    args = parser.parse_args()

    import cv2
    import matplotlib.pyplot as plt
    from mtcnn.mtcnn import MTCNN

    detector = MTCNN()

    images = [f for f in os.listdir(args.images) if os.path.isfile(
        os.path.join(args.images, f))]

    out = "faces.csv"
    f = open(out, 'w')
    f.write("name,x1,x2,y1,y2\n")

    n = len(images)
    i, j = 0, 0
    for img in images:
        im = plt.imread(os.path.join(args.images, img))
        faces = detector.detect_faces(im)

        for face in faces:
            bounding_box = face['box']
            f.write("%s,%d,%d,%d,%d\n" % (
                img, bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]))

            j += 1

        i += 1

        print("%d/%d" % (i, n), end="\r", flush=True)

    f.close()
    print("\n%d files, %d faces" % (i, j))
    print(out)

####################


if __name__ == "__main__":
    main()
