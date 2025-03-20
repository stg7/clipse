#!/usr/bin/env python3
import argparse
import sys
import os
import glob
import json
#import multiprocessing

from tqdm import tqdm
import numpy as np
import pandas as pd
from rich import print

from clip_utils import CLIP


def load_index(index_file):
    print("load index :smiley:")
    if os.path.isfile(index_file + ".npz"):  # load npz
        data = np.load(index_file + ".npz")
        return data["images"], data["embeddings"]

    with open(index_file) as xfp:
        index = json.load(xfp)
    images = []
    embeddings = []
    for x in tqdm(index):
        images.append(x["image"])
        embeddings.append(np.array(x["features"]))

    embeddings = np.array(embeddings).reshape((len(images), -1))
    np.savez_compressed(index_file + ".npz", images=np.array(images), embeddings=embeddings)

    return images, embeddings


def query_index(index_file):

    images, embeddings = load_index(index_file)

    clip = CLIP()
    def do_query(query_text):
        if query_text == "" or not query_text:
            return
        query_embedding = clip.get_text_embedding(query_text)
        res = clip.calc_image_embeddings_text_embedding_similarity(embeddings, query_embedding)
        df = pd.DataFrame({"image": images, "similarity": res}).sort_values(by="similarity", ascending=False)
        return df
    return do_query


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='query clip index',
                                     epilog="stg7 2025",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--query", type=str, default=None, help="search query")
    parser.add_argument("--index_file", type=str, default="index/photos.json", help="index file to load")
    parser.add_argument("--interactive","-i", action="store_true", help="interactive interface")

    a = vars(parser.parse_args())
    do_query = query_index(a["index_file"])

    if a["query"]:
        df = do_query(a["query"])
        print(f"""top 10 matching images to {a["query"]}""")
        print(df.head(10))
        print("done")
        print(df.tail(10))

    if a["interactive"]:
        print("[bold blue]welcome[/bold blue] :smiley: to the interactive search (empty query to exit)")
        query = "."
        while query != "":
            print("[bold red]prompt>[/bold red] ", end="")
            query = input()
            if query != "":
                df = do_query(query)
                print(df.head(10))
                print(":thumbsup:")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
