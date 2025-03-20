# CLIPSE (clip-based image search engine)
small image search engine using clip embeddings

## requirements

* python3 (3.12)
* uv 

## usage
Run uv to setup everyting

e.g. `uv run build_index.py --help` should result in:

```
usage: build_index.py [-h] [--index_folder INDEX_FOLDER] image_folder

create clip index

positional arguments:
  image_folder          images to be processed

options:
  -h, --help            show this help message and exit
  --index_folder INDEX_FOLDER
                        folder for storing the clip features/index (default:
                        index)

stg7 2025

```

## tools
All included tools should be run with `uv run`.

* `build_index.py`: create an index based on a folder with images (recommended to downscale the images, e.g. to 480x480)
* `query.py`: command line interface to perform queries to an created index
* `server.py`: web interface


**Important**: For full-resolution acces in the web-interface.
Independent of the input folder to create the index, the webserver expects the full-resolution images in the same substructure in the `full` directory.
E.g., your lower resolution image for indexing is `my-path/whateverpath/img.jpg` then the full-resolution variant will be expected to be stored in `full//whateverpath/img.jpg`.



## acknowledgments
If you use this software in your research, please include a link to the repository and reference one of the following paper.

```bibtex
@inproceedings{goering2025clipse,
  title={CLIPSE -- a minimalistic CLIP-based image search engine for research},
  author={Steve Göring}
}
```

If you like the software that I develop and contribute, you can [donate me a :coffee:](https://ko-fi.com/binarys3v3n).
 
Because :coffee: is a fundamental source for energy and motivation :smile:.
