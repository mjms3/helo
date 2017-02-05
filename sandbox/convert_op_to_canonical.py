from fuzzywuzzy import process as fuzzy_process

from sandbox.data_access_layer import DataAccessLayer

dal = DataAccessLayer()
Position_Data = dal.tbls.position_data
Operators = dal.tbls.operators

canonical_list_file = 'canonical-list.txt'
with open(canonical_list_file, 'r') as in_file:
    canonical_list = [l.strip().lower().replace('limited', 'ltd').encode('ascii', errors='ignore').decode() for l in
                      in_file.readlines()]

for operator_name in canonical_list:
    if not dal.session.query(Operators).filter_by(canonical_operator_name=operator_name).all():
        op = Operators(canonical_operator_name=operator_name)
        dal.session.add(op)
dal.session.commit()

operators_present = {op[0]: None for op in dal.session.query(Position_Data.Op).distinct().all()}

CRITICAL_SCORE = 95

for op in operators_present:
    closest_match, score = fuzzy_process.extractOne(op.lower().replace('limited', 'ltd'), canonical_list)
    if score > CRITICAL_SCORE:
        operators_present[op] = closest_match

for op, canonical_op_name in operators_present.items():
    if canonical_op_name:
        canonical_op = dal.session.query(Operators).filter_by(canonical_operator_name=canonical_op_name).one()
        dal.session.query(Position_Data).filter_by(Op=op).update({'operator_id': canonical_op.operator_id})
dal.session.commit()
