import os
import sys
import random
import csv
import argparse
import shutil
from PIL import Image


def main():
    parser = argparse.ArgumentParser(
        "crops images listed in csv (original images are not modified)")
    parser.add_argument("images", help="path to directory containing images")
    parser.add_argument(
        "csv", help="path to csv file containing bounding boxes")
    parser.add_argument("-l", "--labels", nargs='+', type=str,
                        help="only crops images with specified labels")
    parser.add_argument("-o", "--out", help="name of output directory")
    args = parser.parse_args()

    if args.out:
        out = args.out
    else:
        out = "cropped"

    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)

    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)
        row_count = sum(1 for row in reader)

    # read csv file
    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')

        fields = next(reader, None)
        indexName = fields.index('name')
        indexClass = fields.index('classname')

        if args.labels:
            gen = (row for row in reader if row[indexClass] in args.labels)
        else:
            gen = (row for row in reader)

        print("cropping images (original images are not modified)")

        i = 0
        for row in gen:
            name, ext = row[indexName].split(".")
            im = Image.open(os.path.join(args.images, row[indexName]))
            (x, y, w, h) = (int(row[1]), int(row[2]), int(row[3]), int(row[4]))

            new_im = im.crop((x, y, x+w, y+h))  # crop
            new_name = os.path.join(out, row[indexName])

            if not os.path.isfile(new_name):
                new_im.save(new_name)
            else:
                new_im.save(os.path.join(
                    out, "%s_%d.%s" % (name, i, ext)))

            i += 1
            print("%d/%d" % (i, row_count), end="\r", flush=True)

        print("done")


if __name__ == "__main__":
    main()
