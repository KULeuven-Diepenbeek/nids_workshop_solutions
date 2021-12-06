import numpy as np

old_filename = '../data/dataset_packets_v1.npy'
new_filename = '../data/dataset_packets_v2.npy'

packet_array = np.load(old_filename)

# Define new data
data_to_change = np.array([112,97,115,115,119,111,114,100,61,103,48,48,100,80,97,36,36,119,48,114,68])
n_bytes = data_to_change.shape[0]

# Change data of packet 15, starting from the 60th byte:
packet_array[15][59:59+n_bytes] = data_to_change

# Save change array in new file
np.save(new_filename, packet_array)

# Print 15th packet of the new file to check:
print(np.load(new_filename)[15])
print(np.load(new_filename)[15][59:59+n_bytes])