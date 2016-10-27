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
  rm features_* gl* initial_network.nc ml100k-u* recs u.csv
done
