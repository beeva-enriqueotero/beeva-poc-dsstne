# beeva-poc-DSSTNE

## Prepare the environment

This proof of concept has been developed by using an EC2 instance (g2.2xlarge).
Steps for AMI implementation detailed at the [repository]('https://github.com/amznlabs/amazon-dsstne') of the aws-DSSTNE project have been followed.

It is important to know that, although the AMI it is offered, it is necessary
to download and compile cuDNN because of it is licensed to registered developers only.
In addition, within the AMI the required dependencies are already downloaded but not compiled.


Python dependencies
```bash
python --version
Python 2.7.12
pip install -r requirements.txt
```

Download movielens 100k and 20m datasets

```bash
wget http://files.grouplens.org/datasets/movielens/ml-100k.zip
wget http://files.grouplens.org/datasets/movielens/ml-20m.zip
```

## Data manipulation

### Data preprocess
Apply before use generateNetCDF utility.

#### adaptMovielensToNetCDF
This script allows to adapt dataset from movielens to the format passed to netcdfconverter from DSSTNE(Invoke the desired method in the main)
* It works with 100k dataset.
* It also works with 20M dataset. We built that one to validate the output was correct (diff <(head -n 6000 ml-20m) <(head -n 6000 ml20m-all))

Example of use:

```bash
python adaptMovielensToNetCDF.py 100k movielens/100k/u2.base -u 2
```
For further info
```bash
python adaptMovielensToNetCDF.py --help
```

### Data postprocess
Apply over DSSTNE's recommendation output

#### exploreRecs

Explores the recommendations produced by DSSTNE and parses them into a format that we can pass to evaluate MAP

Example of use:

```bash
python exploreRecs.py recs --output u2_formatted_recs.csv
```

For further info
```bash
python exploreRecs.py --help
```

## MAP Test

#### metrics.py

[Previous work]('https://github.com/beeva-labs/research-lab-private/blob/master/recsys/benchmark/RecommendationMetrics/MAPTest.py') has been reused for MAP testing.

Example of use:

```bash
python metrics.py formatted_rec ux.test
```
