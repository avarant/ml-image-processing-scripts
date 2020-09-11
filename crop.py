import os
import sys
import random
import csv
import argparse
import shutil
from PIL import Image

####################


def main():
    parser = argparse.ArgumentParser(
        "crops images specified in csv (original images are not modified)")
    parser.add_argument("images", help="path to directory containing images")
    parser.add_argument(
        "csv", help="path to csv file containing bounding boxes")
    args = parser.parse_args()

    out_dir = "out"
    if os.path.isdir(out_dir):
      shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)
        row_count = sum(1 for row in reader)

    # read csv file
    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')

        fields = next(reader, None)
        indexName = fields.index('name')

        i = 0
        for row in reader:
            name, ext = row[indexName].split(".")
            im = Image.open(os.path.join(args.images, row[indexName]))
            (x, y, w, h) = (int(row[1]), int(row[2]), int(row[3]), int(row[4]))

            new_im = im.crop((x, y, x+w, y+h))  # crop
            new_name = os.path.join(out_dir, row[indexName])

            if not os.path.isfile(new_name):
                new_im.save(new_name)
            else:
                new_im.save(os.path.join(
                    out_dir, "%s_%d.%s" % (name, i, ext)))

            i += 1
            print("%d/%d" % (i, row_count), end="\r", flush=True)

        print()

####################


if __name__ == "__main__":
    main()
