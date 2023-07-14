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

import sys
import glob
import nltk # NLP package; used here to split text into sentences

def collect_all_raw(d):
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
                for textfile in glob.glob(issue + '/**/*.txt'): # Iterate over all files with extension .txt in the directory named fol
                    with open(textfile, 'r') as f:
                        text = f.read()
                        sent_tokenized_text = nltk.sent_tokenize(text, language='spanish') # Split text into sentences using the NLTK tokenizer
                        sentences.extend(sent_tokenized_text) # Add the sentences to the list such that it is a flat list (not a list of list; compare to using "append" instead of "extend")
    return sentences

'''
Essays and metadata are lists of paths to folders.
Each path looks like this:
'/Users/olzama/Research/GAUSS/cowsl2h-master/terrible/F18/essays'
or: 
'/Users/olzama/Research/GAUSS/cowsl2h-master/terrible/F18/metadata'

This function, for each file under each essays path:
tokenizes the input using NLTK Spanish sentence tokenizer;
strips each sentence of initial and final hyphens and quotation marks;
puts sentences in a list;
creates the following metadata for each file:
1. the topic of the essay, which corresponds to the word "terrible" in the example above, so, the third parent folder name;
2. the semester name, e.g. F18, so, the second parent folder name;
3. IF a file with the exact  same name is found under the "metadata" folder path, include the entire text of the metadata file in a field called "metadata file".
Return a dictionary which contains the list of sentences from all files under all "essays" folders as well as all the additional data described above.
'''
def build_single_corpus(essays, metadata):
    pass

if __name__ == "__main__":
    path_to_corpus = sys.argv[1]  # sys.argv[1] is the first argument passed to the program through e.g. pycharm (or command line). In Pycharm, look at Running Configuration
    exclude_folders = 'csv'

    '''
    Find folders named "essays" in the corpus.
    Sanity check report of relevant folders.
    '''
    print('Working with corpus {}'.format(path_to_corpus))
    essays = find_relevant_folders(path_to_corpus, "essays")
    metadata = find_relevant_folders(path_to_corpus, "metadata")
    print('Found {} folders named essays in the corpus.'.format(len(essays)))

    sentences_with_metadata = bulid_single_corpus(essays, metadata)

    '''
    Save all sentences from all selected files in a single file.
    '''
    print('Looking for sentences in essays.')
    raw_lst = get_raw_list(essays)
    print('Total {} sentences.'.format(len(raw_lst)))
    with open('output/COWSL2H_essays.txt','w') as f:
        for s in raw_lst:
            f.write(s + '\n')

    '''
    Find folders containing annotated essays in the corpus.
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
    with open('output/COWSL2H_annotated.txt', 'w') as f:
        for s in sent_lst:
            f.write(s + '\n')

