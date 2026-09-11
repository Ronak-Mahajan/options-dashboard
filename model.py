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
            # Edge case: zero volatility. The deterministic limit compares the
            # spot to the DISCOUNTED strike K*exp(-rT), not to K: with sigma -> 0
            # the call is worth max(S - K e^{-rT}, 0) and the put
            # max(K e^{-rT} - S, 0). Comparing S to K instead produced negative
            # put prices for S in (K e^{-rT}, K].
            if self.sigma == 0:
                forward_strike = self.K * np.exp(-self.r * self.T)
                if self.S > forward_strike:
                    self._d1 = np.inf
                elif self.S < forward_strike:
                    self._d1 = -np.inf
                else:
                    self._d1 = 0.0
            else:
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

    def _gamma(self, pdf_d1: float, sqrt_T: float) -> float:
        # Gamma is identical for calls and puts. At sigma == 0 the closed form
        # divides by zero (pdf(+-inf)/0 = nan off the forward, pdf(0)/0 = inf
        # at it). The sigma -> 0 limit is 0 everywhere except exactly at the
        # discounted strike, where it is a Dirac spike with no finite value;
        # return the finite limit 0.0 rather than a nan/inf that the UI would
        # render literally.
        if self.sigma == 0:
            return 0.0
        return pdf_d1 / (self.S * self.sigma * sqrt_T)

    def call_greeks(self) -> Greeks:
        if self.T <= 0:
            delta = 1.0 if self.S > self.K else 0.0
            return Greeks(delta=delta, gamma=0.0, theta=0.0, vega=0.0, rho=0.0)

        sqrt_T = np.sqrt(self.T)
        pdf_d1 = norm.pdf(self.d1)
        discount = np.exp(-self.r * self.T)

        # With sigma == 0, d1 is +-inf (or 0 at the discounted strike), so
        # cdf/pdf below evaluate to their limits: delta in {0, 0.5, 1}, the
        # sigma-weighted theta term vanishes, vega/rho take their limiting
        # values, and gamma is guarded in _gamma().
        delta = norm.cdf(self.d1)
        gamma = self._gamma(pdf_d1, sqrt_T)
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
        gamma = self._gamma(pdf_d1, sqrt_T)
        theta = (
            -(self.S * pdf_d1 * self.sigma) / (2 * sqrt_T)
            + self.r * self.K * discount * norm.cdf(-self.d2)
        ) / 365
        vega = self.S * pdf_d1 * sqrt_T / 100
        rho = -self.K * self.T * discount * norm.cdf(-self.d2) / 100

        return Greeks(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)
