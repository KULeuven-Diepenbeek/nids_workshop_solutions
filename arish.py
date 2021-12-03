#!/usr/bin/python3

import hashlib

# The following lines are dirty hacks to import from a no-child folder
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 


# LOAD THE DATASET
from lib.dataset import NIDSDataset

data_file = '../data/packets.npy'
labels_file = '../data/labels.npy'

dataset = NIDSDataset(data_file, labels_file)



# INITIALISE THE COUNTERS TO ZERO

wordcounter=0
framecounter=0
flowid = ""
library = {}

# loop over all datasets
for d in dataset:

    decision_is_made = 0
    wordcounter = 0
    flowid = ""

    # loop over all words
    for word in d:
        # stop parsing if a decission is made
        if decision_is_made == 0:

            # assert Ethertype is 0x0800 - in link layer header
            if wordcounter == 3:
                if(word[0] == 8) and (word[1] == 0):
                    decision_is_made = 0
                else:
                    decision_is_made = 1
            
            # assert proto is tpc or udp 6/17 - in network layer header
            if wordcounter == 5:
                if(word[3] == 6)or(word[3] == 17):
                    decision_is_made = 0
                else:
                    decision_is_made = 1

            # examine Source Address - in network layer header
            if wordcounter == 6:
                flowid += hex(word[2])[2:]  # ip SA 1/4
                flowid += hex(word[3])[2:]  # ip SA 2/4

            # examine Destination Address - in network layer header
            if wordcounter == 7:
                flowid += hex(word[0])[2:]  # ip SA 3/4
                flowid += hex(word[1])[2:]  # ip SA 4/4
                flowid += hex(word[2])[2:]  # ip DA 1/4
                flowid += hex(word[3])[2:]  # ip DA 2/4

            if wordcounter == 8:
                flowid += hex(word[0])[2:]  # ip DA 3/4
                flowid += hex(word[1])[2:]  # ip DA 4/4
                flowid += hex(word[2])[2:]  # ip SPort 1/2
                flowid += hex(word[3])[2:]  # ip SPort 2/2

            # examine Destination port - in transport layer header
            if wordcounter == 9:
                flowid += hex(word[0])[2:]  # ip DPort 1/2
                flowid += hex(word[1])[2:]  # ip DPort 2/2
                decision_is_made = 2

                # TODO here you should break out of the for loop that
                #      iterates over the words

        # print(word, end='')
        wordcounter += 1

        if flowid in library:
            library[flowid] += 1
        else:
            library[flowid] = 1

    # end of iteration over words

# end of iteration over datasets

for flowid in library:  
    print(flowid, '->', library[flowid])