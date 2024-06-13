import sys, glob
from delphin import itsdb, commands

if __name__ == '__main__':
    path_to_ids = '/home/olga/delphin/GAUSS/gauss-repo/data/dev-test/experiment/target/testset-ids'
    path_to_testsuites = '/home/olga/delphin/GAUSS/gauss-repo/cow-corpus-proc/output/by-length/tsdb/reconstructed_target'
    output_path = '/home/olga/delphin/GAUSS/gauss-repo/data/dev-test/experiment/target/tsdb/'
    relations = '/home/olga/delphin/GAUSS/gauss-repo/data/relations'
    # read a list of ids from the file:
    ids = []
    with open(path_to_ids, 'r') as f:
        for line in f:
            ids.append(line.strip())
    relevant_sentences = []
    for i, ts_path in enumerate(sorted(glob.iglob(path_to_testsuites + '/**'))):
        # ts = itsdb.TestSuite(ts_path)
        # # Retrieve the sentences with relevant ids:
        # for i, row in enumerate(ts['item']):
        #     if row['i-id'] in ids:
        #         relevant_sentences.append({'sentence': row['i-input'], 'id': row['i-id']})
        # Create a new tsdb profile:
        query = 'i-id = ' + ' or i-id = '.join([str(i) for i in ids])
        new_profile_name = ts_path.split('/')[-1]
        commands.mkprof(output_path + '/' + new_profile_name, source=ts_path, schema=relations, where=query, full=True)

