import numpy as np
from scipy.stats import norm
from dataclasses import dataclass


@dataclass
class Greeks:
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


class BlackScholes:
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self._d1: float | None = None
        self._d2: float | None = None

    @property
    def d1(self) -> float:
        if self._d1 is None:
            self._d1 = (
                np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T
            ) / (self.sigma * np.sqrt(self.T))
        return self._d1

    @property
    def d2(self) -> float:
        if self._d2 is None:
            self._d2 = self.d1 - self.sigma * np.sqrt(self.T)
        return self._d2

    def call_price(self) -> float:
        if self.T <= 0:
            return max(self.S - self.K, 0.0)
        return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)

    def put_price(self) -> float:
        if self.T <= 0:
            return max(self.K - self.S, 0.0)
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    def call_greeks(self) -> Greeks:
        if self.T <= 0:
            delta = 1.0 if self.S > self.K else 0.0
            return Greeks(delta=delta, gamma=0.0, theta=0.0, vega=0.0, rho=0.0)

        sqrt_T = np.sqrt(self.T)
        pdf_d1 = norm.pdf(self.d1)
        discount = np.exp(-self.r * self.T)

        delta = norm.cdf(self.d1)
        gamma = pdf_d1 / (self.S * self.sigma * sqrt_T)
        theta = (
            -(self.S * pdf_d1 * self.sigma) / (2 * sqrt_T)
            - self.r * self.K * discount * norm.cdf(self.d2)
        ) / 365  # daily theta
        vega = self.S * pdf_d1 * sqrt_T / 100  # per 1% move
        rho = self.K * self.T * discount * norm.cdf(self.d2) / 100  # per 1% move

        return Greeks(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)

    def put_greeks(self) -> Greeks:
        if self.T <= 0:
            delta = -1.0 if self.S < self.K else 0.0
            return Greeks(delta=delta, gamma=0.0, theta=0.0, vega=0.0, rho=0.0)

        sqrt_T = np.sqrt(self.T)
        pdf_d1 = norm.pdf(self.d1)
        discount = np.exp(-self.r * self.T)

        delta = norm.cdf(self.d1) - 1
        gamma = pdf_d1 / (self.S * self.sigma * sqrt_T)
        theta = (
            -(self.S * pdf_d1 * self.sigma) / (2 * sqrt_T)
            + self.r * self.K * discount * norm.cdf(-self.d2)
        ) / 365
        vega = self.S * pdf_d1 * sqrt_T / 100
        rho = -self.K * self.T * discount * norm.cdf(-self.d2) / 100

        return Greeks(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)
