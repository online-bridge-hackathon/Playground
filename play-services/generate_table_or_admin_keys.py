#!/usr/bin/env python

# generate_table_or_admin_keys.py
# generates a bunch of table or admin keys and writes them as a JSON object to a file
# Kiat Huang <kiat.huang@gmail.com>

import sys
import json
import random
import string

if __name__ == "__main__":

    # get user's request for key type
    # example argument format '{"mykeytype" : "(table|admin)"}'
    args = json.loads(sys.argv[1])
    keytype = args.get("keytype")
    howmanyadminkeys = args.get("howmanyadminkeys")

    tablekeysdir = "outputs/"
    table_key_length = 16
    number_of_adminkeys = int(howmanyadminkeys)
    number_of_tablekeys = 1000*number_of_adminkeys
    
    # create file with a randomid
    filestring = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(table_key_length)])
 
    if keytype == "admin":
        filepath = ''.join(["outputs/adminkeys.",filestring,".json"])
        number_of_keys = number_of_adminkeys
    elif keytype == "table":
        filepath = ''.join(["outputs/tablekeys.",filestring,".json"])
        number_of_keys = number_of_tablekeys
    else:
        table_json = {'result': 'fail', 'message': 'requires a json arg: \'{\'mykeytype\' : \'(table|admin)\'}\''}
        jsonStr = json.dumps(table_json)
        print(jsonStr)
        sys.exit(1)


    table_keys = {}
    table_tuple = {}
    
    for i in range(0,number_of_keys):
        table_keys[i] = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(table_key_length)])
        table_tuple.update({i: table_keys[i]}) 

    # create the immutable table_json object
    table_json = json.dumps(table_tuple, indent = 4)
    print(table_json)

    with open(filepath,"w+") as outfile:
        json.dump(table_tuple, outfile)
    
   