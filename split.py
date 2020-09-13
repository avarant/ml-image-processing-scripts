import os
import sys
import random
import shutil
import argparse
import csv
from itertools import islice
from itertools import chain
from time import sleep


def copy(loc, dest, files):
    n = len(files)
    i = 0
    for file in files:
        shutil.copy(os.path.join(loc, file), os.path.join(dest, file))
        i += 1
        print("Moving file %d/%d     " % (i, n), end="\r", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="splits images into random partitions")
    parser.add_argument("images", help="path to directory containing images")
    parser.add_argument("csv", help="path to csv file containing labels")
    parser.add_argument("-l", "--labels", nargs='+', type=str,
                        help="creates a subfolder in train and valid for each label", required=True)
    parser.add_argument("-s", "--size", type=float,
                        help="train percentage (between 0 and 1)")
    parser.add_argument("-o", "--out", help="name of output directory")
    args = parser.parse_args()

    if not os.path.isdir(args.images):
        sys.exit()

    cwd = os.getcwd()
    sub_dirs = ["train", "valid"]

    if args.size:
        train_size = args.size
    else:
        train_size = 0.8

    if args.out:
        out = args.out
    else:
        out = "out"

    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)

    os.chdir(out)

    print("creating directories")
    for sub_dir in sub_dirs:
        os.makedirs(sub_dir)
        for lbl in args.labels:
            os.makedirs(sub_dir + "/" + lbl)

    os.chdir(cwd)

    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        fields = next(reader, None)
        indexName = fields.index('name')
        indexClass = fields.index('classname')
        n = sum(1 for row in reader if row[indexClass] in args.labels)
        ntrain = int(train_size * n)

    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')

        if args.labels:
            gen = (row for row in reader if row[indexClass] in args.labels)
        else:
            gen = (row for row in reader)

        print("copying files")

        i = 0
        for row in gen:
            name = row[indexName]
            label = row[indexClass]

            if os.path.isfile(os.path.join(args.images, name)):
                dest = "%s/%s/%s/%s" % (out, "train" if i <
                                        ntrain else "valid", label, name)
                shutil.copy(os.path.join(args.images, name), dest)
                i += 1
                print("%d/%d" % (i, n), end="\r", flush=True)

        print("\ndone")


if __name__ == "__main__":
    main()
