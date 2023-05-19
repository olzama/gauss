'''
This script assumes the directory structure and file format and conventions
from the COW-SL second language learner corpus of Spanish
developed at UC Davis: https://github.com/ucdaviscl/cowsl2h

The purpose of the script:
Combine COW-SL corpus files in to a single file, one sentence per line.

The program can be run as follows:
python3 script_name
parameter1_path_to_cowsl2h-master
parameter2_essays
'''

import sys, os
import glob
import nltk # NLP package; used here to split text into sentences

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
    folders = glob.glob(d + "**/**/" + k, recursive=True)
    return folders


'''
Return a single string containing all texts from a list of folders.   
'''
def get_sent_list(relevant_folders):
    sentences = [] # Empty list
    for fol in relevant_folders:
        issues = glob.glob(fol + '/**')
        for issue in issues:
            if issue.endswith("gender_number"):
                for textfile in glob.glob(issue + '/**/*.txt'): # Iterate over all files with extention .txt in the directory named fol
                    with open(textfile, 'r') as f:
                        text = f.read()
                        sent_tokenized_text = nltk.sent_tokenize(text, language='spanish') # Split text into sentences using the NLTK tokenizer
                        sentences.extend(sent_tokenized_text) # Add the sentences to the list such that it is a flat list (not a list of list; compare to using "append" instead of "extend")
    return sentences


if __name__ == "__main__":
    path_to_corpus = sys.argv[1] # sys.argv[1] is the first argument passed to the program through e.g. pycharm (or command line). In Pycharm, look at Running Configuration
    print('Working with corpus {}'.format(path_to_corpus))
    folders_to_find = sys.argv[2] # Second argument passed to the program
    relevant_folders = find_relevant_folders(path_to_corpus, folders_to_find)
    for fol in relevant_folders:
        print(fol)
    print('Found {} folders named {} in the corpus.'.format(len(relevant_folders), folders_to_find))
    sent_lst = get_sent_list(relevant_folders)
    print('Total {} sentences in {} in the corpus.'.format(len(sent_lst),folders_to_find))
    with open('COWSL2H_'+ folders_to_find.replace('/','-') + '.txt', 'w') as f:
        for s in sent_lst:
            f.write(s + '\n')


