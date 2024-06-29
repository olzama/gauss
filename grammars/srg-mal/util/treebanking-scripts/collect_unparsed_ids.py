import os.path
import sys, glob
from delphin import itsdb

def collect_0results(treebanks_folder):
    path_to_items = sorted(glob.iglob(treebanks_folder + '/**'))
    path_to_ids = sys.argv[2]
    if not os.path.exists(path_to_ids):
        os.mkdir(path_to_ids)
    for tsuite in path_to_items:
        unparsed_items = []
        ts = itsdb.TestSuite(tsuite)
        ts_name = tsuite.split('/')[-1]
        for response in ts.processed_items():
            if len(response['results']) == 0:
                unparsed_items.append(response)
        with open(path_to_ids + '/' + ts_name + '.txt', 'w') as f:
            for item in unparsed_items: #write each unparsed item's id in a text file
                f.write(str(item['i-id']) + '\n')


if __name__ == '__main__':
    path_to_treebanks = sys.argv[1] # path to a folder containing parsed testsuites
    collect_0results(path_to_treebanks)