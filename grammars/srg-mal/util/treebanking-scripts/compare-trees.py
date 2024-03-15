import sys
from delphin import itsdb
import glob
import os

# Open a folder which contains two sets of treebanks. Store the processed items of each set in two dictionaries.
def prepare_treebanks(treebanks_path):
    old_treebanks = {}
    new_treebanks = {}
    ot_path = sorted(glob.iglob(treebanks_path + '/old/**'))
    nt_path = sorted(glob.iglob(treebanks_path + '/new/**'))
    for old_tsuite, new_tsuite in zip(ot_path, nt_path):
        old_folder = os.path.basename(old_tsuite)
        new_folder = os.path.basename(new_tsuite)
        old_ts = itsdb.TestSuite(old_tsuite)
        new_ts = itsdb.TestSuite(new_tsuite)
        old_treebanks[old_folder] = list(old_ts.processed_items())
        new_treebanks[new_folder] = list(new_ts.processed_items())
    # Iterate over two dictionaries comparing key names and number of items in each key.
    if old_treebanks.keys() == new_treebanks.keys():
        for (old_folder, old_items), (new_folder, new_items) in zip(old_treebanks.items(), new_treebanks.items()):
            if len(old_items) == len(new_items):
                print('Collecting parsed items from {}'.format(old_folder))
                old_parses = collect_parsed(old_items)
                new_parses = collect_parsed(new_items)
                for old_response, new_response in zip(old_parses, new_parses):
                    if old_response['i-id'] == new_response['i-id']:
                        orr = old_response['results']
                        nrr = new_response['results']
                        if len(orr) == len(nrr):
                            #Compare results of two lits of items and report the differences.
                            for o, n in zip(orr, nrr):
                                if o != n:
                                    print('Different results found for item {}'.format(o['parse-id']))

#Iterate over a list of dictionaries, storing them in a list if their attribute ['results'] is not empty.
def collect_parsed(items):
    parsed_items = []
    for response in items:
        if len(response['results']) > 0:
            parsed_items.append(response)
    return parsed_items

if __name__ == '__main__':
    prepare_treebanks(sys.argv[1])