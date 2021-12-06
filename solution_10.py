#!/usr/bin/python3

import re

message = "the quick brown fox jumps over the lazy dog"

number = 1

################################################################
result = re.match("a", message)

if result:
    print("This pattern (%d) matches" % number)
else:
    print("This pattern (%d) does not match" % number)
number += 1

################################################################
# must match if the message contains the number "7"
regex = ".*7.*"

if re.match(regex, message):
    print("This pattern (%d) matches" % number)
else:
    print("This pattern (%d) does not match" % number)
number += 1

################################################################
# must match if the message contains an "ox"
regex = ".*ox.*"

if re.match(regex, message):
    print("This pattern (%d) matches" % number)
else:
    print("This pattern (%d) does not match" % number)
number += 1

################################################################
# must match if the message contains a space " "
regex = ".* .*"

if re.match(regex, message):
    print("This pattern (%d) matches" % number)
else:
    print("This pattern (%d) does not match" % number)
number += 1

################################################################
# must match if the animal is either a "fox" or a "cat"
message1 = "the quick brown fox jumps over the lazy dog"
message2 = "the quick brown owl jumps over the lazy dog"
message3 = "the quick brown cat jumps over the lazy dog"
regex = ".*(fox|cat).*"

if (re.match(regex, message1)) and not(re.match(regex, message2)) and (re.match(regex, message3)) :
    print("This pattern (%d) matches" % number)
else:
    print("This pattern (%d) does not match" % number)
number += 1

################################################################
# must match if the message ENDS on "dog"
message1 = "the quick brown fox jumps over the lazy dog"
message2 = "the quick brown dog jumps over the lazy fox"
regex = ".*dog$"

if (re.match(regex, message1)) and not(re.match(regex, message2)):
    print("This pattern (%d) matches" % number)
else:
    print("This pattern (%d) does not match" % number)
number += 1