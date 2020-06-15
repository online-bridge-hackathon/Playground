#!/usr/bin/env python

# generate_table.py
# creates a table, watches it and manages all the action
# Kiat Huang <kiat.huang@gmail.com>

import sys
import json
import random
import string
from datetime import datetime
import collections
import pika

# Played deal - bidding workflow
# 1. user presents a token, requesting a table
# 2. user gets a table ID and 4 player keys, one each for N, E, S, W
# 3. user issues a seat and key ID to each of 4 players - players can be humans or robots
# 4. the 4 players present their seat and key ID and get pub+sub rights
# 5. (kibs can also get pub rights, TDs can get pub+sub - not planned to code that here)
# 6. a deal is imported
# 7. a trigger occurs and the appropriate hands in the deal are issued to the players
# 8. one player is identfied as the dealer and the vulnerabilities are issued via pub
# 9. the dealer makes the first bid via sub
# 9. the bid is recorded in a deal file
# 10. all players recieve notification of the bid via sub
# 11. the next player in sequence makes the next bid and steps 9. and 10. repeat
# 12. when three players have issued pass bids the contract is recorded
# 13. all players recieve notification of the contract via sub


if __name__ == "__main__":
    tablekeysdir = "outputs/"
    tablekeysfile = ''.join([tablekeysdir, "tablekeys.SJdjPOzwFZOOf4JB.json"])

    # get user's submitted table_key    
    # example argument format '{"mytablekey" : "MpnH72Sm"}'
    args = json.loads(sys.argv[1])
    user_table_key = args.get("mytablekey")
    # print(user_table_key)

    # load current table_keys file on disk into memory
    with open(tablekeysfile, "r") as infile:
        tablekeys = json.load(infile)

    # check if the supplied table_key matches
    match = "no"
    for n, tablekey in tablekeys.items():
        if user_table_key == tablekey and n.isdigit():
            # register success
            match = "yes"
            key_index = n
            player_table_key = user_table_key

    # exit if the key did not match
    if match == "no":
        table_json = {"mytablekey": user_table_key, "result": "fail", "message": "no matching key found"}
        jsonStr = json.dumps(table_json)
        print(jsonStr)
        sys.exit(1)

    # now verified, mark the table as in progress
    # first remove the key from the stack
    popped_key = tablekeys.pop(key_index)
    # now add it back in with the the "p" (in progress) flag
    modified_key_index = ''.join([key_index, "p"])
    tablekeys.update({modified_key_index: player_table_key})
    sorted_tablekeys = collections.OrderedDict(sorted(tablekeys.items()))

    with open(tablekeysfile, "w+") as outfile:
        json.dump(sorted_tablekeys, outfile)

    ## construct a play_id from the date+time and the verified table key (which has > 10^14 possibilities)
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    play_id = ''.join([dt_string, ".", player_table_key])
 
    ## Create an array of seats N, S, E, W
    seats = ["N", "E", "S", "W"]
    # initialise keys list
    seat_keys = [''] * 4

    # create four random strings into an array - these are keys for players
    key_length = 32
    # each key string contains "key_length" characters from 0-9a-zA-Z so 62^32 > 10^57
    for i in range(0,4):
        # generate seat keys
        seat_keys[i] = ''.join([seats[i],":",''.join([random.choice(string.ascii_letters + string.digits) for n in range(key_length)])])
        # write the seat keys to a file
        # f.write("%s\n" % seat_keys[i])
    
    # create json for the table and seat keys
    table_list = {'table_key': player_table_key, 'table_create_time': dt_string, 'seat_keys': seat_keys}
    table_json = json.dumps(table_list)
    print(table_json)
    # write out the table file containing seat keys
    table_with_seat_keys_file = ''.join([tablekeysdir, dt_string, ".", player_table_key, ".json"]) 
    with open(table_with_seat_keys_file, "w+") as outfile:
        json.dump(table_list, outfile)
   
    # create a guest or kibitzer table key based on the verified_table_key
    viewer_table_key = player_table_key[8:]

    # create a messaging bus
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # open separate channels for players and viewers
    # players
    ptable = ''.join(["ptable_",player_table_key])
    channel.queue_declare(queue = ptable, durable=True)
    initial_msg = ''.join(["table \"", ptable, "\" created for players"])
    channel.basic_publish(exchange = '',
                      routing_key = ptable,
                      body = initial_msg,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    print(" [x] Sent %s" % initial_msg)

    # viewers
    vtable = ''.join(["vtable_",viewer_table_key])
    channel.queue_declare(queue = vtable, durable=True)
    initial_msg = ''.join(["table \"", vtable, "\" created for viewers"])
    channel.basic_publish(exchange = '',
                      routing_key = vtable,
                      body = initial_msg,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    print(" [x] Sent %s" % initial_msg)

    # exit
    sys.exit(0)
