#!/usr/bin/python3

# LOAD THE DATASET
from lib.dataset import NIDSDataset


data_file = 'data/dataset_packets_v2.npy'
labels_file = 'data/dataset_labels_v1.npy'

dataset = NIDSDataset(data_file, labels_file)


# DEFINE THE PATTERN
pattern = "password=g00dPa$$w0rD"

# INITIALISE THE COUNTERS TO ZERO
framecounter=0
regex_pointer = 0
number_of_alerts = 0

# loop over all datasets
for d in dataset:

    wordcounter = 0

    regex_pointer = 0

    print(framecounter, end="")

    # loop over all words
    for word in d:

        # examine Ethertype - in link layer header
        if wordcounter == 3:
            if not((word[0] == 8) and (word[1] == 0)):
                break; # out of frame loop
        
        # examine Protocol - in network layer header
        if wordcounter == 5:
            if(word[3] != 6):
                break; # out of frame loop

        if wordcounter >= 9:
            for i in range(0, len(word)):
                if word[i] == ord(pattern[regex_pointer]): 
                    regex_pointer += 1
                    if framecounter == 15:
                        print("[%03d|%03d|%03d] %d (%d) (%s)" % (framecounter, wordcounter, i, word[i], regex_pointer, chr(word[i])))
                    if regex_pointer == len(pattern):
                        number_of_alerts += 1
                        break; # out of word loop
                else:
                    regex_pointer = 0


            if number_of_alerts > 0:
                break; # out of frame loop
                

        # print(word, end='')
        wordcounter += 1
    
    print("ACK")

    # end of iteration over words

    framecounter += 1

# end of iteration over datasets

# print summary
print("\nWe've received %d frames" % framecounter)
print("\t%d alerts are given" % number_of_alerts)