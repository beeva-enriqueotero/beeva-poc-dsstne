# beeva-poc-dsstne

## **adaptMovielensToNetCDF**
This script allows to adapt dataset from movielens to the passed to netcdfconverter from amazondsstne(Invoke the desired method in the main)
* It works with 100k dataset.
* It also works with 20M dataset. We built that one to validate the output was correct (diff <(head -n 6000 ml-20m) <(head -n 6000 ml20m-all))

## **exploreRecs**

Explores the recommendations produced by dsstne and parses into a format that we can pass to evaluate MAP
