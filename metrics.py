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

recs = pd.read_json(args.recs)
actions = pd.read_csv(args.actions, names=['user_id', 'item_id', 'value', 'timestamp'], sep=r'[\t:,]+', engine='python')

users_at_test = actions.user_id.unique()
recs_at_test = recs[recs['user'].isin(users_at_test)]
recs_at_test_json = json.loads(recs_at_test.to_json(orient='records'))

res = map_test.mean_average_precision(recommendations=recs_at_test_json, users=None, threshold=args.threshold, actions=actions, at=args.at)

print res
