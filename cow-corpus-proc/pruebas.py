import re

def collect_all_annotated(d):
    annotated_sentences = []
    with open(d, 'r') as f:
        sentences = f.readlines()
        for sentence in sentences:
            if re.search("[\[\]{}<>]", sentence):
                annotated_sentences.append(sentence)
    return annotated_sentences
def collect_all_raw(d):
    raw_sentences = []

    return raw_sentences