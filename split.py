import os
import sys
import shutil
import argparse
import csv


def main():
    parser = argparse.ArgumentParser(
        description="randomly samples files and splits into train and valid")
    parser.add_argument("images", help="path to directory containing files")
    parser.add_argument("csv", help="path to csv file containing labels")
    parser.add_argument("-l", "--labels", nargs='+', type=str,
                        help="only copies files with given labels")
    parser.add_argument("-s", "--size", type=float,
                        help="size of training set (between 0 and 1)")
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

    # create directories
    for sub_dir in sub_dirs:
        os.makedirs(sub_dir)
        if args.labels:
            for lbl in args.labels:
                os.makedirs(sub_dir + "/" + lbl)

    os.chdir(cwd)

    # get field names and csv length
    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        fields = next(reader, None)
        indexName = fields.index('name')
        indexClass = fields.index('classname')
        if args.labels:
            n = sum(1 for row in reader if row[indexClass] in args.labels)
        else:
            n = sum(1 for row in reader)
        ntrain = int(train_size * n)

    # read csv
    with open(args.csv) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')

        if args.labels:
            gen = (row for row in reader if row[indexClass] in args.labels)
        else:
            gen = (row for row in reader)

        # copy files
        i = 0
        for row in gen:
            name = row[indexName]
            label = row[indexClass]
            path = os.path.join(args.images, name)

            if os.path.isfile(path):
                dest = "%s/%s/%s" % (out, "train" if i <
                                     ntrain else "valid", label)
                if not os.path.isdir(dest):
                    os.mkdir(dest)

                shutil.copy(path, "%s/%s" % (dest, name))
                i += 1
                print("copying file %d/%d     " % (i, n), end="\r", flush=True)

        print()


if __name__ == "__main__":
    main()
