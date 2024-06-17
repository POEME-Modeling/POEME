
    
exec(open("./pop.py").read())
exec(open("./H2O.py").read())
exec(open("./H2O2.py").read())


H2 = H2O("H2")
O2 = H2O2("H2O2")

print(eval("O2.x.desc"))
H2V = H2.VIDL

for v in H2V:
    print(v.name)


O2.y.v = 10.
O2.calc()

# Create an objective function
def objective_function():
    return -1

hj = HookeJeeves(ind_list, dep_list, step, objective_function)
	
solved_ind_list = hj.Solve()
	
#eval( "H2.calc()" )
#eval( "O2.calc()" )


print(O2.isa("Ato"))