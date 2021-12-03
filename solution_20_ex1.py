#!/usr/bin/python3

# LOAD THE DATASET
from lib.dataset import NIDSDataset


data_file = 'data/dataset_packets_v2.npy'
labels_file = 'data/dataset_labels_v1.npy'

dataset = NIDSDataset(data_file, labels_file)


# INITIALISE THE COUNTERS TO ZERO

wordcounter=0
flowid = ""

# Python dictionary to store the flowid and its sizes. 
# Here we are taking only flow sizes 
# (i.e; the size of  each packet is taken as 1)
library = {} 


# loop over all datasets
for d in dataset:

    wordcounter = 0
    flowid = ""

    # loop over all words
    for word in d:


        # examine Ethertype - in link layer header
        if wordcounter == 3:
            if not((word[0] == 8) and (word[1] == 0)):
               break
        
        # examine Protocol - in network layer header
        if wordcounter == 5:
            if not( (word[3] == 6) or (word[3] == 17)):
                break

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

            if flowid in library:
                library[flowid] += 1
            else:
                library[flowid] = 1
                
        # print(word, end='')
        wordcounter += 1
        
    # end of iteration over words

# PRINTS all the flowids along with the sizes
for flowid in library:  
    print(flowid, '->', library[flowid])
