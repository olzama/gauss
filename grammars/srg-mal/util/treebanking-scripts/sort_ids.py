import sys, glob
from delphin import itsdb

'''
This script reads sorts items from a corpus of treebanks according to whether they got parses or not. For this purpose,
it reads into each item's ['results']. If its length 0, its ID is written into "unparsed_ids.txt"; if it's not,
it's written into "parsed_ids.txt".
'''

def collect_unparsed_ids(treebanks_folder):
    unparsed_items = []
    path_to_items = sorted(glob.iglob(treebanks_folder + '/mal/**'))
    for tsuite in path_to_items:
        ts = itsdb.TestSuite(tsuite)
        for response in ts.processed_items():
            if len(response['results']) == 0:
                unparsed_items.append(response)
    print('{} unparsed items.'.format(len(unparsed_items)))
    return unparsed_items

def collect_parsed_ids(treebanks_folder):
    parsed_items = []
    path_to_items = sorted(glob.iglob(treebanks_folder + '/mal/**'))
    for tsuite in path_to_items:
        ts = itsdb.TestSuite(tsuite)
        for response in ts.processed_items():
            if len(response['results']) != 0:
                parsed_items.append(response)
    print('{} parsed items.'.format(len(parsed_items)))
    return parsed_items

if __name__ == '__main__':
    path_to_treebanks = sys.argv[1] # path to a folder containing testsuites (for example, "path_to_testsuites/whatevertreebanks8")
    unparsed_items = collect_unparsed_ids(path_to_treebanks)
    with open(path_to_treebanks + '/unparsed_ids.txt', 'w') as f:
        for item in unparsed_items: # write each item's id in a text file
            f.write(str(item['i-id']) + '\n')

    parsed_items = collect_parsed_ids(path_to_treebanks)
    with open(path_to_treebanks + '/parsed_ids.txt', 'w') as f:
        for item in parsed_items:  # write each item's id in a text file
            f.write(str(item['i-id']) + '\n')
