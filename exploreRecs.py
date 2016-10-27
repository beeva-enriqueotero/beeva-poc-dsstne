__author__='carlos.gonzalez@beeva.com'
"""
Given a recommendation file obtained from aws dsstne, this script returns an array of dicts with
the form {user:user_id, recommendations:[,]} which is the format accepted by MAPTest script.
"""

import re
import json
import argparse

parser = argparse.ArgumentParser(description="""Given a recommendation file obtained from aws dsstne,
                                                this script returns an array of dicts with
                                                the form {user:user_id, recommendations:[,]}
                                                which is the format accepted by MAPTest script. """)

parser.add_argument('file', metavar='F', type=str, help='AWS DSSTNE Recommendation file')
parser.add_argument('--output', dest='output', type=str, default='formatted_rec.csv', help='Output filename')
args = parser.parse_args()

def recommendations(recs_path):
    """
    Analyze recommendations and prepare them to be measured
    :return:
    """
    with open(recs_path) as f:
        lines = f.readlines()
        parsed_elements = map(lambda s: re.sub(',[0-9.]+:',',', s.rstrip('\n')).rstrip(',:').split('\t'),lines)
        formatted_elements = map(lambda x: {'user':int(x[0]), 'recommendation': [int(a) for a in x[1].split(',')]}, parsed_elements)
        recomendations_length = map(lambda s: len(s[1].split(',')),parsed_elements)
        print "Total recommendations {}".format(len(parsed_elements))
        incomplete_rec = filter(lambda x: x!=10,recomendations_length)
        print "Number of incomplete recommendations {} ".format(len(incomplete_rec))
        return formatted_elements

def create_file():
    """
    Writes formatted recommendations to a file
    """
    info = recommendations(args.file)
    f = open(args.output, 'w+')
    f.write(json.dumps(info))
    f.close()


if __name__ == '__main__':
    create_file()
