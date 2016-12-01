import argparse

parser1 = argparse.ArgumentParser(conflict_handler='resolve')

def setParameters(userDestination):

    parser1.add_argument('--DestiantionTest', default = userDestination, type = int,
                         help='No of Destination User wants to travel.')

    parser1.add_argument('--DestiantionTest', default=userDestination, type=int,
                         help='No of Destination User wants to travel.')

    print parser1.parse_args()


setParameters(4)
