#!/usr/bin/env python3
import argparse
import sys
import os
import glob
import json

from tqdm import tqdm
from rich import print

from clip_utils import CLIP


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='create clipse index',
                                     epilog="stg7 2025",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("image_folder", type=str, help="images to be processed")
    parser.add_argument("--index_folder", type=str, default="index", help="folder for storing the clipse index")

    a = vars(parser.parse_args())

    os.makedirs(a["index_folder"], exist_ok=True)

    print(f"""calculate embeddings for folder {a["image_folder"]} """)
    clip = CLIP()
    images = list(glob.glob(os.path.join(a["image_folder"], "*")))
    print(f"""{len(images)} images to handle """)
    res = list(map(clip.get_image_features, tqdm(images)))
    imgfoldername = os.path.basename(os.path.normpath(a["image_folder"]))
    with open(os.path.join(a["index_folder"], imgfoldername + ".json"), "w") as xfp:
        json.dump(res, xfp)
    print("done :cat:")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
