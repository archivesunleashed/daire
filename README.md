# DAIRE


### Setup

#### Data 
Move the image parquet files to data/images/

Move the image graph parquet files to data/imagegraph/

Put all the images extract from the parquet files in images/

If you already have a HNSW index, put the .bin and .txt files in bin/

#### Running the Code
```sh
pip install -r requirements.txt
python script/extract-parquets.py # extract images to img/ & generate img/imgs.txt
python server.py
```
Visit [http://tuna.cs.uwaterloo.ca:5432/](http://tuna.cs.uwaterloo.ca:5432/)

### Scalability
[Large dataset with hnswlib](https://github.com/nmslib/hnswlib/issues/81)
