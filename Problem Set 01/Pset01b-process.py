

#### PSET 1B TRIAL AND ERROR PROCESS
#### TRYING FROM SIMPLE SOLUTION, BREAKING INTO SMALLER STEPS INTO THE NECESSARY SOLUTION

""" 1. TRIED FIRST WITH LESS ITEMS TO BUILD THE LOGIC, WORKS WITH 2 TYPES OF EGGS

if 'egg_count' not in memo:
    memo['egg_count'] = 0
    memo['weight_left'] = target_weight         


if memo['weight_left'] == 0:
   return memo  

if egg_weights[1] <= memo['weight_left']:          
   egg_count = memo['egg_count'] + 1
   weight_left = memo['weight_left']          
   
   take_last = dp_make_weight(egg_weights, target_weight, {'egg_count': egg_count, 'weight_left': weight_left-egg_weights[1]})
   take_other = dp_make_weight(egg_weights, target_weight, {'egg_count': egg_count, 'weight_left': weight_left-egg_weights[0]})      
   
elif egg_weights[0] <= memo['weight_left']:
    memo['egg_count'] += 1
    memo['weight_left'] -= egg_weights[0]
    return dp_make_weight(egg_weights, target_weight, memo)        

return take_last if take_last['egg_count'] < take_other['egg_count'] else take_other     
""" 

""" 2. MADE IT BETTER, BUT STILL 2 OPTIONS

if 'egg_count' not in memo:
    memo['egg_count'] = 0
    memo['weight_left'] = target_weight         


if memo['weight_left'] <= 0:
   return memo      
     
egg_count = memo['egg_count'] + 1
weight_left = memo['weight_left']          

take_last = dp_make_weight(egg_weights, target_weight, {'egg_count': egg_count, 'weight_left': weight_left-egg_weights[1]})
take_other = dp_make_weight(egg_weights, target_weight, {'egg_count': egg_count, 'weight_left': weight_left-egg_weights[0]})      
   
return take_last if take_last['egg_count'] < take_other['egg_count'] and take_last['weight_left'] == 0 else take_other

"""  

""" 3. MADE IT EVEN BETTER AND USING MEMOISATION 

    if target_weight == 0:
        return egg_count
        
    if target_weight < 0:
        return 99999999        
  
    if target_weight in memo:
        return memo[target_weight]                 
        
    egg_count += 1      
    
    take_last = dp_make_weight(egg_weights, target_weight - egg_weights[1], egg_count, memo)
    take_other = dp_make_weight(egg_weights,  target_weight - egg_weights[0], egg_count, memo)      

    result = take_last if take_last < take_other else take_other
    
    memo[target_weight] = result    
    
    return result

""" 


""" 4. VERSION 3 HAD A BUG (BECAUSE OF NEGATIVE RESULTS). THIS ONE WORKS WITH LIST OF 3 ELEMENTS AND FIXES IT 

 if target_weight == 0:
     return egg_count        

 if target_weight in memo and memo[target_weight] < egg_count:            
     return memo[target_weight]

 if target_weight < 0:
     return 99999999          
     
 egg_count += 1    
 
 take_first = dp_make_weight(egg_weights, target_weight - egg_weights[0], egg_count, memo)    
 take_sec = dp_make_weight(egg_weights,  target_weight - egg_weights[1], egg_count, memo)      
 take_third = dp_make_weight(egg_weights,  target_weight - egg_weights[2], egg_count, memo)  

 result = min(take_first,take_sec,take_third)    

 memo[target_weight] = result   
 
 return result

""" 
 
""" 5. WORKS WITH ANY NUMBER OF EGGS, BUT STILL SLOW... SOMETHING MUST CHANGE, MAYBE IN STORING / USING RESULTS STORED?

 ## RETURN THEN THERE IS NO MORE WEIGHT
 if target_weight == 0:       
     return egg_count        

 ## IF THERES A BETTER RESULT IN MEMO, RETURN RESULT -- DON'T RETURN EQUAL RESULTS BECAUSE OF THE NEGATIVE CASES (FIX A BUG)
 if target_weight in memo and memo[target_weight] < egg_count:            
     return memo[target_weight]
 
 ## WHEN THERE'S NEGATIVE WEIGHT, ITS NOT A REAL SOLUTION, THEN RETURN AN ABSURD POSITIVE NUMBER (TO BE DESCONSIDERED IN RESULTS)
 if target_weight < 0:
     return 99999999          
 
 ## INCREASE 1 EGG IN EACH TURN    
 egg_count += 1             
 
 ## CREATE A LIST OF LISTS OF ARGUMENTS DO THE FUNCTION, FOR EACH POSSIBLE EGG WEIGHT
 list_parameters = list(map(lambda x: [egg_weights, target_weight - x, egg_count, memo], egg_weights))   
 
 ## PASS THEM TO MAP, DOING THE FUNCTION TO EACH ITEM (SPREADING FIRST), AND TAKING THE MIN RESULT (LEGG EGGS)
 result = min(list(map(lambda x: dp_make_weight(*x), list_parameters)))     

 ## INSERT BETTER RESULT INTO MEMO
 memo[target_weight] = result
 
 return result    
""" 

""" 6. DIFFERNT APPROACH, BUT STILL SLOW

## RETURN THEN THERE IS NO MORE WEIGHT
if target_weight == 0:       
    return egg_count  

if target_weight in memo:            
    return memo[target_weight]   

## INCREASE 1 EGG IN EACH TURN    
egg_count += 1           

result = 100000
for egg in egg_weights:
    if target_weight - egg >= 0:            
        fun = dp_make_weight(egg_weights, target_weight - egg, egg_count, memo)            
        result = fun if fun < result else result
        
memo[target_weight] = result    
return result  

"""

""" 7. COULDN'T FIND AN ANSWER TO DO IT OUT OF ORDER... SO JUST MADE MAP VERSION A LITTLE BETTER AND THATS IT
## TOOK EXTRA PARAMETER OFF SUMMING 1 TO RESULT

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
    
"""

def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
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


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1,2,3,4,5,6,7)
    n = 150
    print("Actual output:", dp_make_weight(egg_weights, n))












