import sys, os
import glob
import nltk  # NLP package; used here to compute sentence length
import re
from datetime import datetime
from collections import OrderedDict
from unidecode import unidecode  # used to remove diacritics from text
import spacy  # used to split text into sentences
from delphin import commands, itsdb

SENT_TOK = spacy.load('es_core_news_sm')  # sentence tokenizer

def find_relevant_folders(d, k):
    folders = glob.glob(d + "**/**/" + k, recursive=True)
    #return folders # This mysteriously included duplicate paths, not always though (?)
    return list(set(folders))

def build_corpus(corpus_path, essays, metadata):
    filename_codes = {}
    max_filecode = 0
    essays_with_metadata = {}
    sentences_by_length = {}
    for fol in essays:
        topic = fol.split('/')[-3]
        semester = fol.split('/')[-2]
        path = fol + '/gender_number/**/*.txt'
        essay_count = {}
        for textfile in sorted(list(glob.glob(path))):
            print("Processing {}".format(textfile))
            annotator = textfile.split('/')[-2]
            if not annotator in essays_with_metadata:
                essays_with_metadata[annotator] = []
            if not annotator in sentences_by_length:
                sentences_by_length[annotator] = {'by id': {}, 'by length': {}}
            if not annotator in essay_count:
                essay_count[annotator] = 0
            essay_count[annotator] += 1
            subcorpus = {'text id': '', 'filename': '', 'sentences': {}, 'topic': '', 'semester': '', 'metadata_file': '', 'author': ''}
            subcorpus['filename'] = textfile.split('/')[-1]
            author = subcorpus['filename'].split('.')[0]
            subcorpus['author'] = author
            if not subcorpus['filename'][:-6] in filename_codes:
                filename_codes[subcorpus['filename'][:-6]] = max_filecode + 1
                max_filecode += 1
            subcorpus['text id'] = subcorpus['filename'][:-6]
            subcorpus['topic'] = topic
            subcorpus['semester'] = semester
            subcorpus['error'] = 'gender_and_number'
            # Find a folder in the metadata list of folders that has the same semester and topic:
            fill_metadata(corpus_path, metadata, semester, subcorpus, textfile, topic, True, annotator)
            process_essay_text(filename_codes[subcorpus['text id']], subcorpus, sentences_by_length[annotator], textfile)
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

'''
    for i, sentence in enumerate(sentence_list):
        annotations = find_annotations(sentence)
        sentence_length = len(sentence.split(" "))
        if annotations == None:
            corpus[i] = {"origin":"", "register":"", "format":"none", "difficulty":1, "category":"S",
                        "annotated":sentence, "learner":"", "corrected":"", "wf":1, "length":sentence_length,
                        "author":"", "date":today}
            print("Sentence {}".format(i))
            print(sentence)
'''

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
                subcorpus['metadata_file'] = meta_data
                if annotated:
                    meta_data['annotator'] = annotator

        else:
            print("No metadata file found for {}".format(textfile))

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

def find_annotations(dict):
    annotations = re.compile('(\[(?P<original_word>\w+)]{(?P<target_word>\w+)})*<(?P<issues>[\w+:]+)>')
    matches = re.search(annotations, dict['sentence'])
    return matches

def process_essay_text(folder_id, essay_with_metadata, corpus, textfile):
    with open(textfile, 'r') as f:
        text = f.read()
        #sent_tokenized_text = nltk.sent_tokenize(text, language='spanish')
        sent_tokenized_text = [i for i in SENT_TOK(text).sents]
        sent_id = 0
        for sent_obj in sent_tokenized_text:
            sent = sent_obj.orth_
            sent_id += 1
            unique_id = folder_id*1000 + sent_id
            #if '154043.S17_FamousGNPA.txt' in textfile:
            #    print('stop')
            clean_sent = sent.strip('-"“”*&–')
            # Replace unsupported punctuation:
            clean_sent = re.sub('[“”]', '"', clean_sent)
            clean_sent = re.sub('–', "-", clean_sent)
            assert unique_id not in essay_with_metadata['sentences'] and unique_id not in corpus['by length'] and unique_id not in corpus['by id']
            essay_with_metadata['sentences'][unique_id] = clean_sent
            sen_len = len(nltk.tokenize.word_tokenize(clean_sent, language='spanish'))
            item = {'sentence': sent, 'filename': essay_with_metadata['filename'], 'unique_id': unique_id,
                    'topic': essay_with_metadata['topic'], 'semester': essay_with_metadata['semester'],
                  'metadata_file': essay_with_metadata['metadata_file'], 'error': essay_with_metadata['error'], 'len': sen_len}
            annotations = find_annotations(item)
            if annotations == None:
                if sen_len not in corpus['by length']:
                    corpus['by length'][sen_len] = []
                corpus['by length'][sen_len].append(item)
                corpus['by id'][unique_id] = item



def output_string(id, sentence_item, date):
    output = str(id) + '@' + sentence_item['filename'] + '@essay@none@1@S@' + sentence_item['sentence'].strip('\n') + '@1@' \
             + str(sentence_item['len']) + '@@@' + date + '\n'
    return output

def write_ids(dir, sentences_by_annotator):
    for annotator, corpus in sentences_by_annotator.items():
        if not os.path.exists(dir + '/' + annotator + '/'):
            os.makedirs(os.path.dirname(dir + '/' + annotator + '/'))
        for len, sent in corpus['by length'].items():
            if not os.path.exists(dir + '/' + annotator + '/uniqueid/'):
                os.mkdir(dir + '/' + annotator + '/' + 'uniqueid/' )
            with open(dir + '/' + annotator + '/uniqueid/' + str(len) + '.txt', 'w') as f:
                for item in sent:
                    f.write(str(item['unique_id']) + '\n')

def write_filename_codes(dir, filename_codes):
    with open(dir + '/filename_codes.txt', 'w') as f:
        for k, v in filename_codes.items():
            f.write(str(filename_codes[k]))

def write_sentences_by_annotator(dir, sentences_by_annotator):
    for annotator, corpus in sentences_by_annotator.items():
        if not os.path.exists(dir + '/' + annotator + '/'):
            os.makedirs(os.path.dirname(dir + '/' + annotator + '/'))
        for len, sent in corpus['by length'].items():
            if not os.path.exists(dir + '/' + annotator + '/txt/'):
                os.mkdir(dir + '/' + annotator + '/txt/')
            with open(dir + '/' + annotator + '/txt/' + str(len) + '.txt', 'w') as f:
                for item in sent:
                    f.write(item['sentence'] + '\n')

def write_tsdb_item_output_by_annotator(dir, sentences_by_annotator):
    today = datetime.today().strftime('%Y-%m-%d')
    for annotator, corpus in sentences_by_annotator.items():
        if not os.path.exists(dir + '/' + annotator + '/'):
            os.makedirs(os.path.dirname(dir + '/' + annotator + '/'))
        for len, sent in corpus['by length'].items():
            if not os.path.exists(dir + '/' + annotator + '/meta/'):
                os.mkdir(dir + '/' + annotator + '/meta/')
            with open(dir + '/' + annotator + '/meta/' + str(len) + '.txt', 'w') as f:
                simple_id = 0
                for item in sent:
                    simple_id += 1
                    tsdb_string = output_string(simple_id, item, today)
                    f.write(str(tsdb_string))

def read_metadata(metadata_file):
    md = []
    with open(metadata_file, 'r') as f:
        content = f.readlines()
        for line in content:
            meta = line.strip('\n').split('@')
            md.append({'i-id': meta[0], 'i-origin': meta[1], 'i-register': meta[2], 'i-format': meta[3], 'i-difficulty': meta[4],
                           'i-category': meta[5], 'i-input': meta[6], 'i-wf': meta[7], 'i-length': meta[8],
                           'i-comment': meta[9], 'i-author': meta[10], 'i-date': meta[11]})
    return md
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
'''


def read_ids(id_file):
    ids = []
    with open(id_file, 'r') as f:
        for line in f:
            ids.append(line.strip())
    return ids

def update_profile(ts, ids, md):
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-id':ids[i], 'i-origin':md[i]['i-origin'], 'i-register':md[i]['i-register'],
                              'i-format':md[i]['i-format'], 'i-difficulty':md[i]['i-difficulty'],
                              'i-category':md[i]['i-category'], 'i-input':md[i]['i-input'],
                              'i-wf':md[i]['i-wf'], 'i-length':md[i]['i-length'],
                              'i-comment':md[i]['i-comment'], 'i-author':md[i]['i-author'],
                              'i-date':md[i]['i-date']})
    ts.commit()

if __name__ == '__main__':
    corpus_dir = sys.argv[1]
    output_dir = sys.argv[2]

    annotated = find_relevant_folders(corpus_dir, 'annotated')
    meta = find_relevant_folders(corpus_dir, 'metadata')

    essays_with_metadata, sorted_sentences, filename_codes = build_corpus(corpus_dir, annotated, meta)

    write_ids(output_dir, sorted_sentences)
    write_filename_codes(output_dir, filename_codes)
    write_sentences_by_annotator(output_dir, sorted_sentences)
    write_tsdb_item_output_by_annotator(output_dir, sorted_sentences)

    for k, v in sorted_sentences.items():
        sentences_dir = output_dir + '/' + k + '/txt/'
        metadata_dir = output_dir + '/' + k + '/meta/'
        destination_dir = output_dir + '/' + k + '/tsdb/'
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)
        ids_dir = output_dir + '/' + k + '/uniqueid/'
        relations = output_dir + '/relations'
    for filename in sorted(os.listdir(sentences_dir)):
        if filename.endswith('.txt'):
            sentence_file = sentences_dir + filename
            destination = destination_dir + 'cow' +  filename[:-4]
            ids = read_ids(ids_dir + filename)
            metadata = read_metadata(metadata_dir + filename)
            commands.mkprof(destination, source=sentence_file, schema=relations)
            tsdb_profile = itsdb.TestSuite(destination)
            update_profile(tsdb_profile, ids, metadata)

