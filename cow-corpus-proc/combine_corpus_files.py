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

def find_annotations(sentence):
    annotations = re.compile(r'(?P<annotation>\[(?P<original_word>\w+)]{(?P<target_word>\w+)}<(?P<issues>[\w+:]+)>)')
    annotated_sentence = re.search(annotations, sentence)
    return annotated_sentence

'''
Return a list containing annotated texts from a text file.
'''
def collect_all_annotated(d):
    annotated_sentences = []
    with open(d, 'r') as f:
        sentences = f.readlines()
        for sentence in sentences:
            annotations = find_annotations(sentence)
            if annotations != None:
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
Save anotated sentences from a list into a dictionary.
'''
def create_dictionary(sentence_list):
    dictionary = {}
    for i, sentence in enumerate(sentence_list):
        annotations = find_annotations(sentence)
        if annotations != None:
            dictionary[i] = sentence
            print("Sentence {}".format(i))
            print(sentence)
    return dictionary

'''
Break annotated sentences into parts.
'''
def break_sentence(sentence):
    annotations = re.compile(r'(?P<annotation>\[(?P<original_word>\w+)]{(?P<target_word>\w+)}<(?P<issues>[\w+:]+)>)')
    sentence_parts = annotations.split(sentence)
    return sentence_parts

'''
Returns two parallel sentences, one with the original word from the annotation and the other with the target word.
'''
def reconstruct_sentence(sentence, replacement):
    annotation = re.compile(r'(?P<annotation>\[(?P<original_word>\w+)]{(?P<target_word>\w+)}<(?P<issues>[\w+:]+)>)')
    reconstructed = annotation.sub(replacement, sentence)
    return reconstructed

if __name__ == "__main__":
    path_to_corpus = sys.argv[1]# sys.argv[1] is the first argument passed to the program through e.g. pycharm (or command line). In Pycharm, look at Running Configuration
    '''
    Use the function find_relevant_folders to find folders named "essays" in the corpus.
    Sanity check report of relevant folders.
    '''
    print('Working with corpus {}'.format(path_to_corpus))
    essays = find_relevant_folders(path_to_corpus, "essays")
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
    Find folders containing essays in the corpus.
    Sanity check report of relevant folders.  
    '''
    annotated = find_relevant_folders(path_to_corpus, "annotated")
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
    Select only annotated sentences and save them in a dictionary.
    Sanity check report.
    '''
    annotations = 'COWSL2H_annotated.txt'
    print('Looking for annotated sentences in {}'.format(annotations))
    relevant_sentences = collect_all_annotated(annotations)
    print('Total {} annotated sentences in {}.'.format(len(relevant_sentences), annotations))
    gen_num_dictionary = create_dictionary(sent_lst)


    '''
    Reconstruct original and target sentences from the dictionary of annotated sentences and save each version in parallel dictionaries.
    '''
    gen_num_original = {}
    gen_num_target = {}

    original = '\g<original_word>'
    target = '\g<target_word>'

    for key, value in gen_num_dictionary.items():
        gen_num_original[key] = reconstruct_sentence(value, original)
        gen_num_target[key] = reconstruct_sentence(value, target)

    '''
    Save dictionaries into .txt files.
    '''
    with open('COWSL2H_gender_number.txt', 'w') as f:
        for k, v in gen_num_dictionary.items():
            f.write("{} {}\n".format(k, v))

    with open('COWSL2H_original_gen_num.txt', 'w') as f:
        for k, v in gen_num_original.items():
            f.write("{} {}\n".format(k, v))

    with open('COWSL2H_target_gen_num.txt', 'w') as f:
        for k, v in gen_num_target.items():
            f.write("{} {}\n".format(k, v))