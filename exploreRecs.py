import re
import sys

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
    if len(sys.argv) == 2:
        recommendations(sys.argv[1])
    else:
        print 'Usage: \npython exploreRecs.py pathfile'