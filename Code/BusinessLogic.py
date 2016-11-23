from __future__ import absolute_import
import try_tsp
from itertools import tee, islice, chain, izip

import argparse
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


userDestination=raw_input("Please enter number of destination you are going\n")

parser = argparse.ArgumentParser()
parser.add_argument('--Destiantion', default = userDestination, type = int,
                     help='No of Destination User wants to travel.')
parser.add_argument('--tsp_use_random_matrix', default=True, type=bool,
                     help='Use random cost matrix.')
parser.add_argument('--tsp_random_forbidden_connections', default = 0,
                    type = int, help='Number of random forbidden connections.')
parser.add_argument('--tsp_random_seed', default = 0, type = int,
                    help = 'Random seed.')
parser.add_argument('--light_propagation', default = False,
                    type = bool, help = 'Use light propagation')


Uber =[]
Lyft =[]
counter=0
combined=[]

def item_and_next(some_iterable):
    items, nexts = tee(some_iterable, 2)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(items, nexts)

def Optimalprice(DestinationList):

    Tsp_cor = []
    list = []

    obj = try_tsp.RandomMatrix(4, 0, DestinationList)
    Tsp_cor = try_tsp.tsp(parser.parse_args(), DestinationList)
    print Tsp_cor

    for item, nxt in item_and_next(Tsp_cor):
        if (nxt == None):
            nxt = "0";

        print DestinationList[int(item)][int(nxt)],




def CombinedOptimal(pricelistmatrix,type):
    global counter
    global Uber
    global Lyft
    if type == 'UBER':
        Uber = pricelistmatrix
        counter += 1
        print "inside uber"
        print counter

    elif type == 'LYFT':
        Lyft = pricelistmatrix
        counter += 1
        print "inside lift"
        print counter


    print counter


    if(counter==2):

        for i in range(len(pricelistmatrix)):
            combined.append([])
            for j in range(len(pricelistmatrix)):
                combined[i].append(0)



        for i in range(len(pricelistmatrix)):
            for j in range(len(pricelistmatrix) ):
                if(Uber[i][j]>Lyft[i][j]):
                    combined[i][j]=Lyft[i][j]

                elif (Uber[i][j]<=Lyft[i][j]):
                    combined[i][j] = Uber[i][j]

        Optimalprice(combined)


        # for i in range(len(pricelistmatrix)):
        #     for j in range(len(pricelistmatrix) ):
        #         print combined[i][j],
        #     print '\n'




