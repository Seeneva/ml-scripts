#!/usr/bin/env python3

# Copyright 2021 Sergei Solodovnikov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Script will split wide comic book pages into small pieces

import argparse
import os
from pathlib import Path

from PIL import Image

def split_img(src: Image.Image, src_path: Path, src_yolo_path: Path, step: float = 0.5):
    times = int(1 / step)

    for i in range(times):
        # Path to the destination image
        dst_path = src_path.parent / f"{src_path.stem}-{i}{src_path.suffix}"

        crop = (src.width * step * i, 0, src.width * step * (i+1), src.height)

        dst_w = crop[2]-crop[1]

        src.crop(crop).save(dst_path)

        if src_yolo_path.exists():
            dst_yolo_path = src_yolo_path.parent / f"{dst_path.stem}.txt"

            with open(src_yolo_path, 'r') as src_yolo:
                objects = [line.rstrip('\n').split(' ')
                           for line in src_yolo.readlines()]

            with open(dst_yolo_path, 'w') as dst_yolo:
                for obj, cx, cy, w, h in objects:
                    w = float(w) * times
                    cx = (float(cx) - step * i) * times

                    # Convert to pixels
                    w_p = w * dst_w
                    cx_p = cx * dst_w

                    # New left and right edge of the bounding box
                    lb = cx_p - w_p * 0.5
                    rb = cx_p + w_p * 0.5

                    # Do not save this bounding box if it is outside of the destination image
                    if lb < 0 or rb > dst_w:
                        continue

                    dst_yolo.write(f"{obj} {cx} {cy} {w} {h}\n")

def run(dataset_path: Path, dataset_wide_backup_path: Path):
    dataset_path = dataset_path.absolute()
    dataset_wide_backup_path = dataset_path.absolute()

    for img_path in dataset_path.glob('*.jpg'):
        with Image.open(img_path) as img:
            if img.width > img.height:
                img_yolo_path = dataset_path / f"{img_path.stem}.txt"

                # Calculate slit step. Some images should be splitted more than once
                split_img(img, img_path, img_yolo_path,
                        1 / (img.width // img.height + 1))

                print(f"{img_path} has been splitted")

                # Move src image and YOLO to backup folder
                dataset_wide_backup_path.mkdir(exist_ok=True)

                os.rename(img_path, dataset_wide_backup_path / img_path.name)

                if img_yolo_path.exists():
                    os.rename(img_yolo_path, dataset_wide_backup_path /
                            img_yolo_path.name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script will split wide comic book pages into small pieces')

    parser.add_argument('--dataset',
                        default='./yolo/dataset/',
                        help='Path to the YOLO dataset')
    
    parser.add_argument('--backup',
                        default='./yolo/data_wide_backup/',
                        help='Path to the backup directory')

    args = parser.parse_args()

    run(Path(args.dataset), Path(args.backup))
