import math
from pysat.formula import CNF
from pysat import *
from pysat.solvers import *

class sudoSolver:
    def __init__(self, name = "Minisat22"):
        self.name = name
       
    def _solve(self, cnf_clause, clues):
        with Solver(self.name, use_timer=True) as s:
            s.append_formula(cnf_clause)
            s.solve(clues)
            time = s.time()
            novars = cnf_clause.nv
            noclauses = cnf_clause.clauses.__len__()
            solution = s.get_model()
        return solution, time, novars, noclauses
        