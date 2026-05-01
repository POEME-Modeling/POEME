from popclean import Newton, Output, g
from popclean.spring_mass import Damper, Fp, Mass, Spring, Wall

g.out = open("pop.out", "a")
g.pretty = open("pretty.out", "a")


W1 = Wall("W1")
W1.xloc = 0.0
W1.Fp1 = Fp(W1, "in", "")
W1.Fp2 = Fp(W1, "in", "")

S1 = Spring("S1")
S1.k = 0.1
S1.LN = 3.0

D1 = Damper("Damper")
D1.c = 0.01

M1 = Mass("Mass")
M1.mass = 1.0
M1.xloc = 3.0
M1.Fp1 = Fp(M1, "in", "")
M1.Fp2 = Fp(M1, "in", "")

S1.Fp1.link_fp(W1.Fp1)
S1.Fp2.link_fp(M1.Fp1)

D1.Fp1.link_fp(W1.Fp2)
D1.Fp2.link_fp(M1.Fp2)

g.check()

g.NS = Newton("g.NS")

estuff = Output("estuff")
estuff.filename = "1mass.out"
estuff.vars = [g.NS.time, S1.L, M1.xloc]

g.NS.solve()

g.set("trans", True)
g.NS.timeLast = 100.0
g.NS.dtime = 0.01

M1.xloc = M1.xloc + 1.0

g.NS.trim()


print(M1.x)

g.NS.run()
