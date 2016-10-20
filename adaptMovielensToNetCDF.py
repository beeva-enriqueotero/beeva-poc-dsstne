"""
Prepares data to go through the generatenetcdf amazon script
"""
import pandas as pd

def prepare_100k_dataset(path):
    dataset = pd.read_csv(path, delimiter= '\t', names = ['user_id', 'movie_id', 'rating', 'timestamp'])
    print len(dataset['user_id'].distinct())
if __name__ == '__main__':
    prepare_100k_dataset('u1.base')