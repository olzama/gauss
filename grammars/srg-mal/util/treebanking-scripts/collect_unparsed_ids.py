import os.path
import sys, glob
from delphin import itsdb

def collect_0results(treebanks_folder):
    unparsed_items = []
    path_to_items = sorted(glob.iglob(treebanks_folder + 'srg/**'))
    path_to_ids = sys.argv[2]
    for tsuite in path_to_items:
        ts = itsdb.TestSuite(tsuite)
        for response in ts.processed_items():
            if len(response['results']) == 0:
                unparsed_items.append(response)
        with open(treebanks_folder + '/unparsed_ids.txt', 'w') as f:
            for item in unparsed_items: # write each unparsed item's id in a text file
                f.write(str(item['i-id']) + '\n')


if __name__ == '__main__':
    path_to_treebanks = sys.argv[1] # path to a folder containing parsed testsuites
    collect_0results(path_to_treebanks)