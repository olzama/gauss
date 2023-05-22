import re

def find_annotated_sentences(f):
    annotated_sentences = []
    with open(f,'r') as f:
        sentences = f.readlines()
        for sentence in sentences:
            if re.search("[\[\]{}<>]", sentence):
                annotated_sentences.append(sentence)
    return annotated_sentences

with open ('COWSL2H_gender_number.txt', 'w') as f:
    relevant_sentences = find_annotated_sentences('COWSL2H_annotated.txt')
    print('Looking for annotated sentences in COWSL2H_annotated.txt.')
    for sentence in relevant_sentences:
        f.write(sentence)
    print('Found {} annotated sentences.'.format(len(relevant_sentences)))