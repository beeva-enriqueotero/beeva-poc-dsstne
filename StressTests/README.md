# Amazon DSSTNE benchmarks

## Stress tests

#### Testbed

* Infrastructure: g2.2x
* Algorithm: Autoencoder
* Dataset: Movielens 10M (subset u1)
* k = 10..30 recs
* n_samples = 1,10,50,100
* b = 50

#### Generate recommendations
```
time predict -b 50 -d gl -i features_input -o features_output -k 10 -n gl.nc -f "ml10m-u1train.bak" -s recs -r "ml10m-u1train.bak"
```

#### Results:
| k | n_samples | batch size | Time to load model | Time to generate recommendations
| --- | -----------| ---- | --- | ---
| 10 | 69878 | 50 | 26.5s | 5.2s
| 10 | 69878 | 1024 | 26.9s | 3.7s
