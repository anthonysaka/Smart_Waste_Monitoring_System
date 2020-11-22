"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def build_distance_matrix(response):
    distance_matrix = []
    
    for row in range(len(response['distances'])):
        for col in range(len(response['distances'])):
            response['distances'][row][col] = int(response['distances'][row][col])
        distance_matrix.append(response['distances'][row])
    return distance_matrix

def create_data_model(distanceMatrix,demands,truckCapacities,truckAmount):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = build_distance_matrix(distanceMatrix)   
    data['demands'] = demands
    data['truck_capacities'] = truckCapacities
    data['num_truck'] = truckAmount
    data['depot'] = 0

    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    total_load = 0
    respuesta = {'rutas':''}
    for vehicle_id in range(int(data['num_truck'])):
        index = routing.Start(vehicle_id)
        plan_output = '{}:'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            #plan_output += '{0}@{1}:'.format(node_index, route_load)
            plan_output += '{0}:'.format(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        #plan_output += '{0}@{1}\n'.format(manager.IndexToNode(index),
        #                                        route_load)
        plan_output += '{0}:'.format(manager.IndexToNode(index))
        plan_output += '{}:'.format(route_distance)
        plan_output += '{};'.format(route_load)
        respuesta['rutas'] += plan_output
        print(plan_output)
        
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))

    respuesta['total_distance'] = total_distance
    respuesta['total_volumen'] = total_load
    return respuesta

def generate_smart_routes(distanceMatrix,demands,truckCapacities,truckAmount):

    data = create_data_model(distanceMatrix,demands,truckCapacities,truckAmount)
   
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),int(data['num_truck']),int(data['depot']))
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)                                        

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_callback_index,
                                            0,  # null capacity slack
                                            data['truck_capacities'],  # vehicle maximum capacities
                                            True,  # start cumul to zero
                                            'Capacity')
    

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 20
    search_parameters.log_search = True

     # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        solucion = print_solution(data, manager, routing, solution)

        return solucion