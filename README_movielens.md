## Movielens datasets
#### Movielens 10M
*How to generate repeatable partitions r1-r5 for 5 k-fold*


```
unzip ml-10m.zip
cd ml-10M100K
get_seeded_random()
{
  seed="$1"
  openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
    </dev/zero 2>/dev/null
}
cp ratings.dat ratings.dat.bak
shuf ratings.dat.bak --random-source=<(get_seeded_random 42) > ratings.dat
./split_ratings.sh
```
