'''
This script assumes the directory structure and file format and conventions
from the COW-SL second language learner corpus of Spanish
developed at UC Davis: https://github.com/ucdaviscl/cowsl2h

The purpose of the script:
Combine COW-SL corpus files in to a single file, one sentence per line.

The program can be run as follows:
python3 script_name
parameter1_path_to_cowsl2h-master

The program assumes the existence of a subdirectory called output.
'''

import sys
import os
import glob
import nltk # NLP package; used here to split text into sentences

'''
Traverse d recursively, looking for folders named k.
Return the list of folders named k.
'''
def find_relevant_folders(d, k):
    folders = glob.glob(d + "**/**/" + k, recursive=True)
    return folders

'''
Save all texts from a list of folders in a list.
'''
def collect_all_sentences (relevant_folders):
    sentences = []

    for fol in relevant_folders:
        if fol.endswith('annotated'):
            issues = glob.glob(fol + '/**')
            for issue in issues:
                if issue.endswith('gender_number'):
                    for textfile in glob.glob(issue + '/**/*.txt'):# Iterate over all files with extension .txt in the directory named fol
                        file_name = os.path.basename(textfile)
                        with open(textfile, 'r') as f:
                            text = f.read()
                            sent_tokenized_text = nltk.sent_tokenize(text, language='spanish')  # Split text into sentences using the NLTK tokenizer
                        sentences.extend(sent_tokenized_text)
        else:
            files = glob.glob(fol + '/*.txt')
            for textfile in files: # Iterate over all files with extension .txt in the directory named fol
                with open(textfile, 'r') as f:
                    file_name = os.path.basename(textfile)
                    text = f.read()
                sent_tokenized_text = nltk.sent_tokenize(text, language='spanish') # Split text into sentences using the NLTK tokenizer
                sentences.extend(sent_tokenized_text) # Add the sentences to the list such that it is a flat list (not a list of list; compare to using "append" instead of "extend")

    return sentences


def output_string(id, sentence):
    output = str(id) + '@' + str(sentence['number']) + '@' + str(sentence['input']) + '\n'
    return output


if __name__ == "__main__":
    path_to_corpus = sys.argv[1]  # sys.argv[1] is the first argument passed to the program through e.g. pycharm (or command line). In Pycharm, look at Running Configuration
    '''
    Find folders named "essays" in the corpus.
    Sanity check report of relevant folders.
    '''
    print('Working with corpus {}'.format(path_to_corpus))
    essays = find_relevant_folders(path_to_corpus, "essays")
    print('Found {} folders named essays in the corpus.'.format(len(essays)))

    '''
    Save all sentences from all selected files in a single file.
    Sanity check report.
    '''
    print('Looking for sentences in essays.')
    raw_sentences = collect_all_sentences(essays)
    print('Total {} raw sentences.'.format(len(raw_sentences)))
    with open('output/COWSL2H_essays.txt', 'w') as f:
        for sentence in raw_sentences:
            f.write(sentence + '\n')

    """
    Find folders containing annotated essays in the corpus.
    Sanity check report of relevant folders.
    """
    annotated = find_relevant_folders(path_to_corpus, "annotated")
    print('Found {} folders named annotated in the corpus.'.format(len(annotated)))

    '''
    Combine all annotated files into one.
    Sanity check report.
    '''
    print('Compiling sentences from {} annotated folders.'.format(len(annotated)))
    annotated_sentences = collect_all_sentences(annotated)
    print('Total {} annotated sentences in the corpus.'.format(len(annotated_sentences)))
    with open('output/COWSL2H_annotated.txt', 'w') as f:
        for sentence in annotated_sentences:
            f.write(sentence + '\n')

    '''
    Find folders named "corrected" in the corpus.
    Sanity check report of relevant folders.
    '''
    corrected = find_relevant_folders(path_to_corpus, "corrected")
    print('Found {} folders named corrected in the corpus.'.format(len(corrected)))

    '''
    Combine all corrected files into one.
    Sanity check report.
    '''
    print('Looking for sentences in corrected.')
    corrected_sentences = collect_all_sentences(corrected)
    print('Total {} corrected sentences.'.format(len(corrected_sentences)))
    with open("output/COWSL2H_corrected.txt", 'w') as f:
        for sentence in corrected_sentences:
            f.write(sentence + '\n')
