#!/usr/bin/env python3
import argparse
import sys
import os
import json

import torch
from PIL import Image
import open_clip
from tqdm import tqdm
from rich import print
import numpy as np
from matplotlib import pyplot as plt


class CLIP:
    def __init__(self):
        """
        possible other models (output of print(open_clip.list_pretrained()))
        [('RN50', 'openai'), ('RN50', 'yfcc15m'), ('RN50', 'cc12m'), ('RN101', 'openai'), ('RN101', 'yfcc15m'), ('RN50x4', 'openai'), ('RN50x16', 'openai'), ('RN50x64', 'openai'), ('ViT-B-32', 'openai'), ('ViT-B-32', 'laion400m_e31'), ('ViT-B-32', 'laion400m_e32'), ('ViT-B-32', 'laion2b_e16'), ('ViT-B-32', 'laion2b_s34b_b79k'), ('ViT-B-32', 'datacomp_xl_s13b_b90k'), ('ViT-B-32', 'datacomp_m_s128m_b4k'), ('ViT-B-32', 'commonpool_m_clip_s128m_b4k'), ('ViT-B-32', 'commonpool_m_laion_s128m_b4k'), ('ViT-B-32', 'commonpool_m_image_s128m_b4k'), ('ViT-B-32', 'commonpool_m_text_s128m_b4k'), ('ViT-B-32', 'commonpool_m_basic_s128m_b4k'), ('ViT-B-32', 'commonpool_m_s128m_b4k'), ('ViT-B-32', 'datacomp_s_s13m_b4k'), ('ViT-B-32', 'commonpool_s_clip_s13m_b4k'), ('ViT-B-32', 'commonpool_s_laion_s13m_b4k'), ('ViT-B-32', 'commonpool_s_image_s13m_b4k'), ('ViT-B-32', 'commonpool_s_text_s13m_b4k'), ('ViT-B-32', 'commonpool_s_basic_s13m_b4k'), ('ViT-B-32', 'commonpool_s_s13m_b4k'), ('ViT-B-32', 'metaclip_400m'), ('ViT-B-32', 'metaclip_fullcc'), ('ViT-B-32-256', 'datacomp_s34b_b86k'), ('ViT-B-16', 'openai'), ('ViT-B-16', 'laion400m_e31'), ('ViT-B-16', 'laion400m_e32'), ('ViT-B-16', 'laion2b_s34b_b88k'), ('ViT-B-16', 'datacomp_xl_s13b_b90k'), ('ViT-B-16', 'datacomp_l_s1b_b8k'), ('ViT-B-16', 'commonpool_l_clip_s1b_b8k'), ('ViT-B-16', 'commonpool_l_laion_s1b_b8k'), ('ViT-B-16', 'commonpool_l_image_s1b_b8k'), ('ViT-B-16', 'commonpool_l_text_s1b_b8k'), ('ViT-B-16', 'commonpool_l_basic_s1b_b8k'), ('ViT-B-16', 'commonpool_l_s1b_b8k'), ('ViT-B-16', 'dfn2b'), ('ViT-B-16', 'metaclip_400m'), ('ViT-B-16', 'metaclip_fullcc'), ('ViT-B-16-plus-240', 'laion400m_e31'), ('ViT-B-16-plus-240', 'laion400m_e32'), ('ViT-L-14', 'openai'), ('ViT-L-14', 'laion400m_e31'), ('ViT-L-14', 'laion400m_e32'), ('ViT-L-14', 'laion2b_s32b_b82k'), ('ViT-L-14', 'datacomp_xl_s13b_b90k'), ('ViT-L-14', 'commonpool_xl_clip_s13b_b90k'), ('ViT-L-14', 'commonpool_xl_laion_s13b_b90k'), ('ViT-L-14', 'commonpool_xl_s13b_b90k'), ('ViT-L-14', 'metaclip_400m'), ('ViT-L-14', 'metaclip_fullcc'), ('ViT-L-14', 'dfn2b'), ('ViT-L-14', 'dfn2b_s39b'), ('ViT-L-14-336', 'openai'), ('ViT-H-14', 'laion2b_s32b_b79k'), ('ViT-H-14', 'metaclip_fullcc'), ('ViT-H-14', 'metaclip_altogether'), ('ViT-H-14', 'dfn5b'), ('ViT-H-14-378', 'dfn5b'), ('ViT-g-14', 'laion2b_s12b_b42k'), ('ViT-g-14', 'laion2b_s34b_b88k'), ('ViT-bigG-14', 'laion2b_s39b_b160k'), ('ViT-bigG-14', 'metaclip_fullcc'), ('roberta-ViT-B-32', 'laion2b_s12b_b32k'), ('xlm-roberta-base-ViT-B-32', 'laion5b_s13b_b90k'), ('xlm-roberta-large-ViT-H-14', 'frozen_laion5b_s13b_b90k'), ('convnext_base', 'laion400m_s13b_b51k'), ('convnext_base_w', 'laion2b_s13b_b82k'), ('convnext_base_w', 'laion2b_s13b_b82k_augreg'), ('convnext_base_w', 'laion_aesthetic_s13b_b82k'), ('convnext_base_w_320', 'laion_aesthetic_s13b_b82k'), ('convnext_base_w_320', 'laion_aesthetic_s13b_b82k_augreg'), ('convnext_large_d', 'laion2b_s26b_b102k_augreg'), ('convnext_large_d_320', 'laion2b_s29b_b131k_ft'), ('convnext_large_d_320', 'laion2b_s29b_b131k_ft_soup'), ('convnext_xxlarge', 'laion2b_s34b_b82k_augreg'), ('convnext_xxlarge', 'laion2b_s34b_b82k_augreg_rewind'), ('convnext_xxlarge', 'laion2b_s34b_b82k_augreg_soup'), ('coca_ViT-B-32', 'laion2b_s13b_b90k'), ('coca_ViT-B-32', 'mscoco_finetuned_laion2b_s13b_b90k'), ('coca_ViT-L-14', 'laion2b_s13b_b90k'), ('coca_ViT-L-14', 'mscoco_finetuned_laion2b_s13b_b90k'), ('EVA01-g-14', 'laion400m_s11b_b41k'), ('EVA01-g-14-plus', 'merged2b_s11b_b114k'), ('EVA02-B-16', 'merged2b_s8b_b131k'), ('EVA02-L-14', 'merged2b_s4b_b131k'), ('EVA02-L-14-336', 'merged2b_s6b_b61k'), ('EVA02-E-14', 'laion2b_s4b_b115k'), ('EVA02-E-14-plus', 'laion2b_s9b_b144k'), ('ViT-B-16-SigLIP', 'webli'), ('ViT-B-16-SigLIP-256', 'webli'), ('ViT-B-16-SigLIP-i18n-256', 'webli'), ('ViT-B-16-SigLIP-384', 'webli'), ('ViT-B-16-SigLIP-512', 'webli'), ('ViT-L-16-SigLIP-256', 'webli'), ('ViT-L-16-SigLIP-384', 'webli'), ('ViT-SO400M-14-SigLIP', 'webli'), ('ViT-SO400M-16-SigLIP-i18n-256', 'webli'), ('ViT-SO400M-14-SigLIP-378', 'webli'), ('ViT-SO400M-14-SigLIP-384', 'webli'), ('ViT-L-14-CLIPA', 'datacomp1b'), ('ViT-L-14-CLIPA-336', 'datacomp1b'), ('ViT-H-14-CLIPA', 'datacomp1b'), ('ViT-H-14-CLIPA-336', 'laion2b'), ('ViT-H-14-CLIPA-336', 'datacomp1b'), ('ViT-bigG-14-CLIPA', 'datacomp1b'), ('ViT-bigG-14-CLIPA-336', 'datacomp1b'), ('nllb-clip-base', 'v1'), ('nllb-clip-large', 'v1'), ('nllb-clip-base-siglip', 'v1'), ('nllb-clip-base-siglip', 'mrl'), ('nllb-clip-large-siglip', 'v1'), ('nllb-clip-large-siglip', 'mrl'), ('MobileCLIP-S1', 'datacompdr'), ('MobileCLIP-S2', 'datacompdr'), ('MobileCLIP-B', 'datacompdr'), ('MobileCLIP-B', 'datacompdr_lt'), ('ViTamin-S', 'datacomp1b'), ('ViTamin-S-LTT', 'datacomp1b'), ('ViTamin-B', 'datacomp1b'), ('ViTamin-B-LTT', 'datacomp1b'), ('ViTamin-L', 'datacomp1b'), ('ViTamin-L-256', 'datacomp1b'), ('ViTamin-L-336', 'datacomp1b'), ('ViTamin-L-384', 'datacomp1b'), ('ViTamin-L2', 'datacomp1b'), ('ViTamin-L2-256', 'datacomp1b'), ('ViTamin-L2-336', 'datacomp1b'), ('ViTamin-L2-384', 'datacomp1b'), ('ViTamin-XL-256', 'datacomp1b'), ('ViTamin-XL-336', 'datacomp1b'), ('ViTamin-XL-384', 'datacomp1b'), ('RN50-quickgelu', 'openai'), ('RN50-quickgelu', 'yfcc15m'), ('RN50-quickgelu', 'cc12m'), ('RN101-quickgelu', 'openai'), ('RN101-quickgelu', 'yfcc15m'), ('RN50x4-quickgelu', 'openai'), ('RN50x16-quickgelu', 'openai'), ('RN50x64-quickgelu', 'openai'), ('ViT-B-32-quickgelu', 'openai'), ('ViT-B-32-quickgelu', 'laion400m_e31'), ('ViT-B-32-quickgelu', 'laion400m_e32'), ('ViT-B-32-quickgelu', 'metaclip_400m'), ('ViT-B-32-quickgelu', 'metaclip_fullcc'), ('ViT-B-16-quickgelu', 'openai'), ('ViT-B-16-quickgelu', 'dfn2b'), ('ViT-B-16-quickgelu', 'metaclip_400m'), ('ViT-B-16-quickgelu', 'metaclip_fullcc'), ('ViT-L-14-quickgelu', 'openai'), ('ViT-L-14-quickgelu', 'metaclip_400m'), ('ViT-L-14-quickgelu', 'metaclip_fullcc'), ('ViT-L-14-quickgelu', 'dfn2b'), ('ViT-L-14-336-quickgelu', 'openai'), ('ViT-H-14-quickgelu', 'metaclip_fullcc'), ('ViT-H-14-quickgelu', 'dfn5b'), ('ViT-H-14-378-quickgelu', 'dfn5b'), ('ViT-bigG-14-quickgelu', 'metaclip_fullcc')
        """
        self.tokenizer = open_clip.get_tokenizer('ViT-B-32')
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
        self.model.eval()

    def get_text_embedding(self, text):
        text = self.tokenizer([text])
        text_features = self.model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features

    def calc_image_embeddings_text_embedding_similarity(self, image_embeddings, text_embedding):
        sims = (100.0 * torch.tensor(image_embeddings, dtype=torch.float) @ text_embedding.T)
        return sims.flatten().tolist()

    def get_image_features(self, image_path):
        with Image.open(image_path) as img_data:
            image = self.preprocess(img_data).unsqueeze(0)
            with torch.no_grad():
                image_features = self.model.encode_image(image)
                image_features /= image_features.norm(dim=-1, keepdim=True)
        return {
            "features": image_features.tolist(),
            "image": image_path
        }



def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='extract clip embeddings from an image',
                                     epilog="stg7 2025",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("image", nargs="+", type=str, help="image to process")
    parser.add_argument("--embeddings_folder", type=str, default="embeddings", help="folder for storing the embeddings")

    a = vars(parser.parse_args())

    os.makedirs(a["embeddings_folder"], exist_ok=True)

    clip = CLIP()
    for image in tqdm(a["image"]):
        basename = os.path.splitext(os.path.basename(image))[0]
        res = clip.get_image_features(image)
        em = np.array(res["features"]).reshape((32, 16))
        plt.imshow(em)
        plt.savefig(f"""{a["embeddings_folder"]}/{basename}.pdf""", bbox_inches="tight")
        with open(f"""{a["embeddings_folder"]}/{basename}.json""", "w") as xfp:
            json.dump(res, xfp)

    print("done :cat:")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))