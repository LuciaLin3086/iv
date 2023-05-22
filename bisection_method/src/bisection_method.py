from util.CRR_binomial_tree_better import OneDimTree
from util.BlackScholes import BS

# hyperparameter
S0 = 100
r = 0.05
q = 0.02
T = 0.5
K = 90
n = 100

market_price = 12
convergence_criterion = 10 ** (-6)

# starting interval
an = 0.01
bn = 2


class BisectionMethod:
    # 此 bisection method 是為 option pricing 所設定，所以起始設定需輸入 which_option, option_type
    def __init__(self, f, market_price, an, bn, convergence_criterion, C_P, E_A):
        self.f = f  # the function that you want to find its root
        self.market_price = market_price
        self.an = an
        self.bn = bn
        self.convergence_criterion = convergence_criterion
        self.C_P = C_P
        self.E_A = E_A

    def value_diff(self, x): # 模型所得的price與實際market price之間的誤差，希望誤差為0
        if self.f == "Tree":
            Tree_value = OneDimTree(S0, K, r, q, x, T, n, self.C_P, self.E_A)
            value_diff = Tree_value.get_option_value() - self.market_price

        elif self.f == "BS":
            BS_value = BS(S0, r, q, x, T, K, self.C_P)
            value_diff = BS_value.option_value() - self.market_price

        else:
            value_diff = print("Please define the function f.")

        return value_diff

    def find_root(self): # find the root to make value difference to be 0.
        f_an = self.value_diff(self.an)
        f_bn = self.value_diff(self.bn)

        if f_an * f_bn >= 0:
            return "Please change the starting interval [an, bn]."

        else:
            an = self.an # 為了使下面迴圈中不會直接更改起始值，用另一個變數存
            bn = self.bn
            while True: # while True : infinite loop
                xn = (an + bn) / 2
                f_xn = self.value_diff(xn)

                if abs(f_xn) < self.convergence_criterion:
                    break

                else:
                    if f_an * f_xn < 0:
                        an = an
                        bn = xn
                    else:
                        an = xn
                        bn = bn

            return xn



#####################
# Black-Scholes Model
#####################
EuropeanCall_BS = BisectionMethod("BS", market_price, an, bn, convergence_criterion, "C", "E")
EuropeanPut_BS = BisectionMethod("BS", market_price, an, bn, convergence_criterion, "P", "E")

print("Black-Scholes Model")
print(f"Implied volatility of EuropeanCall: {EuropeanCall_BS.find_root()}")
print(f"Implied volatility of EuropeanPut: {EuropeanPut_BS.find_root()}")

#####################
# Binomial Tree Model
#####################
EuropeanCall_tree = BisectionMethod("Tree", market_price, an, bn, convergence_criterion, "C", "E")
EuropeanPut_tree = BisectionMethod("Tree", market_price, an, bn, convergence_criterion, "P", "E")
AmericanCall_tree= BisectionMethod("Tree", market_price, an, bn, convergence_criterion, "C", "A")
AmericanPut_tree = BisectionMethod("Tree", market_price, an, bn, convergence_criterion, "P", "A")

print("\nBinomial Tree Model")
print(f"Implied volatility of EuropeanCall: {EuropeanCall_tree.find_root()}")
print(f"Implied volatility of EuropeanPut: {EuropeanPut_tree.find_root()}")
print(f"Implied volatility of AmericanCall: {AmericanCall_tree.find_root()}")
print(f"Implied volatility of AmericanPut: {AmericanPut_tree.find_root()}")



