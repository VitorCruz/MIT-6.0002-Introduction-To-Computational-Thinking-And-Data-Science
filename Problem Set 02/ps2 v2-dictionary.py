# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
import csv
from graph import Digraph, Node, WeightedEdge
import functools
import random

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: 
# Nodes = buildings
# Edges = path between buildings
# Distances = how much distance is between 2 nodes, and the second distance how much of it is outside


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """    
    ## LIST TO INSERT FROM FILE
    list_edges = []
    
    ## READ FROM FILE AND INSERT INTO A LIST
    #print("Loading map from file...")
    with open(map_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list_edges.append(row[0].split(' '))
    
    ## CREATE A DIGRAPH
    graph = Digraph()
    
    ## INSERT NODES
    for edge in list_edges:       
        src_node = Node(edge[0])
        dest_node = Node(edge[1])
        try: 
            graph.add_node(src_node)
        except ValueError as e:           
            #print(e)
            pass
        try: 
            graph.add_node(dest_node)
        except ValueError as e:           
            #print(e)
            pass
                
        new_edge = WeightedEdge(src_node, dest_node, edge[2], edge[3])
        try:
            graph.add_edge(new_edge)
        except ValueError as e:
            #print(e)   
            pass
        
    return graph    
    

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

#
# Problem 3: Finding the Shortest Path using Optimized Search Method#
# Problem 3a: Objective function#
# What is the objective function for this problem? What are the constraints?
#
# Answer: FINDING THE PATH WITH MINIMUM DISTANCE THAT HAS THE MINIMUM LENGTH 
# AND ALSO LESS THEN MAX_DIST_OUTDOORS CONSTRAINT


######## USING IT A LITTLE DIFFERENT THAN ASKED...
######## FELT BETTER ALREADY PASSING START AND END AS NODES
######## BETTER PASSING A DICTIONARY STORING "BEST_PATH"

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_path = {}):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],    
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """    
    
    ## NODE NOT IN GRAPH     
    if not (digraph.has_node(start) or digraph.has_node(end)):
        raise ValueError('Node not in graph')        
       
    ## GOT TO THE END, RETURN SOMETHING
    if start == end:
       return path
    
    ## LOOK AT BEST PATH SO FAR STORED IN DICTIONARY (BEST_PATH)
    if 'best' in best_path and path[1] >= best_path['best'][1]:
        return None    
    
    ## SEE IF THERE ARE MORE EDGES LEFT, ELSE RETURN NONE (END OF PATH)
    edges = digraph.get_edges_for_node(start)    
    if edges == None:
        return None        
    
    ## FILTER OUT EDGES THAT ARE ALREADY ON PATH (AVOID LOOPS). IF THERES NO MORE EDGES LEFT, RETURN NONE 
    edges = [e for e in edges if e.get_destination().get_name() not in path[0]]          
    if len(edges) == 0:
        return None   
    
    ## RECURSIVELY CALL THE FUNCTION ON THE EDGES
    result = list(map(lambda ed: get_best_path(digraph, ed.get_destination(), end
                                      , [path[0] + [ed.get_destination().get_name()], path[1] + int(ed.get_total_distance()), path[2] + int(ed.get_outdoor_distance())]   
                                      , max_dist_outdoors, best_path), edges))      
    
    ## FILTER NONE RESULTS (INVALID PATHS)
    result = [res for res in result if res != None] 
    
    ## FILTER DISTANCES THAT EXCEED max_dist_outdoors
    if max_dist_outdoors != None:
        result = [res for res in result if res[2] <= max_dist_outdoors]      
    
    ## TAKE BEST PATH WHEN THERE IS ONE
    if len(result) > 0:       
        best = functools.reduce(lambda x,y: x if x[1] < y[1] else y, result)           
        best_path['best'] = best
        return best
    else:
        return None       


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    
    start = Node(str(start))
    end  = Node(str(end))
    path = [[start.get_name()],0,0]    
   
    result = get_best_path(digraph, start, end, path, max_dist_outdoors, {})    
   
    if result != None and result[1] <= max_total_dist:
        return result[0]            
    else:
        raise ValueError("There are no paths for provided constraints")
          
    

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)


    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)
        

if __name__ == "__main__":
    unittest.main()
    
    #digraph = load_map('mit_map.txt')
    #start = random.choice(list(digraph.nodes))
    #end = random.choice(list(digraph.nodes))   
    #start = Node('2')
    #end = Node('9')   
    #start = '1'
    #end = '32'
    #print("BEST PATH:", directed_dfs(digraph, start, end, 99999,99999))    
  
   
