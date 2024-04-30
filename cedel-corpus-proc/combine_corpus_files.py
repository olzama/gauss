import sys, os
import glob
import nltk  # NLP package; used here to compute sentence length
import re
from datetime import datetime
from collections import OrderedDict
from unidecode import unidecode  # used to remove diacritics from text
import spacy  # used to split text into sentences

SENT_TOK = spacy.load('es_core_news_sm')  # sentence tokenizer

def build_corpus(path_to_files):
    essays = []
    files = sorted(glob.iglob(path_to_files + '/**'))
    uniqueid = 0
    for file in files:
        uniqueid += 1
        subcorpus = {'file_id': uniqueid, 'metadata': {}}
        with open(file, 'r') as f:
            content = f.read()
            essay = content.split('Text: ')[1].replace('\n', ' ')
            subcorpus['text'] = essay
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if i < 39:
                    meta_title = line.split(': ')[0]
                    meta_content = line.split(': ')[1].strip('\n')
                    subcorpus['metadata'][meta_title] = meta_content
            subcorpus['metadata']['Author'] = subcorpus['metadata']['Filename'].split('_')[6]
            essays.append(subcorpus)
    return essays

def process_text(texts_with_metadata):
    sentences_by_id = {}
    sentences_by_L1 = {}
    for essay in texts_with_metadata:
        sent_tokenized_text = [i for i in SENT_TOK(essay['text']).sents]
        sent_id = 0
        for sent_obj in sent_tokenized_text:
            sent_id += 1
            sent = sent_obj.orth_
            unique_id = essay['file_id'] * 1000 + sent_id
            clean_sent = sent.strip('-"“”*&–')
            # Replace unsupported punctuation:
            clean_sent = re.sub('[“”]', '"', clean_sent)
            clean_sent = re.sub('–', "-", clean_sent)
            assert unique_id not in sentences_by_id and unique_id not in sentences_by_L1
            sent_len = str(len(nltk.tokenize.word_tokenize(clean_sent, language='spanish')))
            item = {'unique_id': unique_id, 'input': clean_sent, 'len': sent_len, 'filename': essay['metadata']['Filename'],
                    'topic': essay['metadata']['Task title'], 'year': essay['metadata']['Year data collection'],
                    'metadata_file': essay['metadata']['Filename'], 'medium': essay['metadata']['Medium'],
                    'author': essay['metadata']['Author'], 'L1': essay['metadata']['L1']}
            L1 = item['L1']
            if L1 not in sentences_by_L1:
                sentences_by_L1[L1] = {}
            if sent_len not in sentences_by_L1[L1]:
                sentences_by_L1[L1][sent_len] = []
            assert unique_id not in sentences_by_L1
            sentences_by_L1[L1][sent_len].append(item)
            sentences_by_id[unique_id] = item
    return sentences_by_id, sentences_by_L1

def write_tsdb_item_output_by_L1(dir, sentences_by_L1):
    today = datetime.today().strftime('%Y-%m-%d')
    for L1, len in sentences_by_L1.items():
        os.makedirs(os.path.dirname(dir + '/' + L1 + '/'))
        for k, v in len.items():
            with open(dir + '/' + L1 + '/' + k + '.txt', 'w') as f:
                simple_id = 0
                for item in v:
                    simple_id += 1
                    sentence = item['input']
                    sent = tsdb_item_string(simple_id, sentence, item, today)
                    f.write(sent + '\n')


def tsdb_item_string(simple_id, sentence, item, today):
    output = str(item['unique_id']) + '@' + item['filename'] + '@essay@' + item['medium'] + '@1@S@' + sentence + \
             '@1@' + str(item['len']) + '@@' + item['author'] + '@' + str(today)
    return output

if __name__ == '__main__':
    path_to_corpus = sys.argv[1] + '/corpus'
    output_dir = sys.argv[1] + '/fresh'
    print('Working with corpus {}'.format(sys.argv[1]))
    essays_with_metadata = build_corpus(path_to_corpus)
    sentences_by_id, sentences_by_L1 = process_text(essays_with_metadata)
    print('Found {} essays. Sentence count: {}'.format(len(essays_with_metadata), len(sentences_by_id)))
    write_tsdb_item_output_by_L1(output_dir, sentences_by_L1)

