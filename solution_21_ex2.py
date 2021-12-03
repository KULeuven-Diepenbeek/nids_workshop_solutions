#!/usr/bin/python3

import hashlib

HASHTABLE_DEPTH = 256 # depth of the hashtable
memory = [None] * HASHTABLE_DEPTH

def _hash(key):
    """ Md5 hash function to calculate the index"""
    md5 = hashlib.md5(str(hash(key)).encode('utf-8'))
    return int(md5.hexdigest(), 16) % HASHTABLE_DEPTH

def add_ht(key, value):
    # write to code to obtain a numeric hash value for the 'key'
    index = _hash(key)
    
    # write the code to check if a value already exists on the obtained address
    # if the address is not set yet, set it the value
    # if the address is already set, overwrite it with the sum of both values
    if memory[index] is None:
        # WRITE the code to Check if the flowid present in the [key,value] pair in the memory[index] is equal to 
        # the incoming flowid. if equal, then add the value to the existing value.
        memory[index] = value
    else: 
        memory[index] += value
    
def query_ht(key):
    """Get a value by key"""
    index = _hash(key)
    if memory[index] is None:
        return 0
    else:
        return memory[index]


# Set a 'key'
key = "the quick brown cat jumps over the lazy dog"

# Query the 'key'
queried_value = query_ht(key)
print("%s => %d" % (key, queried_value))
        
# Add the 'key'
add_ht(key, 123)
queried_value = query_ht(key)
print("%s => %d" % (key, queried_value))

# Add the 'key'
add_ht(key, 321)
queried_value = query_ht(key)
print("%s => %d" % (key, queried_value))
