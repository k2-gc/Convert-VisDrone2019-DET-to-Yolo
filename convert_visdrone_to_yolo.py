import argparse
from pathlib import Path

import cv2
from tqdm import tqdm

def create_path_object(dir_path):
    if not isinstance(dir_path, Path):
        dir_path = Path(dir_path)

    return dir_path


def convert_visdrone_to_yolo_format(
        annotation_dir_path: str,
        image_dir_path: str,
        out_dir_path: str,
):
    """Convert VisDrone 2019 annotation data format to Yolo annotation format.

    Args:
        annotation_dir_path (str): Path to directory that contains VisDrone annotation files.
        image_dir_path (str): Path to directory that contains VisDrone image files.
        out_dir_path (str): Path to directory in which converted yolo format annotation files will be outputted.

    Return:
        None
    """

    annotation_dir_path = create_path_object(annotation_dir_path)
    image_dir_path = create_path_object(image_dir_path)
    out_dir_path= create_path_object(out_dir_path)

    assert annotation_dir_path.exists(), f"Annotation Dir Not Found: '{annotation_dir_path.__str__()}'"
    assert image_dir_path.exists(), f"Image Dir Not Found: '{image_dir_path.__str__()}'"

    out_dir_path.mkdir(exist_ok=True, parents=True)

    txt_path_list = sorted(annotation_dir_path.glob("**/*txt"))

    original_label_to_new_label = {
        "0": 0,
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "10": 9,
        "11": 10,
    }

    ignore_label_list = [
        "0",
        # "1",
        # "2",
        # "3",
        # "4",
        # "5",
        # "6",
        # "7",
        # "8",
        # "9",
        # "10",
    ]

    for txt_path in tqdm(txt_path_list):
        basename = txt_path.name
        image_tmp_path = image_dir_path / basename
        image_path = image_tmp_path.with_suffix(".jpg")
        image = cv2.imread(image_path.__str__())
        image_height, image_width = image.shape[:2]

        with open(txt_path) as f:
            lines = f.read().split('\n')
        with open(out_dir_path / basename, "w") as f:
            for line in lines:
                if line == "":
                    continue
                split_line = line.split(',')
                label = split_line[5]
                if label in ignore_label_list:
                    continue
                bbox_left = int(split_line[0])
                bbox_top = int(split_line[1])
                bbox_width = int(split_line[2])
                bbox_height = int(split_line[3])
                bbox_center_x = bbox_left + int(bbox_width / 2)
                bbox_center_y = bbox_top + int(bbox_height / 2)
                relative_x = bbox_center_x / image_width
                relative_y = bbox_center_y / image_height
                relative_width = bbox_width / image_width
                relative_height = bbox_height / image_height
                print(f"{original_label_to_new_label[label]} {relative_x} {relative_y} {relative_width} {relative_height}", file=f)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotation-dir-path", type=str, default="./VisDrone2019-DET-val/annotations", help="Path to annotation dir")
    parser.add_argument("--image-dir-path", type=str, default="./VisDrone2019-DET-val/images", help="Path to image dir")
    parser.add_argument("--out-dir-path", type=str, default="./VisDrone2019-DET-val/yolo", help="Path to output dir")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_parser()
    convert_visdrone_to_yolo_format(
        args.annotation_dir_path,
        args.image_dir_path,
        args.out_dir_path,
    )