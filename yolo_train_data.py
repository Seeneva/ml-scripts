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

# Generate YOLO train data from provided dataset images

import argparse
import inspect
from pathlib import Path
from shutil import copy

from sklearn.model_selection import train_test_split


def generate_yolo_data(dataset_path: Path):
    dataset_path = dataset_path.absolute()

    cwd = Path.cwd()

    # Check if all images has YOLO txt files even if they are empty
    for img_path in dataset_path.glob('*.jpg'):
        yolo_txt_path = dataset_path / f"{img_path.stem}.txt"
        if not yolo_txt_path.exists():
            print(f"Create empty YOLO txt file: {yolo_txt_path.name}")
            yolo_txt_path.touch()

    train_file_path = dataset_path.parent / 'train.txt'
    test_file_path = dataset_path.parent / 'test.txt'

    obj_names_path = dataset_path.parent / 'obj.names'
    obj_data_path = dataset_path.parent / 'obj.data'

    def write_img_paths(file_path: Path, imgs):
        with open(file_path, 'w') as f:
            for img_path in imgs:
                f.write(f"{img_path.relative_to(cwd)}\n")

    train, test = train_test_split(
        list(dataset_path.glob('*.jpg')), train_size=0.85)

    write_img_paths(train_file_path, train)
    write_img_paths(test_file_path, test)

    copy(dataset_path / 'classes.txt', obj_names_path)

    with open(obj_names_path, 'r') as names_file:
        class_count = sum(1 for _ in names_file)

    obj_data_path.write_text(inspect.cleandoc(f"""classes = {class_count}
    train = {train_file_path.relative_to(cwd)}
    valid = {test_file_path.relative_to(cwd)}
    names = {obj_names_path.relative_to(cwd)}"""))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate YOLO train data')

    parser.add_argument('--dataset',
                        default='./yolo/dataset/',
                        help='Path to the YOLO dataset')

    args = parser.parse_args()

    generate_yolo_data(Path(args.dataset))
