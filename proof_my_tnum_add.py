#prove tnum addition is correct


import z3
#from z3 import * considered bad practice but defines namespace z3

# List of Variables
#a_val, a_mask = z3.BitVecs('a_val a_mask', 8)
#b_val, b_mask = z3.BitVecs('b_val b_mask', 8)
sm, sv, sigma, chi, mu = z3.BitVecs('sm sv sigma chi mu', 8)
#z3.solve(sm == a_mask + b_mask, sv == a_val + b_val, sigma == sm + sv, 
#    chi == sigma ^ sv, mu  == chi | a_mask | b_mask)

a, ta_val, ta_mask, b, tb_val, tb_mask, c, tc_val, tc_mask, out1, out2 = z3.BitVecs('a ta_val ta_mask b tb_val tb_mask c tc_val tc_mask out1 out2', 8)


#val &= i
#mask |= i 

p1 = ta_val == a & ~ta_mask
p2 = ta_mask == a&~ta_mask - a|ta_mask  
#p3 = a>=0 and a <=2**8-1  

formula = z3.ForAll([a, ta_val, ta_mask], z3.Implies(p1, p2))



#z3.prove(z3.Not(z3.Implies(z3.And(p1, p2, p3, p4, p5, p6, p7, p8,p9, p10), output)))
s = z3.Solver()
s.add(z3.Not(formula))
#s.add(formula)
print (s.check())
print (s.model())

'''
a = z3.BitVec('a', 8)
b = z3.BitVec('b',8)
c = z3.BitVec('c',8)
ta_val, ta_mask = z3.BitVec('ta_val, ta_mask',8)
tb_val, tb_mask = z3.BitVec('tb_val, tb_mask',8)
tc_val, tc_mask = z3.BitVec('tc_val, tc_mask',8)

# List of numbering for each variables
ly1 = z3.Int('ly1')
ly2 = z3.Int('ly2')

lx11 = z3.Int('lx11')
lx12 = z3.Int('lx12')
lx21 = z3.Int('lx21')
lx22 = z3.Int('lx22')

# List of components.
phi1 = (Y1 == (X11 - 1))
phi2 = (Y2 == X21 & X22)


#Y1 = I-1
#Y2 = I & Y1
#O = I & (I-1)

# Write the spec
spec_list = []
for t in range(8) :
    input_extract = []
    for tp in range(t + 1) :
        if tp == t :
            input_extract.append(z3.Extract(tp, tp, I) == 1)

        else :
            input_extract.append(z3.Extract(tp, tp, I) == 0)
    
    input_component = z3.And(input_extract)
    output_component = (O == I - z3.BitVecVal(2**t, 8))

    #print (input_extract)
    #print (output_component)

    spec_list.append(z3.Implies(input_component, output_component))

# The case when I = 0 then O should be 0.
#spec_list.append(z3.Implies(I == z3.BitVecVal(0, 8), O == z3.BitVecVal(0, 8)))


spec = z3.And(spec_list)

# phi cons = line number of two different instructions cannot be the same
phicons = z3.And(ly1 != ly2)#, ly2!=ly3, ly1!=ly3)

# We only have three instructions.
# Bound the line number of each instruction and operand.
phibound = z3.And(ly1 >=1 , ly1 <=2 ,
                ly2 >=1 , ly2 <= 2,
                #ly3 >=1 , ly3 <= 2,
                lx11 >=0, lx11 <=2,
                lx21 >=0, lx21 <=2,
                lx22 >=0, lx22 <=2)

# The operands of an instruction should use variables from previous lines.
phidep = z3.And(lx11 < ly1 , lx21 < ly2, lx22 < ly2)

# Connection information:
# First, the simple ones: if lx == 0, then x gets info from I
#                         if ly == 3, then O is y
phiconn = z3.And(z3.Implies(lx11 == 0, X11 == I),
        #z3.Implies(lx12 == 0, X12 == I),
              z3.Implies(lx21 == 0, X21 == I),
              z3.Implies(lx22 == 0, X22 == I),
              z3.Implies(ly1 == 2,Y1 == O),
              z3.Implies(ly2 == 2,Y2 == O))

lys = [ly1, ly2]
lxs = [lx11, lx21, lx22]
lToVDict = {
    ly1: Y1,
    ly2: Y2,
    lx11: X11,
    lx21: X21,
    lx22: X22,
}

for i in lys :
    for j in lxs:
        phiconn = z3.And(phiconn, z3.Implies(i==j, lToVDict[i] == lToVDict[j]))

phiwfp = z3.And(phicons, phidep, phibound)

insideForAll = z3.ForAll([I, O, X11, X21, X22, Y1, Y2], z3.Implies(z3.And(phi1, phi2, phiconn), spec))
final_formula = z3.And(phiwfp, insideForAll)

s = z3.Solver()
s.add(final_formula)
print (s.check())
print (s.model())
'''
