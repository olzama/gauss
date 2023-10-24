'''
For the LREC paper, we will create a test suite of 100 sentences from the COWSLH2 corpus.
The grammaticality judgments were done by Carlos Gomez.
'''

import sys
from delphin import itsdb


def find_relevant_item(ts, sentence_text):
    for item in ts.processed_items():
        if item['i-input'] == sentence_text:
            return item
    return None

'''
ts is the test suite to update with the information from the full corpus.
The full corpus consists of test suites by length.
A sentence of length 4, counting punctuation, will be inder the directory 4/.
'''
def update_testsuite(ts, grammaticality_judgments):
    for i, row in enumerate(ts['item']):
        sentence_text = row['i-input']
        s, grammaticaly_judgment = grammaticality_judgments[i].split('\t')
        assert sentence_text == s
        ts['item'].update(i, {'i-wf': grammaticaly_judgment})
    ts.commit()



if __name__ == '__main__':
    path_to_ts = sys.argv[1]
    path_to_grammaticality_judgments = sys.argv[2]
    ts = itsdb.TestSuite(path_to_ts)
    with open(path_to_grammaticality_judgments, 'r') as f:
        sg_lines = [ ln.strip() for ln in f.readlines() ]
    update_testsuite(ts, sg_lines)