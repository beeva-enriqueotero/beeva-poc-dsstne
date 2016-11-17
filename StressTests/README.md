# Amazon DSSTNE benchmarks

## Stress tests

#### Testbed

* Infrastructure: g2.2x
* Cost: 0.65$/h = 470$/month
* Algorithm: Autoencoder
* Dataset: Movielens 10M (subset u1)
* k = 10..30 recs
* n_samples = 1,10,50,100
* b = 50

#### Generate recommendations
```
cat ml10m-u1train.bak | head -n 1 > ml10m-u1train.head.1
time predict -b 50 -d gl -i features_input -o features_output -k 10 -n gl.nc -f "ml10m-u1train.bak" -s recs -r "ml10m-u1train.head.1"
```

#### Results:
| k | n_samples | batch size | Time to load model | Time to generate recommendations
| --- | -----------| ---- | --- | ---
| 10 | 69878 | 50 | 26.5s | 5.2s
| 10 | 69878 | 1024 | 26.9s | 3.7s
| 10 | 1 | 1024 | 2.31s | 0.036s
| 30 | 1 | 1 | 2.31s | 0.002s
| 30 | 1 | 1024 | 2.31s | 0.035s
| 10 | 10 | 1024 | 2.39s | 0.035s
| 30 | 10 | 1024 | 2.34s | 0.036s
| 10 | 10 | 10 | 2.30s | 0.003s
| 30 | 10 | 10 | 2.30s | 0.003s


#### Conclusions:
* Net time required to serve each recommendation is very low (< 4ms). But **time to load model is very high** (>2s).
* To serve recommendations online with a maximum latency of 0.3s `Predict.cpp` **source code should be modified** to pre-load the model.
* In best case after pre-loading the model a g2.2x instance (500$/month) could be enough to serve 100 requests/s
* Regarding elasticity, additional on demand or [spot](https://ec2price.com/?product=Linux/UNIX&type=g2.2xlarge&region=eu-west-1&window=60) g2.2x instances could be used to *scale up*. One g2.2x is the lower limit to *scale down*.
* But effort required to reimplement `Predict.cpp` to build an online recommender does not worth it. It's **easier to generate batch recommendations**. As shown with [Seldon integration](https://github.com/beeva-labs/beeva-poc-seldon/tree/master/recsys/external-recommender)
