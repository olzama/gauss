'''
This script assumes the directory structure and file format and conventions
from the COW-SL second language learner corpus of Spanish
developed at UC Davis: https://github.com/ucdaviscl/cowsl2h

The purpose of the script:
Combine COW-SL corpus files in to a single file, one sentence per line.
'''

import sys
from pathlib import Path


def collect_all_raw(d):
    pass

def collect_all_annotated(d):
    pass

def collect_per_course_level(d):
    pass

'''
Traverse d recursively, looking for folders named k.
Return a single string containing all texts from all k-named folders.   
'''
def find_relevant_folder(d, k):
    pass

if __name__ == "__main__":
    path_to_corpus = Path(sys.argv[1])
    for p in path_to_corpus.rglob("*"):
        print(p)
