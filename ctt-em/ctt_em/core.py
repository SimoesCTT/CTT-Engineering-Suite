"""
CTT Electromagnetics
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class ElectromagneticSolver:
    """Maxwell's equations with CTT temporal damping."""
    
    def __init__(self, epsilon, mu, sigma=0.0):
        self.eps = epsilon
        self.mu = mu
        self.sigma = sigma
        self.alpha = ALPHA
        
    def solve(self, E0, H0, J, t_final, steps=100):
        """Solve Maxwell's equations with CTT stability."""
        n = len(E0)
        y0 = np.concatenate([E0, H0])
        
        def dynamics(y):
            E = y[:n]
            H = y[n:]
            dE = (1/self.eps) * (np.cross(H, np.ones_like(H)) - self.sigma * E - J)
            dH = -(1/self.mu) * np.cross(E, np.ones_like(E))
            return np.concatenate([dE, dH])
        
        system = TemporalSystem(dynamics, alpha=self.alpha)
        y_final, energy = system.evolve(y0, t_final, steps)
        return y_final[:n], y_final[n:], energy
