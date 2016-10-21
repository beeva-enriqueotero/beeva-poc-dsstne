"""
Prepares data to go through the generatenetcdf amazon script
"""
import pandas as pd
import numpy as np
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

def recommendations(recs_path):
    """
    Analyze recommendations and prepare them to be measured
    :return:
    """
    with open(recs_path) as f:
        lines = f.readlines()
        parsed_elements = map(lambda s: re.sub(',[0-9.]+:',',', s.rstrip('\n')).rstrip(',:').split('\t'),lines)
        recomendations_length = map(lambda s: len(s[1].split(',')),parsed_elements)
        print "Total recommendations {}".format(len(parsed_elements))
        incomplete_rec = filter(lambda x: x!=10,recomendations_length)
        print "Number of incomplete recommendations {} ".format(len(incomplete_rec))
        return parsed_elements

if __name__ == '__main__':
    #prepare_100k_dataset('u1.base', 'ml100k-u1')
    #prepare_20m_dataset('ratings.csv', 'ml-20m')
    recommendations('recs')