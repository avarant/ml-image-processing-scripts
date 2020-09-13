import sys
import os
import argparse


def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    parser = argparse.ArgumentParser(
        description="identifies faces and returns bounding boxes as csv")
    parser.add_argument("images", help="path to directory containing images")
    parser.add_argument("-o", "--out", help="name of output .csv file")
    args = parser.parse_args()

    import cv2
    import matplotlib.pyplot as plt
    from mtcnn.mtcnn import MTCNN

    detector = MTCNN()

    images = [f for f in os.listdir(args.images) if os.path.isfile(
        os.path.join(args.images, f))]

    if args.out:
        out = args.out
    else:
        out = "faces.csv"

    f = open(out, 'w')
    f.write("name,x1,x2,y1,y2\n")

    print("scanning images for faces")

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


if __name__ == "__main__":
    main()
