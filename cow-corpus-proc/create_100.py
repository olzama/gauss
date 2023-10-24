import sys, os
from delphin import commands, itsdb
from create_tsdb_corpus import read_metadata, read_ids

def update_profile(ts, ids, md, selected_profile):
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-id':ids[i], 'i-origin':md[i]['i-origin'], 'i-register':md[i]['i-register'],
                              'i-format':md[i]['i-format'], 'i-difficulty':md[i]['i-difficulty'],
                              'i-category':md[i]['i-category'], 'i-input':md[i]['i-input'],
                              'i-wf':md[i]['i-wf'], 'i-length':md[i]['i-length'],
                              'i-comment':md[i]['i-comment'], 'i-author':md[i]['i-author'],
                              'i-date':md[i]['i-date']})
        for j, row in enumerate(selected_profile['item']):
            if ts['item']['i-input'][i] == selected_profile['item']['i-input'][j]:
                ts['item'].update(i, {'i-selected':1})
    ts.commit()


if __name__ == '__main__':
    common_dir = sys.argv[1]
    sentence_type = 'reconstructed_target/' if  sys.argv[2] == 'target' else 'reconstructed_learner'
    sentences_dir = common_dir + 'txt/' + sentence_type
    metadata_dir = common_dir + 'meta/' + sentence_type
    ids_dir = common_dir + 'uniqueid/'
    relations = common_dir + 'relations'
    destination_dir = common_dir + 'tsdb/'+ sentence_type
    selected_dir = common_dir + '100/'
    commands.mkprof('100/tsdb/cow-selected100', source=selected_dir + '100.txt', schema=relations)
    selected_profile = itsdb.TestSuite('100/tsdb/cow-selected100')
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
            update_profile(tsdb_profile, ids, metadata, selected_profile)
    # sentence_file = sys.argv[1]
    # destination = sys.argv[2]
    # ids = read_ids(sys.argv[4])
    # metadata = read_metadata(sys.argv[5])
    # commands.mkprof(destination, source=sentence_file, schema=relations)
    # tsdb_profile = itsdb.TestSuite(destination)
    # update_profile(tsdb_profile, ids, metadata)