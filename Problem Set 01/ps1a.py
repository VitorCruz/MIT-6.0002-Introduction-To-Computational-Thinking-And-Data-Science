###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Vitor Cruz
# Collaborators: me
# Time: 3h~

from ps1_partition import get_partitions
import time
import csv

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """  
    
    cows = {}
    
    ## DICT READER TO INSERT COWS IN A DICTIONARY
    with open(filename, 'r') as file:
        csvreader = csv.DictReader(file, fieldnames=['name','weight'])    
        for row in csvreader:
            cows[row['name']] = int(row['weight'])
            
    return cows
    

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    ## SORT COWS USING SORTED TO NOT MUTATE THE DICTIONARY
    cows_sorted = sorted(cows.items(), key= lambda x: x[1], reverse=True)
       
    ## CREATE LIST TO BE RETURNED (STILL EMPTY)
    cows_trips = []
    cows_used = []
    
    trip = 1
    weight = limit
    
    while len(cows_used) < len(cows_sorted):   
        list_aux = []
        for cow in cows_sorted:            
            if cow[0] not in cows_used and cow[1] <= weight:
                list_aux.append(cow[0])
                cows_used.append(cow[0])
                weight -= cow[1]        
      
        cows_trips.append(list_aux)
        trip += 1
        weight = limit
        
    return cows_trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_trips = sorted(list(get_partitions(cows)), key=lambda x: len(x))   
    
    for possible_trip in sorted_trips:   
        group_weights = []
        for group in possible_trip:   
            sum_weights = 0
            for i in group:
                sum_weights += cows[i]          
                
            group_weights.append(sum_weights)         
        if max(group_weights) <= 10:          
            return possible_trip     
   
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """    
    cows = load_cows('ps1_cow_data.txt')
    
    start = time.time()
    greedy = greedy_cow_transport(cows,10)
    end = time.time()
    print("GREEDY ALGO","\nTIME:", end - start, "\nTRIPS:", len(greedy), end="\n\n")
    
    start = time.time()
    brute_force = brute_force_cow_transport(cows, 10)
    end = time.time()
    print("BRUTE FORCE ALGO","\nTIME:", end - start, "\nTRIPS:", len(brute_force), end="\n\n")


if __name__== "__main__":
    compare_cow_transport_algorithms()
    
    
"""
ANSWERS TO PROBLEM 5A

1. What were your results from compare_cow_transport_algorithms? Which 
algorithm runs faster? Why?

- Greedy algorithm runs in miliseconds (undetectable) and brute force in 0.83 seconds (slower), but on the second case it's an optimal solution
agains a "good" solution in the first case. Trying every possibility and brute forcing takes time, so performance is worse.

2. Does the greedy algorithm return the optimal solution? Why/why not?

- No. Because there's a better solution (found by brute force) that doesn't start with sorted combinations by the heaviest cow.

3. Does the brute force algorithm return the optimal solution? Why/why not?

- Yes, because it tries all the combinations and return the best on (there are a few optimal in this case, and returns one of them)

"""