'''
For the LREC paper, we will create a test suite of 100 sentences from the COWSLH2 corpus.
The grammaticality judgments were done by Carlos Gomez.
'''

import sys
from delphin import itsdb


'''
ts is the test suite to update with the information from the full corpus.
The full corpus consists of test suites by length.
A sentence of length 4, counting punctuation, will be inder the directory 4/.
'''
def update_testsuite(ts, grammaticality_judgments):
    for i, row in enumerate(ts['item']):
        sentence_text = row['i-input']
        try:
            s, grammaticaly_judgment = grammaticality_judgments[i].split('\t')[:2] #May also contain a comment in the last col
        except:
            print(5)
        if sentence_text != s:
            print(sentence_text)
            print(s)
        #assert sentence_text == s
        ts['item'].update(i, {'i-wf': grammaticaly_judgment})
    ts.commit()





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
    path_to_ts = sys.argv[1]
    path_to_grammaticality_judgments = sys.argv[2]
    ts = itsdb.TestSuite(path_to_ts)
    with open(path_to_grammaticality_judgments, 'r') as f:
        sg_lines = [ ln.strip() for ln in f.readlines() ]
    update_testsuite(ts, sg_lines)