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
Return a single string containing annotated texts from a text file.
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
Return a single string containing all texts from a list of folders.   
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
Return a single string containing all texts from a list of folders within a specific directory.
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
    target_folders = "essays"
    folders_to_find = "annotated"  # Second argument passed to the program
    folders_with_essays = find_relevant_folders(path_to_corpus, target_folders)
    relevant_folders = find_relevant_folders(path_to_corpus, folders_to_find)

    '''
    Use the function find_relevant_folders to find folders named "essays" in the corpus.
    Print the path to each folder.
    Print number of folders found.
    '''
    print('Working with corpus {}'.format(path_to_corpus))
    print('Found {} folders named {} in the corpus.'.format(len(folders_with_essays), target_folders))
    for fol in folders_with_essays:
        print(fol)

    '''
    Use the function get_raw_list with the files named "essays".
    Read into .txt files under "essays", use nltk to split text into a single list of sentences.
    Write each sentence from the list in a .txt file named "COWSL2h_essays".
    Print number of sentences in the list.
    '''
    print('Looking for sentences in {} folders.'.format(len(folders_with_essays)))
    raw_lst = get_raw_list(folders_with_essays)
    print('Total {} sentences in {} in the corpus.'.format(len(raw_lst), target_folders))
    with open('COWSL2H_' + target_folders.replace('/', '-') + '.txt','w') as f:
        for s in raw_lst:
            f.write(s + '\n')

    '''
    Use the function find_relevant_folders to find folders containing essays in the corpus.
    Print the path to each relevant folder.
    Print number of relevant folders found.  
    '''
    print('Looking for folders in {} folders.'.format(len(folders_to_find)))
    print('Found {} folders named {} in the corpus.'.format(len(relevant_folders), folders_to_find))
    for fol in relevant_folders:
        print(fol)

    '''
    Use the function get_sent_list with folders named "annotated".
    For each folder, find .txt files stored under "gender_number/**/".
    Read into each .txt file, use nltk to split text into a single list of sentences.
    Write each sentence from the list in a .txt file named "COWSL2H_annotated.txt".
    Print number of sentences written in the file.
    '''
    print('Compiling sentences from {} folders.'.format(len(relevant_folders)))
    sent_lst = get_sent_list(relevant_folders)
    print('Total {} sentences in {} in the corpus.'.format(len(sent_lst),folders_to_find))
    with open('COWSL2H_'+ folders_to_find.replace('/','-') + '.txt', 'w') as f:
        for s in sent_lst:
            f.write(s + '\n')

    '''
    Open a .txt file named "COWSL2H_gender_number.txt".
    Use the function collect_all_annotated to retrieve annotated sentences from COWSL2H_annotated.txt.
    Write retrieved sentences in the new .txt file.
    Print number of retrieved sentences written in the file.
    '''
    annotations = 'COWSL2H_annotated.txt'
    print('Looking for annotated sentences in {}'.format(annotations))
    relevant_sentences = collect_all_annotated(annotations)
    print('Total {} annotated sentences in {}.'.format(len(relevant_sentences),annotations))
    with open('COWSL2H_gender_number.txt', 'w') as f:
        for sentence in relevant_sentences:
            f.write(sentence)

