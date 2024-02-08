import sys
from delphin import itsdb, derivation
import glob


def report_stats(treebanks_path):
    all_sentences = []
    all_accepted = []
    all_rejected = []
    for i, tsuite in enumerate(sorted(glob.iglob(treebanks_path + '/**'))):
        sentences = []
        accepted = []
        rejected = []
        ts = itsdb.TestSuite(tsuite)
        items = list(ts.processed_items())
        #print("{} sentences in corpus {} including possible sentences with no parse.".format(len(items), ts.path.stem))
        for response in items:
            all_sentences.append(response['i-input'])
            sentences.append(response['i-input'])
            # In a thinned parsed forest, results will be empty if the item was not accepted as correct in treebanking.
            if len(response['results']) > 0:
                accepted.append(response['i-input'])
                all_accepted.append(response['i-input'])
            else:
                #print('Rejected: {}'.format(response['i-input']))
                rejected.append(response['i-input'])
                all_rejected.append(response['i-input'])
        acc = len(accepted)/len(sentences)
        print('Corpus {} accuracy {} out of {} ({:.2f})'.format(ts.path.stem, len(accepted), len(sentences), acc))
    acc = len(all_accepted) / len(all_sentences)
    print('Total accuracy: {} out of {} ({:.2f})'.format(len(all_accepted), len(all_sentences), acc))

def report_rule_counts(treebanks_path):
    all_rules_count = {}
    rule_count_list = []
    for i, tsuite in enumerate(sorted(glob.iglob(treebanks_path + '/**'))):
        ts = itsdb.TestSuite(tsuite)
        items = list(ts.processed_items())
        for response in items:
            if len(response['results']) > 0:
                # try looking at response['results'][0] to see which phrase structure rules were used
                r0 = response['results'][0]
                # A derivation is a tree that consists of nodes. Nodes can be phrase structure rules or lexical rules or "terminals" (words).
                deriv = derivation.from_string(r0['derivation']) # Exercise: Try to find in the pydelphin docs how to get a flat list of the derivation nodes.
                rule_count = count_rules(deriv)
                rule_count_list.append(rule_count)
        # Collect rule counts from each test suite and store them in one dictionary.
        for phsr, info in rule_count.items():
            if info['is_root'] is False:
                all_rules_count[phsr] = sum(info['counts'] for rule_count in rule_count_list if phsr in rule_count)
    for k, v in all_rules_count.items():
        print('Rule {}: {} uses.'.format(k, v))
    print('Total number of constraints used: {}'.format(len(all_rules_count)))


def count_rules(d):
    counts = {}
    constraints = []
    # get a flat list of tree nodes
    # iterate over node list collecting values stored in the entity field of each node
    nodes = d.internals()
    for node in nodes:
        phsr = node.entity
        constraints.append(phsr)
        counts[node.entity] = {'counts': constraints.count(node.entity), 'is_root': node.is_root()}
    return counts

if __name__ == '__main__':
    report_stats(sys.argv[1])
    report_rule_counts(sys.argv[1])