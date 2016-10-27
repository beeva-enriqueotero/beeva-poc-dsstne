# beeva-poc-DSSTNE

## Prepare the environment

This proof of concept has been developed by using an EC2 instance (g2.2xlarge).
Steps for AMI implementation detailed at the [repository](https://github.com/amznlabs/amazon-dsstne) of the aws-DSSTNE project have been followed.

It is important to note that, although the AMI it is offered, it is necessary
to download and compile cuDNN due to the fact that it is licensed to registered developers only.
In addition, within the AMI, the required dependencies are already downloaded but not compiled.


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
This script allows us to adapt dataset from movielens to the format passed to netcdfconverter from DSSTNE(Invoke the desired method in the main)
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

This method explores the recommendations produced by DSSTNE and parses them into a format that we can pass to evaluate MAP

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

[Previous work](https://github.com/beeva-labs/research-lab-private/blob/master/recsys/benchmark/RecommendationMetrics/MAPTest.py) has been reused for MAP testing.

Example of use:

```bash
python metrics.py formatted_rec ux.test
```

## Experiment

### Tests Autoencoder for Movielens 100K

It must be taken into account that AWS DSSTNE does not consider the rating feature at the training stage on the example
exposed by their developers at github. The timestamp of the interaction is used instead of the rating.

### Tests Autoencoder for Movielens 100K

Metric: MAP@10 (Mean Average Precission at 10)

Algorithm: Autoencoder

Dataset: Movielens 100K

DSSTNE Configuration: [config.json](https://github.com/beeva-carlosgonzalez/beeva-poc-dsstne/blob/master/100k_autoencoder_test/config.json)

Model validation: K-fold cross validation with k=5

#### Running script
For simplicity, you can use run_100k.sh script at the root of the project to generate all recomendation files for the k-folding
and write to files the MAP@10 results. It cleans everything but the MAP results once has finished.
```
#!/bin/sh

for i in 1 2 3 4 5
do
  echo 'adapting subset u'$i
  echo "movielens/100k/ml-100k/u$i.base"
  python adaptMovielensToNetCDF.py 100k "movielens/100k/ml-100k/u$i.base" -u $i
  generateNetCDF -d gl_input -i "ml100k-u$i" -o gl_input.nc -f features_input -s samples_input -c
  generateNetCDF -d gl_output -i "ml100k-u$i" -o gl_output.nc -f features_output -s samples_input -c
  train -c config.json -i gl_input.nc -o gl_output.nc -n gl.nc -b 256 -e 10
  predict -b 1024 -d gl -i features_input -o features_output -k 10 -n gl.nc -f "ml100k-u$i" -s recs -r "ml100k-u$i"
  echo "MAP for u"$i >> map10
  python exploreRecs.py recs --output u_formatted_recs.csv >> map10
  python metrics.py --threshold 3 u_formatted_recs.csv "movielens/100k/ml-100k/u$i.test" >> map10
  rm features_* gl* initial_network.nc ml100k-u* recs u.csv u_formatted_recs.csv
done


```

#### Results
| DSSTNE Version | DSSTNE Parameters | Test parameters | MAP@10 | Missing results
| --- | --- | -----------| ---- | --- | ---
|HEAD detached at [9f08739](https://github.com/amznlabs/amazon-dsstne/tree/9f08739b62b3d3f7c742e30f83c55b65aaf7920b) , Amazon DSSTNE (ami-d6f2e6bc)| p = 0.5, beta = 2.0 |threshold=0, k-fold=5|0.1369| 0%
|HEAD detached at [9f08739](https://github.com/amznlabs/amazon-dsstne/tree/9f08739b62b3d3f7c742e30f83c55b65aaf7920b) , Amazon DSSTNE (ami-d6f2e6bc)| p = 0.8, beta = 2.0 |threshold=0, k-fold=5|0.1431| 0%
|HEAD detached at [9f08739](https://github.com/amznlabs/amazon-dsstne/tree/9f08739b62b3d3f7c742e30f83c55b65aaf7920b) , Amazon DSSTNE (ami-d6f2e6bc)| p = 0.2, beta = 2.0 |threshold=0, k-fold=5|0.1386| 0%
|HEAD detached at [9f08739](https://github.com/amznlabs/amazon-dsstne/tree/9f08739b62b3d3f7c742e30f83c55b65aaf7920b) , Amazon DSSTNE (ami-d6f2e6bc)| p = 0.5, beta = 2.0 |threshold=3, k-fold=5|0.1202| 0%
|HEAD detached at [9f08739](https://github.com/amznlabs/amazon-dsstne/tree/9f08739b62b3d3f7c742e30f83c55b65aaf7920b) , Amazon DSSTNE (ami-d6f2e6bc)| p = 0.5, beta = 1.5 |threshold=3, k-fold=5|0.1211| 0%

##### Conclusions

- Amazon DSSTNE does not have good documentation.
- It works well on movielens but as a magic box.
- After have changed the training feature from timestamp to rating, the results went down notably. It is not clear if it is due to a missconfiguration or not, so that is the reason to not to include it as a result.

#### Future work

- Exhaustive tuning of the configurations offered by the library.
  - Using different features (e.g rating)
  - Modifying parameters at config.json
