import sys, os
import glob
import nltk  # NLP package; used here to compute sentence length
import re
from delphin import commands, itsdb
from datetime import datetime
from collections import OrderedDict
from unidecode import unidecode  # used to remove diacritics from text
import spacy  # used to split text into sentences

SENT_TOK = spacy.load('es_core_news_sm')  # sentence tokenizer

'''
This script assumes the data structure of the CEDEL corpus: http://cedel2.learnercorpora.com/user_guide/metadata.
'''

def build_corpus(path_to_files):
    essays = []
    files = sorted(glob.iglob(path_to_files + '/**'))
    uniqueid = 0
    for file in files:
        uniqueid += 1
        essays_with_metadata = {'file_id': '', 'metadata': {}, 'text': ''}
        with open(file, 'r') as f:
            content = f.read()
            essay = content.split('Text: ')[1].replace('\n', ' ')
            essays_with_metadata['text'] = essay
            essays_with_metadata['file_id'] = uniqueid
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if i < 39: # transform the essay's metadata in a dictionary to separate it from the text
                    meta_title = line.split(': ')[0]
                    meta_content = line.split(': ')[1].strip('\n')
                    essays_with_metadata['metadata'][meta_title] = meta_content
            essays.append(essays_with_metadata)
    return essays

def process_text(texts_with_metadata):
    sentences_by_id = {}
    sentences_by_L1 = {}
    for text in texts_with_metadata:
        sent_tokenized_text = [i for i in SENT_TOK(text['text']).sents]
        sent_id = 0
        for sent_obj in sent_tokenized_text:
            sent_id += 1
            sent = sent_obj.orth_
            unique_id = text['file_id'] * 1000 + sent_id
            clean_sent = sent.strip('-"“”*&–')
            # Replace unsupported punctuation:
            clean_sent = re.sub('[“”]', '"', clean_sent)
            clean_sent = re.sub('–', "-", clean_sent)
            assert unique_id not in sentences_by_id and unique_id not in sentences_by_L1
            sent_len = str(len(nltk.tokenize.word_tokenize(clean_sent, language='spanish')))
            item = {'unique_id': unique_id, 'input': clean_sent, 'len': sent_len, 'filename': text['metadata']['Filename'],
                    'topic': text['metadata']['Task title'], 'year': text['metadata']['Year data collection'],
                    'metadata_file': text['metadata'], 'medium': text['metadata']['Medium'], 'L1': text['metadata']['L1']}
            L1 = item['L1']
            if L1 not in sentences_by_L1:
                sentences_by_L1[L1] = {}
            if sent_len not in sentences_by_L1[L1]:
                sentences_by_L1[L1][sent_len] = []
            sentences_by_L1[L1][sent_len].append(item)
            sentences_by_id[unique_id] = item
    return sentences_by_id, sentences_by_L1

def write_tsdb_item_output_by_L1(dir, sentences_by_L1):
    today = datetime.today().strftime('%Y-%m-%d')
    for L1, len in sentences_by_L1.items():
        if not os.path.exists(dir + '/' + L1 + '/'):
            os.makedirs(os.path.dirname(dir + '/' + L1 + '/'))
        for k, v in len.items():
            if not os.path.exists(dir + '/' + L1 + '/meta/'):
                os.mkdir(dir + '/' + L1 + '/meta/')
            with open(dir + '/' + L1 + '/meta/' + k + '.txt', 'w') as f:
                simple_id = 0
                for item in v:
                    simple_id += 1
                    sentence = item['input']
                    sent = tsdb_item_string(simple_id, sentence, item, today)
                    f.write(sent + '\n')


def tsdb_item_string(simple_id, sentence, item, today):
    author = item['filename'].split('_')[6]
    comment = metadata_str(item['metadata_file'])
    output = (str(item['unique_id']) + '@' + item['filename'] + '@essay@' + item['medium'] + '@1@S@' + sentence + '@1@' +
              str(item['len']) + '@' + comment + '@' + author + '@' + str(today))
    return output

def metadata_str(metadata): # extract the values of the metadata dict and put them in a string
    md = ''
    for k in metadata:
        md += ''.join([k, ': ', metadata[k] + '; '])
    return md

def write_filename_codes(dir, filename_codes):
    with open(dir + '/filename_codes.txt', 'w') as f:
        for code in filename_codes:
            f.write(str(code['file_id']))

def write_sentences_by_L1(dir, sentences_by_L1):
    for L1, len in sentences_by_L1.items():
        if not os.path.exists(dir + '/' + L1 + '/'):
            os.makedirs(os.path.dirname(dir + '/' + L1 + '/'))
        for k, v in len.items():
            if not os.path.exists(dir + '/' + L1 + '/txt/'):
                os.mkdir(dir + '/' + L1 + '/txt/')
            with open(dir + '/' + L1 + '/txt/' + k + '.txt', 'w') as f:
                for item in v:
                    f.write(item['input'] + '\n')

def write_ids_by_L1(dir, sentences_by_L1):
    for L1, len in sentences_by_L1.items():
        if not os.path.exists(dir + '/' + L1 + '/'):
            os.makedirs(os.path.dirname(dir + '/' + L1 + '/'))
        for k, v in len.items():
            if not os.path.exists(dir + '/' + L1 + '/uniqueid/'):
                os.mkdir(dir + '/' + L1 + '/uniqueid/')
            with open(dir + '/' + L1 + '/uniqueid/' + k + '.txt', 'w') as f:
                for item in v:
                    f.write(str(item['unique_id']) + '\n')

def read_metadata(metadata_file):
    md = []
    with open(metadata_file, 'r') as f:
        for line in f:
            line = line.strip().split('@')
            # cut off the data before the first ||| in the comment, because it is the unique id which we already have:
            comment = line[9].split('|||')
            comment = ';'.join(comment[1:])
            md.append({'i-origin':line[1], 'i-register':line[2], 'i-format':line[3], 'i-difficulty':line[4],
                           'i-category':line[5], 'i-input':line[6], 'i-wf':line[7], 'i-length':line[8],
                           'i-comment':comment, 'i-author':line[10], 'i-date':line[11]})
    return md

def read_ids(id_file):
    ids = []
    with open(id_file, 'r') as f:
        for line in f:
            ids.append(line.strip())
    return ids

def update_profile(ts, ids, md):
    for (i, row), id, meta in zip(enumerate(ts['item']), ids, md):
        ts['item'].update(i, {'i-id':id, 'i-origin':meta['i-origin'], 'i-register':meta['i-register'],
                              'i-format':meta['i-format'], 'i-difficulty':meta['i-difficulty'],
                              'i-category':meta['i-category'], 'i-input':meta['i-input'],
                              'i-wf':meta['i-wf'], 'i-length':meta['i-length'],
                              'i-comment':meta['i-comment'], 'i-author':meta['i-author'],
                              'i-date':meta['i-date']})
    try:
        ts.commit()
    except:
        print('stop!!')

if __name__ == '__main__':
    path_to_corpus = sys.argv[1] + '/corpus'
    output_dir = sys.argv[1] + '/output'
    print('Working with corpus {}'.format(sys.argv[1]))
    essays_with_metadata = build_corpus(path_to_corpus)
    sentences_by_id, sentences_by_L1 = process_text(essays_with_metadata)
    print('Found {} essays. Sentence count: {}'.format(len(essays_with_metadata), len(sentences_by_id)))
    write_tsdb_item_output_by_L1(output_dir, sentences_by_L1)
    write_filename_codes(output_dir, essays_with_metadata)
    write_sentences_by_L1(output_dir, sentences_by_L1)
    write_ids_by_L1(output_dir, sentences_by_L1)

    tsdb_output_dirs = glob.iglob(output_dir + '/**/')
    for tsdb_output_dir in tsdb_output_dirs:
        if not tsdb_output_dir.endswith('.txt'):
            sentences_dir = tsdb_output_dir + 'txt/'
            if not os.path.exists(sentences_dir):
                os.mkdir(sentences_dir)
            metadata_dir = tsdb_output_dir + 'meta/'
            if not os.path.exists(metadata_dir):
                os.mkdir(metadata_dir)
            ids_dir = tsdb_output_dir + 'uniqueid/'
            if not os.path.exists(ids_dir):
                os.mkdir(ids_dir)
            relations = sys.argv[1] + '/relations'
            destination_dir = tsdb_output_dir + 'tsdb/'
            if not os.path.exists(destination_dir):
                os.mkdir(destination_dir)

    # iterate over files in sentences dir. Use the file name (before the extension)
    # to refer to all other files in other directories, including the new tsdb output directories.
        for filename in sorted(os.listdir(sentences_dir)):
            if filename.endswith('.txt'):
                sentence_file = sentences_dir + filename
                destination = destination_dir + 'cedel' + filename[:-4]
                ids = read_ids(ids_dir + filename)
                metadata = read_metadata(metadata_dir + filename)
                commands.mkprof(destination, source=sentence_file, schema=relations)
                tsdb_profile = itsdb.TestSuite(destination)
                update_profile(tsdb_profile, ids, metadata)
    # sentence_file = sys.argv[1]
    # destination = sys.argv[2]
    # ids = read_ids(sys.argv[4])
    # metadata = read_metadata(sys.argv[5])
    # commands.mkprof(destination, source=sentence_file, schema=relations)
    # tsdb_profile = itsdb.TestSuite(destination)
    # update_profile(tsdb_profile, ids, metadata)

