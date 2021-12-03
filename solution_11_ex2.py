#!/usr/bin/python3

# LOAD THE DATASET
from lib.dataset import NIDSDataset



data_file = 'data/dataset_packets_v1.npy'
labels_file = 'data/dataset_labels_v1.npy'

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

    decision_is_made = 0
    wordcounter = 0

    # loop over all words
    for word in d:
        # stop parsing if a decission is made
        if decision_is_made == 0:

            # examine Ethertype - in link layer header
            if wordcounter == 3:
                if(word[0] == 8) and (word[1] == 0):
                    number_of_ipv4_frames += 1
                elif(word[0] == 8) and (word[1] == 6):
                    number_of_arp_frames += 1
                    decision_is_made = 1
                else:
                    decision_is_made = 1
            
            # examine Protocol - in network layer header
            if wordcounter == 5:
                if(word[3] == 1):
                    number_of_icmp_frames += 1
                    decision_is_made = 1
                elif(word[3] == 6):
                    number_of_tcp_frames += 1
                elif(word[3] == 17):
                    number_of_udp_frames += 1
                    decision_is_made = 1

            # examine Source Address - in network layer header
            if wordcounter == 6:
                if(word[2] == 192)and(word[3] == 168):
                    print(word)
                else: 
                    decision_is_made = 1

            # examine Destination Address - in network layer header
            if wordcounter == 7:
                if(word[2] == 172)and(word[3] == 16):
                    print(word)
                else: 
                    decision_is_made = 1

            # examine Destination port - in transport layer header
            if wordcounter == 9:
                if(word[0] == 193)and(word[1] == 127):
                    decision_is_made = 2
                else:
                    decision_is_made = 1
                

        # print(word, end='')
        wordcounter += 1
    
    # end of iteration over words

    framecounter += 1
    if decision_is_made == 2:
        print("This frame is not allowed")
        decision[2] += 1
    elif decision_is_made == 1:
        print("This frame is allowed")
        decision[1] += 1
    if decision_is_made == 0:
        print("couldn't reach decision")
        decision[0] += 1
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