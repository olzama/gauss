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

def collect_all_sentences(relevant_folders):
    sentences = []
    dictionary = {}

    for fol in relevant_folders:
        if not fol.endswith("annotated"):
            textfiles = glob.glob(fol + '/*.txt')
        else:
            issues = glob.glob(fol + '/**')
            for issue in issues:
                if issue.endswith("gender_number"):
                    textfiles = glob.glob(issue + '/**/*.txt')
        for textfile in textfiles:
            file_name = os.path.basename(textfile)
            with open(textfile, 'r') as f:
                text = f.read()
            sent_tokenized_text = nltk.sent_tokenize(text, language='spanish')
            sentences.extend(sent_tokenized_text)
            dictionary[file_name] = {}
            for i, sentence in enumerate(sent_tokenized_text):
                dictionary[file_name][i] = sentence

    return dictionary

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
        for file, sentences in raw_sentences.items():
            for num, sen in sentences.items():
                f.write(str(file) + '@' + str(num) + '@' + str(sen) + '\n')

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
    # # print('Total {} annotated sentences in the corpus.'.format(len(annotated_sentences)))
    with open('output/COWSL2H_annotated.txt', 'w') as f:
        for file, sentences in annotated_sentences.items():
            for num, sen in sentences.items():
                f.write(str(file) + '@' + str(num) + '@' + str(sen) + '\n')

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
        for file, sentences in corrected_sentences.items():
            for num, sen in sentences.items():
                f.write(str(file) + '@' + str(num) + '@' + str(sen) + '\n')
