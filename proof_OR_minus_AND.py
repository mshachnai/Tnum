#Proof that shows that a tnum value and mask can be derived by taking the 
#bitwise AND between all elements in range for value, and taking OR - AND
# of all elements in range for mask

import z3
#from z3 import * considered bad practice but defines namespace z3

#change the amount of bits in the tnum to see that indeed the proof holds for all 
#values (works for 16 bits so far)
bits = 16

# List of Variables
a, ta_val, ta_mask, b, tb_val, tb_mask, c, tc_val, tc_mask, out1, out2 = z3.BitVecs('a ta_val ta_mask b tb_val tb_mask c tc_val tc_mask out1 out2', bits)

#create set that contains at most 2**n elements based on number of bits in tnum
X = [ z3.BitVec('x%s' % i, bits) for i in range(2**bits) ]
#print(X)

f_AND, f_OR = z3.BitVecs('f_AND f_OR', bits)

f_AND = X[0]
f_OR = X[0]
 

#set of properties that define a tnum (the set has a min/ max values and every 
#member of the tnum range must equal the tnum value when bitwise AND with negation of mask
range_constraint = z3.And([X[i] <= X[i+1] for i in range(2**bits-1)])
tnum_def_constraint = z3.And([X[i] & ~ta_mask == ta_val for i in range(2**bits)])
#tnum val and mask cannot share 1 in the same bit index
and_property = ta_mask & ta_val == 0
#tnum_property = ta_val & ~ta_mask == ta_val
#print (f_AND)


#AND/OR of all elements in set
for i in range(1, len(X)):
    f_AND &=  X[i]
    f_OR |=  X[i]

#ta_val = f_AND
#ta_mask = f_OR-f_AND
#print(f_AND, f_OR)
#formula = z3.Implies(z3.And(range_constraint,tnum_def_constraint, and_property,
#    tnum_property), z3.And(f_AND == ta_val, f_OR-f_AND == ta_mask))

formula = z3.Implies(z3.And(range_constraint, ta_val == f_AND, ta_mask == f_OR-f_AND), 
    z3.And(tnum_def_constraint))
    #tnum_property), z3.And(f_AND == ta_val, f_OR-f_AND == ta_mask))

#useful to print formulation on low bits
#print(formula)
#prove formula
z3.prove(formula)
#verify by taking negation and trying to find satisfiable interpretation
s = z3.Solver()
s.add(z3.Not(formula))
print(s.check())
print(s.model())








######for later use maybe


#set of properties 
#p3 = ta_val == X[0] & ~ta_mask
#p4 = ta_val == X[1] & ~ta_mask
#p5 = ta_val == X[2] & ~ta_mask
#p6 = ta_val == X[3] & ~ta_mask

#constraints  
#And_constraint = z3.And(X[0] <= X[1], X[1] <= X[2], X[2] <= X[3])
#not_eq_constraint = z3.And(X[0] != X[1], X[1] != X[2], X[2] != X[3])
#min_max = X[0] & X[3]
#not_empty = z3.And(X[0] >= 0, X[1] >= 0, X[2] >= 0, X[3] >= 0)


#p1 = ta_val == a & ~ta_mask
#p2 = ta_mask == a&~ta_mask - a|ta_mask 

#s.add(f_AND == min_max, And_constraint, not_eq_constraint )
#s.add(z3.ForAll([X[0], X[1], X[2], X[3], X[4]], z3.Implies(z3.And(And_constraint,
#    not_eq_constraint), f_AND == min_max)))
#s.add(z3.Not(z3.Implies(z3.And(And_constraint, not_empty), f_AND == min_max)))


#z3.solve(And_constraint, p3,p4,p5,p6,  f_AND == ta_val, f_OR-f_AND == ta_mask)
#formula = z3.ForAll([X[0], X[1], X[2], X[3],ta_mask, ta_val], 
#    z3.Implies(z3.And(And_constraint, p3,p4,p5,p6, xor_property), 
#    z3.And(f_AND == ta_val, f_OR-f_AND == ta_mask)))

#z3.prove(z3.Implies(z3.And(And_constraint, not_eq_constraint), p))
#formula = z3.ForAll([a, ta_val, ta_mask], z3.Implies(p1, p2))
#formula = z3.ForAll([X[0], X[1], X[2], X[3], X[4]], )
