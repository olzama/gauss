import sys, os
from delphin import commands, itsdb

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

Example from the TIBIDABO treebank, tbdb01/item:

679@unknown@formal@none@1@S@Bien.@1@1@@montse@25-04-2010
1148@unknown@formal@none@1@S@-Comprenden?@1@1@@montse@25-04-2010
'''
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
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-id':ids[i], 'i-origin':md[i]['i-origin'], 'i-register':md[i]['i-register'],
                              'i-format':md[i]['i-format'], 'i-difficulty':md[i]['i-difficulty'],
                              'i-category':md[i]['i-category'], 'i-input':md[i]['i-input'],
                              'i-wf':md[i]['i-wf'], 'i-length':md[i]['i-length'],
                              'i-comment':md[i]['i-comment'], 'i-author':md[i]['i-author'],
                              'i-date':md[i]['i-date']})
    ts.commit()

if __name__ == '__main__':
    common_dir = sys.argv[1]
    sentence_type = 'reconstructed_target/' if  sys.argv[2] == 'target' else 'reconstructed_learner'
    sentences_dir = common_dir + 'txt/' + sentence_type
    metadata_dir = common_dir + 'meta/' + sentence_type
    ids_dir = common_dir + 'uniqueid/'
    relations = common_dir + 'relations'
    destination_dir = common_dir + 'tsdb/'+ sentence_type
    # iterate over files in sentences dir. Use the file name (before the extension)
    # to refer to all other files in other directories, including the new tsdb output directories.
    for filename in sorted(os.listdir(sentences_dir)):
        if filename.endswith('.txt'):
            sentence_file = sentences_dir + filename
            destination = destination_dir + 'cow' +  filename[:-4]
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