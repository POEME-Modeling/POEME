from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
import g
from Independent import Independent
from BooleanT import BooleanT
import math

class FlightConditions( Element ):
    
    def __init__(f,name):
        super().__init__(name, "FlowStart" )
        f.type = "FlowStart"
        
        f.desc = "Start a Flow stream."
        
        # variables
        f.comp = StringT( f, desc="Composition of the stream." )
        f.alt = RealT( f, units="ft", desc="Altitude" )
        f.MN =  RealT( f, desc = "MN" )
        f.Pamb = RealT( f, units="lbm/in2", desc="Ambient pressure" )
        f.Pt = RealT( f, units="lbm/in2", desc="Total pressure" )        
        f.Tamb = RealT( f, units="R", desc="Ambient temperature" )
        f.Tt = RealT( f, units="R", desc="Ambient temperature" )        
        f.W = RealT( f, units="lbm/sec", descc="Weight" )
        f.size = BooleanT( f, v=True, desc="Determine if the element is in design mode or not" )        

		# pressure temperature tables
        f.Ptable = Table1d( f, desc="Table of pressure versus altitude" )
        f.Ptable.x = [ 0., 36089, 65617., 104987.]
        f.Ptable.y = [ 101325.*0.000145038, 22632.1*0.000145038, 5474.89*0.000145038, 868.019*0.000145038 ]
        f.Ttable = Table1d( f, desc="Table of temperature versus altitude" )
        f.Ttable.x = [ 0., 36089, 65617., 104987.]
        f.Ttable.y = [ 288.15*9./5., 216.65*9./5., 216.65*9./5., 228.65*9./5. ]

        f.Ptable = Table1d( f, desc="Table of pressure versus altitude" )
        f.Ptable.x = [  -5000, -4000, -3000, -2000, -1000,     0,
                         1000,  2000,  3000,  4000,  5000,  6000,  7000,  8000,  9000, 10000,
                        11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                        21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000,
                        31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000,
                        41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000,
                        51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000,
                        61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000,
                        71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000,
                        81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000,
                        91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000,100000 ] # altitude, 'ft'
        f.Ptable.y = [  17.5529, 16.9483, 16.3607, 15.7896, 15.2348, 14.6959,
               14.1726, 13.6644, 13.1711, 12.6923, 12.2277, 11.7770, 11.3398, 10.9159, 10.5049, 10.1065,
                9.7204, 9.34636, 8.98405, 8.63321, 8.29354, 7.96478, 7.64665, 7.33889, 7.04123, 6.75343,
               6.47523, 6.20638, 5.94664, 5.69578, 5.45355, 5.21974, 4.99410, 4.77644, 4.56651, 4.36413,
               4.16906, 3.98112, 3.80010, 3.62580, 3.45803, 3.29661, 3.14191, 2.99447, 2.85395, 2.72003,
               2.59239, 2.47073, 2.35479, 2.24429, 2.13897, 2.03860, 1.94293, 1.85176, 1.76486, 1.68204,
               1.60311, 1.52788, 1.45618, 1.38785, 1.32272, 1.26065, 1.20149, 1.14511, 1.09137, 1.04016,
              0.991347,0.944827,0.900489,0.858232,0.817958,0.779578,0.743039,0.708261,0.675156,0.643641,
              0.613638,0.585073,0.557875,0.531976,0.507313,0.483825,0.461455,0.440148,0.419853,0.400519,
              0.382101,0.364553,0.347833,0.331902,0.316720,0.302253,0.288464,0.275323,0.262796,0.250856,
              0.239473,0.228621,0.218275,0.208410,0.199003,0.190032,0.181478,0.173319,0.165537,0.158114 ] # pressure, 'psi'


        f.Ttable = Table1d( f, desc="Table of temperature versus altitude" )
        f.Ttable.x = [ -5000, -4000, -3000, -2000, -1000,     0,
                 1000,  2000,  3000,  4000,  5000,  6000,  7000,  8000,  9000, 10000,
                11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000,
                31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000,
                41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000,
                51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000,
                61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000,
                71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000,
                81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000,
                91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000,100000] # altitude, 'ft'

        f.Ttable.y = [536.501,532.935,529.368,525.802,522.236,518.670,
              515.104,511.538,507.972,504.405,500.839,497.273,493.707,490.141,486.575,483.008,
              479.442,475.876,472.310,468.744,465.178,461.611,458.045,454.479,450.913,447.347,
              443.781,440.214,436.648,433.082,429.516,425.950,422.384,418.818,415.251,411.685,
              408.119,404.553,400.987,397.421,393.854,390.288,389.970,389.970,389.970,389.970,
              389.970,389.970,389.970,389.970,389.970,389.970,389.970,389.970,389.970,389.970,
              389.970,389.970,389.970,389.970,389.970,389.970,389.970,389.970,389.970,389.970,
              389.970,389.970,389.970,389.970,389.970,390.180,390.729,391.278,391.826,392.375,
              392.923,393.472,394.021,394.569,395.118,395.667,396.215,396.764,397.313,397.861,
              398.410,398.958,399.507,400.056,400.604,401.153,401.702,402.250,402.799,403.348,
              403.896,404.445,404.994,405.542,406.091,406.639,407.188,407.737,408.285,408.834 ] #temperature, 'Rankine'      
      
      
		# fluid locations
        f.FNo = FN( f, io="out", desc="Outgoing flow" )

		# solver stuff	
        f.ind_1 = Independent( f, indname="W", perturb=.05, scale=100, perturb_type="Relative", active=False, desc="Vary mass flow" )   
            
    def calc(f):
    	
    	# set the comp
    	f.FNo.comp.set( f.comp );
    	
    	# read atmospheric coniditions 
    	f.Tamb.set( f.Ttable.calc( f.alt ))
    	f.Pamb.set( f.Ptable.calc( f.alt ))
		
		# determine the total conditions
    	f.FNo.setTP( f.Tamb, f.Pamb )
    	
    	hs = f.FNo.ht
    	V = f.MN * math.sqrt( f.FNo.gamt * f.FNo.Rt.v * f.FNo.Tt*25037. )

    	ht = hs + V**2./(2.*25037.)
    	f.FNo.MN.set( f.MN )
    	f.FNo.set_hs( ht, f.FNo.s )

    	# determine the weight flow
    	f.FNo.setW( f.W )
    	
    	
    def precheck( f ):

        # design point turn off solver stuff
        if f.size == True:
        	f.ind_1.active = False
		# off design turn on solver stuff        	
        else:
            f.ind_1.active = True
           
    def dump( f ): 
    	#dump output variables    	
        print( f.name1, "FlowStart", file=g.out )
        super().realPrint()       
  
       
       