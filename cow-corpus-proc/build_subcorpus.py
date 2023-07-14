import re
import sys
from datetime import datetime

'''
This script assumes the file format and annotation conventions
from the COW-SL second language learner corpus of Spanish
developed at UC Davis: https://github.com/ucdaviscl/cowsl2h

From a corpus of annotated learner sentences, select a subcorpus based on annotation type (e.g. error type).
Output the subcorpus in the format of DELPH-IN corpus database [incr tsdb()] aka tsdb++ (Oepen 1998).
'''

'''
Return a list containing annotated texts from a text file.
'''
def collect_all_annotated(sentences):
    annotated_sentences = []
    for sentence in sentences:
        annotations = find_annotations(sentence)
        if annotations != None:
            annotated_sentences.append(sentence)
    return annotated_sentences

'''
Save annotated sentences from a list into a dictionary.
'''
def create_dictionary(sentence_list, metadata=None):
    dictionary = {}
    today = datetime.today().strftime('%Y-%m-%d')
    for i, sentence in enumerate(sentence_list):
        annotations = find_annotations(sentence)
        sentence_length = len(sentence.split(" "))
        if annotations != None:
            dictionary[i] = {"origin":"", "register":"", "format":"none", "difficulty":1, "category":"S",
                             "annotated":sentence, "learner":"", "corrected":"", "wf":-1, "length":sentence_length,
                             "author":"", "date":today}  # annotated is the original sentence from the corpus
            print("Sentence {}".format(i))
            print(sentence)
    return dictionary

'''
Break annotated sentences into parts.
'''
def break_sentence(sentence):
    annotations = re.compile('(\[(?P<original_word>\w+)]{(?P<target_word>\w+)})*<(?P<issues>[\w+:]+)>')
    sentence_parts = annotations.split(sentence)
    return sentence_parts

'''
Returns two parallel sentences, one with the original word from the annotation and the other with the target word.
'''
def reconstruct_sentence(sentence, replacement):
    annotation = re.compile('(\[(?P<original_word>\w+)]{(?P<target_word>\w+)})*<(?P<issues>[\w+:]+)>')
    reconstructed = annotation.sub(replacement, sentence)
    return reconstructed


def reconstruct_sentences(gen_num_dictionary):
    '''
    Reconstruct original and target sentences from the dictionary of annotated sentences and save each version in parallel dictionaries.
    '''
    #gen_num_original = {}
    #gen_num_target = {}
    learner = '\g<original_word>'
    corrected = '\g<target_word>'
    for key, sentence_info in gen_num_dictionary.items():
        gen_num_dictionary[key]['learner'] = reconstruct_sentence(sentence_info['annotated'], learner)
        gen_num_dictionary[key]['corrected'] = reconstruct_sentence(sentence_info['annotated'], corrected)
    #return gen_num_original, gen_num_target

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
1490@unknown@formal@none@1@S@Precisamente.@1@1@@montse@25-04-2010
2706@unknown@formal@none@1@S@¿Aznar?@1@1@@montse@25-04-2010
3023@unknown@formal@none@1@S@-¿Solo?@1@1@@montse@25-04-2010
3024@unknown@formal@none@1@S@-Solo.@1@1@@montse@25-04-2010
'''
def output_string(id, sentence_info, sentence_type):
    wf = 0 if sentence_type == 'learner' else 1
    output = str(id) + '@fullcorpus@essay@none@1@S@' + sentence_info[sentence_type].strip('\n') + '@@@@' + str(wf) + '@'\
             + str(sentence_info['length']) + '@' + '@' + sentence_info['author'] + '@' + sentence_info['date'] + '\n'
    simple_output = sentence_info[sentence_type]
    return output, simple_output

def find_annotations(sentence):
    annotations = re.compile('(\[(?P<original_word>\w+)]{(?P<target_word>\w+)})*<(?P<issues>[\w+:]+)>')
    annotated_sentence = re.search(annotations, sentence)
    return annotated_sentence


if __name__ == '__main__':
    '''
        Select only annotated sentences and save them in a dictionary.
        Sanity check report.
    '''
    sentence_file = sys.argv[1]
    with open(sentence_file, 'r') as f:
        sent_lst = f.readlines()
    print('Looking for annotated sentences in {}'.format(sentence_file))
    relevant_sentences = collect_all_annotated(sent_lst)
    print('Total {} annotated sentences in {}.'.format(len(relevant_sentences), sentence_file))
    gen_num_dictionary = create_dictionary(sent_lst)

    reconstruct_sentences(gen_num_dictionary)

    '''
    Save dictionaries into .txt files.
    '''
    with open('output/COWSL2H_gender_number.txt', 'w') as f:
        for k, v in gen_num_dictionary.items():
            # f.write('@'.join([str(vv) for vv in v.values()])+'\n')
            f.write(output_string(k, v, 'annotated')[1])

    with open('output/COWSL2H_original_gen_num.txt', 'w') as f:
        for k, v in gen_num_dictionary.items():
            # f.write('@'.join([str(vv) for vv in v.values()])+'\n')
            f.write(output_string(k, v, 'learner')[1])
    with open('output/COWSL2H_target_gen_num.txt', 'w') as f:
        for k, v in gen_num_dictionary.items():
            # f.write('@'.join([str(vv) for vv in v.values()])+ '\n')
            f.write(output_string(k, v, 'corrected')[1])
    with open('output/COWSL2H_original_gen_num_meta.txt', 'w') as f:
        for k, v in gen_num_dictionary.items():
            # f.write('@'.join([str(vv) for vv in v.values()])+'\n')
            f.write(output_string(k, v, 'learner')[0])
    with open('output/COWSL2H_target_gen_num_meta.txt', 'w') as f:
        for k, v in gen_num_dictionary.items():
            # f.write('@'.join([str(vv) for vv in v.values()])+ '\n')
            f.write(output_string(k, v, 'corrected')[0])
