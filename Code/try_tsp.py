

import random
import argparse
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def Distance(i, j):
  """will us for final amount calculation after optimal path"""

  return i + j


class RandomMatrix(object):
  """Random matrix."""

  def __init__(self, size, seed,list):
    """Initialize random matrix."""

    #List1 = [[0,9,78,77],[9,0,70,72],[78,70,0,6],[77,72,6,0]]
    List1=list
    rand = random.Random()
    rand.seed(seed)

    #distance_max = 100
    self.matrix = {}
    for from_node in range(size):
      self.matrix[from_node] = {}
      for to_node in range(size):
        if from_node == to_node:
          self.matrix[from_node][to_node] = 0
        else:
          self.matrix[from_node][to_node] = List1[from_node][to_node]       #rand.randrange(distance_max)

  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]


def tsp(args,list):
  # Create routing model
  if args.Destiantion > 0:

    routing = pywrapcp.RoutingModel(args.Destiantion, 1, 0)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    # Setting first solution heuristic (cheapest addition).
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Setting the cost function.
    # Put a callback to the distance accessor here. The callback takes two
    # arguments (the from and to node inidices) and returns the distance between
    # these nodes.

    matrix = RandomMatrix(args.Destiantion, args.tsp_random_seed,list)

    for k,v in  matrix.matrix.iteritems():
      print k, v


    matrix_callback = matrix.Distance



    if args.tsp_use_random_matrix:
      routing.SetArcCostEvaluatorOfAllVehicles(matrix_callback)
    else:
      routing.SetArcCostEvaluatorOfAllVehicles(Distance)
    # Forbid node connections (randomly).
    rand = random.Random()
    rand.seed(args.tsp_random_seed)
    forbidden_connections = 0
    while forbidden_connections < args.tsp_random_forbidden_connections:
      from_node = rand.randrange(args.Destiantion - 1)
      to_node = rand.randrange(args.Destiantion - 1) + 1
      if routing.NextVar(from_node).Contains(to_node):
        print('Forbidding connection ' + str(from_node) + ' -> ' + str(to_node))
        routing.NextVar(from_node).RemoveValue(to_node)
        forbidden_connections += 1

    # Solve, returns a solution if any.
#    assignment = routing.SolveWithParameters(search_parameters)
    assignment = routing.Solve()
    if assignment:
      # Solution cost.
      print(assignment.ObjectiveValue())
      # Inspect solution.
      # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
      route_number = 0
      node = routing.Start(route_number)
      route = ''
      while not routing.IsEnd(node):
        route += str(node) + ' -> '
        node = assignment.Value(routing.NextVar(node))
      route += '0'
      print(route)
    else:
      print('No solution found.')
  else:
    print('Specify an instance greater than 0.')
#
# if __name__ == '__main__':
#   main(parser.parse_args())