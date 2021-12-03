#!/usr/bin/python3

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

number_of_ipv4_frames = 0
number_of_arp_frames = 0
decision_is_made = 0
number_of_icmp_frames = 0
number_of_tcp_frames = 0
number_of_udp_frames = 0

decision = [0, 0, 0]

# loop over all datasets
for d in dataset:

    wordcounter = 0

    # loop over all words
    for word in d:
        if wordcounter >= 11:
            if wordcounter == 11:
                print("%02X %02X -> " % (word[2], word[3]), end="")

                # print(  (int(word[2])).to_bytes(1,'big').decode('utf-8') )
                print(chr(word[2]), end="")
                print(chr(word[3]))

                # print( str.encode(int(word[2]), 'utf-8') + str.encode(int(word[3]), 'utf-8') )
            else:
                print("%02X %02X %02X %02X -> " % (word[0], word[1], word[2], word[3]), end="")
                print(chr(word[0]), end="")
                print(chr(word[1]), end="")
                print(chr(word[2]), end="")
                print(chr(word[3]))

                

        # print(word, end='')
        wordcounter += 1
    
    # end of iteration over words

    framecounter += 1
   
# end of iteration over datasets

# print summary
print("\nWe've received %d frames" % framecounter)
print("\tIPv4: %d frames" % number_of_ipv4_frames)
print("\t\tICMP: %d frames" % number_of_icmp_frames)
print("\t\tTCP: %d frames" % number_of_tcp_frames)
print("\t\tUDP: %d frames" % number_of_udp_frames)
print("\tARP: %d frames" % number_of_arp_frames)
print("\nWe've decided to alert")
print("\tok: %d frames" % decision[1])
print("\talert: %d frames" % decision[2])