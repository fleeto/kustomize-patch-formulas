#!/usr/bin/env python3
import argparse
from string import Template
import os
from shutil import copyfile



parser = argparse.ArgumentParser(description='Create patch')
parser.add_argument('-i', '--input', type=str, nargs='+', help='File list for input.', required=True)
parser.add_argument('-o', '--output', type=str, help='Path name for output.', required=True)

args = parser.parse_args()
filename_list = args.input
target_path = args.output

base = os.path.join(target_path, 'base')
overlay = os.path.join(target_path, 'overlay')
os.makedirs(base, exist_ok=True)
os.makedirs(overlay, exist_ok=True)

# copy files 

for file_name in filename_list:
    target_file = os.path.join(base, os.path.basename(file_name))
    copyfile(file_name, target_file)

with open(os.path.join(base, "kustomization.yaml"), "w") as fhandler:
    fhandler.write("resources:\n")
    for file_name in filename_list:
        fhandler.write( "".join(["  - ", os.path.basename(file_name), "\n"]))