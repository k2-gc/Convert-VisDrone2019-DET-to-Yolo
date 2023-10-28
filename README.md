# Convert tool from VisDrone format to Yolo format

## Introduction
This is tools for converting object detection annotation file format from VisDrone to Yolo.
Only support for VisDrone2019-DET. Could be used for VisDrone2018-DET.

## Prerequisites
* Python3
* opencv
* tqdm

### Linux or Mac
```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -U pip
$ pip install opencv-python tqdm
```

## Usage
```bash
$ python convert_visdrone_to_yolo.py --annotation-dir-path /PATH/TO/ANNOTATION_DIR --image-dir-path /PATH/TO/IMAGE_DIR --out-dir-path /PATH/TO/OUTPUT_DIR
```
Or just run command below if you use default path settings.
```bash
$ python convert_visdrone_to_yolo.py 
```