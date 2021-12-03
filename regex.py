#!/usr/bin/python3

import re

message = "the quick brown cat jumps over the lazy dog"




# result = re.search("a", message)

# if result:
#     print("This pattern matches")
# else:
#     print("This pattern does not match")



regex = ".*(fox|cat).*"
if re.match(regex, message):
    print("This pattern matches")
else:
    print("This pattern does not match")
