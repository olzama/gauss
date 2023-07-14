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
import re

'''
Traverse d recursively, looking for folders named k.
Return the list of folders named k.
'''
def find_relevant_folders(d, k):
    folders = glob.glob(d + "**/**/" + k, recursive=True)
    return folders

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
def build_single_corpus(corpus_path, essays, metadata, annotated):
    essays_with_metadata = []
    folder_id = 0
    for fol in essays:
        folder_id += 1
        topic = fol.split('/')[-3]
        semester = fol.split('/')[-2]
        # The annotated folders have additional structure:
        # There will be a subfolder called "gender_number", and below that there will be one or more
        # folders named "annotator1", "annotator2", etc.
        # We need to descend into each "annotator" folder and collect the sentences from there.
        # We will keep the annotator name in the metadata under an "annotator" field.
        # "gender_number" will be the "error" field.
        if annotated:
            path = fol + '/gender_number/**/*.txt'
        else:
            path = fol + '/*.txt'
            annotator = None
        essay_id = 0
        for textfile in glob.glob(path):
            essay_id += 1
            subcorpus = {'filename': '', 'sentences': {}, 'reconstructed_learner':{},'reconstructed_target':{},
                         'topic': '', 'semester': '', 'metadata_file': ''}
            subcorpus['filename'] = textfile.split('/')[-1]
            subcorpus['topic'] = topic
            subcorpus['semester'] = semester
            if annotated:
                subcorpus['error'] = 'gender_and_number'
                annotator = textfile.split('/')[-2]
            # Find a folder in the metadata list of folders that has the same semester and topic:
            fill_metadata(corpus_path, metadata, semester, subcorpus, textfile,
                          topic,annotated, annotator)
            process_essay_text(annotated, essay_id, folder_id, subcorpus, textfile)
            essays_with_metadata.append(subcorpus)
    return essays_with_metadata


def process_essay_text(annotated, essay_id, folder_id, subcorpus, textfile):
    with open(textfile, 'r') as f:
        text = f.read()
        sent_tokenized_text = nltk.sent_tokenize(text, language='spanish')
        sent_id = 0
        for sent in sent_tokenized_text:
            sent_id += 1
            include = False
            sent = sent.strip('-"')
            unique_id = str(folder_id) + '_' + str(essay_id) + '_' + str(sent_id)
            assert unique_id not in subcorpus['sentences'] and unique_id not in subcorpus['reconstructed_learner'] \
                   and unique_id not in subcorpus['reconstructed_target']
            if annotated:
                annotations = find_annotations(sent)
                if annotations:
                    include = True
            if not annotated or include:
                subcorpus['sentences'][unique_id] = sent
                if annotated and include:
                    reconstructed_learner = reconstruct_sentence(sent, '\g<original_word>')
                    reconstructed_target = reconstruct_sentence(sent, '\g<target_word>')
                    subcorpus['reconstructed_learner'][unique_id] = reconstructed_learner
                    subcorpus['reconstructed_target'][unique_id] = reconstructed_target


def fill_metadata(corpus_path, metadata, semester, subcorpus, textfile, topic, annotated, annotator=None):
    # capitalize the first letter of the topic because this is how it appears in the metadata subdirectories:
    camel_topic = topic[0].upper() + topic[1:]
    metafol = corpus_path + '/' + topic + '/' + semester + '/' + 'metadata'
    if metafol in metadata:
        # The file ID is the part of the textfile name before the semester and the topic:
        file_id = textfile.split('/')[-1].split('.')[0]
        corresponding_file = corpus_path + '/' + topic + '/' + semester + '/' + 'metadata/' + file_id + '.' + semester + '.metadata.txt'
        alt_corr_file = corpus_path + '/' + topic + '/' + semester + '/' + 'metadata/' + file_id + '.' + semester + '_' + camel_topic + '.metadata.txt'
        if (corresponding_file in glob.glob(metafol + '/*.txt')) \
                or (alt_corr_file in glob.glob(metafol + '/*.txt')):
            metafile = corresponding_file if corresponding_file in glob.glob(metafol + '/*.txt') else alt_corr_file
            with open(metafile, 'r') as f:
                meta = f.read()
                meta_data = extract_metadata(meta, semester)
                if annotated:
                    meta_data['annotator'] = annotator
                subcorpus['metadata_file'] = meta_data
        else:
            print("No metadata file found for {}".format(textfile))

#TODO: bug: inspect sentence 1_1_10
def reconstruct_sentence(sentence, replacement):
    annotation = re.compile('(\[(?P<original_word>\w+)]{(?P<target_word>\w+)})*<(?P<issues>[\w+:]+)>')
    reconstructed = annotation.sub(replacement, sentence)
    return reconstructed

def extract_metadata(meta, semester):
    '''
                        Metadata files consist of the following data items separated by "|||".
                        For semesters other than S21 and W21:
                            1) Course enrolled
                            2) Age
                            3) Gender
                            4) L1 language
                            5) Other L1 language(s)
                            6) Language(s) spoken at home
                            7) Language(s) studied
                            8) listening comprehension *
                            9) reading comprehension *
                            10) speaking ability **
                            11) writing ability **
                            12) Have you ever lived in a Spanish-speaking country?
                        '''
    meta = meta.split('|||')
    if semester not in ['S21', 'W21']:
        meta_data = {'course': meta[0], 'age': meta[1], 'gender': meta[2], 'l1': meta[3],
                     'other_l1': meta[4], 'home_lang': meta[5], 'studied_lang': meta[6],
                     'listening': meta[7], 'reading': meta[8], 'speaking': meta[9],
                     'writing': meta[10], 'lived_in_spanish_country': meta[11]}
    else:
        '''
        For semesters S21 and W21:
            1) Course enrolled
            2) Age
            3) Gender
            4) How many years of Spanish courses had you taken before arriving to UC Davis?
            5) What was the first Spanish course you took at UC Davis? 
            6) How many previous Spanish upper division courses have you been enrolled in?
            7) Which language(s) do you consider to be your mother tongue(s)?
            8) Did you grow up in a Spanish-speaking household?
            9) How many languages can you communicate in (including your mother tongue)?
            10) Have you ever spent more than 1 month in a Spanish-speaking country?
            11) Where did you attend elementary school?
            12) Where did you attend High School?
            13) Did you ever attend a bilingual (Spanish-English) school during K-12?
            14) On a normal day, how much exposure (radio, papers, movies, people talking to you, etc.) to the Spanish language do you get outside of your Spanish language class?
            15) Why do you study Spanish?
            16) I feel [1] understanding my instructor when they speak Spanish in class.
            17) feel [2] understanding a Spanish-speaking movie without subtitles.
            18) feel [3] understanding the readings in the Spanish textbook or other classroom materials.
            19) feel [4] understanding a newspaper article in Spanish.
            20) feel [5] speaking Spanish in class.
            21) feel [6] speaking Spanish outside of class.
            22) feel [7] writing assignments for my Spanish course.
            23) feel [8] writing a blog post in Spanish. 
            24) [1]  that I will get a good grade for my current Spanish course.
            25) I feel [2] about my current Spanish class. 
            26) I feel that my Spanish course is [3].
        '''
        meta_data = {'course': meta[0], 'age': meta[1], 'gender': meta[2], 'l1': meta[6],
                 'other_l1': meta[6], 'home_lang': 'N/A', 'studied_lang': meta[8],
                 'listening': meta[16], 'reading': meta[18], 'speaking': meta[20],
                 'writing': meta[22], 'lived_in_spanish_country': meta[9]}
    return meta_data

def metadata_str(metadata):
    md = ''
    for k in metadata:
        md += '|||'.join([k, ': ', metadata[k]])
    return md

def find_annotations(sentence):
    annotations = re.compile('(\[(?P<original_word>\w+)]{(?P<target_word>\w+)})*<(?P<issues>[\w+:]+)>')
    return re.search(annotations, sentence)


def write_output(output_file, sentences_with_metadata, k):
    with open(output_file, 'w') as f:
        for essay in sentences_with_metadata:
            for id in essay[k]:
                sent = essay[k][id]
                f.write(str(id) + '\t' + sent + '\n')


if __name__ == "__main__":
    path_to_corpus = sys.argv[1]  # sys.argv[1] is the first argument passed to the program through e.g. pycharm (or command line). In Pycharm, look at Running Configuration
    relevant_essays = sys.argv[2]
    output_file = sys.argv[3]
    annotated = relevant_essays == 'annotated'
    print('Working with corpus {}'.format(path_to_corpus))
    essays = find_relevant_folders(path_to_corpus, relevant_essays)
    metadata = find_relevant_folders(path_to_corpus, "metadata")
    print('Found {} essay folders in the corpus.'.format(len(essays)))
    sentences_with_metadata = build_single_corpus(path_to_corpus, essays, metadata, annotated)
    #sum of all sentences in all essay files:
    total_sentences = len([sent for essay in sentences_with_metadata for sent in essay['sentences']])
    print('Total {} sentences in {} essays.'.format(total_sentences, len(sentences_with_metadata)))
    # Write the corpus into a single file:
    write_output(output_file, sentences_with_metadata, 'sentences')
    write_output(output_file + '.learner', sentences_with_metadata, 'reconstructed_learner')
    write_output(output_file + '.target', sentences_with_metadata, 'reconstructed_target')


