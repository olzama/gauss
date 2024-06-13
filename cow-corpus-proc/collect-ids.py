import sys, glob
from delphin import itsdb, commands

if __name__ == '__main__':    # read a list of ids from the file:
    ids = []
    sentences = []
    for ts_path in sorted(glob.iglob(sys.argv[1] + '/**')):
        ts = itsdb.TestSuite(ts_path)
        # Retrieve the sentences with relevant ids:
        for i, row in enumerate(ts['item']):
            sentences.append({'sentence': row['i-input'], 'id': str(row['i-id'])})
    # Print out sentences and ids in tab-separated file: id\t sentence:
    with open(sys.argv[2], 'w') as f:
        for sentence in sentences:
            #f.write(sentence['id'] + '\t' + sentence['sentence'] + '\n')
            f.write(sentence['id'] + '\n')
