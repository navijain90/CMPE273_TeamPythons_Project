# import argparse
#
# parser1 = argparse.ArgumentParser(conflict_handler='resolve')
#
# def setParameters(userDestination):
#
#     parser1.add_argument('--DestiantionTest', default = userDestination, type = int,
#                          help='No of Destination User wants to travel.')
#
#     parser1.add_argument('--DestiantionTest', default=userDestination, type=int,
#                          help='No of Destination User wants to travel.')
#
#     print parser1.parse_args()
#
#
# setParameters(4)

import re
str="my name is navneet's jain"
print str
esc=re.escape(str)
print esc

my_string = "Web's GReat thing-ok"
pattern = re.compile('[^A-Za-z0-9 -]')
new_string = pattern.sub('',my_string)
print new_string