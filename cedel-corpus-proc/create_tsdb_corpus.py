import sys, os
import glob
from delphin import commands, itsdb

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
        # print('updating item {} from essay {}'.format(id, meta['i-origin']))
        ts['item'].update(i, {'i-id':id, 'i-origin':meta['i-origin'], 'i-register':meta['i-register'],
                              'i-format':meta['i-format'], 'i-difficulty':meta['i-difficulty'],
                              'i-category':meta['i-category'], 'i-input':meta['i-input'],
                              'i-wf':meta['i-wf'], 'i-length':meta['i-length'],
                              'i-comment':meta['i-comment'], 'i-author':meta['i-author'],
                              'i-date':meta['i-date']})
    ts.commit()

if __name__ == '__main__':
    output_dir = sys.argv[1] + '/output'
    # if not os.path.exists(output_dir):
    #     os.mkdir(output_dir)
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
        # Iterate over the files in sentences dir. Use the file name (before the extension) to refer to all the files
        # in other directories, including the new tsdb output directories.
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