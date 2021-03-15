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
from pathlib import Path


def run(dataset_path: Path):
    for img_path in dataset_path.absolute().glob('*.png'):
        txt_path = Path.cwd() / f"{img_path.stem}.gt.txt"
        txt_path.touch(exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create empty *.gt.txt for each image inside Tesseract dataset directory')

    parser.add_argument('--dataset',
                        default='./tesseract/eng_seeneva-ground-truth',
                        help='Tesseract train dataset')

    args = parser.parse_args()

    run(Path(args.dataset))
