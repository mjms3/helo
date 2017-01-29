TIME_STAMP=$(basename $2 .json)
unzip -p $1 $2  | jq -r ".acList[] | select((.Species | . == 4) and(.Long | .>-6 and . <2) and (.Lat | . >50 and . <59)) | [.Id, .Icao, .Reg, .Alt, .GAlt, .Call, .CallSus, .Lat, .Long, .Spd, .Trak, .Type, .Mdl, .Man, .CNum, .From, .To, .Op, .OpCode, .Mil, .Cou, .Gnd, \"${TIME_STAMP}\"] | @csv" | sed 's@true@1@g; s@false@0@g'
