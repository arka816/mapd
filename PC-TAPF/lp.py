from typing import List
import numpy as np
import re

variable_regex = "(>|<)=*[ ]*[0-9]+"
variable_pattern = re.compile(variable_regex)
inequality_symbols = ['>=', '<=', '>', '<']

numeric_regex = "[0-9]+"
numeric_pattern = re.compile(numeric_regex)

class Variable:
    def __init__(self, name, symbol, limit) -> None:
        self.name = name
        self.symbol = symbol
        self.limit = limit

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __hash__(self) -> int:
        return hash(self.name)

class Simplex:
    def __init__(self, type="max") -> None:
        self.type = type
        self.variables = set()
        self.constraints = []
        self.objective = None

    def create_variable(self, name, limit) -> None:
        if name in self.variables:
            raise Exception('variable already created')
        else:
            if not variable_pattern.match(limit):
                raise Exception('limit definition invalid')
            else:
                for symbol in inequality_symbols:
                    if symbol in limit:
                        limit_val = int(limit[limit.index(symbol) + len(symbol):].strip())
                        v = Variable(name, symbol, limit_val)
                        self.variables.insert(v)
                        return

        
    def add_constraint(self, equation) -> None:
        self.constraints.append(equation)

    def create_objective(self, objective) -> None:
        self.objective = objective

    def __parseexpression(self, exp) -> List[float]:
        pass

    def __parse(self) -> None:
        n = len(self.variables)

        # parse constraint
        A = []
        B = []
        for constraint in self.constraints:
            flag = False
            for symbol in inequality_symbols:
                if symbol in constraint:
                    lhs = constraint[:constraint.index(symbol)].strip()
                    rhs = constraint[constraint.index(symbol) + len(symbol):].strip()
                    flag = True
                    break

            if not flag:
                raise Exception('invalid constraint equation')
            elif not numeric_pattern.match(rhs):
                raise Exception('right hand side of constraint equation invalid')
            else:
                b = int(rhs)
                a = self.__parseexpression(lhs)
                B.append(b)
                A.append(a)

        # parse objective
        C = self.__parseexpression(self.objective)

        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)


        


