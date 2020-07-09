# DAIRE


### Setup
Move all the parquet files to data/
```sh
python -m pip install -r requirements.txt
python script/extract-parquets.py # extract images to img/ & generate img/imgs.txt
python server.py
```
Visit [http://tuna.cs.uwaterloo.ca:5432/](http://tuna.cs.uwaterloo.ca:5432/)

### Scalability
[Large dataset with hnswlib](https://github.com/nmslib/hnswlib/issues/81)
