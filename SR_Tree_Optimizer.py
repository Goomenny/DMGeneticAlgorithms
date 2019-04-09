from scipy.optimize import minimize, differential_evolution
import numpy as np
import copy
class SR_Tree_Optimizer:


    def res_func(self, x, tree, coefficient_nodes,obj_func):
        for xi, node in zip(x, coefficient_nodes):
            node.cargo = xi
        return obj_func(tree.get_result)

    def optimize(self,tree,obj_func):
        copy_tree = copy.deepcopy(tree)
        coefficient_nodes = copy_tree.root.get_constant_nodes()

        if coefficient_nodes:
            x0 = np.array([coef_node.cargo for coef_node in coefficient_nodes])
            try:
                res = minimize(self.res_func, x0, args=(copy_tree, coefficient_nodes,obj_func), method='L-BFGS-B', options={'maxiter': 10, 'disp': False})

                #res = differential_evolution(self.res_func, bounds,args=(tree, coefficient_nodes,obj_func),updating='immediate',maxiter=10)
            except:
                print("Ошибка оптимизации коэффициентов")
            else:
                for xi, node in zip(res.x, tree.root.get_constant_nodes()):
                    node.cargo = xi