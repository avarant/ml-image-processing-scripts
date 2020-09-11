import os
import sys
import random
import shutil
import argparse
import csv
from itertools import islice
from itertools import chain
from time import sleep

####################

# https://stackoverflow.com/questions/24527006/split-a-generator-into-chunks-without-pre-walking-it/24527424


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


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
    parser.add_argument(
        "csv", nargs='?', help="path to csv file containing labels")
    parser.add_argument("-l", "--labels", nargs='+', type=str,
                        help="creates a subfolder in train and valid for each label")
    parser.add_argument("-s", "--size", type=float,
                        help="train percentage (between 0 and 1)")
    args = parser.parse_args()

    if args.labels and not args.csv:
        print("must specify path to csv file")
        sys.exit()

    cwd = os.getcwd()
    out_dir = "out2"
    sub_dirs = ["train", "valid"]

    if args.size:
        train_size = args.size
    else:
        train_size = 0.8

    if not os.path.isdir(args.images):
        sys.exit()

    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)

    os.makedirs(out_dir)
    os.chdir(out_dir)

    for sub_dir in sub_dirs:
        os.makedirs(sub_dir)
        if args.labels:
            for lbl in args.labels:
                os.makedirs(sub_dir + "/" + lbl)

    os.chdir(cwd)

    if not args.labels:
        lst = os.listdir(args.images)
        n = len(lst)
        random.shuffle(lst)

        ntrain = int(train_size * n)
        train = lst[0:ntrain]
        valid = lst[ntrain:]

        copy(args.images, out_dir + "/train", train)
        copy(args.images, out_dir + "/valid", valid)
    else:
        with open(args.csv) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            fields = next(reader, None)
            indexClass = fields.index('classname')
            n = sum(1 for row in reader if row[indexClass] in args.labels)

        with open(args.csv) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')

            fields = next(reader, None)
            indexName = fields.index('name')
            indexClass = fields.index('classname')

            ntrain = int(train_size * n)

            i = 0
            for row in reader:
                label = row[indexClass]
                if label in args.labels:
                    name = row[indexName]
                    dest = "%s/%s/%s/%s" % (out_dir, "train" if i <
                                            ntrain else "valid", label, name)
                    shutil.copy(os.path.join(args.images, name), dest)
                    i += 1
                    print("%d/%d" % (i, n), end="\r", flush=True)

            print()


####################
if __name__ == "__main__":
    main()
