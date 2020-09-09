import os
import sys
import random
import csv
import argparse
import shutil
from PIL import Image

parser = argparse.ArgumentParser("crops images specified in csv (original images are not modified)")
parser.add_argument("images", help="path to directory containing images")
parser.add_argument("csv", help="path to csv file")
# parser.add_argument("--classname", type=list,help="only crops entries with specified classname(s)")
args = parser.parse_args()

# labels = ["face_with_mask", "face_no_mask"]

dir_name = "data"
if os.path.isdir(dir_name) is False:
  os.makedirs(dir_name)

with open(args.csv) as fp:
  reader = csv.reader(fp, delimiter=",", quotechar='"')
  row_count = sum(1 for row in reader)

# read csv file
with open(args.csv) as fp:
  reader = csv.reader(fp, delimiter=",", quotechar='"')

  fields = next(reader, None)
  indexName = fields.index('name')
  # indexClass = fields.index('classname')

  i = 0
  for row in reader:
    # if row[indexClass] in labels:
    name, ext = row[indexName].split(".")
    im = Image.open(os.path.join(args.images, row[indexName]))
    (x, y, w, h) = (int(row[1]),int(row[2]),int(row[3]),int(row[4]))
    
    new_im = im.crop((x, y, x+w, y+h)) # crop
    new_name = os.path.join(dir_name, row[indexName])

    if not os.path.isfile(new_name):
      new_im.save(new_name)
    else:
      new_im.save(os.path.join(dir_name, "%s_%d.%s"%(name, i, ext)))

    i += 1
    print("%d/%d"%(i, row_count), end="\r", flush=True)


