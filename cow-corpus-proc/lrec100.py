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
def update_testsuite(ts, path_to_complete_testsuites, grammaticality_judgments):
    for i, row in enumerate(ts['item']):
        sentence_text = row['i-input']
        s, grammaticaly_judgment = grammaticality_judgments[i].split('\t')
        assert sentence_text == s
        punctuation = ['.', ',', '!', '?']
        sl = row['i-length'] + 1 if sentence_text[-1] in punctuation else row['i-length']
        meta_ts = itsdb.TestSuite(path_to_complete_testsuites + '/cow' + str(sl))
        relevant_item = find_relevant_item(meta_ts, sentence_text)
        if not relevant_item:
            print('Could not find item for sentence: ' + sentence_text)
            continue
        for field in row.keys():
            if field not in ['i-id','i-input', 'i-length']:
                if field != 'i-wf':
                    ts['item'].update(i, {field: relevant_item[field]})
                else:
                    ts['item'].update(i, {field: grammaticaly_judgment})
    ts.commit()



if __name__ == '__main__':
    path_to_ts = sys.argv[1]
    path_to_complete_testsuites = sys.argv[2]
    path_to_grammaticality_judgments = sys.argv[3]
    ts = itsdb.TestSuite(path_to_ts)
    with open(path_to_grammaticality_judgments, 'r') as f:
        sg_lines = [ ln.strip() for ln in f.readlines() ]
    update_testsuite(ts, path_to_complete_testsuites, sg_lines)