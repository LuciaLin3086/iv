from util.CRR_binomial_tree_better import OneDimTree
from util.BlackScholes import BS

# inputs
S0 = 100
r = 0.05
q = 0.02
T = 0.5
K = 90
n = 100

market_price = 12
convergence_criterion = 10 ** (-4)

# initial
x0 = 0.5

# for differential
h = 10 ** (-8)

class NewtonsMethod:

    def __init__(self, f, market_price, x0, convergence_criterion, C_P, E_A):
        self.f = f
        self.market_price = market_price
        self.x0 = x0
        self.convergence_criterion = convergence_criterion
        self.C_P = C_P
        self.E_A = E_A

    def value_diff(self, x):
        if self.f == "Tree":
            Tree_value = OneDimTree(S0, K, r, q, x, T, n, self.C_P, self.E_A)
            value_diff = Tree_value.get_option_value() - self.market_price

        elif self.f == "BS":
            BS_value = BS(S0, r, q, x, T, K, self.C_P)
            value_diff = BS_value.option_value() - self.market_price

        else:
            value_diff = print("Please define the function f.")

        return value_diff

    def first_differential(self, x):
        first_diff = (self.value_diff(x + h) - self.value_diff(x)) / h

        return first_diff

    def find_root(self):
        xn = self.x0
        while True:
            xn_1 = xn - self.value_diff(xn) / self.first_differential(xn)
            diff = xn_1 - xn
            if abs(diff) < self.convergence_criterion:
                break
            xn = xn_1

        return xn_1

#####################
# Black-Scholes Model
#####################
EuropeanCall_BS = NewtonsMethod("BS", market_price, x0, convergence_criterion, "C", "E")
EuropeanPut_BS = NewtonsMethod("BS", market_price, x0, convergence_criterion, "P", "E")

print("Black-Scholes Model")
print(f"Implied volatility of EuropeanCall: {EuropeanCall_BS.find_root()}")
print(f"Implied volatility of EuropeanPut: {EuropeanPut_BS.find_root()}")

#####################
# Binomial Tree Model
#####################
EuropeanCall_tree = NewtonsMethod("Tree", market_price, x0, convergence_criterion, "C", "E")
EuropeanPut_tree = NewtonsMethod("Tree", market_price, x0, convergence_criterion, "P", "E")
AmericanCall_tree= NewtonsMethod("Tree", market_price, x0, convergence_criterion, "C", "A")
AmericanPut_tree = NewtonsMethod("Tree", market_price, x0, convergence_criterion, "P", "A")

print("\nBinomial Tree Model")
print(f"Implied volatility of EuropeanCall: {EuropeanCall_tree.find_root()}")
print(f"Implied volatility of EuropeanPut: {EuropeanPut_tree.find_root()}")
print(f"Implied volatility of AmericanCall: {AmericanCall_tree.find_root()}")
print(f"Implied volatility of AmericanPut: {AmericanPut_tree.find_root()}")


