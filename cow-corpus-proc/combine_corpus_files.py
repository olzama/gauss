'''
This script assumes the directory structure and file format and conventions
from the COW-SL second language learner corpus of Spanish
developed at UC Davis: https://github.com/ucdaviscl/cowsl2h

The purpose of the script:
Combine COW-SL corpus files in to a single file, one sentence per line.

The program can be run as follows:
python3 script_name
parameter1_path_to_cowsl2h-master
'''

import sys, os
import glob
import nltk # NLP package; used here to split text into sentences
import re

def collect_all_raw(d):
    pass

'''
Return a list containing annotated texts from a text file.
'''
def collect_all_annotated(d):
    annotated_sentences = []
    with open(d, 'r') as f:
        sentences = f.readlines()
        for sentence in sentences:
            if re.search("[\[\]{}<>]", sentence):
                annotated_sentences.append(sentence)
    return annotated_sentences

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
Return a list containing all texts from a list of folders.   
'''
def get_raw_list(relevant_folders):
    sentences = []
    for fol in relevant_folders:
        for textfile in glob.glob(fol + '/*.txt'):
            with open(textfile, 'r') as f:
                text = f.read()
            sent_tokenized_text = nltk.sent_tokenize(text, language='spanish')
            sentences.extend(sent_tokenized_text)
    return sentences

'''
Return a list containing all texts from a list of folders within a specific directory.
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

'''
Find desired folders in the corpus.
'''
def relevant_folders (f):
    path_to_corpus = sys.argv[1]# sys.argv[1] is the first argument passed to the program through e.g. pycharm (or command line). In Pycharm, look at Running Configuration
    folders = find_relevant_folders(path_to_corpus, f)
    return folders

if __name__ == "__main__":
    '''
    Use the function find_relevant_folders to find folders named "essays" in the corpus.
    Sanity check report of relevant folders.
    '''
    print('Working with corpus {}'.format(path_to_corpus))
    essays = relevant_folders("essays")
    print('Found {} folders named essays in the corpus.'.format(len(essays)))

    '''
    Save all sentences from all selected files in a single file.
    '''
    print('Looking for sentences in essays.')
    raw_lst = get_raw_list(essays)
    print('Total {} sentences.'.format(len(raw_lst)))
    with open('COWSL2H_essays.txt','w') as f:
        for s in raw_lst:
            f.write(s + '\n')

    '''
    Use the function find_relevant_folders to find folders containing essays in the corpus.
    Sanity check report of relevant folders.  
    '''
    annotated = relevant_folders("annotated")
    print('Found {} folders named annotated in the corpus.'.format(len(annotated)))

    '''
    Combine all annotated files into one.
    Sanity check report.
    '''
    print('Compiling sentences from annotated folders.'.format(len(annotated)))
    sent_lst = get_sent_list(annotated)
    print('Total {} sentences in the corpus.'.format(len(sent_lst)))
    with open('COWSL2H_annotated.txt', 'w') as f:
        for s in sent_lst:
            f.write(s + '\n')

    '''
    Select only annotated sentences and save them in a file.
    Sanity check report.
    '''
    annotations = 'COWSL2H_annotated.txt'
    print('Looking for annotated sentences in {}'.format(annotations))
    relevant_sentences = collect_all_annotated(annotations)
    print('Total {} annotated sentences in {}.'.format(len(relevant_sentences),annotations))
    with open('COWSL2H_gender_number.txt', 'w') as f:
        for sentence in relevant_sentences:
            f.write(sentence)

