"""
CTT Financial Modelling
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class FinancialModel:
    """Financial simulations with CTT stability."""
    
    def __init__(self, drift, volatility, alpha=ALPHA):
        self.mu = drift
        self.sigma = volatility
        self.alpha = alpha
        
    def simulate(self, S0, T, steps=100):
        """Simulate asset price with CTT damping."""
        dt = T / steps
        S = np.array(S0)
        energy = []
        
        for d in range(33):
            for _ in range(steps // 33):
                dW = np.random.randn(len(S0)) * np.sqrt(dt)
                S = S + self.mu * S * dt + self.sigma * S * dW
            # CTT energy decay ensures stability
            S = S * np.exp(-self.alpha)
            energy.append(np.sum(S**2))
            
        return S, energy
    
    def price_option(self, S0, K, T, r, steps=100):
        """Price option using CTT-stable simulation."""
        S, _ = self.simulate(S0, T, steps)
        payoff = np.maximum(S - K, 0)
        return np.exp(-r * T) * np.mean(payoff)
