import sys
from delphin import itsdb, derivation
import glob
import os

def compare_treebanks(srg_path, srgmal_path):
    identical = True
    srg_treebanks = {}
    srgmal_treebanks = {}
    srg_path = sorted(glob.iglob(srg_path + '/**'))
    mal_path = sorted(glob.iglob(srgmal_path + '/**'))
    for srg_tsuite, mal_tsuite in zip(srg_path, mal_path):
        add_to_dict(srg_treebanks, srg_tsuite)
        add_to_dict(srgmal_treebanks, mal_tsuite)
        # Iterate over two dictionaries comparing key names and number of items in each key.
        if srg_treebanks.keys() == srgmal_treebanks.keys():
            for (srg_folder, srg_items), (mal_folder, mal_items) in zip(srg_treebanks.items(), srgmal_treebanks.items()):
                if len(srg_items) == len(mal_items):
                    print('Collecting parsed items from {}.'.format(srg_folder))
                    srg_unparsed = collect_unparsed(srg_items)
                    mal_parsed = collect_parsed(mal_items)
                    # mal_unparsed = collect_unparsed(mal_items)
                    print('{} items do not get a parse from SRG.'.format(len(srg_unparsed)))
                    # for item in mal_unparsed:
                    #     print('No parses for item {} in either SRG or SRG-mal.'.format(item['i-id']))
                    # Given two lists of parsed items, compare the results of items with the same id.
                    for srg_response, mal_response in zip(srg_unparsed, mal_parsed):
                        srg_derivs = []
                        mal_derivs = []
                        if srg_response['i-id'] == mal_response['i-id']:
                            srg_results = srg_response['results']
                            mal_results = mal_response['results']
                            # if len(mal_results) == 0:
                            #     print('No parses for item {} in either SRG or SRG-mal.'.format(srg_response['i-id']))
                            if len(mal_results) > 0:
                                print('SRG-mal parsed item {}.'.format(mal_response['i-id']))
                            # for o, n in zip(srg_results, mal_results):
                            #     srg_deriv = derivation.from_string(o['derivation'])
                            #     mal_deriv = derivation.from_string(n['derivation'])
                            #     if srg_deriv not in srg_derivs:
                            #         srg_derivs.append(srg_deriv)
                            #     if mal_deriv not in mal_derivs:
                            #         mal_derivs.append(mal_deriv)

def add_to_dict(treebanks, tsuite):  # Process items of a tsuite and stores them in a dictionary.
    folder = os.path.basename(tsuite)
    if folder not in treebanks.keys():
        treebanks[folder] = []
    ts = itsdb.TestSuite(tsuite)
    treebanks[folder] = list(ts.processed_items())

def collect_parsed(items):
    parsed_items = []
    for response in items:
        if len(response['results']) > 0:
            parsed_items.append(response)
    return parsed_items

def collect_unparsed(items):
    unparsed_items = []
    for response in items:
        if len(response['results']) == 0:
            unparsed_items.append(response)
    return unparsed_items

if __name__ == '__main__':
    compare_treebanks(sys.argv[1], sys.argv[2])