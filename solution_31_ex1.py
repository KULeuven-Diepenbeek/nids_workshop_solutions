#!/usr/bin/python3

import torch
import numpy as np
from lib.dataset import NIDSDataset


# Initialize the dataset
dset = NIDSDataset(
    packets_file="./data/dataset_packets_v2.npy", 
    labels_file="./data/dataset_labels_v1.npy")

# The input_buffer contains all input features
input_buffer = []
label_buffer = [0]*64

# Iterate over the dataset, and add all valid input features to the buffer
# Accordingly, also extract the label for each of those packets and save it as well

for packet in dset:
    label = packet.get_label()
    input_sample = np.zeros(64)
    
    # For each valid packet, extract the features to the input_sample and append the input_sample to the 
    # input_buffer. Do not forget the labels!
    # Your code starts here
    counter = 0
    for word in packet:
        for i in range(len(word)):
            input_sample[counter+i] = word[i]
        counter += 4
        if counter < 64-1:
            break;
    input_buffer.append(input_sample)
    
print("We extracted {} input samples.".format(len(input_buffer)))