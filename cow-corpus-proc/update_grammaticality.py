'''
For the LREC paper, we will create a test suite of 100 sentences from the COWSLH2 corpus.
The grammaticality judgments were done by Carlos Gomez.
'''

import sys
from delphin import itsdb, commands


'''
ts is the test suite to update with the information from the full corpus.
The full corpus consists of test suites by length.
A sentence of length 4, counting punctuation, will be inder the directory 4/.
'''
def update_testsuite(ts, ts_target_path, grammaticality_judgments):
    for i, row in enumerate(ts['item']):
        sentence_text = row['i-input']
        id = row['i-id']
        q = '* from item' + ' where i-id = ' + str(id)
        selection = commands.select(q, ts_target_path)
        target_text = selection.data[0][6].strip()
        grammaticaly_judgment = grammaticality_judgments.get(target_text)
        if grammaticaly_judgment is None:
            print('No grammaticality judgment for: ' + target_text)
        ts['item'].update(i, {'i-wf': grammaticaly_judgment})
    ts.commit()


def read_judgments(path_to_grammaticality_judgments):
    js = {}
    with open(path_to_grammaticality_judgments, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            js[line[0].strip()] = line[1]
    return js


'''
python3 update_grammaticality.py path/to/tsdb/testsuite path/to/tab-separated/grammaticality/judgments/textfile

for example: 

Shakira es divertida.	1
Ella es rica.	1
Es muy buena.	1
Blake es mixto.	0
Es muy bonito.	1


python3 update_grammaticality.py output/by-length/tsdb/reconstructed_target/cow4 output/by-length/grammaticality/reconstructed_target/4.txt
'''
if __name__ == '__main__':
    path_to_ts = sys.argv[1] # The text of the sentence may slightly differ but we cannot at this point rely on the order
    path_to_ts2 = sys.argv[2] # this test suite will have the same sentences form as in the grammaticality judgments file
    path_to_grammaticality_judgments = sys.argv[3]
    ts = itsdb.TestSuite(path_to_ts)
    gjs = read_judgments(path_to_grammaticality_judgments)
    update_testsuite(ts, path_to_ts2, gjs)