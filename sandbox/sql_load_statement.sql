load data infile '$CSV_FILE'
into table esp.raw_data
fields terminated by ','
optionally enclosed by '"' escaped by ''
lines terminated by '\n' starting by ''
(Id, Icao, Reg, Alt, GAlt,`Call`, CallSus, Lat, `Long`, Spd, Trak, `Type`, Mdl, Man, CNum, `From`, `To`, Op, OpCode, Mil, Cou, Gnd, @var1)
SET
position_data_id = NULL,
`TimeStamp` = STR_TO_DATE(@var1,'%Y-%m-%d-%H%iZ')
