import numpy as np
from math import exp, sqrt, pow


class OneDimTree: # use one dimension array to store the tree

    def __init__(self, S0, K, r, q, sigma, T, n, C_P, E_A):
        self.S0 = S0
        self.K = K
        self.r = r
        self.q = q
        self.sigma = sigma
        self.T = T
        self.n = n
        self.C_P = C_P
        self.E_A = E_A

        self.delta_T = self.T / self.n
        self.u = exp(self.sigma * sqrt(self.delta_T))
        self.d = exp(- self.sigma * sqrt(self.delta_T))
        self.p = (exp((self.r - self.q) * self.delta_T) - self.d) / (self.u - self.d)

        # store the tree: 此 class 就是用於建立 tree，所以起始設定要先有 tree
        self.tree = np.zeros(self.n + 1) # one dimension array

        self.create_tree()

    def get_price(self, time, down_steps):
        price = self.S0 * pow(self.u, time - down_steps) * pow(self.d, down_steps)
        return price

    def get_payoff(self, price):
        if self.C_P == "C":
            payoff = max(price - self.K, 0)
            return payoff
        else:
            payoff = max(self.K - price, 0)
            return payoff


    def get_maturity_payoff(self):
        maturityPayoff_ls = []
        for down_steps in range(0, self.n + 1):
            maturityPayoff_ls.append(self.get_payoff(self.get_price(self.n, down_steps)))

        return np.array(maturityPayoff_ls)

    def get_tree_value(self, down_steps):
        tree_value = exp(-self.r * self.delta_T) * (self.p * self.tree[down_steps] + (1 - self.p) * self.tree[down_steps + 1])

        return tree_value

    def create_tree(self):
        self.tree = self.get_maturity_payoff() # insert to the last column of tree
        for time in list(reversed(range(0, self.n))):
            for down_steps in range(0, time + 1):
                if self.E_A == "A":
                    exercise_value = self.get_payoff(self.get_price(time, down_steps))
                    intrinsic_value = self.get_tree_value(down_steps)
                    self.tree[down_steps] = max(exercise_value, intrinsic_value)
                else:
                    self.tree[down_steps] = self.get_tree_value(down_steps)


    def get_option_value(self):
        return self.tree[0]



if __name__ == "__main__":
    S0 = 100
    r = 0.05
    q = 0.02
    sigma = 0.5
    T = 0.5
    K = 90
    n = 100

    EuropeanCall = OneDimTree(S0, K, r, q, sigma, T, n, "C", "E")
    EuropeanPut = OneDimTree(S0, K, r, q, sigma, T, n, "P", "E")
    AmericanCall= OneDimTree(S0, K, r, q, sigma, T, n, "C", "A")
    AmericanPut = OneDimTree(S0, K, r, q, sigma, T, n, "P", "A")

    print(f"European Call value: {EuropeanCall.get_option_value():.4f}")
    print(f"European Put value: {EuropeanPut.get_option_value():.4f}")
    print(f"American Call value: {AmericanCall.get_option_value():.4f}")
    print(f"American Put value: {AmericanPut.get_option_value():.4f}")

    print("value: {:.4f}".format(AmericanCall.get_option_value()))














    # def get_payoff_tree(self):
    #     pprice_tree = np.zeros((n + 1, n + 1))# array of given shape, filled with zeros
    #     payoff_tree = np.zeros((n + 1, n + 1))
    #     for j in range(1, n+1): # range from 1 for n+1 steps
    #         price_tree[0, j] = price_tree[0, j-1] * u
    #         for i in range(1, j+1):
    #             price_tree[i, j] = price_tree[i-1, j-1] * d
    #
    #     return price_tree
