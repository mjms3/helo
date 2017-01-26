jq '.acList[] | select(.Species | . == 4) | select(.Long | .>-6 and . <2) | select(.Lat | . >50 and . <59)'
