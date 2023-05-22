import scipy.stats as stats
from math import log, pow, sqrt, exp

# hyperparameter
S0 = 100
r = 0.05
q = 0.02
sigma = 0.5
T = 0.5
K = 90


def N(x):
    return stats.norm.cdf(x)  # normal cdf

class BS:
    def __init__(self, S0, r, q, sigma, T, K, C_P): # C_P: Calls or Puts
        self.S0 = S0
        self.r = r
        self.q = q
        self.sigma = sigma
        self.T = T
        self.K = K
        self.C_P = C_P

        self.d1 = (log(self.S0 / self.K) + (self.r - self.q + pow(self.sigma, 2) / 2) * self.T) / (
                    self.sigma * sqrt(self.T))
        self.d2 = self.d1 - self.sigma * sqrt(self.T)

    # def N(self):
    #     self.N() = stats.norm.cdf()
    #     return stats.norm.cdf()

    def option_value(self):
        if self.C_P == "C":
            value = self.S0 * exp(-self.q * self.T) * N(self.d1) - self.K * exp(-self.r * self.T) * N(self.d2)
        else:
            value = self.K * exp(-self.r * self.T) * N(-self.d2) - self.S0 * exp(-self.q * self.T) * N(-self.d1)

        return value


EuropeanCall = BS(S0, r, q, sigma, T, K, "C")
EuropeanPut = BS(S0, r, q, sigma, T, K, "P")

print(f"European Call Value : {EuropeanCall.option_value():.4f}")  # .4f取小數點後4位，float
print(f"European Put Value : {EuropeanPut.option_value():.4f}")



#%%
import scipy.stats as stats

from math import log, pow, sqrt, exp

# hyperparameter
S0 = 100
r = 0.05
q = 0.02
sigma = 0.5
T = 0.5
K = 90
which_option = "C"

d1 = (log(S0 / K) + (r - q + pow(sigma, 2) / 2) * T) / (sigma * sqrt(T))
d2 = (log(S0 / K) + (r - q - pow(sigma, 2) / 2) * T) / (sigma * sqrt(T))
# d2 = d1 - sigma * sqrt(T)
def N(x):
    return stats.norm.cdf(x)  # normal cdf

if which_option == "C":
    value = S0 * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2)
else:
    value = K * exp(-r * T) * N(-d2) - S0 * exp(-q * T) * N(-d1)

print("option value = ", value)


