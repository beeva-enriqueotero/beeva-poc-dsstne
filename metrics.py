"""
Metrics calculation for movielens at asw dsstne.
"""

import argparse
import json
import MAPTest as map_test
import pandas as pd


parser = argparse.ArgumentParser(description='Calculates MAP for the given recommendations')
parser.add_argument('recs', metavar='R', type=str, help='File with a list of dicts of the type {user:user_id, recommendations:rec_list}')
parser.add_argument('actions', metavar='A', type=str, help='File with a list of interactions')
parser.add_argument('--threshold', dest='threshold', default=0.0, type=float)
parser.add_argument('--at', dest='at', default=10)

args = parser.parse_args()

recs = None
with open(args.recs) as f:
    recs = json.loads(f.read())

actions = None
with open(args.actions) as f:
    actions = pd.read_csv(f, names=['user_id', 'item_id', 'value', 'timestamp'], sep='\t')

res = map_test.mean_average_precision(recommendations=recs, users=None, threshold=args.threshold, actions=actions, at=args.at)

print res
