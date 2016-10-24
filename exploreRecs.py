import re
import sys
import json
def recommendations(recs_path):
    """
    Analyze recommendations and prepare them to be measured
    :return:
    """
    with open(recs_path) as f:
        lines = f.readlines()
        parsed_elements = map(lambda s: re.sub(',[0-9.]+:',',', s.rstrip('\n')).rstrip(',:').split('\t'),lines)
        formatted_elements = map(lambda x: {'user':x[0], 'recommendation': x[1].split(',')}, parsed_elements)
        recomendations_length = map(lambda s: len(s[1].split(',')),parsed_elements)
        print "Total recommendations {}".format(len(parsed_elements))
        incomplete_rec = filter(lambda x: x!=10,recomendations_length)
        print "Number of incomplete recommendations {} ".format(len(incomplete_rec))
        return formatted_elements

if __name__ == '__main__':
    if len(sys.argv) == 2:
        info = recommendations(sys.argv[1])
        f = open(sys.argv[1] + 'parsed.csv', 'w+')
        f.write(json.dumps(info))
        f.close()
    else:
        print 'Usage: \npython exploreRecs.py pathfile'