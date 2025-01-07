#!/usr/bin/env python3
import argparse
import sys
import glob
import multiprocessing

import torch
from PIL import Image
import open_clip


class CLIP:
    def __init__(self):
        self.tokenizer = open_clip.get_tokenizer('ViT-B-32')
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
        self.model.eval()  # model in train mode by default, impacts some models with BatchNorm or stochastic depth active
        print(open_clip.list_pretrained())

    def parse_text(self, text):
        text = self.tokenizer([text])
        text_features = self.model.encode_text(text)

        text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features

    def calc_image_embedding_text_embedding_similarity(self, image_embedding, text_embedding):
        text_probs = (100.0 * image_embedding @ text_embedding.T).softmax(dim=-1)
        return text_probs

    def get_image_features(self, image_path):
        image = self.preprocess(Image.open(image_path)).unsqueeze(0)
        with torch.no_grad(), torch.cuda.amp.autocast():
            image_features = self.model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)

        return image_features


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='create clip index',
                                     epilog="stg7 2025",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("image_folder", type=str, help="images to be processed")
    parser.add_argument("--index_folder", type=str, default="index", help="folder for storing the clip features/index")
    parser.add_argument('--cpu_count', type=int, default=multiprocessing.cpu_count(), help='thread/cpu count')

    a = vars(parser.parse_args())
    pool = multiprocessing.Pool(a["cpu_count"])

    print("Hello from my-clipsearch!")
    clip = CLIP()
    print(res := clip.get_image_features("./imgs/-0_ww2ACIw8.jpg"))

    breakpoint()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
