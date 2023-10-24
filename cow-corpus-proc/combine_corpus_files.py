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
from datetime import datetime
from collections import OrderedDict
from unidecode import unidecode # used to remove diacritics from text

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
def build_single_corpus_from_annotated(corpus_path, essays, metadata):
    filename_codes = {}
    max_filecode = 0
    essays_with_metadata = {}
    sentences_by_length = {}
    for fol in essays:
        topic = fol.split('/')[-3]
        semester = fol.split('/')[-2]
        # The annotated folders have additional structure:
        # There will be a subfolder called "gender_number", and below that there will be one or more
        # folders named "annotator1", "annotator2", etc.
        # We need to descend into each "annotator" folder and collect the sentences from there.
        # We will keep the annotator name in the metadata under an "annotator" field.
        # "gender_number" will be the "error" field.
        path = fol + '/gender_number/**/*.txt'
        essay_count = {}
        for textfile in sorted(list(glob.glob(path))):
            annotator = textfile.split('/')[-2]
            if not annotator in essays_with_metadata:
                essays_with_metadata[annotator] = []
            if not annotator in sentences_by_length:
                sentences_by_length[annotator] = {'by id': {}, 'by length': {}}
            if not annotator in essay_count:
                essay_count[annotator] = 0
            essay_count[annotator] += 1
            subcorpus = {'filename': '', 'sentences': {}, 'reconstructed_learner':{},'reconstructed_target':{},
                         'topic': '', 'semester': '', 'metadata_file': ''}
            subcorpus['filename'] = textfile.split('/')[-1]
            author = subcorpus['filename'].split('.')[0]
            if not subcorpus['filename'][:-6] in filename_codes:
                filename_codes[subcorpus['filename'][:-6]] = max_filecode + 1
                max_filecode += 1
            subcorpus['topic'] = topic
            subcorpus['semester'] = semester
            subcorpus['error'] = 'gender_and_number'
            # Find a folder in the metadata list of folders that has the same semester and topic:
            fill_metadata(corpus_path, metadata, semester, subcorpus, textfile,
                          topic, True, annotator)
            process_essay_text(True, filename_codes[subcorpus['filename'][:-6]], subcorpus,
                               sentences_by_length[annotator], textfile)
            essays_with_metadata[annotator].append(subcorpus)
    # Created a dict where keys are sorted in increasing order:
    for annotator in sentences_by_length:
        sorted_by_length = OrderedDict()
        sorted_by_id = OrderedDict()
        for len in sorted(sentences_by_length[annotator]['by length'].keys()):
            sorted_by_length[len] = sentences_by_length[annotator]['by length'][len]
        sentences_by_length[annotator]['by length'] = sorted_by_length
        for id in sorted(sentences_by_length[annotator]['by id'].keys()):
            sorted_by_id[id] = sentences_by_length[annotator]['by id'][id]
        sentences_by_length[annotator]['by id'] = sorted_by_id
    return essays_with_metadata, sentences_by_length, filename_codes

def build_single_corpus_from_unannotated(corpus_path, essays, metadata):
    essays_with_metadata = []
    sentences_by_length = {}
    folder_id = 0
    for fol in essays:
        folder_id += 1
        topic = fol.split('/')[-3]
        semester = fol.split('/')[-2]
        path = fol + '/*.txt'
        essay_id = 0
        for textfile in glob.glob(path):
            essay_id += 1
            subcorpus = {'filename': '', 'sentences': {}, 'reconstructed_learner':{},'reconstructed_target':{},
                         'topic': '', 'semester': '', 'metadata_file': ''}
            subcorpus['filename'] = textfile.split('/')[-1]
            subcorpus['topic'] = topic
            subcorpus['semester'] = semester
            # Find a folder in the metadata list of folders that has the same semester and topic:
            fill_metadata(corpus_path, metadata, semester, subcorpus, textfile,
                          topic,False, None)
            process_essay_text(False, essay_id, folder_id, subcorpus, sentences_by_length, textfile)
            essays_with_metadata.append(subcorpus)
    # Created a dict where keys are sorted in increasing order:
    sorted_by_length = OrderedDict()
    for len in sorted(sentences_by_length.keys()):
        sorted_by_length[len] = sentences_by_length[len]
    return essays_with_metadata, sorted_by_length



def process_essay_text(annotated, folder_id, subcorpus, corpus_by_length, textfile):
    with open(textfile, 'r') as f:
        text = f.read()
        sent_tokenized_text = nltk.sent_tokenize(text, language='spanish')
        sent_id = 0
        for sent in sent_tokenized_text:
            sent_id += 1
            include = False
            unique_id = folder_id*1000 + sent_id
            #if '154043.S17_FamousGNPA.txt' in textfile:
            #    print('stop')
            clean_sent = sent.strip('-"“”*&–')
            # Replace unsupported punctuation:
            clean_sent = re.sub('[“”]', '"', clean_sent)
            clean_sent = re.sub('–', "-", clean_sent)
            assert unique_id not in subcorpus['sentences'] and unique_id not in subcorpus['reconstructed_learner'] \
                   and unique_id not in subcorpus['reconstructed_target']
            if annotated:
                reconstructed_learner, reconstructed_target = find_annotations_and_reconstruct(sent)
                if reconstructed_learner is not None:
                    include = True
            if not annotated or include:
                subcorpus['sentences'][unique_id] = clean_sent
                if annotated and include:
                    #reconstructed_learner = reconstruct_sentence(clean_sent, pattern, matches, '\g<original_word>')
                    #reconstructed_target = reconstruct_sentence(clean_sent, pattern, matches,'\g<target_word>')
                    sen_len = len(nltk.tokenize.word_tokenize(reconstructed_target, language='spanish'))
                    if sen_len not in corpus_by_length['by length']:
                        corpus_by_length['by length'][sen_len] = []
                    item = {'reconstructed_target':reconstructed_target, 'reconstructed_learner':reconstructed_learner,
                                                      'original':sent, 'filename': subcorpus['filename'], 'unique_id': unique_id,
                                                        'topic': subcorpus['topic'], 'semester': subcorpus['semester'],
                                                      'metadata_file': subcorpus['metadata_file'], 'error': subcorpus['error'], 'len': sen_len}
                    corpus_by_length['by length'][sen_len].append(item)
                    corpus_by_length['by id'][unique_id] = item
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

'''
Given a matches iterator from the re module, replace the part passed in the pattern as \g<original_word> with the portion
passed in as 'replacement' (which will be either \g<original_word> or \g<target_word>).
The pattern is already compiled. There may be more than one match in the sentence.
'''
def reconstruct_sentence(sentence, pattern, matches, replacement):
    #correction_map = {original: correction for original, correction, _ in matches}
    #annotation = re.compile('(\[(?P<original_word>[\w\s]+)]{(?P<target_word>[\w\s]+)})*<(?P<issues>[\w+:]+)>')
    reconstructed = pattern.sub(replacement, sentence)
    # Replace multiple spaces with a single space:
    reconstructed = re.sub('\s+', ' ', reconstructed)
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
        md += ''.join([k, ': ', metadata[k] + '; '])
    return md

def find_annotations_and_reconstruct(sentence):
    pat = re.compile('(\[(?P<original_word>[\w\s]+)]\s?{(?P<target_word>[\w\s]+)})*\s?<(?P<issues>[\w+:]+)>')
    # Special case, due to a large number of this exact annotation error in the corpus:
    if 'vacación{vacaciones}' in sentence:
        sentence = sentence.replace('vacación{vacaciones}', r'[vacación]{vacaciones}')
    if 'vacacion{vacaciones}' in sentence:
        sentence = sentence.replace('vacacion{vacaciones}', r'[vacacion]{vacaciones}')
    if 'perfecto{perfecta}' in sentence:
        sentence = sentence.replace('perfecto{perfecta}', r'[perfecto]{perfecta}')
    matches = re.findall(pat, sentence)
    if len(matches) > 0:
        reconstructed_learner = re.sub(pat,'\g<original_word>', sentence)
        reconstructed_target = re.sub(pat,'\g<target_word>', sentence)
        # Replace multiple spaces with a single space:
        reconstructed_learner = re.sub('\s+', ' ', reconstructed_learner)
        reconstructed_target = re.sub('\s+', ' ', reconstructed_target)
        # If there is a space before the final dot or punctuation mark, remove it:
        reconstructed_learner = re.sub('\s+([.,?!;:])', '\g<1>', reconstructed_learner)
        reconstructed_target = re.sub('\s+([.,?!;:])', '\g<1>', reconstructed_target)
        return reconstructed_learner, reconstructed_target
    else:
        return None, None

'''
Given a dict where keys are annotators, pick only sentences which appear in all annotators' data.
For now, assumes only two annotators, and that we always look in the first annotator's data for first.
'''
def pick_only_agreed_by_length(data):
    agreed = {}
    a1_only = {}
    a2_only = {}
    for len in data['annotator1']['by length']:
        for item in data['annotator1']['by length'][len]:
            if item['unique_id'] in data['annotator2']['by id']:
                if reconstructions_are_similar(item['reconstructed_learner'], data['annotator2']['by id'][item['unique_id']]['reconstructed_learner']):
                    if len not in agreed:
                        agreed[len] = []
                    agreed[len].append(item)
                else:
                    print("Annotations don't match for {}".format(item['original']))
            else:
                if len not in a1_only:
                    a1_only[len] = []
                a1_only[len].append(item)
    for len in data['annotator2']['by length']:
        for item in data['annotator2']['by length'][len]:
            if item['unique_id'] not in data['annotator1']['by id']:
                if len not in a2_only:
                    a2_only[len] = []
                a2_only[len].append(item)
    return agreed, a1_only, a2_only

'''
Return true if the only difference between two sentences is in spaces, punctuation, accent/stress, or case.
'''
def reconstructions_are_similar(r1, r2):
    recon1 = unidecode(r1.lower())
    recon2 = unidecode(r2.lower())
    if recon1 == recon2:
        return True
    else:
        if recon1 is None or recon2 is None:
            return False
        else:
            # Remove spaces and punctuation:
            recon1 = re.sub('[\s.,?!;:\"\'`\-_–]', '', recon1)
            recon2 = re.sub('[\s.,?!;:\"\'`\-_–]', '', recon2)
            if recon1 == recon2:
                return True
            else:
                return False

def write_output_by_length(output_file, data, k):
    count = 0
    for len in data:
        with open(output_file + '/txt/' + k + '/' + str(len) + '.txt', 'w') as f:
            for item in data[len]:
                count += 1
                f.write(item[k]+ '\n')
    print("Wrote {} sentences to {}".format(count, output_file + '/txt/' + k + '/'))

def write_uniqueid_by_length(output_file, data):
    count = 0
    for len in data:
        with open(output_file + '/uniqueid/'+ '/' + str(len) + '.txt', 'w') as f:
            for item in data[len]:
                count += 1
                f.write(str(item['unique_id'])+ '\n')
    print("Wrote {} sentences to {}".format(count, output_file + '/uniqueid/' + '/'))



'''
The [incr tsdb()] item format (from the relations file in any tsdb database):
item:
  i-id :integer :key
  i-origin :string
  i-register :string
  i-format :string
  i-difficulty :integer
  i-category :string
  i-input :string
  i-wf :integer
  i-length :integer
  i-comment :string
  i-author :string
  i-date :date

Example of the desired output, from the TIBIDABO treebank, tbdb01/item:

679@unknown@formal@none@1@S@Bien.@1@1@@montse@25-04-2010
1148@unknown@formal@none@1@S@-Comprenden?@1@1@@montse@25-04-2010
'''
def tsdb_item_string(simple_id, sentence, essay, sentence_type, today):
    wf = 0 if sentence_type == 'reconstructed_learner' else 1
    author = essay['filename'] # The author info is encoded in the essay file name
    comment = str(essay['unique_id']) + '|||' + re.sub('\n', ' ', metadata_str(essay['metadata_file']))
    output = str(simple_id) + '@gender-number agreement; two annotators agree@essay@none@1@S@' + sentence + '@' + str(wf) + '@' \
             + str(len(sentence.split())) + '@' + comment + '@' + author + '@' + today
    return output


def write_tsdb_item_output_by_length(output_file, sentences_by_length, k):
    today = datetime.today().strftime('%Y-%m-%d')
    for len in sentences_by_length:
        with open(output_file + '/meta/' + k + '/' + str(len) + '.txt', 'w') as f:
            simple_id = 0
            for item in sentences_by_length[len]:
                simple_id += 1
                sentence = item[k]
                sent = tsdb_item_string(simple_id, sentence, item, k, today)
                f.write(sent + '\n')

def write_tsdb_item_output(output_file, sentences_with_metadata, k):
    today = datetime.today().strftime('%Y-%m-%d')
    with open(output_file, 'w') as f:
        simple_id = 0
        for essay in sentences_with_metadata:
            for id in essay[k]:
                simple_id += 1
                sentence = re.sub('\n', ' ', essay[k][id])
                sent = tsdb_item_string(simple_id, sentence, essay, k, today)
                f.write(sent + '\n')

def write_output(output_file, sentences_with_metadata, k):
    with open(output_file, 'w') as f:
        for essay in sentences_with_metadata:
            for id in essay[k]:
                sent = essay[k][id]
                f.write(re.sub('\n', ' ', sent) + '\n')


def write_filename_codes(output_dir, filename_codes):
    with open(output_dir + 'filename_codes.txt', 'w') as f:
        for code in filename_codes:
            f.write(str(filename_codes[code]) + '\t' + code  + '\n')

if __name__ == "__main__":
    path_to_corpus = sys.argv[1]  # sys.argv[1] is the first argument passed to the program through e.g. pycharm (or command line). In Pycharm, look at Running Configuration
    relevant_essays = sys.argv[2]
    output_dir = sys.argv[3]
    annotated = relevant_essays == 'annotated'
    print('Working with corpus {}'.format(path_to_corpus))
    essays = find_relevant_folders(path_to_corpus, relevant_essays)
    metadata = find_relevant_folders(path_to_corpus, "metadata")
    print('Found {} essay folders in the corpus.'.format(len(essays)))
    sentences_with_metadata, sentences_by_length, filename_codes = build_single_corpus_from_annotated(path_to_corpus, essays, metadata)
    # Filter for sentences which all annotators annotated in the same way:
    filtered, only_a1, only_a2 = pick_only_agreed_by_length(sentences_by_length)
    write_output_by_length(output_dir, filtered, 'reconstructed_target')
    write_uniqueid_by_length(output_dir, filtered)
    write_tsdb_item_output_by_length(output_dir, filtered, 'reconstructed_target')
    write_filename_codes(output_dir, filename_codes)
    #print('Total {} sentences in {} essays.'.format(total_sentences, len(sentences_with_metadata)))
    #write_output_by_length(output_file, sentences_by_length, 'reconstructed_target')
    #write_output_by_length(output_file, sentences_by_length, 'reconstructed_learner')
    #write_tsdb_item_output_by_length(output_file, sentences_by_length, 'reconstructed_target')
    # Write the corpus into a single file:
    #write_output(output_file, sentences_with_metadata, 'sentences')
    #write_output(output_file + '.learner', sentences_with_metadata, 'reconstructed_learner')
    #write_output(output_file + '.reconstructed_target', sentences_with_metadata, 'reconstructed_target')
    #write_tsdb_item_output(output_file + '.tsdb.reconstructed_target', sentences_with_metadata, 'reconstructed_target')


