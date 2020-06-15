# Playground
A space for playing with ideas and experiments

generate_table_or_admin_keys.py
Example usage:
./generate_table_or_admin_keys.py '{"mykeytype" : "admin"}'   # generates 10 x admin keys
./generate_table_or_admin_keys.py '{"keytype" : "table" , "howmanyadminkeys" : "10"}' # generates 10,000 table keys

generate_seat_keys.py
Example usage:
./generate_seat_keys.py '{"mytablekey" : "gpH2Lm1k51mAo8O8"}'
   {"table_create_time": "20200616004134", "table_key": "gpH2Lm1k51mAo8O8", "seat_keys": ["N:NnHVaMbv0RPJUs56P3nGbDXsfbIHIpsY", "E:nAtTxsmA2NA0yEI2w7bakQrSJxoeH9Hu", "S:3vLlYWVDdSax7ij4kiUg1lAl01HOlhhC", "W:j7ixiO6qFUO29jGnJm0GqWE94EdlEGmY"], "pubsub": ["ptable_gpH2Lm1k51mAo8O8", "vtable_51mAo8O8"]}

./generate_table.py '{"mytablekey" : "qlKjNQzTZorMBnBy"}'
{"table_create_time": "20200616004651", "table_key": "qlKjNQzTZorMBnBy", "seat_keys": ["N:KyOtCNNoTMASYkDUunEGbbhjkGVEzeFs", "E:KHaTh2OC0JLHQF78L0CxI9LUl72lnyvr", "S:Sd6ldzUxyws5vTcAmkdFAzvferJKlcOk", "W:zCJrcZDfyk4KVZuAEs3XN9q0jsArZfRC"]}
 [x] Sent table "ptable_qlKjNQzTZorMBnBy" created for players
 [x] Sent table "vtable_ZorMBnBy" created for viewers

