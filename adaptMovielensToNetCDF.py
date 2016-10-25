__author__='carlos.gonzalez@beeva.com'

"""
Prepares data to go through the generatenetcdf amazon script
"""
import pandas as pd
import numpy as np
import argparse
import re

from tqdm import tqdm


parser = argparse.ArgumentParser(description='Prepares 100k/20m movielens dataset to be passed to NetCDFConverter')
parser.add_argument('dataset', metavar='D', type=str, help='Dataset to transform: 100k or 20m')
parser.add_argument('file', metavar='F', type=str, help='File containing dataset.')
parser.add_argument('-u', dest='folding', default=1, type=int, help='Index in the k-folding, Only used for the output filename')
args = parser.parse_args()

actions = dict()

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

actions['100k'] = prepare_100k_dataset
actions['20m'] = prepare_20m_dataset

if __name__ == '__main__':
    dest_path = 'ml%s-u%s' %(args.dataset, args.folding)
    actions[args.dataset](args.file, dest_path)
