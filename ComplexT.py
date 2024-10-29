

class ComplexT (  ):
	real = 0
	imag = 0

	def __init__( self, p, num, name, units, desc ):
		self.num = num
		self.name =  name
		self.units = units
		self.desc = desc
		self.parent = p
		p.addVID( self )
		
	def addVID(self,self1 ):
		pass
	
	def isa( self, type ):
		if type == "ComplexT":
			return True
		else:
			return False
			
	def set( self, val ):
		self.num = val.num
		
	def __add__( self, other ):
		num = self.num+other.num
		return( ComplexT( self, num,"","","" ))
		
	def __sub__( self, other ):
		num = self.num - other.num
		return( ComplexT( self, num,"","","" ))
		
	def __mul__( self, other ):
		num = self.num * other.num
		return( ComplexT( self, num,"","","" ))		

	def __truediv__( self, other ):
		num = self.num / other.num
		return( ComplexT( self, num,"","","" ))		
		
	
	def __str__(self):
		return str( self.num )

	# Returns a list of perturbation possibilities (9 possible for RealT)
	# perturb_type = True means Fractional   
	def Perturb(self, step, perturb_type, perturb):
		real_perturb_val = 0
		imag_perturb_val = 0

		# Perturb real val
		if perturb_type:
			real_perturb_val = self.real * perturb * step
		else:
			real_perturb_val = perturb * step

		# Perturb imaginary val
		if perturb_type:
			imag_perturb_val = self.imag * perturb * step
		
		else:
			imag_perturb_val = perturb * step
            
		perturb_list = [[self.real - real_perturb_val, self.imag - imag_perturb_val], [self.real, self.imag - imag_perturb_val], [self.real + real_perturb_val, self.imag - imag_perturb_val],
						[self.real - real_perturb_val, self.imag], [self.real, self.imag], [self.real + real_perturb_val, self.imag],
						[self.real - real_perturb_val, self.imag + imag_perturb_val], [self.real, self.imag + imag_perturb_val], [self.real + real_perturb_val, self.imag + imag_perturb_val]]

		return perturb_list
	
	def GetVal(self):
		return [self.real, self.imag]
	
	def SetVal(self, vals):
		self.real = vals[0]
		self.imag = vals[1]
		
