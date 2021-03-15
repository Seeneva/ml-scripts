#!/bin/sh

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

# Path to tesstrain https://github.com/tesseract-ocr/tesstrain
TESSTRAIN_PATH=$1

if [ -z "${TESSTRAIN_PATH}" ]; then
    echo 'Use default tesstrain path'
    TESSTRAIN_PATH='./tesstrain'
fi

TESSTRAIN_PATH=$(realpath $TESSTRAIN_PATH)

MODEL_NAME='eng_seeneva'
START_MODEL='eng'
MAX_ITERATIONS=20000

DATA_SRC_PATH=$(realpath ./tesseract/$MODEL_NAME-ground-truth)
DATA_DST_PATH="$TESSTRAIN_PATH/data/$MODEL_NAME-ground-truth"
TESSDATA_PATH="$TESSTRAIN_PATH/data/tessdata"

# Copy all files into tesstrain data folder
mkdir -p $TESSTRAIN_PATH/data/{tessdata,$MODEL_NAME-ground-truth} &&
    cp $DATA_SRC_PATH/* "$DATA_DST_PATH" &&
    # Make all images gray
    magick mogrify -colorspace gray "$DATA_DST_PATH/*.png" &&
    # Download language
    make tesseract-langs -C $TESSTRAIN_PATH TESSDATA=$TESSDATA_PATH MODEL_NAME=$MODEL_NAME START_MODEL=$START_MODEL &&
    # Start training
    make training -C $TESSTRAIN_PATH TESSDATA=$TESSDATA_PATH MODEL_NAME=$MODEL_NAME START_MODEL=$START_MODEL PSM=13 MAX_ITERATIONS=$MAX_ITERATIONS
