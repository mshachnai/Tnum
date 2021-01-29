# find function using bitwise operations such that AND[a,b] = AND(a,....,b)
# and same idea for OR

import z3
#from z3 import * considered bad practice but defines namespace z3

# List of Variables
I = z3.BitVec('I', 3)
J = z3.BitVec('J', 3)
O = z3.BitVec('O',3)
Y1 = z3.BitVec('Y1',3)
Y2 = z3.BitVec('Y2',3)
Y3 = z3.BitVec('Y3',3)
Y4 = z3.BitVec('Y4',3)
X11 = z3.BitVec('X11',3)
X12 = z3.BitVec('X12',3)
X21 = z3.BitVec('X21',3)
X22 = z3.BitVec('X22',3)
X31 = z3.BitVec('X31',3)
X32 = z3.BitVec('X32',3)
X41 = z3.BitVec('X41',3)
X42 = z3.BitVec('X42',3)

# List of numbering for each variables
ly1 = z3.Int('ly1')
ly2 = z3.Int('ly2')
ly3 = z3.Int('ly3')
ly4 = z3.Int('ly4')

lx11 = z3.Int('lx11')
lx12 = z3.Int('lx12')
lx21 = z3.Int('lx21')
lx22 = z3.Int('lx22')
lx31 = z3.Int('lx31')
lx32 = z3.Int('lx32')
lx41 = z3.Int('lx41')
lx42 = z3.Int('lx42')

# List of components. phi-lib
phi1 = (Y1 == X11 ^ X12)
phi2 = (Y2 == X21 | X22)
phi3 = (Y3 == X31 & X32)
phi4 = (Y4 == X41 + X42)


X = [ z3.BitVec('x%s' % i, 3) for i in range(5) ]
print(X)

f_AND = X[0]
AND_max = X[0]
    
And_constraint = z3.And(X[0] <= X[1], X[1] <= X[2], X[2] <= X[3], X[3] <= X[4])
not_eq_constraint = z3.And(X[0] != X[1], X[1] != X[2], X[2] != X[3])
min_max = X[0] & X[4]
not_empty = z3.And(X[0] >= 0, X[1] >= 0, X[2] >= 0, X[3] >= 0, X[4] >= 0)

for i in range(1,len(X)):
    f_AND &=  X[i]

#O = f_AND

# Write the spec
spec = z3.Implies(And_constraint, f_AND == min_max)
#       z3.Implies(dz3.UGT(I,J), O == I))

# phi cons = line number of two different instructions cannot be the same
phicons = z3.And(ly1!=ly2, ly2!=ly3, ly1!=ly3, ly1!=ly4, ly4!=ly2, ly4!=ly3)

# We only have three instructions.
# Bound the line number of each instruction and operand.
phibound = z3.And(ly1 >=2 , ly1 <=5,
                ly2 >=2, ly2 <=5,
                ly3 >=2, ly3 <=5,
                ly4 >=2, ly4 <=5,
                lx11 >=0, lx11 <=5,
                lx12 >=0, lx12 <=5,
                lx21 >=0, lx21 <=5,
                lx22 >=0, lx22 <=5,
                lx31 >=0, lx31 <=5,
                lx32 >=0, lx32 <=5,
                lx41 >=0, lx41 <=5,
                lx42 >=0, lx42 <=5)


# The operands of an instruction should use variables from previous lines. acyclicity
phidep = z3.And(lx11 < ly1 , lx12 < ly1 , lx21 < ly2, lx22 < ly2, lx31 < ly3, lx32 < ly3,
        lx41 < ly4, lx42 < ly4)

# Connection information:
# First, the simple ones: if lx == 0, then x gets info from I
#                         if ly == 5, then O is y
phiconn = z3.And(z3.Implies(lx11 == 0, X11 == X[0]),
              z3.Implies(lx12 == 0, X12 == X[0]),
              z3.Implies(lx21 == 0, X21 == X[0]),
              z3.Implies(lx22 == 0, X22 == X[0]),
              z3.Implies(lx31 == 0, X31 == X[0]),
              z3.Implies(lx32 == 0, X32 == X[0]),
              z3.Implies(lx41 == 0, X41 == X[0]),
              z3.Implies(lx42 == 0, X42 == X[0]),
              z3.Implies(lx11 == 1, X11 == X[4]),
              z3.Implies(lx12 == 1, X12 == X[4]),
              z3.Implies(lx21 == 1, X21 == X[4]),
              z3.Implies(lx22 == 1, X22 == X[4]),
              z3.Implies(lx31 == 1, X31 == X[4]),
              z3.Implies(lx32 == 1, X32 == X[4]),
              z3.Implies(lx41 == 1, X41 == X[4]),
              z3.Implies(lx42 == 1, X42 == X[4]),
              z3.Implies(ly1 == 5,Y1 == f_AND),
              z3.Implies(ly2 == 5,Y2 == f_AND),
              z3.Implies(ly3 == 5,Y3 == f_AND),
              z3.Implies(ly4 == 5,Y4 == f_AND))

lys = [ly1, ly2, ly3, ly4]
lxs = [lx11, lx12, lx21, lx22, lx31, lx32, lx41, lx42]
lToVDict = {
    ly1: Y1,
    ly2: Y2,
    ly3: Y3,
    ly4: Y4,
    lx11: X11,
    lx12: X12,
    lx21: X21,
    lx22: X22,
    lx31: X31,
    lx32: X32,
    lx41: X41,
    lx42: X42
}

for i in lys :
    for j in lxs:
        phiconn = z3.And(phiconn, z3.Implies(i==j, lToVDict[i] == lToVDict[j]))

phiwfp = z3.And(phicons, phidep, phibound)

insideForAll = z3.ForAll([X[0], X[1], X[2], X[3], X[4], X11, X12, X21, X22, X31, X32, 
    X41, X42, Y1, Y2, Y3, Y4], z3.Implies(z3.And(phi1, phi2, phi3, phi4, phiconn), spec))
final_formula = z3.And(phiwfp, insideForAll)

s = z3.Solver()
s.add(final_formula)
print (s.check())
print (s.model())



#for later use maybe

'''              
              z3.Implies(lx11 == 2, X11 == X[2]),
              z3.Implies(lx12 == 2, X12 == X[2]),
              z3.Implies(lx21 == 2, X21 == X[2]),
              z3.Implies(lx22 == 2, X22 == X[2]),
              z3.Implies(lx31 == 2, X31 == X[2]),
              z3.Implies(lx32 == 2, X32 == X[2]),
              z3.Implies(lx41 == 2, X41 == X[2]),
              z3.Implies(lx42 == 2, X42 == X[2]),
              z3.Implies(lx11 == 3, X11 == X[3]),
              z3.Implies(lx12 == 3, X12 == X[3]),
              z3.Implies(lx21 == 3, X21 == X[3]),
              z3.Implies(lx22 == 3, X22 == X[3]),
              z3.Implies(lx31 == 3, X31 == X[3]),
              z3.Implies(lx32 == 3, X32 == X[3]),
              z3.Implies(lx41 == 3, X41 == X[3]),
              z3.Implies(lx42 == 3, X42 == X[3]),
              z3.Implies(lx11 == 4, X11 == X[4]),
              z3.Implies(lx12 == 4, X12 == X[4]),
              z3.Implies(lx21 == 4, X21 == X[4]),
              z3.Implies(lx22 == 4, X22 == X[4]),
              z3.Implies(lx31 == 4, X31 == X[4]),
              z3.Implies(lx32 == 4, X32 == X[4]),
              z3.Implies(lx41 == 4, X41 == X[4]),
              z3.Implies(lx42 == 4, X42 == X[4]),
'''
#print (And_constraint)
#print (f_AND)
#print (min_max)
#z3.solve(And_constraint, not_eq_constraint, f_AND == min_max)
#z3.prove(z3.Implies(z3.And(And_constraint, not_eq_constraint), p))
#formula = z3.ForAll([a, ta_val, ta_mask], z3.Implies(p1, p2))
#formula = z3.ForAll([X[0], X[1], X[2], X[3], X[4]], )

#correct
#z3.prove(z3.Not(z3.Implies(z3.And(And_constraint, not_empty), f_AND == min_max)))

#s = z3.Solver()
#s.add(f_AND == min_max, And_constraint, not_eq_constraint )
#s.add(z3.ForAll([X[0], X[1], X[2], X[3], X[4]], z3.Implies(z3.And(And_constraint,
#    not_eq_constraint), f_AND == min_max)))
#s.add(z3.Not(z3.Implies(z3.And(And_constraint, not_empty), f_AND == min_max)))
#print(s.check())
#print(s.model())

