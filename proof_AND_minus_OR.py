#Proof that shows that a tnum value and mask can be derived by taking the 
#bitwise AND between all elements in range for value, and taking OR - AND
# of all elements in range for mask

import z3
#from z3 import * considered bad practice but defines namespace z3

# List of Variables
a, ta_val, ta_mask, b, tb_val, tb_mask, c, tc_val, tc_mask, out1, out2 = z3.BitVecs('a ta_val ta_mask b tb_val tb_mask c tc_val tc_mask out1 out2', 8)

X = [ z3.BitVec('x%s' % i, 8) for i in range(4) ]
print(X)

f_AND = X[0]
f_OR = X[0]
AND_max = X[0]
 
#s = z3.Solver()
#for i in range (4):

#this is for testing some syntax
#And_constraint = [X[i] <= X[i+1] for i in range(3)]
#print(And_constraint)

#constraints  
And_constraint = z3.And(X[0] <= X[1], X[1] <= X[2], X[2] <= X[3])
not_eq_constraint = z3.And(X[0] != X[1], X[1] != X[2], X[2] != X[3])
#min_max = X[0] & X[3]
#not_empty = z3.And(X[0] >= 0, X[1] >= 0, X[2] >= 0, X[3] >= 0)

#AND/OR of all elements in set
for i in range(len(X)):
    f_AND &=  X[i]
    f_OR &=  X[i]

#set of properties 
p3 = ta_val == X[0] & ~ta_mask
p4 = ta_val == X[1] & ~ta_mask
p5 = ta_val == X[2] & ~ta_mask
p6 = ta_val == X[3] & ~ta_mask
#tnum val and mask cannot share 1 in the same bit index
xor_property = ta_mask ^ ta_val == 0


#print (And_constraint)
#print (f_AND)
#print (min_max)
#z3.solve(And_constraint, p3,p4,p5,p6,  f_AND == ta_val, f_OR-f_AND == ta_mask)
formula = z3.ForAll([X[0], X[1], X[2], X[3],ta_mask, ta_val], 
    z3.Implies(z3.And(And_constraint, p3,p4,p5,p6, xor_property), 
    z3.And(f_AND == ta_val, f_OR-f_AND == ta_mask)))
z3.prove(formula)

s = z3.Solver()
s.add(z3.Not(formula))
print(s.check())
print(s.model())


#for later use maybe

#p1 = ta_val == a & ~ta_mask
#p2 = ta_mask == a&~ta_mask - a|ta_mask 

#s.add(f_AND == min_max, And_constraint, not_eq_constraint )
#s.add(z3.ForAll([X[0], X[1], X[2], X[3], X[4]], z3.Implies(z3.And(And_constraint,
#    not_eq_constraint), f_AND == min_max)))
#s.add(z3.Not(z3.Implies(z3.And(And_constraint, not_empty), f_AND == min_max)))


#z3.prove(z3.Implies(z3.And(And_constraint, not_eq_constraint), p))
#formula = z3.ForAll([a, ta_val, ta_mask], z3.Implies(p1, p2))
#formula = z3.ForAll([X[0], X[1], X[2], X[3], X[4]], )
