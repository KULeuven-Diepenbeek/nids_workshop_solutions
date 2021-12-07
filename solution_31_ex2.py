#!/usr/bin/python3

import torch
import numpy as np
from lib.dataset import NIDSDataset

from lib.nn_model import ExampleCNN1D1x64
from lib.nn_model import label_mapping

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report

################################################################################

# Initialize the dataset
dset = NIDSDataset(
    packets_file="./data/dataset_packets_v2.npy", 
    labels_file="./data/dataset_labels_v1.npy")

# The input_buffer contains all input features
input_buffer = []
label_buffer = []

# Iterate over the dataset, and add all valid input features to the buffer
# Accordingly, also extract the label for each of those packets and save it as well

for packet in dset:
    label = packet.get_label()
    input_sample = np.zeros(64)
    
    # For each valid packet, extract the features to the input_sample and append the input_sample to the 
    # input_buffer. Do not forget the labels!
    # Your code starts here
    pointer = 0
    for word in packet:
        for i in range(len(word)):
            input_sample[pointer] = word[i]
            pointer += 1
        if pointer > 64-1:
            break;

    
    print(input_sample, end="")

    if ((input_sample[12]==8)and(input_sample[13]==0)and(input_sample[23]==6 or input_sample[23]==17)):
        input_buffer.append(input_sample)
        label_buffer.append(label)
        print("=> included")
    else:
        print("=> NOT included")
    
    
print("We extracted {} input samples.".format(len(input_buffer)))
print("We extracted {} labels.".format(len(label_buffer)))

################################################################################

input_tensors = []

for input_sample in input_buffer:
    # Turn the Numpy array into a PyTorch tensor
    input_tensor = torch.from_numpy(input_sample)
    # Change input dimensionality
    input_tensor = input_tensor.view(1, 1, 64)
    
    input_tensors.append(input_tensor)

print("Input samples have been converted to 'tensors'")

################################################################################

model = ExampleCNN1D1x64(13)

# Load the trained parameters
model.load_state_dict(torch.load("./data/cnn1d1x64.model", map_location=torch.device('cpu')))

# Set the Batch Normalization layers for inference
model.eval()

print("Loaded the pre-trained model")
print(model)

################################################################################

predictions = []

for input_tensor in input_tensors:
    output_tensor = model(input_tensor.float())
    
    _, predicted = torch.max(output_tensor, 1)
    predictions.append(predicted)

predictions = torch.stack(predictions, 0).numpy()

################################################################################

# Transform the indices to their corresponding class label:
labelled_predictions = []
for prediction in predictions:
    labelled_predictions.append(label_mapping[prediction[0]])

# Choose output figure size
_, ax = plt.subplots(figsize=(20, 20))

# Calculate the confusion matrix
cm = confusion_matrix(label_buffer, labelled_predictions, labels=label_mapping)

# Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                              display_labels=label_mapping)
disp.plot(ax=ax)
plt.show()

################################################################################

print(classification_report(label_buffer, labelled_predictions, 
                            labels=label_mapping, 
                            target_names=label_mapping,
                            digits=4,
                            zero_division=0
                           ))