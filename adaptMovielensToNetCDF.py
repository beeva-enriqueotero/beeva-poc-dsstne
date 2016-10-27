"""
Prepares data to go through the generatenetcdf amazon script
"""
import pandas as pd
import numpy as np
import sys

from tqdm import tqdm
import re

def prepare_100k_dataset(origin_path, dest_path):
    """
    Prepares 100k movielens dataset to be passed to netcdfconverter
    :param path: Path of the file to transform
    :param dest_path: Path of the output file
    :return:
    """
    dataset = pd.read_csv(origin_path, delimiter='\t', names = ['userId', 'movieId', 'rating', 'timestamp'])
    users = dataset['userId'].unique()
    f = open(dest_path, 'w+')
    for user in tqdm(np.nditer(users), total=users.shape[0]):
        user_line = str(user) + '\t'
        users_value = dataset[dataset['userId'].values == user]
        for row, value in users_value.iterrows():
            user_line += str(value['movieId']) + ',' + str(value['timestamp']) + ':'
        user_line = user_line.rstrip(':')
        f.write(user_line + '\n')
    f.close()

def prepare_20m_dataset(origin_path, dest_path):
    """
    Prepares 20M movielens dataset to be passed to netcdfconverter
    :param origin_path:
    :param dest_path:
    :return:
    """
    dataset = pd.read_csv(origin_path, delimiter=',')
    users = dataset['userId'].unique()
    f = open(dest_path, 'w+')
    for user in tqdm(np.nditer(users), total=users.shape[0]):
        user_line = str(user) + '\t'
        users_value = dataset[dataset['userId'].values == user]
        for row, value in users_value.iterrows():
            user_line += str(int(value['movieId'])) + ',' + str(int(value['timestamp'])) + ':'
        user_line = user_line.rstrip(':')
        f.write(user_line + '\n')
    f.close()

def prepare_10m_dataset(origin_path, dest_path):
    """
    Prepares 10M movielens dataset to be passed to netcdfconverter
    :param origin_path:
    :param dest_path:
    :return:
    """
    dataset = pd.read_csv(origin_path, delimiter='::', names = ['userId', 'movieId', 'rating', 'timestamp'])
    users = dataset['userId'].unique()
    f = open(dest_path, 'w+')
    for user in tqdm(np.nditer(users), total=users.shape[0]):
        user_line = str(user) + '\t'
        users_value = dataset[dataset['userId'].values == user]
        for row, value in users_value.iterrows():
            user_line += str(int(value['movieId'])) + ',' + str(int(value['timestamp'])) + ':'
        user_line = user_line.rstrip(':')
        f.write(user_line + '\n')
    f.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Usage: \n python adaptMovielensToNetCDF.py 100k \n python adaptMovielensToNetCDF.py 20m'
    elif sys.argv[1] == '100k':
        prepare_100k_dataset('u1.base', 'ml100k-u1')
    elif sys.argv[1] == '20m':
        prepare_20m_dataset('ratings.csv', 'ml-20m')
    elif sys.argv[1] == '10m':
        prepare_10m_dataset('r1.base', 'ml-10m')
    else:
        print 'Usage: \n python adaptMovielensToNetCDF.py 100k \n python adaptMovielensToNetCDF.py 20m \n python adaptMovielensToNetCDF.py 10m'
