# DAIRE (Deep Archival Image Retrieval Engine)

DAIRE (Deep Archival Image Retrieval Engine) is an image exploration tool based on latent representations derived from neural networks, which allows scholars to "query" using an image of interest to rapidly find related images within a web archive.
More details can be found in our paper:

+ Tobi Adewoye, Xiao Han, Nick Ruest, Ian Milligan, Samantha Fritz, and Jimmy Lin. [Content-Based Exploration of Archival Images Using Neural Networks.](https://cs.uwaterloo.ca/~jimmylin/publications/Adewoye_etal_JCDL2020.pdf) _Proceedings of the 20th ACM/IEEE-CS Joint Conference on Digital Libraries (JCDL 2020)_, August 2020.

A live demo is available at [`http://daire.cs.uwaterloo.ca/`](http://daire.cs.uwaterloo.ca/), running on images from the "EnchantedForest" neighborhood of GeoCities.
This repo holds the code that runs that demo.

## Installation
If you haven't set up Archives Unleashed Toolkit, follow the instructions [here](https://aut.docs.archivesunleashed.org/docs/home).

Use the Toolkit to [extract image information](https://aut.docs.archivesunleashed.org/docs/aut-spark-submit-app#image-information) and place the parquet files in `data/images/`:
```sh
spark-submit --class io.archivesunleashed.app.CommandLineAppRunner path/to/aut-fatjar.jar --extractor ImageInformationExtractor --input /path/to/warcs/* --output /path/to/daire/data/images --output-format parquet
```

Use the Toolkit to [extract the image graph](https://aut.docs.archivesunleashed.org/docs/aut-spark-submit-app#image-graph) and place the parquet files in `data/imagegraph/`:
```sh
spark-submit --class io.archivesunleashed.app.CommandLineAppRunner path/to/aut-fatjar.jar --extractor ImageInformationExtractor --input /path/to/warcs/* --output /path/to/daire/data/imagegraph --output-format parquet
```

Install DAIRE dependencies:
```sh
pip install -r requirements.txt
```

## Preprocessing the Data

Set `save_image=True` in `script/extract-all-parquet-multi.py` ([configuration here](https://github.com/archivesunleashed/daire/blob/master/script/extract-all-parquets-multi.py#L27)):
```sh
python script/extract-all-parquets-multi.py
```
This will save the images to `img/` and generate `full_info.txt`, along with some intermediate files.

Generate the [HNSW index](https://github.com/nmslib/hnswlib):
```sh
python script/index-hnsw.py
```
The resulting index will be saved in `bin/<index_number>.bin` and `bin/<index_number>.txt`.

In future runs, you can load from an index as follows:
```sh
python script/index-hnsw.py <index_number>
```

## Running the App

The front-end is built with TypeScript and React. To make changes, follow the steps in the `ui/` directory [here](https://github.com/archivesunleashed/daire/blob/master/ui/README.md).

Finally, start up the Flask server:
```sh
python server.py
```

## Resources
**How I scale HNSW to larger magnitudes of images (10^6, 10^7, 10^8)?**
Discussion in in [this Github issue](https://github.com/nmslib/hnswlib/issues/81).
