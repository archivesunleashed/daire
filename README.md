# DAIRE (Deep Archival Image Retrieval Engine)

DAIRE (Deep Archival Image Retrieval Engine) is an image exploration tool based on latent representations derived from neural networks, which allows scholars to "query" using an image of interest to rapidly find related images within a web archive.
More details can be found in our paper:

+ Tobi Adewoye, Xiao Han, Nick Ruest, Ian Milligan, Samantha Fritz, and Jimmy Lin. [Content-Based Exploration of Archival Images Using Neural Networks.](https://cs.uwaterloo.ca/~jimmylin/publications/Adewoye_etal_JCDL2020.pdf) _Proceedings of the 20th ACM/IEEE-CS Joint Conference on Digital Libraries (JCDL 2020)_, August 2020.

A live demo is available at [`http://daire.cs.uwaterloo.ca/`](http://daire.cs.uwaterloo.ca/), running on images from the "EnchantedForest" neighborhood of GeoCities.
This repo holds the code that runs that demo.

## Data 

Move the image parquet files to data/images/

Move the image graph parquet files to data/imagegraph/

Put all the images extract from the parquet files in images/

If you already have a HNSW index, put the .bin and .txt files in bin/

## Running the Code

```sh
pip install -r requirements.txt
python script/extract-parquets.py # extract images to img/ & generate img/imgs.txt
python server.py
```

## Scalability

[Large dataset with hnswlib](https://github.com/nmslib/hnswlib/issues/81)
