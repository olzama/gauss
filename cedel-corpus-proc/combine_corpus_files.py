'''
This script assumes the metadata format of the CEDEL corpus: http://cedel2.learnercorpora.com/user_guide/metadata
The purpose of this script is to combine corpus files into a single file, one sentence per line.
The program can be run as follows:
python3 script_name
parameter1_path_to_cedel-corpus
'''

import sys, os
import glob
import nltk  # NLP package; used here to compute sentence length
import re
from datetime import datetime
from collections import OrderedDict
from unidecode import unidecode  # used to remove diacritics from text
import spacy  # used to split text into sentences

SENT_TOK = spacy.load('es_core_news_sm')  # sentence tokenizer


def build_corpus(path_to_corpus):
    files = sorted(glob.iglob(path_to_corpus + '/**'))
    essays = []
    sentences_by_length = OrderedDict()
    sentences_by_id = {}
    file_id = 0
    for file in files:
        file_id += 1
        subcorpus = extract_metadata(file)
        subcorpus['file_id'] = file_id
        subcorpus['Sentences'] = {}
        process_essay_text(file, subcorpus, sentences_by_id, sentences_by_length)
        essays.append(subcorpus)
    return essays, sentences_by_id, sentences_by_length


def extract_metadata(file):
    metadata = {}
    with open(file) as f:
        content = f.readlines()
        for i, line in enumerate(content):
            if i < 39:
                info = line.split(": ")[0]
                meta = line.split(": ")[1].strip('\n')
                metadata[info] = meta
        metadata['Initials'] = metadata['Filename'].split('_')[6]
    return metadata


def process_essay_text(file, corpus, output_by_id, output_by_length):
    with open(file, 'r') as f:
        file_contents = f.read()
        essay = file_contents.split("Text: ")[1]
        essay = essay.replace("\n", " ")
        sent_tokenized_text = [i for i in SENT_TOK(essay).sents]
        sent_id = 0
        for sent_obj in sent_tokenized_text:
            sent_id += 1
            sent = sent_obj.orth_
            unique_id = corpus['file_id'] * 1000 + sent_id
            clean_sent = sent.strip('-"“”*&–')
            # Replace unsupported punctuation:
            clean_sent = re.sub('[“”]', '"', clean_sent)
            clean_sent = re.sub('–', "-", clean_sent)
            assert unique_id not in corpus['Sentences'] and unique_id not in output_by_id
            corpus['Sentences'][unique_id] = clean_sent
            sent_len = str(len(nltk.tokenize.word_tokenize(clean_sent, language='spanish')))
            item = {'unique_id': unique_id, 'input': clean_sent, 'len': sent_len, 'filename': corpus['Filename'],
                    'topic': corpus['Task title'], 'year': corpus['Year data collection'],
                    'metadata_file': corpus['Filename'], 'medium': corpus['Medium'],
                    'author': corpus['Initials']}
            if sent_len not in output_by_length:
                output_by_length[sent_len] = []
            assert unique_id not in output_by_length[sent_len]
            output_by_length[sent_len].append(item)
            output_by_id[unique_id] = item
    return output_by_id, output_by_length


def write_tsdb_item_output_by_length(output_dir, sentences_by_length):
    today = datetime.today().strftime('%Y-%m-%d')
    for len in sentences_by_length:
        with open(output_dir + len + '.txt', 'w') as f:
            simple_id = 0
            for item in sentences_by_length[len]:
                simple_id += 1
                sentence = item['input']
                sent = tsdb_item_string(simple_id, sentence, item, today)
                f.write(sent + '\n')


def tsdb_item_string(simple_id, sentence, item, today):
    output = str(item['unique_id']) + '@' + item['filename'] + '@essay@' + item['medium'] + '@1@S@' + sentence + \
             '@1@' + str(item['len']) + '@@' + item['author'] + '@' + str(today)
    return output


if __name__ == '__main__':
    path_to_corpus = sys.argv[1]
    output_dir = sys.argv[2]
    print('Working with corpus {}'.format(path_to_corpus))
    essays, sentences_by_id, sentences_by_length = build_corpus(path_to_corpus)
    print('Found {} essays. Sentence count: {}'.format(len(essays), len(sentences_by_id)))
    write_tsdb_item_output_by_length(output_dir, sentences_by_length)
