from Element import Element


# No dependents or constraints yet
# Still need to generate independent list from elements
class HookeJeeves(Element):
    ind_list = ''
    element_list = ''
    step = 0
    objective = ''

    def __init__ (self,element_list, step, objective):
        self.element_list = element_list
        self.step = step
        self.objective = objective
        self.ind_list = list()
        
        for e in self.element_list:
            self.ind_list = self.ind_list + e.ind_list


    def Solve(self):
        best_vector = list()
        new_point = list()
        best_vals = list()
        last_obj = -999999999 # Practically Negative Infinity
        step_tolerance = 0.000000001
        step_reduction = 0.1

        # 5. Repeat 1-4 until required tolerance is reached
        while self.step > step_tolerance:
            # 3. Repeat 1-2 until returned vector is 0
            while self.Magnitude(self.BestNeighbor(self.step)) != 0:
                # 1. Cast about original neighborhood
                best_vector = self.BestNeighbor(self.step)

                last_obj = -999999999
                best_vals = list()

                # 2. Travel along the vector until no improvement is seen
                while self.ReturnObjective() > last_obj:
                    self.SearchInDirection(best_vector)

                    last_obj = self.ReturnObjective(self.ind_list)

            # 4. Reduce the interval
            self.step = self.step * step_reduction


    def Magnitude(self, vector):
        sum = 0

        for dim in vector:
            sum += dim ** 2

        return sum ** (0.5)


    def SearchInDirection(self, vector):
        new_point = list()

        for i in range(len(self.ind_list)):
            self.ind_list[i].SetVal(self.ind_list.GetVal() + vector[i])


    # Double check HJ
    def BestNeighbor(self, step):
        orig_point = list()
        best_point = list()
        best_vector = list()

        for i in range(len(self.ind_list)):
            best_objective = self.ReturnObjective()
            best_in_dim = self.ind_list[i].GetVal()

            # Set current value to best in dimension
            
            # Check all possible perturbations and set the best value
            # Have perturb return list of all possible values and take turns setting best
            
            perturb_list = self.ind_list[i].Perturb(step)
            
            print(self.ind_list[i].val)
            print(perturb_list)

            for perturbed_val in perturb_list:
                self.ind_list.SetVal(perturbed_val)
                
                current_objective = self.ReturnObjective()

                if(current_objective > best_objective):
                    best_in_dim = self.ind_list[i].GetVal()
            
            best_point.append(best_in_dim)

        for i in range(len(best_point)):
            best_vector.append(best_point[i] - orig_point[i])

        return best_vector
    
    def AdjustModel(self):
        for e in self.element_list:
            e.precheck()
		
        for e in self.element_list:
            e.preset()
			
        for e in self.element_list:
            e.calc()
     
            
    def ReturnObjective(self):
        self.AdjustModel()
        
        return self.objective()
        
