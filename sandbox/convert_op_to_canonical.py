from collections import defaultdict

from sandbox.data_abstraction_layer import DataAbstractionLayer, PositionData
from fuzzywuzzy import process as fuzzy_process

data_layer = DataAbstractionLayer()

canonical_list_file = 'canonical-list.txt'

with open(canonical_list_file, 'r') as in_file:
    canonical_list = [l.strip().lower().replace('limited', 'ltd').encode('ascii', errors='ignore').decode() for l in in_file.readlines()]


operators_present = [r[0] for r in data_layer.session.query(PositionData.Op).distinct()]

with open('operators_present.txt','w') as out_file:
    for op in operators_present:
        out_file.write(op)
        out_file.write('\n')


operators_to_ignore = []
synonymn_lists = defaultdict(list)

CRITICAL_SCORE = 95

for op in operators_present:
    closest_match, score = fuzzy_process.extractOne(op, canonical_list)
    if score < CRITICAL_SCORE:
        operators_to_ignore.append(op)
    else:
        synonymn_lists[closest_match].append(op)

with open('synonyms_list.txt','w') as out_file:
    for k, v in synonymn_lists.items():
        out_file.write('{}\t{}\n'.format(k,repr(v)))

with open('excluded_op.txt','w') as out_file:
    for op in operators_to_ignore:
        out_file.writelines(op+'\n')