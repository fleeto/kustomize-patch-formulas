#!/usr/bin/env python3
import argparse
from string import Template
import os
import shutil


parser = argparse.ArgumentParser(description='Create patch')
parser.add_argument('filename', type=str, help='A file name for patch template')
parser.add_argument('--set', type=str, nargs='*', help='--set name1=value1 name2=value2')
parser.add_argument('-t', '--target', type=str, help='Path name for output.', required=True)

args = parser.parse_args()
filename = args.filename
set_list = args.set
target_path = os.path.join(args.target, "overlay")

values_map = {}

if set_list is not None:
    for line in set_list:
        pair = line.split("=")
        values_map[pair[0]] = pair[1]

tmpl = ""

# read from template
with open(filename) as fhandler:
    content = "".join(fhandler)
    tmpl = Template(content)
    basename = os.path.basename(filename)
    shutil.copyfile(filename, os.path.join(target_path, basename))

target_yml = os.path.join(target_path, "kustomization.yaml")

if not os.path.exists(target_yml):
    with open(target_yml, "w") as fhandler:
        fhandler.write("bases:\n- ../base\npatchesStrategicMerge:\n" )

target_patch = os.path.join(target_path, os.path.basename(filename))
with open(target_patch, "w") as patch_handler:
    patch_handler.writelines(tmpl.substitute(values_map))
    with open(target_yml, "a") as fhandler:
        fhandler.write(" ".join(["  -", os.path.basename(target_patch), "\n"]))