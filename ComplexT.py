from ValueT import ValueT

class ComplexT ( ValueT ):
	real = 0
	imag = 0

	def __init__( self, p, name, desc ):
		self.c = complex( 0., 0. )
		self.name = name
		self.desc = desc
		
	def isa( self, type ):
		if type == "ComplexT":
			return True
		else:
			return False

	# Returns a list of perturbation possibilities (9 possible for RealT)
	# perturb_type = True means Fractional   
	def Perturb(self, step, perturb_type, perturb):
		real_perturb_val = 0
		imag_perturb_val = 0

		# Perturb real val
		if perturb_type:
			real_perturb_val = self.real * perturb
		else:
			real_perturb_val = perturb

		# Perturb imaginary val
		if perturb_type:
			imag_perturb_val = self.imag * perturb
		else:
			imag_perturb_val = perturb
            
		perturb_list = [[self.real - real_perturb_val, self.imag - imag_perturb_val], [self.real, self.imag - imag_perturb_val], [self.real + real_perturb_val, self.imag - imag_perturb_val],
						[self.real - real_perturb_val, self.imag], [self.real, self.imag], [self.real + real_perturb_val, self.imag],
						[self.real - real_perturb_val, self.imag + imag_perturb_val], [self.real, self.imag + imag_perturb_val], [self.real + real_perturb_val, self.imag + imag_perturb_val]]

		return perturb_list
	
	def GetVal(self):
		return [self.real, self.imag]
	
	def SetVal(self, vals):
		self.real = vals[0]
		self.imag = vals[1]
		
	



