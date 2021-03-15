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

import argparse
import re
from pathlib import Path


def check(dataset: Path):
    print(f"Start checking tesseract data: {dataset}")

    # Check if all objects has related txt file
    for img_path in dataset.glob('*.png'):
        tesseract_txt_path = dataset / f"{img_path.stem}.gt.txt"

        if not tesseract_txt_path.exists():
            print(
                f"Provide Tesseract {tesseract_txt_path.name} file for object '{img_path.name}'")
            continue

        fixed_img_name = re.sub('[() ]', '_', img_path.name)

        if fixed_img_name != img_path.name:
            print(f"Rename invalid file name {img_path.name} to {fixed_img_name}")
            img_path = img_path.rename(dataset / fixed_img_name)
            tesseract_txt_path = tesseract_txt_path.rename(
                dataset / f"{img_path.stem}.gt.txt")

        # Check how many lines in each tesseract txt file
        with open(tesseract_txt_path, 'r') as txt:
            lines_count = sum(1 for _ in txt)

            if lines_count != 1:
                print(
                    f"'{tesseract_txt_path.name}' file contains wrong line numbers: {lines_count}. Should be 1!")

    print("Tesseract data checked.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check tesseract train data')

    parser.add_argument('--dataset',
                        default='./tesseract/eng_seeneva-ground-truth',
                        help='Tesseract train dataset')

    args = parser.parse_args()

    check(Path(args.dataset))