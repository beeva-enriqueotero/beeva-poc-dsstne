#!/bin/sh

for i in 1 2 3 4 5
do
  echo 'adapting subset u'$i
  echo ml10m-u$i\train
  python adaptMovielensToNetCDF.py 10m "~/movielens/10M/ml-10M100K/ml10m-u$itrain" -u $i
  generateNetCDF -d gl_input -i ml10m-u$i\train -o gl_input.nc -f features_input -s samples_input -c
  generateNetCDF -d gl_output -i ml10m-u$i\train -o gl_output.nc -f features_output -s samples_input -c
  train -c config.json -i gl_input.nc -o gl_output.nc -n gl.nc -b 256 -e 10
  predict -b 1024 -d gl -i features_input -o features_output -k 10 -n gl.nc -f ml10m-u$i\train -s recs -r ml10m-u$i\train
  echo "MAP for u"$i >> map10
  python exploreRecs.py recs --output u_formatted_recs.csv >> map10
  python metrics.py --threshold 0 u_formatted_recs.csv ~/movielens/10M/ml-10M100K/r$i.test >> map10
  rm features_* gl* initial_network.nc recs
done
