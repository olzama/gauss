'''
This script is to iterate over pydelphin tsdb profiles and create a random dev-test split
'''

import sys
import glob
import random
from delphin import itsdb, commands

def get_sentences(path_to_profiles, test_ratio):
    sents = []
    profiles = {}
    for ts_path in glob.glob(path_to_profiles + '/*'):
        ts = itsdb.TestSuite(ts_path)
        profiles[ts_path] = ts
        for item in ts['item']:
            sents.append({'sent': item['i-input'], 'ts': ts_path, 'id': item['i-id']})
    random.shuffle(sents)
    split_index = int(len(sents) * test_ratio)
    return sents[:split_index], sents[split_index:], profiles

def split_ids(path_to_profiles, test_ratio):
    ids = []
    for ts_path in glob.glob(path_to_profiles + '/*'):
        ts = itsdb.TestSuite(ts_path)
        for item in ts['item']:
            ids.append(item['i-id'])
    random.shuffle(ids)
    split_index = int(len(ids) * test_ratio)
    return ids[:split_index], ids[split_index:]

def create_dev_test_split(path_to_profiles, output_dir, test_ratio, db_schema):
    # Split item ids into dev and test:
    dev_ids, test_ids = split_ids(path_to_profiles, test_ratio)
    # From a list of ids, create a query of the form: 'i-id = id1 or i-id = id2 or ...':
    dev_query = 'i-id = ' + ' or i-id = '.join([str(i) for i in dev_ids])
    test_query = 'i-id = ' + ' or i-id = '.join([str(i) for i in test_ids])
    for ts_path in glob.glob(path_to_profiles + '/*'):
        dev_profile_name = ts_path.split('/')[-1] + '_dev'
        commands.mkprof(output_dir + '/dev/' + dev_profile_name, source=ts_path, schema=db_schema, where=dev_query, full=True)
        test_profile_name = ts_path.split('/')[-1] + '_test'
        commands.mkprof(output_dir + '/test/' + test_profile_name, source=ts_path, schema=db_schema, where=test_query, full=True)



# def create_dev_test_split1(path_to_profiles, output_dir, test_ratio, db_schema):
#     # Split item ids into dev and test:
#     dev_ids, test_ids = split_ids(path_to_profiles, test_ratio)
#     # Create a temporary empty text file:
#     with open(output_dir + '/temp.txt', 'w') as f:
#         f.write('')
#     commands.mkprof(output_dir + '/dev/', source=output_dir + '/temp.txt', schema=db_schema)
#     commands.mkprof(output_dir + '/test/', source=output_dir + '/temp.txt', schema=db_schema)
#     dev_profile = itsdb.TestSuite(output_dir + '/dev/')
#     test_profile = itsdb.TestSuite(output_dir + '/test/')
#     for ts_path in glob.glob(path_to_profiles + '/*'):
#         ts = itsdb.TestSuite(ts_path)
#         for i,item in enumerate(ts['item']):
#             if item['i-id'] in dev_ids:
#                 copy_from_db(dev_profile, item, ts_path)
#             elif item['i-id'] in test_ids:
#                 copy_from_db(test_profile, item, ts_path)
#             else:
#                 print('Item in neither set.')
#     dev_profile.commit()
#     test_profile.commit()


# def copy_from_db(profile, item, ts_path):
#     profile['item'].append(item)
#     q_parse = '* from parse where i-id = ' + str(item['i-id'])
#     selection_parse = commands.select(q_parse, ts_path)
#     related_tables = ['run', 'decision', 'edge', 'preference', 'result', 'tree']
#     for sdp in selection_parse.data:
#         r = itsdb.Row(selection_parse.fields, sdp)
#         parse_id = r['parse-id']
#         profile['parse'].append(r)
#         for rt in related_tables:
#             q = '* from ' + rt + ' where parse-id = ' + str(parse_id)
#             selection = commands.select(q, ts_path)
#             for sd in selection.data:
#                 rs = itsdb.Row(selection.fields, sd)
#                 profile[rt].append(rs)

if __name__ == '__main__':
    path_to_profiles = sys.argv[1]
    output_dir = sys.argv[2]
    test_ratio = float(sys.argv[3])
    db_schema = sys.argv[4]
    create_dev_test_split(path_to_profiles, output_dir, test_ratio, db_schema)