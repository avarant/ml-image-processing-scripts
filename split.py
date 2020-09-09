import os
import sys
import random
import shutil


# create directories
dir_name = "data"
if os.path.isdir(dir_name) is False:
  os.makedirs(dir_name)
  os.makedirs(dir_name + '/train/mask')
  os.makedirs(dir_name + '/train/no-mask')
  os.makedirs(dir_name + '/valid/mask')
  os.makedirs(dir_name + '/valid/no-mask')
  os.makedirs(dir_name + '/test/mask')
  os.makedirs(dir_name + '/test/no-mask')
else:
  sys.exit()

move images
print("moving images")

def move(loc, dest, files):
  for file in files:
    shutil.move(os.path.join(loc, file), os.path.join(dest, file))
    print(file, end="\r", flush=True)

cwd = os.getcwd()

# mask
path = os.path.join(cwd, "data/train/mask")
dir_list = os.listdir(path)
n = len(dir_list)
random.shuffle(dir_list)

nvalid = int((pvalid / 100) * n)
new_path = os.path.join(cwd, "data/valid/mask")
move(path, new_path, dir_list[0:nvalid])

ntest = int((ptest / 100) * n)
new_path = os.path.join(cwd, "data/test/mask")
move(path, new_path, dir_list[nvalid:(nvalid+ntest)])

# no mask
path = os.path.join(cwd, "data/train/no-mask")
dir_list = os.listdir(path)
n = len(dir_list)
random.shuffle(dir_list)

nvalid = int((pvalid / 100) * n)
new_path = os.path.join(cwd, "data/valid/no-mask")
move(path, new_path, dir_list[0:nvalid])

ntest = int((ptest / 100) * n)
new_path = os.path.join(cwd, "data/test/no-mask")
move(path, new_path, dir_list[nvalid:(nvalid+ntest)])

