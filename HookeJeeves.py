from Element import Element


# No dependents or constraints yet
class HookeJeeves(Element):
    ind_list = ''
    dep_list = ''
    step = 0
    objective = ''

    def __init__ (self, ind_list, dep_list, step, objective):
        self.ind_list = ind_list
        self.dep_list = dep_list
        self.step = step
        self.objective = objective


    def Solve(self):
        best_vector = list()
        new_point = list()
        best_vals = list()
        last_obj = -999999999 # Practically Negative Infinity
        step_tolerance = 0.0001
        step_reduction = 0.1

        # 5. Repeat 1-4 until required tolerance is reached
        while step > step_tolerance:
            # 3. Repeat 1-2 until returned vector is 0
            while self.Magnitude(self.BestNeighbor()) != 0:
                # 1. Cast about original neighborhood
                best_vector = self.BestNeighbor(step)

                last_obj = -999999999
                best_vals = list()

                # 2. Travel along the vector until no improvement is seen
                while self.objective(self.ind_list) > last_obj:
                    new_point = self.SearchInDirection(best_vector)

                    for i in range(self.ind_list.size()):
                        self.ind_list[i].val = new_point[i]

                    last_obj = self.objective(self.ind_list)
                    best_vals = new_point


            # 4. Reduce the interval
            step = step * step_reduction

        return self.ind_list


    def Magnitude(vector):
        sum = 0

        for dim in vector:
            sum += dim ** 2

        return sum ** (0.5)


    def SearchInDirection(self, vector):
        new_point = list()

        for i in range(self.ind_list.size()):
            new_point.append(self.ind_list[i].val + vector[i])

        return new_point

    # Double check HJ
    def BestNeighbor(self, step):
        orig_point = list()
        best_point = list()
        best_vector = list()

        for i in range(self.ind_list.size()):
            orig_point.append(self.ind_list[i])
            best_objective = self.objective(self.ind_list)
            best_in_dim = self.ind_list[i].val

            ind_val = self.ind_list[i].val
            perturb_val = self.ind_list[i].GetPerturbVal()

            self.ind_list[i].val = ind_val + perturb_val

            if self.objective(self.ind_list) > best_objective:
                best_objective = self.objective(self.ind_list)
                best_in_dim = self.ind_list[i].val

            self.ind_list[i].val = ind_val - 2 * perturb_val

            if self.objective(self.ind_list) > best_objective:
                best_objective = self.objective(self.ind_list)
                best_in_dim = self.ind_list[i].val

            self.ind_list[i].val = best_in_dim
            
            best_point.append(best_in_dim)

        for i in range(best_point.size):
            best_vector.append(best_point[i] - orig_point[i])

        return best_vector