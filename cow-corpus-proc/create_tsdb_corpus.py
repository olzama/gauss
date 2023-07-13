import sys
import delphin

def read_metadata(md_file):
    pass

def update_profile(ts, md):
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-id':md[i]['i-id']})
    ts.commit()

if __name__ == '__main__':
    sentence_file = sys.argv[1]
    destination = sys.argv[2]
    relations = sys.argv[3]
    metadata = read_metadata(sys.argv[4])
    tsdb_profile = delphin.commands.mkprof(destination, source=sentence_file, schema=relations)
    update_profile(tsdb_profile, metadata)