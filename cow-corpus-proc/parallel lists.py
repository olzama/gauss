import re

def find_annotations(sentence):
    annotations = re.compile(r'(?P<annotation>\[(?P<original_word>\w+)]{(?P<target_word>\w+)}<(?P<issues>[\w+:]+)>)')
    annotated_sentence = re.search(annotations, sentence)
    return annotated_sentence

def break_sentence(sentence):
    annotations = re.compile(r'(?:\[(?P<original_word>\w+)]{(?P<target_word>\w+)}<(?:[\w+:]+)>)')
    sentence_parts = annotations.split(sentence)
    return sentence_parts

def reconstruct_sentence(sentence, replacement):
    annotation = re.compile(r'(?P<annotation>\[(?P<original_word>\w+)]{(?P<target_word>\w+)}<(?P<issues>[\w+:]+)>)')
    reconstructed = annotation.sub(replacement, sentence)
    return reconstructed

def create_dictionary(sentence_list):
    dictionary = {}
    for i, sentence in enumerate(sentence_list):
        dictionary[i] = sentence
        print("Sentence {}".format(i))
        print(sentence)
    return dictionary

if __name__ == "__main__":
    gn_list = ["En el [vacación]{vacaciones}<in:s:noun:inan> [perfecto]{perfecta}<ga:fm:adj:inan>, no hay muchas otras personas en la playa.",
               "En la noche vamos a caminar sobre de [la]{el}<ga:mf:det:inan> pueblo.",
               "No es frío, yes las estrallas son muy [facíl]{fáciles}<na:ps:adj:inan> a ver."
    ]

    tagged_sentences = create_dictionary(gn_list)
    original_sentences = {}
    target_sentences = {}

    for key,value in tagged_sentences:
        original_sentences[key] = reconstruct_sentence(value, '\g<original_word>')
        target_sentences[key] = reconstruct_sentence(value, '\g<target_word>')

    print(target_sentences)