from sandbox.data_access_layer import DataAccessLayer

dal = DataAccessLayer()

Position_Data = dal.tbls.position_data
Helicopters = dal.tbls.helicopters

result = dal.session.query(Position_Data).filter(Position_Data.operator_id.isnot(None)).group_by(Position_Data.Reg, Position_Data.operator_id).all()
for r in result:
    helicopter = Helicopters(helicopter_reg=r.Reg,
                             operator_id=r.operator_id,
                             position_data_Id=r.Id)
    dal.session.add(helicopter)
dal.session.commit()