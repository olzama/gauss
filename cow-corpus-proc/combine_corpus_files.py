'''
This script assumes the directory structure and file format and conventions
from the COW-SL second language learner corpus of Spanish
developed at UC Davis: https://github.com/ucdaviscl/cowsl2h

The purpose of the script:
Combine COW-SL corpus files in to a single file, one sentence per line.
'''

import sys, os
import glob
import nltk

def collect_all_raw(d):
    pass

def collect_all_annotated(d):
    pass

def collect_per_course_level(d):
    pass

'''
Traverse d recursively, looking for folders named k.
Return the list of folders named k.
'''
def find_relevant_folders(d, k):
    return glob.glob(d + "**/**/" + k, recursive=True)


'''
Return a single string containing all texts from a list of folders.   
'''
def get_sent_list(relevant_folders):
    sentences = []
    for fol in relevant_folders:
        for textfile in glob.glob(fol + '/*.txt'):
            with open(textfile, 'r') as f:
                text = f.read()
            sent_tokenized_text = nltk.sent_tokenize(text, language='spanish')
            sentences.extend(sent_tokenized_text)
    return sentences


if __name__ == "__main__":
    path_to_corpus = sys.argv[1]
    print('Working with corpus {}'.format(path_to_corpus))
    folders_to_find = sys.argv[2]
    relevant_folders = find_relevant_folders(path_to_corpus, folders_to_find)
    print('Found {} folders named {} in the corpus.'.format(len(relevant_folders), folders_to_find))
    sent_lst = get_sent_list(relevant_folders)
    print('Total {} sentences in {} in the corpus.'.format(len(sent_lst),folders_to_find))
    with open('COWSL2H_'+ folders_to_find.replace('/','-') + '.txt', 'w') as f:
        for s in sent_lst:
            f.write(s + '\n')