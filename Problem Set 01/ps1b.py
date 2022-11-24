
###########################
# 6.0002 Problem Set 1b: Space Change
# Name: VITOR CRUZ
# Time: 12h
# Collaborators: ME
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1


def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoizat
    ion (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """        
    
 ## RETURN THEN THERE IS NO MORE WEIGHT
    if target_weight == 0:     
        return 0        
       
    ## IF THERES A RESULT IN MEMO, RESULT RESULT
    if target_weight in memo:            
        return memo[target_weight]              
    
    ## USE ONLY EGGS THAT WILL HAVE A >= 0 OUTCOME    
    egg_weights = [egg for egg in egg_weights if target_weight - egg >= 0]      
    
    ## USE TRY TO CALL FUNCTION AGAIN ONLY WHEN THERE ARE AVAILABLE EGGS IN EGG_WEIGHTS, WHEN THERES AN EXCEPTION JUST PASS AND NOT CALL IT = INVALID SOLUTION
    try:
        if min(egg_weights) >= 0: 
            
            ## CREATE A LIST OF LISTS OF ARGUMENTS DO THE FUNCTION, FOR EACH POSSIBLE EGG WEIGHT
            list_parameters = list(map(lambda x: [egg_weights, target_weight - x, memo], egg_weights))             
                
            ## PASS THEM TO MAP, DOING THE FUNCTION TO EACH ITEM (SPREADING FIRST), AND TAKING THE MIN RESULT (LEGG EGGS)
            result = 1 + min(list(map(lambda x: dp_make_weight(*x), list_parameters)))                
               
            ## INSERT BETTER RESULT INTO MEMO
            memo[target_weight] = result            
            return result
    except:
        pass

    return result      


if __name__ == '__main__':    
    egg_weights = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)    
    n = 99    
    print("Egg weights = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)")
    print("n = 99")
    print("Expected ouput: 4 (3* 30 + 1 * 9)")
    print("Actual output:", dp_make_weight(egg_weights, n, {}))
    print()
     
    egg_weights = (1,2,3,4,5,6,7)    
    n = 150   
    print(f"Egg weights = {egg_weights}")
    print(f"n = {n}")
    print("Expected ouput: 22 (21 * 7 + 1 * 3)")    
    print("Actual output:", dp_make_weight(egg_weights, n, {}))
    print()    
    
    egg_weights = (1,2,20,30,3,4,5,6,7,8,27,150,600)    
    n = 120   
    print(f"Egg weights = {egg_weights}")
    print(f"n = {n}")
    print("Expected ouput: 4 (4 * 30)")    
    print("Actual output:", dp_make_weight(egg_weights, n, {}))
    print()  
    
  
"""    
1. Explain why it would be difficult to use a brute force algorithm to solve this problem if there 
were 30 different egg weights. You do not need to implement a brute force algorithm in order to 
answer this.

- BECAUSE ITS AN EXPONENTIAL PROBLEM, BIG O NOTATION OF N^N.


2. If you were to implement a greedy algorithm for finding the minimum number of eggs 
needed, what would the objective function be? What would the constraints be? What strategy 
would your greedy algorithm follow to pick which coins to take? You do not need to implement a 
greedy algorithm in order to answer this.

- JUST STARTING FROM THE HEAVIEST EGG AND PUTTING IN THE SHIP (WHEN AVAILABLE WEIGHT >= HEAVIEST EGG) ELSE TAKING THE NEXT HEAVIEST AND SO ON,
ULTIL NO MORE WEIGHT IS AVAILABLE. 


3. Will a greedy algorithm always return the optimal solution to this problem? Explain why it is 
optimal or give an example of when it will not return the optimal solution. Again, you do not need 
to implement a greedy algorithm in order to answer this.

- IN THIS PARTICULAR CASE, GREEDY ALGORITHM WOULD ALSO BE OPTIMAL AND HAPPENS TO BE FASTER, BUT IT NEEDS THE LIST TO BE SORTED.
SINCE THERE ARE NO COMBINATIONS HERE, YOU CAN TAKE ANY AMOUNT OF ANY EGG, GOING FROM HEAVIEST TO LIGHTER IN ORDER AND PUTTING ALWAYS THE HEAVIEST POSSIBLE
IN THE SHIP, GREEDY TURNS TO BE THE OPTIMAL SOLUTION.


"""