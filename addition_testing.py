#simulate 2 bit tnum addition over all valid tnum numbers (3^n)
#using tnum addition as defined by linux kernel.

import z3
from itertools import combinations
import numpy as np
from collections import Counter
from itertools import chain 

#generate all valid tnum numbers in n-bit range
def generate_tnums(n):
    max_val = 2**n
    tnum_list = []
    for i in range(max_val):
        for j in range(max_val):
            if(valid_tnum(i, j, n)):
                tnum_list.append((i,j))
    return tnum_list

#addition of two tnum numbers as defined in linux kernel
def tnum_add(a, b, bits): 
    print("tnum a: ", a, "- tnum b: ", b)
    sm = a[1] + b[1] if a[1] + b[1] <=2**bits-1 else (a[1] + b[1])%2**bits
    sv = a[0] + b[0] if a[0] + b[0] <=2**bits-1 else (a[0] + b[0])%2**bits
    sigma = sm + sv if sm+sv <=2**bits-1 else (sm + sv)%2**bits
    chi = sigma ^ sv 
    mu = chi | a[1] | b[1] 
    print("sm: ", sm, "\nsv: ", sv, "\nsigma: ", sigma, "\nchi: ", chi, "\nmu: ", mu,
        "\nresult: ", sv&~mu,",", mu)
    return sv & ~mu, mu

def new_tnum_add(a, b, bits):
    print("tnum a: ", a, "- tnum b: ", b)
    a_list, b_list, res = [], [], []
    #find range of both tnum numbers
    for i in range(2**bits):
        if i & ~a[1] == a[0]: a_list.append(i)
        if i & ~b[1] == b[0]: b_list.append(i)
    #addition of all elements in both lists nC2 - this is the actual range of the 
    #new tnum
    print(a_list, b_list)
    for i in a_list:
        for j in b_list:
            res.append((i+j)%(2**bits))
    print(res)
        
    #derive tnum from given range
    #if two complementing numbers exist in the set(range) then it must contain all possible
    #values allowed for n-bits
    val = res[0]
    mask = res[0]
    #this is a correct way of deriving val/mask from range full range
    #for i in res:
        #val &= i
        #mask |= i

        #Dont need this part----check if complements are in the set and if true, return < 0, 2^n-1 >
        #if(abs(i-(2**bits-1)) in res and i in res):
        #    print("result: ", 0, ",", 2**bits-1)
        #    return (0, 2**bits-1)
    
    #if no complements in set
    #val is the AND of all elements in range
    #mask is OR of all elements in range minus val, take absolute value
    ####correct code
    #mask = abs(val-mask)
    
    #testing theory - do the same but only with max/min of values
    val = (max(res) & min(res))
    mask = abs(val - (max(res) | min(res)))
    '''
    #another test (taking max-min AND max >> 1 until min(res))
    tst = max(res) - min(res)
    val=max(res)
    if(tst < min(res)):
        val &= min(res)
    else:
        while(tst>=min(res)):
            val &= tst
            tst >>= 1
    '''
    print("result: ", val, ",", mask)
    return val, mask


#check tnum number is valid - mask and val cannot have 1 in the same bit position
def valid_tnum(val, mask, bits):
    for i in range(bits+1):
        if(val%2 == 1 and mask%2 == 1):
            return False
        val, mask = int(val/2), int(mask/2) 
    return True
   


#################################### MAIN FUNCTION
def main():
    for i in range(4):
        #define size of tnum and number of valid values
        n = i
        valid_set = 3**n
        complete_set = 2**(2**n)

        count = 0
        tnum_values = generate_tnums(n)
        result_list = []
        result_list1 = []
        #var to decide whether to add all valid tnum values or just 3**n choose n
        #combinations
        all_add = 1

        #for testing
        #a, b = (0,1), (1,0)
        #a, b = (0,2), (3,0)
        #new_tnum_add(a, b, n)


        if(all_add):
            #make all 3**n * 3**n additions
            for i in range(valid_set):
                for j in range(valid_set):
                    #linux original
                    result_list.append(tnum_add(tnum_values[i], tnum_values[j], n))
                    #my algo
                    result_list1.append(new_tnum_add(tnum_values[i], tnum_values[j], n))
                    if(result_list[-1] != result_list1[-1]):
                        print("MISMATCH - WRONG RESULT, Correct Result: ",result_list[-1])
                    count += 1
        else:
            #since tnum is commutative, we can make list of all combinations rather than 
            #checking all 3^n * 3^n options
            comb = combinations(tnum_values, 2)
            #combine all possible valid values 3**n choose 2
            for i in list(comb):  
                    #linux algo
                    result_list.append(tnum_add(i[0], i[1], n))
                    #--------------------
                    #my algo
                    result_list1.append(new_tnum_add(i[0], i[1], n))
                    if(result_list[-1] != result_list1[-1]):
                        print("MISMATCH - WRONG RESULT, Correct Result: ", tnum_add(i[0], i[1], n))
                    count += 1

        #verify results:
        print(n, "- bits")
        print(count, "additions performed")
        #print additions solution occurences 
        print("Linux: ", Counter(elem for elem in result_list))
        print("My Algo: ", Counter(elem for elem in result_list1))
        #compare against correct tnum addition algorithm
        if(Counter(elem for elem in result_list) == (Counter(elem for elem in
            result_list1))):
            print("Correct\n\n")
        else:
            print("Verification failed\n\n")
            #break;

        #remove duplicates and you get all the original valid tnums
        #result_list = list(set(result_list)) 
            

    


if __name__ == "__main__":
    main()

