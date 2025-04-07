#!/usr/bin/env -S uv run
import argparse
import sys
import os
import glob
import json

from tqdm import tqdm
import numpy as np
import pandas as pd
from rich import print

from clip_utils import CLIP


def transform_json_index(index_json):
    images = []
    embeddings = []
    for x in tqdm(index_json):
        images.append(x["image"])
        embeddings.append(np.array(x["features"]))
    return np.array(images), np.array(embeddings).reshape((len(images), -1))


def load_index(index_file, cache=True):
    cached_index = index_file + ".npz"
    index_size = os.stat(index_file).st_size
    if os.path.isfile(cached_index):
        npzfile = np.load(cached_index)
        images = npzfile["images"]
        embeddings = npzfile["embeddings"]
        # check if file size has been changed, if not all is fine
        if npzfile["index_size"] == index_size:
            return images, embeddings

    with open(index_file) as xfp:
        index = json.load(xfp)
    images, embeddings = transform_json_index(index)
    if cache:
        np.savez(
            index_file + ".npz",
            images=images,
            embeddings=embeddings,
            index_size=index_size
        )

    return images, embeddings


def query_index(index_file):

    print("load index :smiley:")
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
    parser = argparse.ArgumentParser(description='query clipse index',
                                     epilog="stg7 2025",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--query", type=str, default=None, help="search query")
    parser.add_argument("--index_file", type=str, default="index/test_images.json", help="index file to load")
    parser.add_argument("--interactive","-i", action="store_true", help="interactive interface")
    parser.add_argument('--num_results', type=int, default=10, help='number of results to be shown')

    a = vars(parser.parse_args())
    do_query = query_index(a["index_file"])

    if a["query"]:
        df = do_query(a["query"])
        print(f"""top 10 matching images to "{a["query"]}" """)
        print(df.head(a["num_results"]))
        print(df.head(a["num_results"]).to_json(index=False))
        print("done")

    if a["interactive"]:
        print("[bold blue]welcome[/bold blue] :smiley: to the interactive clipse search (empty query to exit)")
        query = "."
        while query != "":
            print("[bold red]prompt>[/bold red] ", end="")
            query = input()
            if query != "":
                df = do_query(query)
                print(df.head(a["num_results"]))
                print(":thumbsup:")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
